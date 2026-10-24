import fs from 'node:fs'
import path from 'node:path'
import { spawn, spawnSync } from 'node:child_process'
import net from 'node:net'

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))
const portNumber = (value) => {
  const port = Number(value || 4322)
  if (!Number.isInteger(port) || port < 1024 || port > 65535)
    throw new Error('--port 应为 1024 到 65535 之间的端口。')
  return port
}
async function listening(port) {
  return new Promise((resolve) => {
    const socket = net.connect({ host: '127.0.0.1', port })
    socket.setTimeout(1000)
    socket.once('connect', () => {
      socket.destroy()
      resolve(true)
    })
    socket.once('error', () => {
      socket.destroy()
      resolve(false)
    })
    socket.once('timeout', () => {
      socket.destroy()
      resolve(false)
    })
  })
}
export async function previewReady(base, fetcher = fetch) {
  try {
    const response = await fetcher(base + '/', { signal: AbortSignal.timeout(2500) })
    const html = await response.text()
    return response.ok && html.includes('/@vite/client') && html.includes('Semt0')
  } catch {
    return false
  }
}
export async function waitForArticle(url, fetcher = fetch, timeout = 15000) {
  const deadline = Date.now() + timeout
  do {
    try {
      const response = await fetcher(url, { signal: AbortSignal.timeout(2500) })
      if (response.ok) {
        await response.body?.cancel()
        return
      }
      await response.body?.cancel()
    } catch {}
    await delay(300)
  } while (Date.now() < deadline)
  throw new Error(
    '文章尚未完成编译。请检查预览日志；若刚修改过站点配置，可重启开发服务器后运行 pnpm live。'
  )
}
export function openTypora(file, runner = spawnSync) {
  if (process.platform !== 'darwin') return '自动打开 Typora 仅适用于 macOS，请手动打开 Markdown。'
  const result = runner('open', ['-a', 'Typora', file], { stdio: 'ignore' })
  return result.status === 0 ? null : '文件已创建；未能打开 Typora，请确认已安装该应用。'
}
export function openBrowser(url, runner = spawnSync) {
  if (process.platform !== 'darwin') return '请在浏览器打开：' + url
  const result = runner('open', [url], { stdio: 'ignore' })
  return result.status === 0 ? null : '未能自动打开浏览器，请手动打开：' + url
}
export async function ensurePreview(root, value) {
  const port = portNumber(value)
  const base = 'http://127.0.0.1:' + port
  let child, record
  const cache = path.join(root, '.astro')
  const log = path.join(cache, 'writing-preview.log')
  if (!(await listening(port))) {
    fs.mkdirSync(cache, { recursive: true })
    const astroPackage = path.join(root, 'node_modules/astro')
    if (!fs.existsSync(path.join(astroPackage, 'package.json')))
      throw new Error('缺少 Astro 依赖，请先运行 pnpm install。')
    const bin = JSON.parse(fs.readFileSync(path.join(astroPackage, 'package.json'), 'utf8')).bin
      .astro
    const cli = path.resolve(astroPackage, bin)
    const fd = fs.openSync(log, 'a')
    try {
      child = spawn(process.execPath, [cli, 'dev', '--host', '127.0.0.1', '--port', String(port)], {
        cwd: root,
        detached: true,
        stdio: ['ignore', fd, fd]
      })
      await new Promise((resolve, reject) => {
        child.once('spawn', resolve)
        child.once('error', reject)
      })
      child.unref()
    } finally {
      fs.closeSync(fd)
    }
    record = path.join(cache, 'writing-preview-' + port + '.json')
    fs.writeFileSync(record, JSON.stringify({ pid: child.pid, cli, root, port }) + '\n')
  }
  const deadline = Date.now() + 45000
  while (Date.now() < deadline) {
    if (await previewReady(base)) return { base, started: !!child, log }
    if (child?.exitCode !== null && child?.exitCode !== undefined) break
    await delay(500)
  }
  if (child) {
    try {
      process.kill(child.pid, 'SIGTERM')
    } catch {}
    if (record && fs.existsSync(record)) fs.unlinkSync(record)
    throw new Error('开发预览未能启动，日志：' + log)
  }
  throw new Error(`端口 ${port} 没有响应为本站开发预览。请检查原服务，或加 --port 4323。`)
}
export function stopPreview(root, value) {
  const port = portNumber(value)
  const record = path.join(root, '.astro', 'writing-preview-' + port + '.json')
  if (!fs.existsSync(record))
    throw new Error('此服务并非写作脚本启动。请在运行 pnpm dev / quick_start 的终端按 Ctrl+C。')
  const info = JSON.parse(fs.readFileSync(record, 'utf8'))
  const pkg = path.join(root, 'node_modules/astro')
  const expectedCli = path.resolve(
    pkg,
    JSON.parse(fs.readFileSync(path.join(pkg, 'package.json'), 'utf8')).bin.astro
  )
  if (
    info.root !== root ||
    info.cli !== expectedCli ||
    !Number.isInteger(info.pid) ||
    info.pid <= 1 ||
    info.port !== port
  )
    throw new Error('预览进程记录无效，不会停止其他服务。')
  const result = spawnSync('ps', ['-p', String(info.pid), '-o', 'command='], { encoding: 'utf8' })
  if (result.status !== 0 || !result.stdout.trim()) {
    fs.unlinkSync(record)
    return false
  }
  if (
    !result.stdout.includes(info.cli) ||
    !result.stdout.includes('--host 127.0.0.1') ||
    !result.stdout.includes('--port ' + port)
  ) {
    throw new Error('预览进程身份不匹配，不会停止其他服务。')
  }
  process.kill(info.pid, 'SIGTERM')
  fs.unlinkSync(record)
  return true
}
