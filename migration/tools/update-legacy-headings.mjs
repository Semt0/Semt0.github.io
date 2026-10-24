import fs from 'node:fs'
import path from 'node:path'
import { fromHtml } from 'hast-util-from-html'
import { visit } from 'unist-util-visit'
import { pathToFileURL } from 'node:url'
import legacyRedirects from '../../src/plugins/legacy-redirects.ts'

const root = path.resolve(import.meta.dirname, '../..')
const sourceSite = process.argv[2]
if (!sourceSite) throw new Error('Usage: node migration/tools/update-legacy-headings.mjs /path/to/old/site')
const report = JSON.parse(fs.readFileSync(path.join(root, 'migration/report.json'), 'utf8'))
function headingText(node) {
  if (node.type === 'text') return node.value
  const classes = node.properties?.className || []
  if (classes.includes('anchor') || classes.includes('headerlink')) return ''
  if (classes.includes('katex')) {
    let tex = ''
    visit(node, 'element', item => {
      if (item.tagName === 'annotation' && item.properties?.encoding === 'application/x-tex') {
        tex = (item.children || []).map(headingText).join('')
      }
    })
    return tex
  }
  return (node.children || []).map(headingText).join('')
}
function headings(file) {
  const values = []
  visit(fromHtml(fs.readFileSync(file, 'utf8')), 'element', node => {
    if (/^h[1-6]$/.test(node.tagName) && node.properties?.id) {
      const label = headingText(node).replace(/\\[()[\]]/g, '').replace(/[^\p{L}\p{N}]+/gu, '').toLowerCase()
      values.push({ id: node.properties.id, rank: node.tagName, label })
    }
  })
  return values
}
const routes = {}, unmatched = []
let count = 0
for (const post of report.posts) {
  const oldFile = path.join(sourceSite, post.old_route, 'index.html')
  const newFile = path.join(root, 'dist', post.route, 'index.html')
  if (!fs.existsSync(oldFile)) throw new Error('Original built page needed for heading mapping: ' + post.old_route)
  const old = headings(oldFile), current = headings(newFile)
  const map = {}
  let cursor = 0
  for (const heading of old) {
    const index = current.findIndex((entry, i) => i >= cursor && entry.rank === heading.rank && entry.label === heading.label)
    if (index < 0) { unmatched.push({ route: post.old_route, ...heading }); continue }
    cursor = index + 1
    map[heading.id] = current[index].id
    count++
  }
  routes[post.old_route] = map
}
fs.writeFileSync(path.join(root, 'migration/legacy-heading-map.json'), JSON.stringify({ sourceCommit: report.source_commit, count, routes, unmatched }, null, 2) + '\n')
console.log(`Matched ${count} old headings across ${report.posts.length} articles; ${unmatched.length} need inspection.`)
const redirects = JSON.parse(fs.readFileSync(path.join(root, 'src/legacy-note-redirects.json'), 'utf8'))
await legacyRedirects(redirects).hooks['astro:build:done']({ dir: pathToFileURL(path.join(root, 'dist/')) })
