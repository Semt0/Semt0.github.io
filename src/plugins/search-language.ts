import { fileURLToPath } from 'node:url'
import { rm } from 'node:fs/promises'
import { join } from 'node:path'
import type { AstroIntegration } from 'astro'
import * as pagefind from 'pagefind'

/** Keep Chinese word segmentation for the existing corpus while the UI is English. */
export default function searchLanguage(): AstroIntegration {
  return {
    name: 'content-search-language',
    hooks: {
      'astro:build:done': async ({ dir }) => {
        const target = fileURLToPath(dir)
        const { index } = await pagefind.createIndex({ forceLanguage: 'zh' })
        if (!index) throw new Error('Could not create the content search index')
        try {
          await index.addDirectory({ path: target })
          await rm(join(target, 'pagefind'), { recursive: true, force: true })
          await index.writeFiles({ outputPath: join(target, 'pagefind') })
        } finally {
          await pagefind.close()
        }
      }
    }
  }
}
