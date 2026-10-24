import fs from 'node:fs'
import path from 'node:path'
import { parseArgs } from 'node:util'
import YAML from 'yaml'

const root = path.resolve(import.meta.dirname, '..')
const { values, positionals } = parseArgs({ allowPositionals: true, options: {
  title: { type: 'string' }, course: { type: 'string' }, date: { type: 'string' }, help: { type: 'boolean' }
} })
if (values.help || !positionals.length) {
  console.log('Usage: pnpm new <slug> --title "文章标题" [--course ode] [--date YYYY-MM-DD]')
  console.log('Examples: pnpm new hello-world --title "第一篇博客"')
  console.log('          pnpm new ode/06 --title "第六章笔记"')
  process.exit(values.help ? 0 : 1)
}
const slug = positionals[0]
if (!/^[a-z0-9]+(?:[/-][a-z0-9]+)*$/.test(slug)) throw new Error('Use lowercase English letters, numbers, hyphens and optional course folders for the slug.')
if (!values.title || values.title.length > 60) throw new Error('Provide --title with at most 60 characters.')
const policy = JSON.parse(fs.readFileSync(path.join(root, 'src/data/course-tags.json'), 'utf8'))
const migration = JSON.parse(fs.readFileSync(path.join(root, 'migration/report.json'), 'utf8'))
const prefix = slug.split('/')[0]
const content = path.join(root, 'src/content/blog')
const courseNotes = fs.readdirSync(content, { recursive: true })
  .filter(name => /\.mdx?$/.test(name) && name.split(path.sep)[0] === prefix)
  .flatMap(name => {
    const front = fs.readFileSync(path.join(content, name), 'utf8').match(/^---\s*\n([\s\S]*?)\n---/)
    return front ? [YAML.parse(front[1])] : []
  })
const inferred = courseNotes.find(post => post.course)?.course || migration.posts.find(post => post.course && post.id.split('/')[0] === prefix)?.course
const selected = values.course || inferred
const course = selected && Object.keys(policy).find(key => key === selected || policy[key][1] === selected)
if (selected && !course) throw new Error('Unknown course; add it to src/data/course-tags.json first.')
const date = values.date || new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Shanghai' }).format(new Date())
if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || Number.isNaN(Date.parse(date))) throw new Error('Date must be YYYY-MM-DD.')
const file = path.join(root, 'src/content/blog', slug + '.md')
if (fs.existsSync(file)) throw new Error('The article already exists: ' + file)
const data = { title: values.title, description: '在这里写一句内容简介。', publishDate: date,
  tags: course ? policy[course] : ['博客'], draft: true, language: '中文' }
if (course) {
  data.course = course
  const orders = courseNotes.map(post => Number(post.order || 0))
  data.order = Math.max(0, ...orders) + 1
}
fs.mkdirSync(path.dirname(file), { recursive: true })
fs.writeFileSync(file, '---\n' + YAML.stringify(data) + '---\n\n## 开始\n\n在这里写正文。\n', { flag: 'wx' })
console.log('Created: ' + path.relative(root, file))
console.log('Run pnpm dev to preview. Set draft: false before publishing.')
