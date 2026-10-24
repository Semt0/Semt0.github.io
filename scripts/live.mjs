import path from 'node:path'
import fs from 'node:fs'
import { parseArgs } from 'node:util'
import { ensurePreview, openBrowser, stopPreview, waitForArticle } from './lib/preview.mjs'

const root = path.resolve(import.meta.dirname, '..')
try {
  const { values, positionals } = parseArgs({
    allowPositionals: true,
    options: {
      port: { type: 'string' },
      'no-open': { type: 'boolean' },
      stop: { type: 'boolean' },
      help: { type: 'boolean' }
    }
  })
  if (values.help) {
    console.log('pnpm live [ode/06] [--port 4322] [--no-open]\npnpm live --stop [--port 4322]')
  } else if (values.stop) {
    console.log(
      stopPreview(root, values.port) ? '写作预览已停止。' : '写作预览已退出，已移除旧记录。'
    )
  } else {
    const slug = positionals[0]
    if (
      positionals.length > 1 ||
      (slug &&
        (!/^[a-z0-9]+(?:[/-][a-z0-9]+)*$/.test(slug) ||
          !['.md', '.mdx'].some((ext) =>
            fs.existsSync(path.join(root, 'src/content/blog', slug + ext))
          )))
    ) {
      throw new Error('请指定已有文章的路径，例如 pnpm live ode/05。')
    }
    console.log('正在连接本地开发预览……')
    const { base } = await ensurePreview(root, values.port)
    const url = base + (slug ? '/blog/' + slug : '/')
    if (slug) await waitForArticle(url)
    console.log('实时预览：' + url + '\n保存 Markdown 后自动刷新；草稿仅在开发预览中显示。')
    if (!values['no-open']) {
      const warning = openBrowser(url)
      if (warning) console.warn(warning)
    }
  }
} catch (error) {
  console.error('未完成：' + error.message)
  process.exitCode = 1
}
