import type { Root, RootContent } from 'mdast'

type StudyNode = {
  type: string
  name?: string
  attributes?: Record<string, string>
  data?: Record<string, unknown>
  children?: StudyNode[]
}

/** Preserve imported MkDocs callouts and proof disclosure states using semantic HTML. */
export default function remarkStudyBlocks() {
  return (tree: Root) => {
    function walk(node: StudyNode) {
      if (node.type === 'containerDirective' && ['study-note', 'study-proof', 'study-tab'].includes(node.name || '')) {
        const collapsible = node.name === 'study-proof'
        const tab = node.name === 'study-tab'
        const kind = (node.attributes?.kind || 'note').replace(/[^a-z-]/g, '')
        node.data = {
          ...node.data,
          hName: collapsible ? 'details' : tab ? 'section' : 'aside',
          hProperties: {
            className: [tab ? 'study-tab' : 'study-block', `study-${kind}`],
            ...(collapsible && node.attributes?.open === 'true' ? { open: true } : {})
          }
        }
        const label = node.children?.[0]
        if (label?.data?.directiveLabel) {
          label.data = { ...label.data, hName: collapsible ? 'summary' : 'div',
            hProperties: { className: ['study-title'] } }
        }
      }
      node.children?.forEach(walk)
    }
    tree.children.forEach((node: RootContent) => walk(node as StudyNode))
  }
}
