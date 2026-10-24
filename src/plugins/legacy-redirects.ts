import type { AstroIntegration } from 'astro'
import { readFile, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

/** Static redirects preserve existing article bookmarks, query strings and heading fragments. */
export default function legacyRedirects(redirects: Record<string, string>): AstroIntegration {
  return {
    name: 'legacy-article-bookmarks',
    hooks: {
      'astro:build:done': async ({ dir }) => {
        let headings: Record<string, Record<string, string>> = {}
        try {
          headings = JSON.parse(await readFile(path.resolve('migration/legacy-heading-map.json'), 'utf8')).routes
        } catch { /* The first migration build supplies the heading map afterwards. */ }
        const scriptJSON = (value: object | string) => JSON.stringify(value).replace(/[<>&\u007f-\uffff]/g,
          (character) => '\\u' + character.charCodeAt(0).toString(16).padStart(4, '0'))
        for (const [old, target] of Object.entries(redirects)) {
          const file = path.join(fileURLToPath(dir), old.slice(1), 'index.html')
          const html = await readFile(file, 'utf8')
          const script = `<script data-legacy-bookmark>const headings=${scriptJSON(headings[old] || {})};let fragment=location.hash;try{const mapped=headings[decodeURIComponent(fragment.slice(1))];if(mapped)fragment='#'+encodeURIComponent(mapped)}catch{}location.replace(${scriptJSON(target)}+location.search+fragment)</script>`
          await writeFile(file, html.replace(/<script data-legacy-bookmark>[\s\S]*?<\/script>/, '').replace('<meta charset="utf-8">', '').replace('<!doctype html>', '<!doctype html><meta charset="utf-8">' + script))
        }
      }
    }
  }
}
