# Trust-Wise (trust-wise.org)

Astro blog for Malaysians: trips and lifestyle near us (Thailand, Malaysia, Singapore, fitness).
Earns through affiliate links: Klook, Agoda, Trip.com, Shopee, ClassPass.

## Goal

**Get the first affiliate sales by 31 December 2026.** Every change should help bring in
traffic (search, social) or turn visitors into affiliate clicks and bookings.

## How the owner wants me to work

- **Full autonomy.** Make any change I think is needed without asking first: edit or
  improve existing articles, write new articles, change the homepage, layout, internal
  links, SEO, social post drafts, anything that helps the goal.
- **Commit, push and deploy without asking.** Commit on the `trustwise-blog` branch,
  `git push origin trustwise-blog`, then build and deploy to trust-wise.org.
- **Weekly report.** Tell the owner once a week what I did: posts added or changed,
  deploys, traffic or affiliate results if known, and what I plan next.
- **Ask only when I need something from the owner**, for example: a new affiliate link or
  approval, Shopee links for products, GA4 or affiliate dashboard numbers, photos, or
  account access.

## Stay within the law (the one hard rule)

- Every page with affiliate links shows the affiliate disclosure (`Disclosure` component;
  full page at /disclosure/). Never hide or remove it.
- Honest content only: no fake reviews, testimonials, ratings, prices, or claims that I
  stayed somewhere or tried something. Mark prices and dates as approximate and check
  them; say when something may have changed.
- Follow each affiliate program's terms (no brand-name bidding, no misleading coupon
  claims, no cookie stuffing, no spam). Don't promote brands we are not partners with as
  if we were (e.g. no Fitness First mentions).
- Images: only our own, Unsplash, or CC0/public-domain. No copied text or photos.
- Don't impersonate any official body, event, or brand. No health, legal, or visa advice
  stated as fact without pointing to the official source.
- Respect Malaysian PDPA: keep the privacy page accurate when adding tracking or forms.

## Workflow

- `npm run build` must pass before deploying. Post descriptions are max 170 chars.
- Deploy: build, then deploy `dist/` to trust-wise.org with the Hostinger hosting deploy tool.
- Plain klook.com URLs in posts become affiliate links at build
  (`src/lib/rehype-affiliate.mjs`, `src/lib/affiliate.ts`). Shopee links live in
  `src/data/shopee.ts` (`<ShopeeItem product="..." />`). Hotels use `HotelBox`
  (Agoda main, Trip.com compare).
- Homepage blocks are edited in `src/data/home.ts`. Social post drafts are in
  `social/threads-x-posts.md`.
