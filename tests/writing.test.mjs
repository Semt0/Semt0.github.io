import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { spawnSync } from 'node:child_process'
import YAML from 'yaml'
import { createPost, readWriting, resolveCourse, normalizeTags } from '../scripts/lib/writing.mjs'
import { openTypora, openBrowser, previewReady, waitForArticle } from '../scripts/lib/preview.mjs'

const project = path.resolve(import.meta.dirname, '..')
function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'blog-writing-'))
  t.after(() => fs.rmSync(root, { recursive: true, force: true }))
  fs.mkdirSync(path.join(root, 'src/data'), { recursive: true })
  fs.mkdirSync(path.join(root, 'src/content/blog/ode'), { recursive: true })
  for (const file of ['writing.json', 'course-tags.json'])
    fs.copyFileSync(path.join(project, 'src/data', file), path.join(root, 'src/data', file))
  fs.writeFileSync(
    path.join(root, 'src/content/blog/ode/05.md'),
    '---\ntitle: 第五章\ntags: [数学, ode]\norder: 5\n---\n原文\n'
  )
  return root
}
const options = { title: '测试文章', slug: 'example', date: '2026-10-24' }

test('blog and journal route automatically; new tags are preserved and deduplicated', (t) => {
  const root = fixture(t)
  const post = createPost(root, {
    ...options,
    title: '标题: "引号" $(literal)',
    tags: ['技术，Robotics', 'robotics'],
    tag: ['新标签']
  })
  assert.equal(post.id, 'writing/example')
  const meta = YAML.parse(fs.readFileSync(post.file, 'utf8').split('---')[1])
  assert.equal(meta.title, '标题: "引号" $(literal)')
  assert.deepEqual(meta.tags, ['技术', 'robotics', '新标签'])
  assert.equal(meta.draft, true)
  assert.equal(createPost(root, { ...options, type: 'journal' }).id, 'journal/example')
})

test('existing courses accept name, directory and tag; old ode/06 syntax still works', (t) => {
  const root = fixture(t)
  const post = createPost(root, { ...options, slug: 'ode/06' })
  assert.deepEqual(post.data.tags, ['数学', 'ode'])
  assert.equal(post.data.course, '常微分方程')
  assert.equal(post.data.order, 6)
  const next = createPost(root, { ...options, type: 'note', course: '常微分方程', slug: '07' })
  assert.equal(next.id, 'ode/07')
  assert.equal(next.data.order, 7)
  assert.equal(resolveCourse(readWriting(root), 'ODE'), '常微分方程')
})

test('new course registers tags and directory; subsequent notes reuse it without extra setup', (t) => {
  const root = fixture(t)
  const first = createPost(root, {
    ...options,
    type: 'note',
    course: '测度论',
    subject: '数学',
    folder: 'measure-theory',
    slug: '01'
  })
  assert.equal(first.id, 'measure-theory/01')
  assert.equal(first.registeredCourse, true)
  assert.deepEqual(readWriting(root).policy['测度论'], ['数学', '测度论'])
  const second = createPost(root, { ...options, slug: 'measure-theory/02' })
  assert.equal(second.data.order, 2)
  assert.equal(second.data.course, '测度论')
  assert.deepEqual(second.data.tags, ['数学', '测度论'])
})

test('new courses can use explicit tags including a new subject', (t) => {
  const root = fixture(t)
  const post = createPost(root, {
    ...options,
    type: 'note',
    course: '理论力学',
    folder: 'mechanics',
    tags: ['物理,理论力学']
  })
  assert.deepEqual(post.data.tags, ['物理', '理论力学'])
  assert.equal(resolveCourse(readWriting(root), 'mechanics'), '理论力学')
})

test('duplicate files, MDX routes and index aliases cannot be overwritten', (t) => {
  const root = fixture(t)
  const first = createPost(root, options)
  const before = fs.readFileSync(first.file, 'utf8')
  assert.throws(() => createPost(root, options), /不会覆盖/)
  assert.equal(fs.readFileSync(first.file, 'utf8'), before)
  fs.writeFileSync(path.join(root, 'src/content/blog/writing/other.mdx'), 'keep')
  assert.throws(() => createPost(root, { ...options, slug: 'other' }), /不会覆盖/)
  assert.throws(() => createPost(root, { ...options, slug: 'topic/index' }), /index/)
})

test('invalid dates, paths and symlinks do not mutate content or course registration', (t) => {
  const root = fixture(t)
  const policy = fs.readFileSync(path.join(root, 'src/data/course-tags.json'), 'utf8')
  for (const date of ['2026-02-30', 'not-a-date'])
    assert.throws(() => createPost(root, { ...options, date }), /日期/)
  for (const slug of ['../escape', '/tmp/escape', 'has space', 'x.md'])
    assert.throws(() => createPost(root, { ...options, slug }))
  fs.symlinkSync(os.tmpdir(), path.join(root, 'src/content/blog/writing'))
  assert.throws(() => createPost(root, options), /普通文件夹/)
  assert.equal(fs.readFileSync(path.join(root, 'src/data/course-tags.json'), 'utf8'), policy)
  assert.equal(fs.existsSync(path.join(root, '.astro/writing.lock')), false)
})

test('course tag mistakes and folder conflicts cannot relabel existing notes', (t) => {
  const root = fixture(t)
  assert.throws(
    () => createPost(root, { ...options, type: 'note', course: 'ode', tags: ['数学', '多余标签'] }),
    /固定标签/
  )
  assert.throws(
    () =>
      createPost(root, {
        ...options,
        type: 'note',
        course: '新课',
        subject: '数学',
        folder: 'ode'
      }),
    /已经属于/
  )
  assert.throws(
    () => createPost(root, { ...options, type: 'note', course: '新课', subject: '数学' }),
    /英文目录/
  )
  assert.deepEqual(readWriting(root).policy['常微分方程'], ['数学', 'ode'])
})

test('types can be extended through writing.json', (t) => {
  const root = fixture(t),
    state = readWriting(root)
  state.config.types.research = { label: '研究记录', directory: 'research', tags: ['研究'] }
  fs.writeFileSync(state.configFile, JSON.stringify(state.config))
  assert.equal(createPost(root, { ...options, type: 'research' }).id, 'research/example')
})

test('CLI flags create a draft without opening apps or starting servers', (t) => {
  const root = fixture(t)
  fs.mkdirSync(path.join(root, 'scripts/lib'), { recursive: true })
  for (const file of ['new-post.mjs', 'lib/writing.mjs', 'lib/preview.mjs'])
    fs.copyFileSync(path.join(project, 'scripts', file), path.join(root, 'scripts', file))
  fs.symlinkSync(path.join(project, 'node_modules'), path.join(root, 'node_modules'), 'dir')
  const result = spawnSync(
    process.execPath,
    [
      path.join(root, 'scripts/new-post.mjs'),
      '--type',
      'note',
      '--course',
      '测度论',
      '--subject',
      '数学',
      '--folder',
      'measure-theory',
      '--slug',
      '01',
      '--title',
      '第一章',
      '--no-open',
      '--no-preview'
    ],
    { encoding: 'utf8' }
  )
  assert.equal(result.status, 0, result.stderr)
  assert.ok(fs.existsSync(path.join(root, 'src/content/blog/measure-theory/01.md')))
  assert.match(result.stdout, /已登记新课程/)
  assert.equal(fs.readdirSync(path.join(root, '.astro')).length, 0)
})

test('tag validation and preview detection reject unsafe paths and static servers', async () => {
  assert.deepEqual(normalizeTags('数学,ODE，ode'), ['数学', 'ode'])
  assert.throws(() => normalizeTags('../escape'))
  assert.equal(
    await previewReady('http://local', async () => ({
      ok: true,
      text: async () => 'Semt0 /@vite/client'
    })),
    true
  )
  assert.equal(
    await previewReady('http://local', async () => ({
      ok: true,
      text: async () => 'Semt0 static preview'
    })),
    false
  )
  assert.equal(
    await previewReady('http://local', async () => {
      throw new Error('offline')
    }),
    false
  )
})

test(
  'app opening passes file paths and URLs as literal arguments',
  { skip: process.platform !== 'darwin' },
  () => {
    const calls = [],
      runner = (...args) => {
        calls.push(args)
        return { status: 0 }
      }
    const file = '/tmp/a b/$(literal).md'
    assert.equal(openTypora(file, runner), null)
    assert.deepEqual(calls[0][1], ['-a', 'Typora', file])
    assert.equal(openBrowser('http://127.0.0.1:4322/blog/writing/example', runner), null)
    assert.equal(calls[0][2].shell, undefined)
  }
)

test('preview waits for a newly created article to compile', async () => {
  let attempts = 0
  await waitForArticle('http://local/blog/example', async () => ({ ok: ++attempts > 1 }), 1000)
  assert.equal(attempts, 2)
  await assert.rejects(
    waitForArticle('http://local/blog/missing', async () => ({ ok: false }), 1),
    /编译/
  )
})
