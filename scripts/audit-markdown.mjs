import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { unified } from 'unified'
import remarkParse from 'remark-parse'
import remarkGfm from 'remark-gfm'
import remarkMdx from 'remark-mdx'
import remarkMath from 'remark-math'
import remarkDirective from 'remark-directive'
import { visit } from 'unist-util-visit'
import { slug as githubSlug } from 'github-slugger'
import YAML from 'yaml'
import katex from 'katex'

const root = path.resolve(import.meta.dirname, '..')
const base = path.join(root, 'src/content/blog')
const migration = JSON.parse(fs.readFileSync(path.join(root, 'migration/report.json'), 'utf8'))
const policy = JSON.parse(fs.readFileSync(path.join(root, 'src/data/course-tags.json'), 'utf8'))
const sourceById = new Map(migration.posts.map(post => [post.id, post]))
const courseByPrefix = Object.fromEntries(migration.posts.filter(post => post.course).map(post => [post.id.split('/')[0], post.course]))
const posts = [], errors = []
for (const relative of fs.readdirSync(base, { recursive: true }).filter(name => /\.mdx?$/.test(name)).sort()) {
  const raw = fs.readFileSync(path.join(base, relative), 'utf8')
  const front = raw.match(/^---\s*\n([\s\S]*?)\n---\s*\n/)
  if (!front) throw new Error('Missing frontmatter: ' + relative)
  const meta = YAML.parse(front[1])
  const text = raw.slice(front[0].length)
  const id = meta.slug || relative.replace(/\.mdx?$/, '').split(path.sep).map(githubSlug).join('/').replace(/\/index$/, '')
  const imported = sourceById.get(id)
  const course = meta.course || imported?.course || courseByPrefix[id.split('/')[0]] || ''
  const tags = [...new Set((meta.tags || []).map(tag => tag.toLowerCase()))]
  if (course && JSON.stringify(tags) !== JSON.stringify(policy[course])) throw new Error('Use the subject/course tags configured in src/data/course-tags.json: ' + relative)
  let parser = unified().use(remarkParse).use(remarkGfm).use(remarkMath).use(remarkDirective)
  if (relative.endsWith('.mdx')) parser = parser.use(remarkMdx)
  const tree = parser.parse(text)
  const entry = { ...(imported || {}), id, file: 'src/content/blog/' + relative.split(path.sep).join('/'),
    route: '/blog/' + id, course, title: meta.title, tags, publishDate: String(meta.publishDate),
    order: meta.order, draft: !!meta.draft, comment: meta.comment !== false,
    commentPath: meta.commentPath || '/blog/' + id,
    body_sha256: crypto.createHash('sha256').update(text).digest('hex'),
    math: 0, code: 0, admonitions: 0, proofs: 0, open_proofs: 0, tabs: 0, images: 0 }
  visit(tree, node => {
    if (node.type === 'math' || node.type === 'inlineMath') {
      entry.math++
      try { katex.renderToString(node.value, { throwOnError: true, strict: 'ignore', displayMode: node.type === 'math' }) }
      catch (error) { if (!entry.draft) errors.push({ id, line: node.position.start.line, error: String(error) }) }
    }
    if (node.type === 'code') entry.code++
    if (node.type === 'image') entry.images++
    if (node.type === 'html') entry.images += [...node.value.matchAll(/<img\b/gi)].length
    if (node.type === 'mdxJsxFlowElement' || node.type === 'mdxJsxTextElement') { if (node.name === 'img') entry.images++ }
    if (node.type === 'containerDirective') {
      if (['study-note', 'study-proof'].includes(node.name)) entry.admonitions++
      if (node.name === 'study-proof') { entry.proofs++; if (node.attributes?.open === 'true') entry.open_proofs++ }
      if (node.name === 'study-tab') entry.tabs++
    }
  })
  posts.push(entry)
}
if (new Set(posts.map(post => post.id)).size !== posts.length) throw new Error('Duplicate article slugs')
const output = path.join(root, '.astro/markdown-audit.json')
fs.mkdirSync(path.dirname(output), { recursive: true })
fs.writeFileSync(output, JSON.stringify({ posts, errors }, null, 2) + '\n')
console.log(`${posts.length} Markdown articles; ${posts.filter(post => post.draft).length} drafts; ${posts.reduce((n, post) => n + post.math, 0)} math expressions; ${errors.length} TeX errors`)
if (errors.length) { console.error(errors.slice(0, 12)); process.exitCode = 1 }
