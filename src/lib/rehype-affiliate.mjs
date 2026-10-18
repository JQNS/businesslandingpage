// Rehype plugin: rewrites plain shop links inside posts into affiliate links at build time,
// and marks them rel="sponsored". Covers markdown links ([text](https://www.klook.com/...))
// and `href` props on MDX components (<KlookCard href="https://www.klook.com/..." />).
import { toAffiliate } from './affiliate.ts';

const REL = 'sponsored nofollow noopener';

function walk(node) {
  if (node.type === 'element' && node.tagName === 'a' && typeof node.properties?.href === 'string') {
    const next = toAffiliate(node.properties.href);
    if (next) {
      node.properties.href = next;
      node.properties.rel = REL.split(' ');
      node.properties.target = '_blank';
    }
  }
  if ((node.type === 'mdxJsxFlowElement' || node.type === 'mdxJsxTextElement') && Array.isArray(node.attributes)) {
    for (const attr of node.attributes) {
      if (attr.type === 'mdxJsxAttribute' && attr.name === 'href' && typeof attr.value === 'string') {
        const next = toAffiliate(attr.value);
        if (next) attr.value = next;
      }
    }
  }
  if (node.children) node.children.forEach(walk);
}

export default function rehypeAffiliate() {
  return (tree) => walk(tree);
}
