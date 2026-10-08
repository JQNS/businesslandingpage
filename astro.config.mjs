import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';
import { SITE } from './src/config.ts';

// slug -> last modified date, read from post frontmatter, so the sitemap tells Google when a guide changed.
const dir = './src/content/blog';
const lastmod = Object.fromEntries(
  fs.readdirSync(dir).filter((f) => /\.mdx?$/.test(f)).map((f) => {
    const src = fs.readFileSync(`${dir}/${f}`, 'utf8');
    const date = src.match(/^updatedDate:\s*(.+)$/m)?.[1] ?? src.match(/^pubDate:\s*(.+)$/m)?.[1];
    return [f.replace(/\.mdx?$/, ''), date && new Date(date).toISOString()];
  }),
);

export default defineConfig({
  site: SITE.url,
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [
    mdx(),
    sitemap({
      filter: (page) => !page.includes('/404'),
      serialize(item) {
        const slug = item.url.match(/\/blog\/([^/]+)\/$/)?.[1];
        if (slug && lastmod[slug]) item.lastmod = lastmod[slug];
        return item;
      },
    }),
  ],
});
