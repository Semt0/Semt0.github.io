#!/usr/bin/env python3
"""Validate rendered routes, comment mounts and local custom assets after a build."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from update_site import ROOT, collect, frontmatter


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.classes = []
        self.assets = []
        self.links = []
        self.comment_paths = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.classes.extend(attrs.get('class', '').split())
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'script' and 'src' in attrs:
            self.assets.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.assets.append(attrs['href'])
        if attrs.get('id') == 'waline':
            self.comment_paths.append(attrs.get('data-comment-path', ''))
        if 'data-client-url' in attrs:
            self.assets.append(attrs['data-client-url'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])


def check(root=ROOT):
    site = root / 'site'
    errors = []
    pages = list(site.rglob('*.html'))
    if not pages:
        raise ValueError('No built pages; run zensical build first')
    for path in pages:
        page = Page(path.read_text())
        if Counter(page.ids)['waline'] > 1:
            errors.append(f'{path}: duplicate comment mount')
        for url in page.assets:
            parts = urlsplit(url)
            if not parts.netloc and not parts.scheme:
                target = site / unquote(parts.path.lstrip('/')) if parts.path.startswith('/') else path.parent / unquote(parts.path)
                if not target.is_file():
                    errors.append(f'{path}: missing asset {url}')
    sources = [root / 'docs' / entry.path for entry in collect(root / 'docs')]
    sources += [root / 'docs' / name for name in ('index.md', 'blog/index.md', 'note/index.md', 'essay/index.md', 'friends.md')]
    for source in sources:
        rel = source.relative_to(root / 'docs')
        route = rel.with_suffix('.html') if source.name == 'index.md' else rel.with_suffix('') / 'index.html'
        output = site / route
        if not output.is_file():
            errors.append(f'Missing page: {route}')
            continue
        expected = frontmatter(source.read_text()).get('comments') is not False
        if Page(output.read_text()).ids.count('waline') != int(expected):
            errors.append(f'{route}: comments enabled={expected}, incorrect mount count')
    home = Page((site / 'index.html').read_text())
    if home.classes.count('home-hero') != 1 or home.classes.count('home-destination') != 3:
        errors.append('Homepage content was replaced or section links are missing')
    if 'waline' in home.ids:
        errors.append('Homepage must not load comments')
    friends = Page((site / 'friends/index.html').read_text())
    if friends.comment_paths != ['/']:
        errors.append('Friends page must preserve the original homepage comment thread')
    entries = collect(root / 'docs')
    for section in ('blog', 'note', 'essay'):
        page = Page((site / section / 'index.html').read_text())
        if page.classes.count('timeline-item') != sum(e.section == section for e in entries):
            errors.append(f'{section}: timeline entry count does not match source articles')
    # Generated links are checked separately from historical article references.
    for index in ('index.html', 'blog/index.html', 'note/index.html', 'essay/index.html', 'friends/index.html'):
        path = site / index
        for href in Page(path.read_text()).links:
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            target = site / unquote(url.path.lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
            if not target.exists():
                errors.append(f'{index}: broken link {href}')
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'Checked {len(pages)} pages: routes, comment mounts, assets and index links OK')


if __name__ == '__main__':
    check()
