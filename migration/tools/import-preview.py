#!/usr/bin/env python3
"""Repeatable migration of the adjacent public blog; source checkout stays untouched."""
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from urllib.request import ProxyHandler, build_opener
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import argparse
import hashlib
import html
import json
import posixpath
import re
import subprocess
import time
import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT.parent / 'semt0.github.io'
DOCS = SOURCE / 'docs'
COURSE_TAGS = json.loads((ROOT / 'src/data/course-tags.json').read_text())
COURSES = {
    'ODE': ('常微分方程', 'ode'),
    'Introduction to Foundation Models': ('基础模型', 'foundation-models'),
    'CVDL': ('CVDL', 'cvdl'), 'cs231n': ('CS231n', 'cs231n'),
    '复变函数': ('复变函数', 'complex-analysis'),
    '数理方程': ('数理方程', 'mathematical-physics'),
    '计算方法': ('计算方法', 'numerical-methods'),
    '算法设计与分析': ('算法设计与分析', 'algorithms'),
    '并行程序设计': ('并行程序设计', 'parallel-programming'),
    'Rust程序设计': ('Rust程序设计', 'rust'),
    'OJ复习': ('OJ复习', 'oj'), 'ai硬件': ('AI硬件', 'ai-hardware'),
    '抽象代数': ('抽象代数', 'abstract-algebra')
}
ADMONITION = re.compile(r'^( *)(!!!|\?\?\?\+?)\s*([\w-]+)(?:\s+(.*))?$')
TAB = re.compile(r'^( *)===\s+"(.*)"\s*$')
IMAGE = re.compile(r'!\[([^\]\n]*)\]\(([^)\n]+)\)(?:[ \t]*\{([^}\n]*)\})?')
LINK = re.compile(r'(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)')
NAMES = {'abstract': '定义与定理', 'tip': '提示', 'tips': '提示', 'info': '补充说明',
         'note': '说明', 'warning': '注意', 'example': '例题', 'summary': '总结', 'question': '问题'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def split_front(raw):
    match = re.match(r'\A---\s*\n(.*?)\n---\s*(?:\n|$)', raw, re.S)
    meta = (yaml.safe_load(match[1]) or {}) if match else {}
    return {str(k).lower(): v for k, v in meta.items()}, raw[match.end():] if match else raw


def outside_code(text, transform):
    """Keep literal examples and fenced source code untouched."""
    output, block, fence = [], [], None
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            token = marker[1]
            if fence is None:
                output.append(transform(''.join(block)))
                block, fence = [], token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            output.append(line)
        elif fence:
            output.append(line)
        else:
            block.append(line)
    output.append(transform(''.join(block)))
    return ''.join(output)


def normalize_math(lines):
    output, display, fence = [], False, None
    for line in lines:
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        if not fence:
            if line.strip() == '$$':
                display = not display
            elif display and line.rstrip().endswith('$$'):
                indent = line[:len(line) - len(line.lstrip())]
                output.extend([line.rstrip()[:-2], indent + '$$', ''])
                display = False
                continue
        output.append(line)
    return output


def convert_blocks(lines):
    """Preserve nested MkDocs callouts, disclosures and tab-panel contents."""
    result, i, fence = [], 0, None
    while i < len(lines):
        line = lines[i]
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            result.append(line)
            i += 1
            continue
        admonition = None if fence else ADMONITION.match(line)
        tab = None if fence else TAB.match(line)
        if not admonition and not tab:
            result.append(line)
            i += 1
            continue
        indent = (admonition or tab)[1]
        required = len(indent) + 4
        body, j = [], i + 1
        while j < len(lines):
            following = lines[j]
            spaces = len(following) - len(following.lstrip(' '))
            if following.strip() and spaces < required:
                break
            body.append(following[required:] if following.strip() else '')
            j += 1
        inner = convert_blocks(body)
        nested = [len(m[1]) for s in inner if (m := re.match(r'^(:{3,})', s))]
        colon = ':' * (max(nested, default=2) + 1)
        if tab:
            component, kind, title, opened = 'study-tab', 'tab', tab[2], ''
        else:
            _, marker, kind, title = admonition.groups()
            component = 'study-proof' if marker.startswith('?') else 'study-note'
            opened = ' open="true"' if marker == '???+' else ''
            title = (title or NAMES.get(kind, kind)).strip().strip('"')
        # Directive labels support balanced brackets; escaping them corrupts TeX such as sqrt[3].
        result.extend(['', f'{indent}{colon}{component}[{title}]{{kind="{kind}"{opened}}}', ''])
        result.extend(indent + s if s else '' for s in inner)
        result.extend(['', indent + colon, ''])
        i = j
    return result


def inventory():
    files = sorted(p for base in ('note', 'blog', 'essay') for p in (DOCS / base).rglob('*.md') if p.stem != 'index')
    nav = (SOURCE / 'zensical.toml').read_text()
    mapping_file = ROOT / 'migration/content-map.json'
    mapping = json.loads(mapping_file.read_text()) if mapping_file.exists() else {}
    sample = json.loads((ROOT / 'migration/sample-report.json').read_text())
    samples = {p['source']: p for p in sample['posts']}
    counts, records = Counter(), []
    def nav_key(path):
        key = '"' + path.relative_to(DOCS).as_posix() + '"'
        return nav.find(key) if key in nav else 100000, path.as_posix()
    for path in sorted(files, key=nav_key):
        relative = path.relative_to(DOCS).as_posix()
        meta, body = split_front(path.read_text(encoding='utf-8-sig'))
        section = relative.split('/')[0]
        group = relative.split('/')[1] if section == 'note' else section
        counts[group] += 1
        course, prefix = COURSES[group] if section == 'note' else ('', 'journal' if section == 'essay' else 'writing')
        if relative not in mapping:
            sample = samples.get(relative)
            stem = re.sub(r'[^a-z0-9]+', '-', path.stem.lower()).strip('-')
            suffix = stem if re.search('[a-z]', stem) and not re.search('[\u4e00-\u9fff]', path.stem) else f'{counts[group]:02d}'
            mapping[relative] = sample['id'] if sample else prefix + '/' + suffix
        records.append({'source': relative, 'id': mapping[relative], 'course': course, 'order': counts[group],
                        'meta': meta, 'body': body, 'section': section, 'sample_slug': samples.get(relative, {}).get('slug')})
    if len(set(mapping.values())) != len(mapping):
        raise ValueError('Duplicate stable article IDs')
    mapping_file.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + '\n')
    return records, mapping


def main():
    global SOURCE, DOCS
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True, help='Separate checkout of the original Zensical blog')
    parser.add_argument('--offline', action='store_true', help='Only use verified local assets')
    parser.add_argument('--force', action='store_true', help='Explicitly overwrite imported articles edited since the last migration')
    args = parser.parse_args()
    SOURCE = args.source.resolve()
    DOCS = SOURCE / 'docs'
    if SOURCE == ROOT or not DOCS.is_dir():
        raise ValueError('Use a separate checkout of the old blog as --source')
    records, mapping = inventory()
    prior_report = json.loads((ROOT / 'migration/report.json').read_text())
    prior_posts = {entry['source']: entry for entry in prior_report['posts']}
    optimized_path = ROOT / 'migration/optimized-assets.json'
    optimized = json.loads(optimized_path.read_text()) if optimized_path.exists() else {}
    revision = subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', 'HEAD'], text=True).strip()
    tree = subprocess.check_output(['git', '-C', str(SOURCE), 'ls-tree', '-rz', 'HEAD', 'docs'], text=True)
    blobs = {record.split('\t')[1][5:]: record.split('\t')[0].split()[2] for record in tree.split('\0') if record}
    asset_paths, unresolved = set(), []
    routes = {relative: '/blog/' + slug for relative, slug in mapping.items()}
    routes.update({'index.md': '/', 'note/index.md': '/blog', 'blog/index.md': '/blog',
                   'essay/index.md': '/tags/' + quote('手记'), 'friends.md': '/links'})

    def target_url(target, relative, assets):
        target = target.strip().strip('<>')
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            return target
        path = posixpath.normpath(posixpath.join(posixpath.dirname(relative), unquote(url.path))) if not url.path.startswith('/') else unquote(url.path).lstrip('/')
        replacements = {'note/复变函数/pictures/complex_plane.svg': '/migration-diagrams/complex-plane.svg',
                        'note/复变函数/pictures/connected_domain.svg': '/migration-diagrams/connected-domains.svg'}
        if path in replacements:
            return replacements[path]
        for candidate in (path, path + '.md', path.rstrip('/') + '/index.md'):
            if candidate in routes:
                return routes[candidate] + (('?' + url.query) if url.query else '') + (('#' + url.fragment) if url.fragment else '')
        if path in blobs or (DOCS / path).is_file():
            asset_paths.add(path)
            assets.add(path)
            return '/media/' + quote(optimized.get(path, {}).get('output', path), safe='/') + (('#' + url.fragment) if url.fragment else '')
        unresolved.append({'source': relative, 'target': target})
        return target

    report = {'source_commit': revision, 'source_root': str(SOURCE),
              'scope': 'All existing articles in docs/note, docs/blog, docs/essay; generated indexes replaced by Blog/tags/archives.',
              'posts': [], 'assets': {}, 'unresolved_links': unresolved,
              'courses': {label: sum(r['course'] == label for r in records) for label, _ in COURSES.values()}}
    pending = []
    sample_sources = {p['source'] for p in json.loads((ROOT / 'migration/sample-report.json').read_text())['posts']}
    for record in records:
        relative, meta, body = record['source'], record['meta'], record['body']
        assets = set()
        legacy_math = Counter()
        def normalize_tex_delimiters(chunk):
            def prose(part):
                def pair(match):
                    display = match[2] is not None
                    legacy_math['display' if display else 'inline'] += 1
                    delimiter = '$$' if display else '$'
                    return delimiter + (match[2] if display else match[1]) + delimiter
                return re.sub(r'\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]', pair, part)
            return ''.join(part if i % 2 else prose(part) for i, part in enumerate(re.split(r'(`[^`\n]*`|\$\$[\s\S]*?\$\$|(?<!\\)\$(?:\\.|[^$\n])+\$)', chunk)))
        normalized = outside_code(body, normalize_tex_delimiters)
        empty_items = Counter()
        def normalize_empty_items(chunk):
            def merge(match):
                empty_items['fixed'] += 1
                return match[1] + match[2] + ' ' + match[3] + '\n'
            return re.sub(r'^( *)(\d+\.)[ \t]*\n(?:[ \t]*\n)+\1 {4}(!\[[^\n]+)\n', merge, chunk, flags=re.M)
        normalized = outside_code(normalized, normalize_empty_items)
        table_math = Counter()
        def normalize_table_math(chunk):
            def line(text):
                if not text.lstrip().startswith('|'):
                    return text
                def formula(match):
                    value = match[1]
                    if '|' in value:
                        table_math['formulas'] += 1
                        value = value.replace('\\|', '\\Vert ').replace('|', '\\vert ')
                    return '$' + value + '$'
                return re.sub(r'(?<![\\$])\$(?!\$)([^$\n]+)(?<!\\)\$', formula, text)
            return '\n'.join(line(text) for text in chunk.split('\n'))
        normalized = outside_code(normalized, normalize_table_math)
        image_refs = Counter()
        def transform(text):
            def image(match):
                image_refs['count'] += 1
                alt, target, attrs = match.groups()
                rewritten = target_url(target, relative, assets)
                width = re.search(r'width\s*=\s*["\x27]?(\d+)', attrs or '')
                width_attr = f' width="{width[1]}"' if width else ''
                return f'<img src="{html.escape(rewritten, quote=True)}" alt="{html.escape(alt, quote=True)}"{width_attr} loading="lazy" decoding="async">'
            def prose(chunk):
                chunk = LINK.sub(lambda m: f'[{m[1]}]({target_url(m[2], relative, assets)})', chunk)
                return re.sub(r'==([^=\n]+)==', r'<mark>\1</mark>', chunk)
            # Image alt text may itself contain TeX; resolve the complete image before protecting math.
            text = ''.join(part if i % 2 else IMAGE.sub(image, part)
                           for i, part in enumerate(re.split(r'(`[^`\n]*`)', text)))
            # Never interpret TeX bracket pairs or inline code as Markdown links/marks.
            return ''.join(part if i % 2 else prose(part) for i, part in enumerate(re.split(r'(`[^`\n]*`|\$\$[\s\S]*?\$\$|(?<!\\)\$(?:\\.|[^$\n])+\$)', text)))
        lines = [re.sub(r'^[ \t]+', lambda m: m[0].expandtabs(4), line) for line in normalized.splitlines()]
        converted = outside_code('\n'.join(convert_blocks(normalize_math(lines))) + '\n', transform)
        title = str(meta.get('title') or Path(relative).stem)
        summary = re.sub(r'\s+', ' ', str(meta.get('summary') or '')).strip()
        previous = ROOT / 'src/content/blog' / (record['id'] + '.md')
        prior = prior_posts.get(relative, {})
        if previous.exists() and prior.get('file_sha256') and sha(previous.read_bytes()) != prior['file_sha256'] and not args.force:
            raise ValueError('Imported article edited locally; preserve it or explicitly use --force: ' + str(previous))
        previous_meta = split_front(previous.read_text())[0] if previous.exists() else {}
        description = previous_meta.get('description') if relative in sample_sources else None
        description = str(description or summary or (f"{record['course']} · {title}" if record['course'] else title))[:160]
        tags = COURSE_TAGS[record['course']] if record['course'] else list(dict.fromkeys(
            ['手记' if record['section'] == 'essay' else '博客'] + (meta.get('tags') or [])))
        metadata = {'title': title, 'description': description, 'publishDate': str(meta['date'])[:10], 'tags': tags,
                    'draft': bool(meta.get('draft', False)), 'language': '中文', 'comment': meta.get('comments', True) is not False, 'sourcePath': relative,
                    'commentPath': meta.get('comment_path') or '/' + quote(str(Path(relative).with_suffix('')), safe='/') + '/'}
        if record['course']:
            metadata['order'] = record['order']
        raw = (DOCS / relative).read_bytes()
        syntax = Counter()
        def count_syntax(chunk):
            for key, pattern in [('proofs', r'^ *\?\?\?'), ('admonitions', r'^ *(?:!!!|\?\?\?)'), ('tabs', r'^ *===\s+"'), ('open_proofs', r'^ *\?\?\?\+')]:
                syntax[key] += len(re.findall(pattern, chunk, re.M))
            return chunk
        outside_code(body, count_syntax)
        entry = {'source': relative, 'source_sha256': sha(raw), 'collection': 'blog', 'id': record['id'],
                 'route': '/blog/' + record['id'], 'old_route': '/' + str(Path(relative).with_suffix('')),
                 'course': record['course'], 'tags': [t.lower() for t in tags], 'assets': sorted(assets),
                 **{key: syntax[key] for key in ('proofs', 'admonitions', 'tabs', 'open_proofs')},
                 'body_sha256': sha(converted.encode()), 'legacy_math_pairs_converted': dict(legacy_math),
                 'table_math_pipes_normalized': table_math['formulas'],
                 'empty_list_items_fixed': empty_items['fixed'], 'images': image_refs['count'],
                 'math_delimiters_preserved': body.count('$') + 2 * legacy_math['inline'] + 4 * legacy_math['display'] == converted.count('$')}
        if record['sample_slug']:
            entry['sample_slug'] = record['sample_slug']
        entry['file_sha256'] = sha(('---\n' + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + '---\n' + converted).encode())
        if not entry['math_delimiters_preserved']:
            raise ValueError('Math delimiters changed: ' + relative)
        pending.append((record, metadata, converted, raw))
        report['posts'].append(entry)
    (ROOT / 'migration/pending-inventory.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if unresolved:
        raise ValueError('Unresolved source links; see migration/pending-inventory.json')
    proxy_result = subprocess.run(['git', '-C', str(SOURCE), 'config', '--get-urlmatch', 'http.proxy', 'https://github.com'], capture_output=True, text=True)
    proxy = proxy_result.stdout.strip()
    def restore(relative):
        expected = blobs.get(relative)
        caches = [DOCS / relative, ROOT / 'migration/asset-cache' / relative, ROOT / 'public/media' / relative, ROOT.parent / 'fuwari-preview/public/media' / relative]
        data = None
        for cache in caches:
            if cache.is_file():
                candidate = cache.read_bytes()
                if not expected or hashlib.sha1(f'blob {len(candidate)}\0'.encode() + candidate).hexdigest() == expected:
                    data = candidate
                    break
        if data is None:
            if args.offline:
                raise FileNotFoundError('Not cached: ' + relative)
            address = f'https://raw.githubusercontent.com/Semt0/Semt0.github.io/{revision}/docs/' + quote(relative, safe='/')
            for attempt in range(3):
                try:
                    opener = build_opener(ProxyHandler({'https': proxy, 'http': proxy})) if proxy else build_opener()
                    with opener.open(address, timeout=40) as response:
                        data = response.read()
                    break
                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(attempt + 1)
        if expected and hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest() != expected:
            raise ValueError('Source Git blob mismatch: ' + relative)
        destination = ROOT / ('migration/asset-cache' if relative in optimized else 'public/media') / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        return relative, sha(data)
    print(f'Migrating {len(records)} articles; restoring {len(asset_paths)} referenced assets from commit {revision[:8]}…', flush=True)
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {pool.submit(restore, p): p for p in sorted(asset_paths)}
        for i, future in enumerate(as_completed(futures), 1):
            relative, digest = future.result()
            report['assets'][relative] = digest
            if i % 100 == 0 or i == len(futures):
                print(f'Assets verified: {i}/{len(futures)}', flush=True)
    for record, metadata, converted, raw in pending:
        destination = ROOT / 'src/content/blog' / (record['id'] + '.md')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text('---\n' + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + '---\n' + converted)
        original = ROOT / 'migration/originals' / record['source']
        original.parent.mkdir(parents=True, exist_ok=True)
        original.write_bytes(raw)
    redirects = json.loads((ROOT / 'src/legacy-note-redirects.json').read_text())
    redirects.update({'/note': '/blog', '/essay': '/tags/手记', '/friends': '/links'})
    redirects.update({entry['old_route']: entry['route'] for entry in report['posts'] if entry['old_route'] != entry['route']})
    (ROOT / 'src/legacy-note-redirects.json').write_text(json.dumps(redirects, ensure_ascii=False, indent=2) + '\n')
    report['assets'] = dict(sorted(report['assets'].items()))
    (ROOT / 'migration/report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'migration/pending-inventory.json').unlink(missing_ok=True)
    print(f"Imported {len(records)} articles, {len(report['courses'])} courses and {len(report['assets'])} verified assets. Source checkout untouched.", flush=True)


if __name__ == '__main__':
    main()
