import fs from 'node:fs'
import path from 'node:path'
import YAML from 'yaml'

const slugPattern = /^[a-z0-9]+(?:[/-][a-z0-9]+)*$/
export function normalizeTags(value = []) {
  const tags = [
    ...new Set(
      [value]
        .flat()
        .flatMap((item) => String(item).split(/[,，]/))
        .map((tag) => tag.normalize('NFC').trim().toLowerCase())
        .filter(Boolean)
    )
  ]
  if (tags.some((tag) => /[/\\?#\x00-\x1f]/.test(tag) || ['.', '..'].includes(tag))) {
    throw new Error('标签不能包含 /、\\、?、# 或控制字符。')
  }
  return tags
}

export function readWriting(root) {
  const configFile = path.join(root, 'src/data/writing.json')
  const policyFile = path.join(root, 'src/data/course-tags.json')
  const config = JSON.parse(fs.readFileSync(configFile, 'utf8'))
  const policy = JSON.parse(fs.readFileSync(policyFile, 'utf8'))
  const base = path.join(root, 'src/content/blog')
  const posts = fs
    .readdirSync(base, { recursive: true })
    .filter((name) => /\.mdx?$/.test(name))
    .map((name) => {
      const front = fs.readFileSync(path.join(base, name), 'utf8').match(/^---\s*\n([\s\S]*?)\n---/)
      return { name: name.split(path.sep).join('/'), meta: front ? YAML.parse(front[1]) : {} }
    })
  const tags = normalizeTags([
    ...posts.flatMap((post) => post.meta.tags || []),
    ...Object.values(policy).flat()
  ])
  return { configFile, policyFile, config, policy, base, posts, tags }
}

export function resolveCourse(state, value) {
  if (!value) return undefined
  const needle = value.normalize('NFC').trim().toLowerCase()
  return Object.keys(state.policy).find((course) =>
    [course, state.config.courses[course], state.policy[course][1]].some(
      (alias) => alias?.toLowerCase() === needle
    )
  )
}

export function inferType(state, slug = '') {
  const prefix = slug.split('/')[0]
  if (Object.values(state.config.courses).includes(prefix)) return 'note'
  return (
    Object.keys(state.config.types).find((type) => state.config.types[type].directory === prefix) ||
    'blog'
  )
}

function safeDirectory(base, directory) {
  let current = base
  for (const segment of directory.split('/').filter(Boolean)) {
    current = path.join(current, segment)
    if (
      fs.existsSync(current) &&
      (!fs.lstatSync(current).isDirectory() || fs.lstatSync(current).isSymbolicLink())
    ) {
      throw new Error('目标目录必须是博客内的普通文件夹：' + current)
    }
  }
}

function atomicJson(file, value) {
  const temp = file + '.' + process.pid + '.tmp'
  try {
    fs.writeFileSync(temp, JSON.stringify(value, null, 2) + '\n', { flag: 'wx' })
    fs.renameSync(temp, file)
  } finally {
    if (fs.existsSync(temp)) fs.unlinkSync(temp)
  }
}

export function createPost(root, options) {
  const lock = path.join(root, '.astro/writing.lock')
  fs.mkdirSync(path.dirname(lock), { recursive: true })
  let lockFd
  try {
    lockFd = fs.openSync(lock, 'wx')
  } catch {
    throw new Error('另一个新建命令正在执行。若上次异常退出，可删除 .astro/writing.lock 后重试。')
  }
  try {
    const state = readWriting(root)
    const inputSlug = options.slug?.trim()
    if (!inputSlug || !slugPattern.test(inputSlug) || inputSlug.split('/').at(-1) === 'index')
      throw new Error('文件名使用小写英文、数字、短横线，可用 / 分层，末尾不能是 index。')
    const title = options.title?.trim()
    if (!title || title.length > 60) throw new Error('请填写不超过 60 个字符的 --title。')
    const description = options.description?.trim() || '在这里写一句内容简介。'
    if (description.length > 160) throw new Error('简介不能超过 160 个字符。')
    const date =
      options.date ||
      new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Shanghai' }).format(new Date())
    if (
      !/^\d{4}-\d{2}-\d{2}$/.test(date) ||
      Number.isNaN(Date.parse(date)) ||
      new Date(date).toISOString().slice(0, 10) !== date
    ) {
      throw new Error('日期必须是真实的 YYYY-MM-DD 日期。')
    }
    const type = options.type || (options.course ? 'note' : inferType(state, inputSlug))
    if (!Object.hasOwn(state.config.types, type))
      throw new Error('未知类型。运行 pnpm write --list 查看可选类型。')
    const typeConfig = state.config.types[type]
    let directory = options.folder || typeConfig.directory
    let course,
      registration = false
    let tags = normalizeTags([options.tags, options.tag].filter(Boolean).flat())
    if (type === 'note') {
      const requested = options.course || inputSlug.split('/')[0]
      course = resolveCourse(state, requested)
      if (course) {
        directory = state.config.courses[course] || options.folder
        const expected = normalizeTags(state.policy[course])
        if (tags.length && JSON.stringify(tags) !== JSON.stringify(expected))
          throw new Error(`这门课程使用两个固定标签：${expected.join('、')}。`)
        if (options.subject && normalizeTags(options.subject)[0] !== expected[0])
          throw new Error('学科与已有课程不一致。')
        if (options.folder && state.config.courses[course] && options.folder !== directory)
          throw new Error('已有课程请使用目录 ' + directory)
        tags = expected
      } else {
        course = requested.normalize('NFC').trim()
        if (
          !course ||
          /[\x00-\x1f]/.test(course) ||
          ['__proto__', 'constructor', 'prototype'].includes(course)
        )
          throw new Error('课程名称无效。')
        directory =
          options.folder || (/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(course) ? course : undefined)
        if (!directory)
          throw new Error('新中文课程请用 --folder 指定英文目录，例如 --folder measure-theory。')
        if (!tags.length && options.subject) tags = normalizeTags([options.subject, course])
        if (tags.length !== 2)
          throw new Error('新课程需要两个标签：使用 --tags "数学,测度论"，或 --subject 数学。')
        if (options.subject && normalizeTags(options.subject)[0] !== tags[0])
          throw new Error('--subject 应与第一个标签一致。')
        if (
          Object.values(state.config.courses).includes(directory) ||
          Object.values(state.config.types).some((item) => item.directory === directory)
        ) {
          throw new Error('这个目录已经属于其他课程或内容类型，请换一个 --folder。')
        }
        if (Object.keys(state.policy).some((key) => state.policy[key][1] === tags[1]))
          throw new Error('该课程标签已有归属，请使用已有课程名称或换一个标签。')
        registration = true
      }
    } else {
      if (options.course || options.subject)
        throw new Error('--course 和 --subject 只适用于 note 类型。')
      if (!tags.length) tags = normalizeTags(typeConfig.tags)
      if (Object.values(state.config.courses).includes(directory))
        throw new Error('该文件夹属于课程笔记，请使用 --type note。')
    }
    if (!directory || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(directory))
      throw new Error('--folder 使用单层小写英文目录，例如 measure-theory。')
    const slug = inputSlug.startsWith(directory + '/')
      ? inputSlug.slice(directory.length + 1)
      : inputSlug
    const id = directory + '/' + slug
    const file = path.join(state.base, id + '.md')
    safeDirectory(state.base, path.dirname(id))
    if (
      fs.existsSync(file) ||
      fs.existsSync(file.replace(/\.md$/, '.mdx')) ||
      fs.existsSync(path.join(state.base, id, 'index.md')) ||
      fs.existsSync(path.join(state.base, id, 'index.mdx'))
    ) {
      throw new Error('文章已存在，不会覆盖：' + file)
    }
    if (registration && state.posts.some((post) => post.name.startsWith(directory + '/')))
      throw new Error('这个目录已有文章，请选择空目录，避免改变已有内容的分类。')
    const data = { title, description, publishDate: date, tags, draft: true, language: '中文' }
    if (course) {
      data.course = course
      data.order =
        Math.max(
          0,
          ...state.posts
            .filter((post) => post.meta.course === course || post.name.startsWith(directory + '/'))
            .map((post) => Number(post.meta.order) || 0)
        ) + 1
    }
    const originals = [state.policyFile, state.configFile].map((file) =>
      fs.readFileSync(file, 'utf8')
    )
    fs.mkdirSync(path.dirname(file), { recursive: true })
    fs.writeFileSync(file, '---\n' + YAML.stringify(data) + '---\n\n## 开始\n\n在这里写正文。\n', {
      flag: 'wx'
    })
    try {
      if (registration || (course && !state.config.courses[course])) {
        state.config.courses[course] = directory
        if (registration) {
          state.policy[course] = tags
          atomicJson(state.policyFile, state.policy)
        }
        atomicJson(state.configFile, state.config)
      }
    } catch (error) {
      fs.unlinkSync(file)
      fs.writeFileSync(state.policyFile, originals[0])
      fs.writeFileSync(state.configFile, originals[1])
      throw error
    }
    return { file, id, data, type, registeredCourse: registration, route: '/blog/' + id }
  } finally {
    fs.closeSync(lockFd)
    fs.unlinkSync(lock)
  }
}
