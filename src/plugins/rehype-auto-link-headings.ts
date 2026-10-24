import type { Element, ElementContent, Root } from 'hast'
import { visit } from 'unist-util-visit'
import type { VFile } from 'vfile'

const headingRank = (tag: string) => /^h[1-6]$/.test(tag)

// Add # link to headings
export default function rehypeAutolinkHeadings({
  properties = { ariaHidden: 'true', tabIndex: -1 },
  behavior = 'prepend',
  content = { type: 'text', value: '#' } as ElementContent
} = {}) {
  return (tree: Root, file: VFile) => {
    const labels: Record<string, string> = {}
    const headingText = (node: ElementContent | Element): string => {
      if (node.type === 'text') return node.value
      if (node.type !== 'element') return ''
      const classes = node.properties?.className
      if (Array.isArray(classes) && classes.includes('anchor')) return ''
      if (Array.isArray(classes) && classes.includes('katex')) {
        let tex = ''
        visit(node, 'element', (child: Element) => {
          if (child.tagName === 'annotation') tex = child.children.map(headingText).join('')
        })
        return tex
      }
      return node.children.map(headingText).join('')
    }
    visit(tree, 'element', (node: Element) => {
      if (headingRank(node.tagName) && node.properties?.id) {
        labels[node.properties.id.toString()] = headingText(node)
        const link: Element = {
          type: 'element',
          tagName: 'a',
          properties: { ...properties, href: `#${node.properties.id.toString()}` },
          // children: Array.isArray(content) ? content : [content]
          children: Array.isArray(content)
            ? content
            : typeof content === 'object' && content.type
              ? [content]
              : []
        }

        if (!['wrap', 'prepend', 'append'].includes(behavior)) {
          throw new Error(`Invalid behavior: ${behavior}`)
        }

        node.children = node.children || []
        if (behavior === 'wrap') {
          node.children = [link]
        } else if (behavior === 'prepend') {
          node.children.unshift(link)
        } else if (behavior === 'append') {
          node.children.push(link)
        }
      }
    })
    const data = file.data as { astro?: { frontmatter?: Record<string, unknown> } }
    data.astro ??= {}
    data.astro.frontmatter ??= {}
    data.astro.frontmatter.studyHeadings = labels
  }
}
