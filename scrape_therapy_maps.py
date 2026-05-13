#!/usr/bin/env python3
"""
Scrape Google Maps for therapy / psychological services listings in a given city.

Outputs therapy_data.csv with: practice name, website, services/about text, rating,
top 10 review texts, address, phone.

Note: Google Maps markup changes often; you may need to adjust selectors. Automated
scraping may violate Google's Terms of Service — use for personal research only
and respect rate limits.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Iterable
from urllib.parse import quote_plus

from playwright.sync_api import Browser, Page, Playwright, sync_playwright

DEFAULT_QUERY = "psychological services therapists"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


@dataclass
class PlaceRow:
    practice_name: str = ""
    website_url: str = ""
    services_text: str = ""
    rating: str = ""
    reviews: list[str] = field(default_factory=list)
    address: str = ""
    phone: str = ""

    def reviews_blob(self) -> str:
        """Single CSV-safe column: reviews separated by a delimiter."""
        return " ||| ".join(r.replace("\n", " ").strip() for r in self.reviews if r.strip())


def _dismiss_consent(page: Page, timeout_ms: int = 8000) -> None:
    for label in (
        "Accept all",
        "I agree",
        "Tout accepter",
        "Alle akzeptieren",
    ):
        try:
            btn = page.get_by_role("button", name=re.compile(re.escape(label), re.I))
            if btn.first.is_visible(timeout=500):
                btn.first.click(timeout=timeout_ms)
                time.sleep(1)
                return
        except Exception:
            continue


def _scroll_results_feed(page: Page, max_scrolls: int, pause_s: float) -> None:
    feed = page.locator('div[role="feed"]')
    try:
        feed.wait_for(state="visible", timeout=20000)
    except Exception:
        return
    last_height = 0
    for _ in range(max_scrolls):
        feed.evaluate("el => el.scrollTop = el.scrollHeight")
        time.sleep(pause_s)
        h = feed.evaluate("el => el.scrollHeight")
        if h == last_height:
            break
        last_height = h


def _collect_place_hrefs(page: Page, limit: int) -> list[str]:
    links = page.locator('a[href*="/maps/place/"]')
    seen: set[str] = set()
    hrefs: list[str] = []
    count = links.count()
    for i in range(min(count, 500)):
        if len(hrefs) >= limit:
            break
        try:
            href = links.nth(i).get_attribute("href") or ""
        except Exception:
            continue
        if not href or "/maps/place/" not in href:
            continue
        base = href.split("?")[0].split("#")[0]
        if base in seen:
            continue
        seen.add(base)
        hrefs.append(href)
    return hrefs


def _text_or_empty(locator) -> str:
    try:
        t = locator.inner_text(timeout=3000)
        return " ".join(t.split())
    except Exception:
        return ""


def _click_tab_if_present(page: Page, name_pattern: str) -> None:
    try:
        tab = page.get_by_role("tab", name=re.compile(name_pattern, re.I))
        if tab.first.is_visible(timeout=1500):
            tab.first.click()
            time.sleep(0.8)
    except Exception:
        pass
    try:
        btn = page.get_by_role("button", name=re.compile(name_pattern, re.I))
        if btn.first.is_visible(timeout=800):
            btn.first.click()
            time.sleep(0.8)
    except Exception:
        pass


def _main_panel_text(page: Page) -> str:
    main = page.locator('div[role="main"]').first
    if main.count() == 0:
        return ""
    return _text_or_empty(main)


def _extract_services_line(page: Page) -> str:
    """
    Google Maps often shows a single line: 'Services: A, B, C' on the Overview tab.
    """
    text = _main_panel_text(page)
    if not text:
        return ""
    m = re.search(r"Services:\s*([^\n]+)", text, re.I)
    if m:
        return m.group(1).strip()
    return ""


_REVIEW_NOISE = re.compile(
    r"^(More Google reviews|Google review summary|View all|\(\d+\)\s*$|\d+\s*reviews?$|"
    r"Open ·|Closes|Website|Directions|Save|Share|Call)$",
    re.I,
)


def _phone_from_text(text: str) -> str:
    if not text:
        return ""
    patterns = (
        r"(\+?60[\s-]*1[0-9][\s-]*\d{3}[\s-]*\d{4})",
        r"(01[0-9][\s-]*\d{3}[\s-]*\d{4})",
        r"(\(\d{3}\)\s*\d{3}[-\s]?\d{4})",
        r"(\d{3}[-.\s]\d{3}[-.\s]\d{4})",
    )
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return re.sub(r"\s+", " ", m.group(1).strip())
    return ""


def scrape_place_page(page: Page, place_url: str, max_reviews: int = 10) -> PlaceRow:
    row = PlaceRow()
    page.goto(place_url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(1.5)
    _dismiss_consent(page)
    time.sleep(0.5)

    # Title / name
    for sel in ('h1[data-attrid="title"]', 'div[role="main"] h1', "h1.DUwDvf", "h1"):
        loc = page.locator(sel).first
        if loc.count() > 0:
            t = _text_or_empty(loc)
            if t and len(t) > 1:
                row.practice_name = t
                break

    # Rating (e.g. "4.5" near stars)
    aria = page.locator('span[aria-label*="star" i]').first
    if aria.count():
        label = aria.get_attribute("aria-label") or ""
        m = re.search(r"([\d.,]+)\s*star", label, re.I)
        if m:
            row.rating = m.group(1).replace(",", ".")
    if not row.rating:
        t = _text_or_empty(page.locator('div[role="img"][aria-label*="star" i]').first)
        m = re.search(r"([\d.,]+)", t)
        if m:
            row.rating = m.group(1).replace(",", ".")

    # Website
    for sel in (
        'a[data-item-id="authority"]',
        'a[aria-label*="Website" i]',
        'a[data-tooltip="Open website" i]',
    ):
        loc = page.locator(sel).first
        if loc.count():
            href = loc.get_attribute("href") or ""
            if href.startswith("http"):
                row.website_url = href.split("?")[0]
                break

    # Address — often a button copy row
    addr_btn = page.locator('button[data-item-id="address"]').first
    if addr_btn.count():
        row.address = _text_or_empty(addr_btn)
    if not row.address:
        row.address = _text_or_empty(page.locator('[data-tooltip="Copy address" i]').first)

    # Phone
    phone_btn = page.locator('button[data-item-id*="phone" i]').first
    if phone_btn.count():
        row.phone = _text_or_empty(phone_btn)
    if not row.phone:
        for a in page.locator('a[href^="tel:"]').all():
            row.phone = (a.get_attribute("href") or "").replace("tel:", "").strip()
            if row.phone:
                break
    if not row.phone:
        row.phone = _phone_from_text(_main_panel_text(page))

    # Overview: 'Services: …' line + optional About blurb
    _click_tab_if_present(page, r"^Overview$|Overview")
    time.sleep(0.5)
    services_line = _extract_services_line(page)
    about_parts: list[str] = []
    for sel in (
        'div[aria-label*="About" i]',
        "section.HlvSq",
        'div[class*="fontBodyMedium"]',
    ):
        for el in page.locator(sel).all()[:12]:
            tx = _text_or_empty(el)
            if len(tx) > 40 and row.practice_name and row.practice_name not in tx[: len(row.practice_name) + 5]:
                about_parts.append(tx)
    extra = " ".join(dict.fromkeys(about_parts))[:6000]
    if services_line:
        row.services_text = services_line if not extra else f"{services_line} | {extra}"
    else:
        _click_tab_if_present(page, r"About")
        time.sleep(0.4)
        if not services_line:
            services_line = _extract_services_line(page)
        row.services_text = (services_line + " | " + extra) if services_line else extra
    row.services_text = row.services_text.strip(" |")[:8000]

    # Reviews
    _click_tab_if_present(page, r"^Reviews$|Reviews")
    time.sleep(1)
    review_scroll = page.locator('div[role="main"]').first
    texts: list[str] = []

    def pull_visible_reviews() -> list[str]:
        out: list[str] = []
        # Common review body patterns (may need updates when Maps changes)
        for sel in (
            'span.wiI7pd',
            'span[class*="review"]',
            'div[data-review-id] span',
        ):
            for el in page.locator(sel).all():
                tx = _text_or_empty(el)
                if len(tx) < 25:
                    continue
                if _REVIEW_NOISE.match(tx.strip()):
                    continue
                if tx in out:
                    continue
                out.append(tx)
                if len(out) >= max_reviews:
                    return out
        return out

    for _ in range(25):
        texts = pull_visible_reviews()
        if len(texts) >= max_reviews:
            break
        try:
            review_scroll.evaluate("el => el.scrollBy(0, 700)")
        except Exception:
            break
        time.sleep(0.4)

    row.reviews = texts[:max_reviews]
    return row


def write_csv(path: str, rows: Iterable[PlaceRow]) -> None:
    fieldnames = [
        "practice_name",
        "website_url",
        "services",
        "rating",
        "reviews_top_10",
        "address",
        "phone",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(
                {
                    "practice_name": r.practice_name,
                    "website_url": r.website_url,
                    "services": r.services_text,
                    "rating": r.rating,
                    "reviews_top_10": r.reviews_blob(),
                    "address": r.address,
                    "phone": r.phone,
                }
            )


def run(
    playwright: Playwright,
    city: str,
    search_query: str,
    max_places: int,
    out_csv: str,
    headed: bool,
    slow_mo_ms: int,
    delay_between_places_s: float,
    place_urls: list[str] | None = None,
) -> int:
    browser: Browser = playwright.chromium.launch(
        headless=not headed,
        slow_mo=slow_mo_ms,
    )
    context = browser.new_context(
        user_agent=USER_AGENT,
        locale="en-US",
        viewport={"width": 1400, "height": 900},
    )
    page = context.new_page()

    if place_urls:
        hrefs = [u.strip() for u in place_urls if u.strip()]
    else:
        q = quote_plus(f"{search_query} in {city}")
        search_url = f"https://www.google.com/maps/search/{q}?hl=en"
        page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(2)
        _dismiss_consent(page)
        time.sleep(1)
        _scroll_results_feed(page, max_scrolls=25, pause_s=1.2)
        hrefs = _collect_place_hrefs(page, limit=max_places)

    if not hrefs:
        print("No place links found. Try headed mode or adjust city/query.", file=sys.stderr)
        browser.close()
        return 1

    rows: list[PlaceRow] = []
    for i, href in enumerate(hrefs, 1):
        print(f"[{i}/{len(hrefs)}] {href[:80]}...", flush=True)
        try:
            rows.append(scrape_place_page(page, href))
        except Exception as e:
            print(f"  skip: {e}", file=sys.stderr)
        time.sleep(delay_between_places_s)

    write_csv(out_csv, rows)
    browser.close()
    print(f"Wrote {len(rows)} rows to {out_csv}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Google Maps therapy / psych services scraper")
    parser.add_argument(
        "--city",
        default="",
        help='City and region when searching, e.g. "Kajang, Selangor". Not needed with --url.',
    )
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        metavar="MAPS_URL",
        help="Google Maps place URL (repeat for multiple). Skips search; --city optional.",
    )
    parser.add_argument(
        "--query",
        default=DEFAULT_QUERY,
        help="Search phrase when using --city (default: psychological services therapists)",
    )
    parser.add_argument("--max-places", type=int, default=15, help="Max listings to scrape")
    parser.add_argument("--out", default="therapy_data.csv", help="Output CSV path")
    parser.add_argument("--headed", action="store_true", help="Show browser (often more reliable)")
    parser.add_argument("--slow-mo", type=int, default=0, help="Playwright slow_mo ms")
    parser.add_argument(
        "--delay",
        type=float,
        default=2.5,
        help="Seconds between place detail pages",
    )
    args = parser.parse_args()
    place_urls = [u for u in args.url if u]
    if not place_urls and not args.city.strip():
        parser.error("Provide --city for search mode, or pass at least one --url")

    with sync_playwright() as pw:
        raise SystemExit(
            run(
                pw,
                city=args.city.strip(),
                search_query=args.query,
                max_places=args.max_places,
                out_csv=args.out,
                headed=args.headed,
                slow_mo_ms=args.slow_mo,
                delay_between_places_s=args.delay,
                place_urls=place_urls or None,
            )
        )


if __name__ == "__main__":
    main()