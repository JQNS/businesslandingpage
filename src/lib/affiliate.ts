// Turns a normal shop URL into your affiliate link, so posts can use plain links
// (e.g. any klook.com page) and the tracking is added at build time.
// Used by the affiliate components and by the rehype plugin in astro.config.mjs.

export const AFFILIATE = {
  klookAid: '138324',
  // Trip.com deep links need both IDs from the Trip.com affiliate portal (Allianceid + SID).
  // Until tripSid is set, plain trip.com links are left as they are; city links in SITE.tripHotels still work.
  tripAllianceId: '10951620',
  tripSid: '',
  // Agoda Partners site ID ("cid"). Set it once approved and every agoda.com link is tracked.
  agodaCid: '',
};

const host = (url: URL) => url.hostname.replace(/^www\./, '');

/** Returns the affiliate version of `href`, or null when it isn't a shop we can deep-link. */
export function toAffiliate(href: string): string | null {
  let url: URL;
  try {
    url = new URL(href);
  } catch {
    return null; // relative / internal link
  }
  const h = host(url);

  if (h === 'klook.com' || h.endsWith('.klook.com')) {
    if (h === 'affiliate.klook.com') return href; // already an affiliate link
    return `https://affiliate.klook.com/redirect?aid=${AFFILIATE.klookAid}&k_site=${encodeURIComponent(href)}`;
  }

  if (h === 'trip.com' || h.endsWith('.trip.com')) {
    if (url.pathname.startsWith('/t/') || url.searchParams.has('Allianceid')) return href; // portal short link / already tagged
    if (!AFFILIATE.tripSid) return null;
    url.searchParams.set('Allianceid', AFFILIATE.tripAllianceId);
    url.searchParams.set('SID', AFFILIATE.tripSid);
    return url.toString();
  }

  if (h === 'agoda.com' || h.endsWith('.agoda.com')) {
    if (url.searchParams.has('cid')) return href;
    if (!AFFILIATE.agodaCid) return null;
    url.searchParams.set('cid', AFFILIATE.agodaCid);
    return url.toString();
  }

  // Shopee links can't be built in code: they must come from the Shopee Affiliate portal (see src/data/shopee.ts).
  if (h === 's.shopee.com.my') return href;

  return null;
}

/** Affiliate URL if available, otherwise the original link. */
export const aff = (href: string) => toAffiliate(href) ?? href;
