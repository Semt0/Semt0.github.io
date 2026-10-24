import type { CollectionEntry } from 'astro:content'
import { getBlogCollection } from 'astro-pure/server'

export type ContentEntry = CollectionEntry<'blog'>
export const tagHref = (tag: string) => `/tags/${encodeURIComponent(tag)}`
export async function getContentEntries(): Promise<ContentEntry[]> {
  return getBlogCollection()
}

/** Newest posts first; use chapter order to resolve dates shared by one course. */
export function sortContentEntries(entries: ContentEntry[]): ContentEntry[] {
  return [...entries].sort((a, b) => {
    const byDate = b.data.publishDate.valueOf() - a.data.publishDate.valueOf()
    if (byDate) return byDate
    if (a.data.order !== undefined && b.data.order !== undefined && a.id.split('/')[0] === b.id.split('/')[0]) {
      return b.data.order - a.data.order
    }
    return a.id.localeCompare(b.id, 'en')
  })
}
