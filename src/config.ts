// Change these once, used site-wide (SEO, footer, RSS).
export const SITE = {
  name: 'Trust-Wise',
  url: 'https://trust-wise.org',
  description: 'Honest travel guides for Malaysians: where to stay, how to get there, and what to pack.',
  author: 'Trust-Wise Team',
  locale: 'en_MY',
  // Paste the content="..." value from Google Search Console / Bing Webmaster "HTML tag" verification.
  googleVerification: '',
  bingVerification: '',
  gtmId: 'GTM-5MKMXL2F', // Google Tag Manager container; set '' to disable
  // ClassPass referral link (owner's personal refer-a-friend link, chosen knowingly).
  // Note: ClassPass's referral terms restrict SEO/public advertising use; an Impact affiliate link is the approved route.
  classpassUrl: 'https://classpass.com/refer/IL79JGRQ26?placement=Profile',
  classpassAffiliate: true, // adds rel="sponsored" and GA4 affiliate_click tracking
  // Trip.com hotel affiliate links (city hotel search), used by TripHotelBox.
  tripHotels: {
    'Kuala Lumpur': 'https://www.trip.com/t/OXn6G1BgiW2',
    Bangkok: 'https://www.trip.com/t/OSVUciDgiW2',
    Pattaya: 'https://www.trip.com/t/efGrIYJgiW2',
    'Chiang Mai': 'https://www.trip.com/t/PmJMjZKgiW2',
    Phuket: 'https://www.trip.com/t/Q6gGG9MgiW2',
    Hatyai: 'https://www.trip.com/t/nT2aMFNgiW2',
  } as Record<string, string>,
  ga4Id: 'G-CN9J308Y75', // GA4 via gtag.js; don't also add a GA4 tag in GTM or pageviews count twice

};
