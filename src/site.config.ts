import type { Config, IntegrationUserConfig, ThemeUserConfig } from 'astro-pure/types'

export const theme: ThemeUserConfig = {
  title: "Semt0's Blog",
  author: 'Semt0',
  description: 'Notes on math, embodied AI, and the everyday.',
  favicon: '/avatar.svg',
  socialCard: '/avatar.svg',
  locale: { lang: 'en', attrs: 'en_US', dateLocale: 'en-US', dateOptions: { year: 'numeric', month: 'short', day: 'numeric' } },
  logo: { src: '/src/assets/avatar.svg', alt: 'Semt0' },
  titleDelimiter: '•',
  prerender: true,
  npmCDN: 'https://cdn.jsdelivr.net/npm',
  head: [], customCss: [],
  header: { menu: [
    { title: 'Blog', link: '/blog' },
    { title: 'Projects', link: '/projects' },
    { title: 'Archives', link: '/archives' },
    { title: 'Links', link: '/links' },
    { title: 'About', link: '/about' }
  ] },
  footer: {
    year: `© ${new Date().getFullYear()} `,
    links: [], credits: true,
    social: [
      { icon: 'github', label: 'GitHub', href: 'https://github.com/Semt0' },
      { icon: 'rss', label: 'RSS', href: '/rss.xml' }
    ]
  },
  content: { externalLinks: { content: ' ↗', properties: { style: 'user-select:none' } }, blogPageSize: 8, share: [] }
}

export const integ: IntegrationUserConfig = {
  links: { logbook: [], applyTip: [], cacheAvatar: false },
  pagefind: true,
  quote: { server: '', target: '' },
  typography: { class: 'prose text-base', blockquoteStyle: 'italic', inlineCodeBlockStyle: 'modern' },
  mediumZoom: { enable: true, selector: '.prose img', options: { className: 'zoomable' } },
  waline: {
    enable: true,
    server: 'https://my-waline-eta-beige.vercel.app',
    showMeta: false,
    additionalConfigs: { lang: 'en', dark: '.dark', reaction: false }
  }
}

const config = { ...theme, integ } as Config
export default config
