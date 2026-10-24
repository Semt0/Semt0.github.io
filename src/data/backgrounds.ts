import home from '@/assets/images/home-blue.png'
import blog from '@/assets/backgrounds/blog.png'
import projects from '@/assets/backgrounds/projects.png'
import archives from '@/assets/backgrounds/archives.png'
import about from '@/assets/backgrounds/about.png'
import links from '@/assets/backgrounds/links.png'

export const backgrounds = {
  home: { image: home, height: '34rem', opacity: .3, darkOpacity: .12 },
  blog: { image: blog, height: '26rem', opacity: .22, darkOpacity: .1 },
  projects: { image: projects, height: '26rem', opacity: .23, darkOpacity: .1 },
  archives: { image: archives, height: '26rem', opacity: .24, darkOpacity: .1 },
  about: { image: about, height: '28rem', opacity: .26, darkOpacity: .12 },
  links: { image: links, height: '28rem', opacity: .25, darkOpacity: .1 }
}

export function backgroundSection(pathname: string): keyof typeof backgrounds | undefined {
  const section = pathname.split('/').filter(Boolean)[0]
  if (!section) return 'home'
  if (section === 'blog' || section === 'tags' || section === 'search') return 'blog'
  if (section === 'projects' || section === 'archives' || section === 'about' || section === 'links') return section
  return undefined
}
