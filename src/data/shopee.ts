// Shopee affiliate product library. Generate each link once in the Shopee Affiliate portal, add it here,
// then reuse it anywhere with <ShopeeItem product="power-bank" /> (you can still override name/why/price).
// Shopee links can't be built in code, so a shared library is how you avoid making them one by one.

export interface ShopeeProduct {
  name: string;
  href: string;
  icon?: string;
  price?: string;
  why?: string;
}

const s = (code: string) => `https://s.shopee.com.my/${code}`;

export const SHOPEE: Record<string, ShopeeProduct> = {
  // Travel essentials
  'power-bank': { name: 'Travel-safe 10,000mAh power bank', href: s('70KkH17nvy'), icon: '🔋', price: 'RM 40–90', why: 'Under 100Wh, so it is allowed in your cabin bag. Keeps your phone alive for maps, Grab and e-tickets.' },
  'anti-theft-bag': { name: 'Anti-theft crossbody bag', href: s('8AWhgFJoYd'), icon: '👜', price: 'RM 25–50', why: 'Zips that sit against your body. Good for crowded markets, festivals and BTS rush hour.' },
  'luggage-scale': { name: 'Digital luggage scale', href: s('5fpMrLghnt'), icon: '⚖️', why: 'Weigh your bag before the airport so you are not paying overweight fees at the counter.' },
  'neck-fan': { name: 'Portable neck fan', href: s('6L53eegY0E'), icon: '🌀', why: 'Thai afternoons are hot. Small, light and rechargeable.' },
  sunscreen: { name: 'SPF 50 sunscreen', href: s('3VksHZRced'), icon: '🧴', why: 'For temples, beaches and long days outdoors.' },
  adapter: { name: 'Universal travel adapter', href: s('AKbCPhuzf7'), icon: '🔌', why: 'Thailand mostly uses two-pin plugs, so your Malaysian three-pin chargers need an adapter.' },
  'adapter-alt': { name: 'Universal travel adapter (alternative pick)', href: s('1qceI7QCUs'), icon: '🔌' },
  'passport-holder': { name: 'Passport holder and travel document organiser', href: s('AUucc5SDRU'), icon: '🛂', why: 'Keeps your passport, boarding pass and cards in one place at immigration.' },
  'packing-cubes': { name: 'Packing cubes set', href: s('5q8n3i5bKT'), icon: '🧳', why: 'Fit more in a cabin bag and leave space for shopping on the way home.' },
  umbrella: { name: 'Foldable windproof umbrella', href: s('5fpMrT7VVJ'), icon: '☂️', why: 'Afternoon storms are common in Thailand. Fits in a day bag.' },
  duffel: { name: 'Foldable travel duffel bag', href: s('6L53ejQ1SF'), icon: '👜', why: 'Folds flat on the way there, holds your shopping on the way back.' },
  jacket: { name: 'Light packable jacket', href: s('905opMkanD'), icon: '🧥', why: 'For cold buses, trains, malls and cool northern nights.' },
  torch: { name: 'Rechargeable mini torch', href: s('60SDFw2RvC'), icon: '🔦' },
  'thailand-esim-shopee': { name: 'Thailand travel eSIM', href: s('5At64dErix'), icon: '📶' },
  // Festivals and events
  'hydration-pack': { name: 'Foldable festival hydration pack', href: s('6AldImQN24'), icon: '💧', price: 'RM 30–60' },
  earplugs: { name: 'Reusable high-fidelity earplugs', href: s('7ptrHZxPRR'), icon: '🎧', price: 'RM 20–80', why: 'Protect your hearing at concerts and festivals without muffling the music.' },
  // Haze and health
  'n95-adult': { name: 'N95 / KN95 masks (adult box)', href: s('2LYunkkf4K'), icon: '😷' },
  'n95-kids': { name: "Kids' N95 / KN95 masks", href: s('W7GcQ4AZb'), icon: '🧒' },
  'air-purifier': { name: 'HEPA air purifier (bedroom size)', href: s('60SDAbp35A'), icon: '🌬️' },
  'hepa-filter': { name: 'Replacement HEPA filters', href: s('AUucWw7YO2'), icon: '🔄' },
  'eye-drops': { name: 'Lubricating eye drops', href: s('50Zfyrw8cj'), icon: '👁️' },
  'nasal-spray': { name: 'Saline nasal spray', href: s('5VVwZpKNIX'), icon: '👃' },
};
