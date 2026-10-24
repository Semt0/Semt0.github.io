import fs from 'node:fs/promises'
import path from 'node:path'
import crypto from 'node:crypto'
import sharp from 'sharp'

const root = path.resolve(import.meta.dirname, '../..')
const report = JSON.parse(await fs.readFile(path.join(root, 'migration/report.json'), 'utf8'))
const manifestPath = path.join(root, 'migration/optimized-assets.json')
let manifest = {}
try { manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8')) } catch {}
const queue = Object.keys(report.assets).filter(name => name.endsWith('.png'))
const digest = data => crypto.createHash('sha256').update(data).digest('hex')
let completed = 0
sharp.concurrency(1)
async function worker() {
  while (queue.length) {
    const name = queue.shift()
    const original = path.join(root, 'public/media', name)
    const cache = path.join(root, 'migration/asset-cache', name)
    let input
    try { input = await fs.readFile(cache) } catch { input = await fs.readFile(original) }
    if (digest(input) !== report.assets[name]) throw new Error('Source asset changed: ' + name)
    const output = name.replace(/\.png$/, '.webp')
    const destination = path.join(root, 'public/media', output)
    let buffer
    try {
      buffer = await fs.readFile(destination)
      if (digest(buffer) !== manifest[name]?.sha256) buffer = undefined
    } catch {}
    if (!buffer) buffer = await sharp(input).webp({ lossless: true, effort: 3 }).toBuffer()
    await fs.mkdir(path.dirname(destination), { recursive: true })
    await fs.writeFile(destination, buffer)
    const meta = await sharp(input).metadata()
    manifest[name] = { output, sha256: digest(buffer), sourceBytes: input.length, bytes: buffer.length,
      width: meta.width, height: meta.height, lossless: true, resized: false }
    await fs.mkdir(path.dirname(cache), { recursive: true })
    await fs.writeFile(cache, input)
    await fs.rm(original, { force: true })
    if (++completed % 100 === 0) console.log(`Lossless images: ${completed}`)
  }
}
await Promise.all(Array.from({ length: 4 }, worker))
manifest = Object.fromEntries(Object.entries(manifest).sort(([a], [b]) => a.localeCompare(b)))
await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n')
const values = Object.values(manifest)
console.log(`${values.length} lossless images: ${(values.reduce((n, p) => n + p.sourceBytes, 0) / 1048576).toFixed(1)} → ${(values.reduce((n, p) => n + p.bytes, 0) / 1048576).toFixed(1)} MiB; original dimensions retained.`)
