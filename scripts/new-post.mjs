import path from 'node:path'
import { parseArgs } from 'node:util'
import { createInterface } from 'node:readline/promises'
import { createPost, inferType, normalizeTags, readWriting, resolveCourse } from './lib/writing.mjs'
import { ensurePreview, openBrowser, openTypora, waitForArticle } from './lib/preview.mjs'

const root = path.resolve(import.meta.dirname, '..')
const help = `用法：pnpm write [slug] [参数]（不带参数时进入交互选择）
  --type blog|note|journal     博客 / 课程笔记 / 手记
  --title "标题"              文章标题，支持中文
  --slug my-post              英文文件名，也可作为位置参数
  --course ode                已有课程的名称、标签或目录；新课程可直接写中文名
  --tags "数学,ode"            逗号分隔的标签，支持新标签；也可重复 --tag
  --subject 数学               新课程所属学科，与 --course 配合自动生成两个标签
  --folder measure-theory     新中文课程的英文目录
  --description "简介"        文章简介
  --date YYYY-MM-DD           写作日期，默认为北京时间今天
  --list                      列出类型、课程和已有标签
  --no-open                   只创建和准备预览，不打开任何应用
  --no-preview                不启动预览、不打开浏览器
  --no-typora                 不打开 Typora
  --port 4322                 本地预览端口
示例：
  pnpm write ode/06 --title "第六章：课程笔记"
  pnpm write hello --type blog --title "新文章" --tags "技术,随笔"
  pnpm write 01 --type note --course 测度论 --subject 数学 --folder measure-theory --title "第一章"`

async function wizard(options, state) {
  const rl = createInterface({ input: process.stdin, output: process.stdout })
  const ask = async (question, fallback = '') =>
    (await rl.question(question + (fallback ? ` [${fallback}]` : '') + '：')).trim() || fallback
  try {
    const types = Object.keys(state.config.types)
    if (!options.type) {
      console.log(
        types.map((key, i) => `${i + 1}. ${state.config.types[key].label} (${key})`).join('\n')
      )
      const chosen = await ask('选择类型编号或名称', options.course ? 'note' : 'blog')
      options.type =
        types[Number(chosen) - 1] ||
        types.find((key) => state.config.types[key].label === chosen) ||
        chosen
    }
    if (!state.config.types[options.type]) throw new Error('未知类型，请使用列出的类型名称。')
    if (options.type === 'note') {
      const courses = Object.keys(state.policy)
      if (!options.course) {
        console.log(
          courses
            .map(
              (course, i) => `${i + 1}. ${course} (${state.config.courses[course] || '待设置目录'})`
            )
            .join('\n')
        )
        const chosen = await ask('选择课程编号、名称，或直接输入新课程名')
        options.course = courses[Number(chosen) - 1] || chosen
      }
      const known = resolveCourse(state, options.course)
      if (!known) {
        if (!options.course) throw new Error('课程名不能为空。')
        if (!options.tags?.length && !options.tag?.length && !options.subject)
          options.subject = await ask('学科标签，可输入新标签', '数学')
        if (!options.folder)
          options.folder = await ask(
            '新课程英文目录',
            /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(options.course) ? options.course : ''
          )
      } else console.log('课程标签：' + state.policy[known].join('、'))
    }
    if (!options.title) options.title = await ask('文章标题')
    if (!options.slug) {
      const course = resolveCourse(state, options.course)
      const folder = state.config.courses[course]
      const order = folder
        ? Math.max(
            0,
            ...state.posts
              .filter((post) => post.name.startsWith(folder + '/'))
              .map((post) => Number(post.meta.order) || 0)
          ) + 1
        : 1
      const suggestion = options.type === 'note' ? String(order).padStart(2, '0') : ''
      options.slug = await ask('英文文件名（无需 .md）', suggestion)
    }
    if (options.type !== 'note' && !options.tags?.length && !options.tag?.length) {
      console.log('已有标签：' + state.tags.join('、'))
      options.tags = [
        await ask('标签（逗号分隔，可输入新标签）', state.config.types[options.type].tags.join(','))
      ]
    }
    return options
  } finally {
    rl.close()
  }
}

try {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      type: { type: 'string' },
      title: { type: 'string' },
      slug: { type: 'string' },
      course: { type: 'string' },
      tags: { type: 'string', multiple: true },
      tag: { type: 'string', multiple: true },
      subject: { type: 'string' },
      folder: { type: 'string' },
      description: { type: 'string' },
      date: { type: 'string' },
      port: { type: 'string' },
      list: { type: 'boolean' },
      help: { type: 'boolean' },
      'no-open': { type: 'boolean' },
      'no-preview': { type: 'boolean' },
      'no-typora': { type: 'boolean' }
    }
  })
  if (values.help) console.log(help)
  else {
    const state = readWriting(root)
    if (values.list) {
      console.log(
        '类型：' +
          Object.entries(state.config.types)
            .map(([key, item]) => `${key}（${item.label}）`)
            .join('、')
      )
      console.log(
        '\n课程：\n' +
          Object.entries(state.policy)
            .map(
              ([course, tags]) =>
                `${course} → ${state.config.courses[course] || '使用 --folder 设置'} / ${tags.join('、')}`
            )
            .join('\n')
      )
      console.log('\n标签（可直接输入新标签）：' + state.tags.join('、'))
    } else {
      if (positionals.length > 1 || (values.slug && positionals.length))
        throw new Error('只需一个文件名，位置参数和 --slug 选择其一。')
      let options = { ...values, slug: values.slug || positionals[0] }
      if (!options.type && options.slug)
        options.type = options.course ? 'note' : inferType(state, options.slug)
      if (options.type === 'note' && !options.course && options.slug)
        options.course = resolveCourse(state, options.slug.split('/')[0])
      if (!options.title || !options.slug || (options.type === 'note' && !options.course)) {
        if (!process.stdin.isTTY)
          throw new Error(
            '请提供 --title、文件名，以及课程参数；交互选择请直接在终端运行 pnpm write。'
          )
        options = await wizard(options, state)
      }
      options.tags = normalizeTags(options.tags)
      const post = createPost(root, options)
      console.log(
        `已创建：${post.file}\n类型：${state.config.types[post.type].label}；标签：${post.data.tags.join('、')}`
      )
      if (post.registeredCourse)
        console.log('已登记新课程及目录，后续可直接使用 --course ' + post.data.course)
      if (!values['no-open'] && !values['no-typora']) {
        const warning = openTypora(post.file)
        if (warning) console.warn(warning)
      }
      if (!values['no-preview']) {
        console.log('正在连接本地开发预览……')
        try {
          const { base } = await ensurePreview(root, values.port)
          const url = base + post.route
          await waitForArticle(url)
          console.log('实时预览：' + url + '\n在 Typora 保存后，浏览器会自动刷新。')
          if (!values['no-open']) {
            const warning = openBrowser(url)
            if (warning) console.warn(warning)
          }
        } catch (error) {
          console.warn('文件已保留；' + error.message)
          process.exitCode = 1
        }
      }
      console.log('当前为草稿。准备发布时，将 draft 改为 false，再提交并推送。')
    }
  }
} catch (error) {
  console.error('未完成：' + error.message)
  process.exitCode = 1
}
