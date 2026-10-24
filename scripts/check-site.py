#!/usr/bin/env python3
"""Validate imported content, routes, math, disclosures, assets and the search index."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from datetime import date, timedelta
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.images, self.proofs, self.entries = [], [], [], []
        self.content_images = []
        self._stack = []
        self.contributions = {}
        self.backgrounds, self.friends = [], []
        self.math_errors = self.math = 0
        self.callouts = self.tabs = 0
        self.ids = set()
        self.comment_paths = []
        self.canonical = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'comment-component':
            self.comment_paths.append(attrs.get('data-comment-path'))
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        inside = attrs.get('id') == 'content' or (self._stack and self._stack[-1][1])
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self._stack.append((tag, inside))
        if tag == 'img' and attrs.get('src') and inside:
            self.content_images.append(attrs['src'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'img' and attrs.get('src'):
            self.images.append(attrs['src'])
        if attrs.get('data-contribution-date'):
            self.contributions[attrs['data-contribution-date']] = int(attrs['data-count'])
        if attrs.get('data-friend'):
            self.friends.append(attrs['data-friend'])
        if attrs.get('data-background'):
            image = re.search(r"url\('([^']+)'\)", attrs.get('style', ''))
            self.backgrounds.append((attrs['data-background'], image[1] if image else ''))
        classes = attrs.get('class', '').split()
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if 'study-block' in classes:
            self.callouts += 1
        if tag == 'section' and 'study-tab' in classes:
            self.tabs += 1
        if tag == 'details' and 'study-block' in classes:
            self.proofs.append('open' in attrs)
        if 'katex-error' in classes:
            self.math_errors += 1
        if 'katex' in classes:
            self.math += 1
        if 'post-preview' in classes and attrs.get('data-entry'):
            self.entries.append(attrs['data-entry'])

    def handle_endtag(self, tag):
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--migration', action='store_true', help='Also enforce the original migration snapshot byte-for-byte')
    strict = parser.parse_args().migration
    original_report = json.loads((ROOT / 'migration/report.json').read_text())
    audit = json.loads((ROOT / '.astro/markdown-audit.json').read_text())
    report = {**original_report, 'posts': [post for post in audit['posts'] if not post['draft']]}
    original_posts = {entry['id']: entry for entry in original_report['posts']}
    if audit['errors']:
        raise SystemExit('TeX validation failed; run node scripts/audit-markdown.mjs')
    course_tags = json.loads((ROOT / 'src/data/course-tags.json').read_text())
    optimized = json.loads((ROOT / 'migration/optimized-assets.json').read_text())
    markdown_audit = {entry['id']: entry for entry in audit['posts']}
    original_rendering = json.loads((ROOT / 'migration/original-rendering-baseline.json').read_text())['posts']
    dist, issues, proofs, math = ROOT / 'dist', [], 0, 0
    page_cache = {}
    def read_page(path):
        if path not in page_cache:
            page_cache[path] = Page(path.read_text())
        return page_cache[path]
    def fenced_code(text):
        blocks, lines, fence, indent, language = [], [], None, 0, ''
        for line in text.expandtabs(4).splitlines():
            marker = re.match(r'^( *)(`{3,}|~{3,})(.*)', line)
            if marker and fence is None:
                fence, indent, language, lines = marker[2], len(marker[1]), marker[3].strip(), []
            elif marker and fence and marker[2][0] == fence[0] and len(marker[2]) >= len(fence):
                blocks.append((language, '\n'.join(lines).strip()))
                fence = None
            elif fence:
                lines.append((line[indent:] if line[:indent].isspace() else line).rstrip())
        return blocks
    # Source snapshots remain immutable; normal edits and new articles do not alter migration history.
    for entry in original_report['posts']:
        snapshot = ROOT / 'migration/originals' / entry['source']
        if hashlib.sha256(snapshot.read_bytes()).hexdigest() != entry['source_sha256']:
            issues.append('Changed original snapshot: ' + entry['source'])
    for entry in report['posts']:
        if entry['course'] and entry['tags'] != course_tags[entry['course']]:
            issues.append('Course notes must use only subject and course tags: ' + entry['route'])
        imported = ROOT / entry['file']
        body = re.split(r'\A---\s*\n.*?\n---\s*\n', imported.read_text(), maxsplit=1, flags=re.S)[1]
        if hashlib.sha256(body.encode()).hexdigest() != entry['body_sha256']:
            issues.append('Content changed after the audit: ' + entry['route'])
        baseline = original_posts.get(entry['id'])
        if strict and baseline:
            if hashlib.sha256(body.encode()).hexdigest() != baseline['body_sha256']:
                issues.append('Changed migrated body: ' + entry['route'])
            original = ROOT / 'migration/originals' / baseline['source']
            if fenced_code(original.read_text()) != fenced_code(body):
                issues.append('Source code changed during migration: ' + entry['route'])
        built = dist / entry['route'].lstrip('/') / 'index.html'
        if not built.exists():
            issues.append('Missing route: ' + entry['route'])
            continue
        page = read_page(built)
        audit = markdown_audit[entry['id']]
        if page.math != audit['math']:
            issues.append(f"Math count differs from Markdown AST: {entry['route']}: {page.math} != {audit['math']}")
        if baseline and (strict or entry['body_sha256'] == baseline['body_sha256']) and page.math < original_rendering[entry['id']]['math']:
            issues.append('Fewer formulas rendered than on the original blog: ' + entry['route'])
        if len(page.proofs) != entry['proofs']:
            issues.append('Proof count mismatch: ' + entry['route'])
        expected_open = entry['open_proofs']
        if sum(page.proofs) != expected_open:
            issues.append('Proof open state mismatch: ' + entry['route'])
        if page.math_errors:
            issues.append('Math render error: ' + entry['route'])
        if page.callouts != entry['admonitions']:
            issues.append(f"Callout count mismatch: {entry['route']}: {page.callouts} != {entry['admonitions']}")
        if page.tabs != entry['tabs']:
            issues.append('Tab panel count mismatch: ' + entry['route'])
        if len(page.content_images) != entry['images']:
            issues.append(f"Article image count mismatch: {entry['route']}: {len(page.content_images)} != {entry['images']}")
        if page.comment_paths != ([entry['commentPath']] if entry['comment'] else []):
            issues.append('Incorrect historical comment path: ' + entry['route'])
        proofs += len(page.proofs)
        math += page.math
    for path in dist.rglob('*.html'):
        page = read_page(path)
        if page.canonical and urlsplit(page.canonical).netloc != 'semt0.github.io':
            issues.append('Incorrect production canonical URL: ' + str(path.relative_to(dist)))
        for value in page.images + page.links:
            url = urlsplit(value)
            if url.scheme or url.netloc or not url.path:
                continue
            target = dist / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)
            if not target.exists() and not (target / 'index.html').is_file():
                issues.append(f"Broken local link: {path.relative_to(dist)} -> {value}")
        for value in page.links:
            url = urlsplit(value)
            if url.scheme or url.netloc or not url.fragment:
                continue
            target = dist / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path) if url.path else path
            if target.is_dir():
                target /= 'index.html'
            if target.is_file() and target.suffix == '.html' and unquote(url.fragment) not in read_page(target).ids:
                issues.append(f"Broken local heading: {path.relative_to(dist)} -> {value}")
    for relative, expected in report['assets'].items():
        source_asset = ROOT / 'migration/asset-cache' / relative if relative in optimized else dist / 'media' / relative
        if source_asset.exists() and hashlib.sha256(source_asset.read_bytes()).hexdigest() != expected:
            issues.append('Asset hash mismatch: ' + relative)
        if relative in optimized:
            asset = optimized[relative]
            if hashlib.sha256((dist / 'media' / asset['output']).read_bytes()).hexdigest() != asset['sha256']:
                issues.append('Optimized image hash mismatch: ' + relative)
    expected_entries = {f"blog/{entry['id']}" for entry in report['posts']}
    def listing_entries(folder):
        pages = [folder / 'index.html', *sorted((p / 'index.html' for p in folder.iterdir() if p.is_dir() and p.name.isdigit()), key=lambda p: int(p.parent.name))]
        return [entry for p in pages for entry in Page(p.read_text()).entries]
    listing = listing_entries(dist / 'blog')
    if set(listing) != expected_entries or len(listing) != len(expected_entries):
        issues.append('The unified Blog must list every article exactly once across pagination')
    archive = Page((dist / 'archives/index.html').read_text())
    if set(archive.entries) != expected_entries or len(archive.entries) != len(expected_entries):
        issues.append('Archives must include every post, including course notes')
    tags = {tag for entry in report['posts'] for tag in entry['tags']}
    for tag in tags:
        course_entries = listing_entries(dist / 'tags' / tag)
        expected = {f"blog/{entry['id']}" for entry in report['posts'] if tag in entry['tags']}
        if set(course_entries) != expected or len(course_entries) != len(expected):
            issues.append('Course tag membership mismatch: ' + tag)
        if tag == 'ode':
            entries_by_id = {f"blog/{entry['id']}": entry for entry in report['posts']}
            chapters = [entries_by_id[key] for key in course_entries]
            for previous, current in zip(chapters, chapters[1:]):
                if previous['publishDate'] == current['publishDate'] and previous.get('order') is not None and current.get('order') is not None and previous['order'] < current['order']:
                    issues.append('Equal-date course chapters must appear in reverse chapter order')
    for old, new in json.loads((ROOT / 'src/legacy-note-redirects.json').read_text()).items():
        target = dist / old.lstrip('/')
        if target.suffix != '.xml':
            target /= 'index.html'
        if not target.is_file() or new not in unquote(target.read_text()):
            issues.append('Missing legacy redirect: ' + old)
        elif 'data-legacy-bookmark' not in target.read_text():
            issues.append('Legacy redirect must preserve query and fragment: ' + old)
    heading_map = json.loads((ROOT / 'migration/legacy-heading-map.json').read_text())
    redirects = json.loads((ROOT / 'src/legacy-note-redirects.json').read_text())
    if heading_map['unmatched']:
        issues.append('Some original headings have no migration mapping')
    for old, mappings in heading_map['routes'].items():
        page = read_page(dist / redirects[old].lstrip('/') / 'index.html')
        if any(heading not in page.ids for heading in mappings.values()):
            issues.append('An old heading maps to a missing new anchor: ' + old)
    feed = ET.parse(dist / 'rss.xml')
    items = feed.findall('./channel/item')
    if len(items) != len(expected_entries):
        issues.append('RSS must include all posts and course notes')
    for item in items:
        if urlsplit(item.findtext('link')).path.lstrip('/') not in expected_entries:
            issues.append('Incorrect RSS destination: ' + str(item.findtext('link')))
    if len(ET.parse(dist / 'docs/rss.xml').findall('./channel/item')) != len(expected_entries):
        issues.append('The legacy notes feed must preserve access to the unified feed')
    for required in ['index.html', 'blog/index.html', 'projects/index.html', 'archives/index.html', 'about/index.html', 'links/index.html', 'search/index.html', 'pagefind/pagefind.js', 'pagefind/pagefind-entry.json', 'branding/pku-seal.svg']:
        if not (dist / required).is_file():
            issues.append('Missing feature: ' + required)
    home = (dist / 'index.html').read_text()
    if '<html lang="en"' not in home or 'Peking University' not in home or 'home-pku-seal' not in home:
        issues.append('The English homepage or PKU education card is missing')
    background_assets = set()
    for section, route in [('home', 'index.html'), ('blog', 'blog/index.html'),
                           ('projects', 'projects/index.html'), ('archives', 'archives/index.html'),
                           ('about', 'about/index.html'), ('links', 'links/index.html')]:
        page = Page((dist / route).read_text())
        if len(page.backgrounds) != 1 or page.backgrounds[0][0] != section:
            issues.append('Missing section background: ' + route)
            continue
        asset = page.backgrounds[0][1]
        if not asset or not (dist / asset.lstrip('/')).is_file():
            issues.append('Missing optimized background asset: ' + route)
        background_assets.add(asset)
        if '/links' not in page.links:
            issues.append('Missing Links navigation: ' + route)
    if len(background_assets) != 6:
        issues.append('Each main section must use a different background image')
    for route in ['blog/2/index.html', 'tags/ode/index.html', 'blog/foundation-models/gradient-descent/index.html']:
        if Page((dist / route).read_text()).backgrounds[0][0] != 'blog':
            issues.append('Blog pagination, tags and articles must share their section background: ' + route)
    friends = json.loads((ROOT / 'src/data/links.json').read_text())
    links_page = Page((dist / 'links/index.html').read_text())
    if links_page.comment_paths != ['/']:
        issues.append('Links guestbook must retain the original homepage comment path')
    if sorted(links_page.friends) != sorted(friend['url'] for friend in friends):
        issues.append('Links must include every configured friend exactly once')
    projects = json.loads((ROOT / 'src/data/projects.json').read_text())['projects']
    activity = json.loads((ROOT / 'src/data/github-contributions.json').read_text())
    days = activity['days']
    start = date.fromisoformat(activity['from'])
    if (not 350 <= len(days) <= 378 or sum(day['count'] for day in days) != activity['total']
            or days[-1]['date'] != activity['to']
            or any(day['date'] != (start + timedelta(days=i)).isoformat()
                   or not 0 <= day['level'] <= 4 or day['count'] < 0 for i, day in enumerate(days))):
        issues.append('The contribution snapshot is incomplete or inconsistent')
    for route in ['index.html', 'projects/index.html']:
        page = Page((dist / route).read_text())
        if '/projects' not in page.links or '/tags' in page.links:
            issues.append('Projects must replace the standalone Tags navigation: ' + route)
        if page.contributions != {day['date']: day['count'] for day in days}:
            issues.append('Rendered GitHub activity differs from its snapshot: ' + route)
        for project in projects:
            if project['url'] not in page.links:
                issues.append('Missing selected repository: ' + project['name'])
            if project['fork'] and 'https://github.com/' + project['parent'] not in page.links:
                issues.append('Missing fork attribution: ' + project['name'])
    logo = json.loads((ROOT / 'migration/pku-asset.json').read_text())
    if hashlib.sha256((dist / 'branding/pku-seal.svg').read_bytes()).hexdigest() != logo['sha256']:
        issues.append('PKU seal differs from the recorded source asset')
    for name, expected in json.loads((ROOT / 'migration/repaired-diagrams.json').read_text())['assets'].items():
        if hashlib.sha256((dist / 'migration-diagrams' / name).read_bytes()).hexdigest() != expected:
            issues.append('Repaired diagram differs from its provenance: ' + name)
    search = json.loads((dist / 'pagefind/pagefind-entry.json').read_text())
    if sum(data['page_count'] for data in search['languages'].values()) < len(report['posts']):
        issues.append('The search index is incomplete')
    if not any(lang.startswith('zh') for lang in search['languages']):
        issues.append('Chinese word segmentation must be preserved with the English interface')
    if issues:
        print('\n'.join(dict.fromkeys(issues)))
        raise SystemExit(1)
    print(f"OK: {len(report['posts'])} articles, {len(report['assets'])} original assets, {proofs} proofs, {math} math expressions, {len(list(dist.rglob('*.html')))} HTML pages; Blog, tags, archives, RSS, redirects, search, {len(projects)} projects, {len(days)} contribution days, 6 section backgrounds and {len(friends)} friends verified.")


if __name__ == '__main__':
    main()
