# Trust-Wise — travel guide blog (Astro)

## Run locally
    npm install
    npm run dev      # http://localhost:4321

## Add a new guide
Create `src/content/blog/<url-slug>.mdx` (copy the Tomorrowland post as a template).
Affiliate blocks you can use inside posts:
- `<HotelCard name area price rating pros={[...]} href="AGODA/BOOKING LINK" />`
- `<ShopeeItem name why price href="SHOPEE AFFILIATE LINK" />`
- `<AffButton href label variant="primary|outline" />`
- `<Callout type="tip|warn|info" title="...">text</Callout>`

Search the post for `#AFFILIATE-LINK` / `#SHOPEE-LINK` to find placeholders to replace.

## Deploy to Hostinger
1. Set your real domain in `src/config.ts` and `public/robots.txt`.
2. `npm run build`
3. Upload the **contents** of `dist/` into `public_html/` (hPanel → File Manager, or FTP).

## SEO / Google indexing (after first deploy)
1. Google Search Console → Add property (Domain) → verify via DNS TXT record in Hostinger hPanel → DNS Zone
   (or use "HTML tag" and paste the code into `googleVerification` in `src/config.ts`).
2. Search Console → Sitemaps → submit `sitemap-index.xml`.
3. Search Console → URL Inspection → paste each new guide URL → "Request indexing".
4. Optional: Bing Webmaster Tools → import from Google Search Console.
5. New guide? Add `faq:` in frontmatter for Q&A snippets, set `updatedDate` when you edit, and link to it from related guides.
