import type { APIContext } from 'astro'
import rss from '@astrojs/rss'
import config from 'virtual:config'
import { getContentEntries, sortContentEntries } from '@/utils/content'

// Keep the feed small even when the archive contains entire courses of mathematical notes.
export async function GET(context: APIContext) {
  const posts = sortContentEntries(await getContentEntries())
  return rss({
    trailingSlash: false,
    xmlns: { atom: 'http://www.w3.org/2005/Atom' },
    stylesheet: '/scripts/pretty-feed-v3.xsl',
    title: config.title,
    description: config.description,
    site: context.site ?? import.meta.env.SITE,
    items: posts.map(({ id, data }) => ({
      title: data.title,
      description: data.description,
      pubDate: data.publishDate,
      link: `/blog/${id}`,
      categories: data.tags,
      customData: data.updatedDate
        ? `<atom:updated>${data.updatedDate.toISOString()}</atom:updated>`
        : ''
    }))
  })
}
