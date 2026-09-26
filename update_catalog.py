"""
OP TCG South Africa - catalog updater.

Pulls live product data from tracked competitor stores and writes catalog.json
in the shape the dashboard (optcg-dashboard.html) expects:

[
  {
    "id": "...",
    "name": "...",
    "set": "...",
    "category": "sealed" | "singles",
    "globalUsd": 0,               # left at 0 unless a global benchmark is wired in
    "stores": {"Store Name": price_in_zar, ...}
  },
  ...
]

HOW EACH STORE IS HANDLED
--------------------------
Shopify stores (Level Up Store, The Big Bang Shop) expose every product as
public JSON at <store>/products.json - no login, no scraping HTML, no
selectors to break. We paginate through it and keep anything whose title
contains "one piece".

Stores NOT included here, and why:
  - Solarpop: wholesale/trade distributor. Prices are hidden behind a
    customer login and everything shows "Out of Stock" publicly. This looks
    like a supplier account, not a retail competitor - nothing to scrape
    without trade credentials, and scraping a supplier's trade price to
    compare against your own retail price would be comparing the wrong
    numbers anyway.
  - Mirage Gaming: WooCommerce store, but its live navigation only shows
    Pokemon categories (Mega / Scarlet and Violet / Sword and Shield
    singles). No One Piece section was visible. Confirm with them whether
    they stock One Piece before adding a scraper for this one.
  - Unplugged Games: this is a North Carolina, USA shop (prices in USD) -
    not a South African competitor. Re-check the intended URL if you meant
    a different store.

ADDING A STORE LATER
---------------------
- Another Shopify store: just add its base URL to SHOPIFY_STORES below.
- A WooCommerce store: needs a separate scraper (WooCommerce has no public
  products.json by default) - ask for that when you have a confirmed URL.
"""

import json
import re
import time
import requests

# Shopify stores to pull from. Add more base URLs here as they're confirmed.
SHOPIFY_STORES = {
    "Level Up Store": "https://levelupstore.co.za",
    "The Big Bang Shop": "https://bigbangshop.co.za",
}

KEYWORD = "one piece"
REQUEST_TIMEOUT = 20
PAGE_SIZE = 250  # Shopify's max per page
USER_AGENT = "OPTCG-SA-Catalog-Bot/1.0 (+internal price comparison tool)"


def fetch_shopify_products(base_url, keyword=KEYWORD):
    """
    Pull every product from a Shopify store's public /products.json feed,
    paginating until an empty page is returned, and keep only products whose
    title contains `keyword` (case-insensitive).

    Returns a list of dicts: {title, price_zar, in_stock, vendor, product_type, url}
    """
    matches = []
    page = 1
    headers = {"User-Agent": USER_AGENT}

    while True:
        url = f"{base_url}/products.json"
        params = {"limit": PAGE_SIZE, "page": page}
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [warn] request failed for {base_url} page {page}: {e}")
            break

        try:
            data = resp.json()
        except ValueError:
            print(f"  [warn] non-JSON response from {base_url} page {page}")
            break

        products = data.get("products", [])
        if not products:
            break  # no more pages

        for p in products:
            title = p.get("title", "")
            if keyword.lower() not in title.lower():
                continue

            variants = p.get("variants", [])
            if not variants:
                continue

            # Use the lowest-priced in-stock variant; if none are in stock,
            # fall back to the lowest price overall so it still shows up
            # (flagged as unavailable) rather than disappearing silently.
            in_stock_variants = [v for v in variants if v.get("available")]
            chosen_pool = in_stock_variants or variants
            cheapest = min(chosen_pool, key=lambda v: float(v.get("price", "inf")))

            matches.append({
                "title": title,
                "price_zar": float(cheapest.get("price", 0)),
                "in_stock": bool(in_stock_variants),
                "product_type": p.get("product_type", ""),
                "vendor": p.get("vendor", ""),
                "url": f"{base_url}/products/{p.get('handle', '')}",
            })

        page += 1
        time.sleep(0.5)  # be polite - don't hammer the store's server

    return matches


def guess_category(title, product_type=""):
    """Sealed product vs single card, based on title/type keywords."""
    text = f"{title} {product_type}".lower()
    sealed_signals = ["booster box", "booster pack", "starter deck", "display",
                       "double pack", "case", "tin", "bundle", "elite trainer"]
    if any(sig in text for sig in sealed_signals):
        return "sealed"
    return "singles"


def guess_set(title):
    """Pull an OP-##/EB-##/ST-## style set code out of the title if present."""
    match = re.search(r"\b(OP|EB|ST|DP|PRB|IB|DF)-?\s?(\d{1,2})\b", title, re.IGNORECASE)
    if match:
        return f"{match.group(1).upper()}-{match.group(2).zfill(2)}"
    return "Unknown"


def slugify_id(title):
    slug = re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-").upper()
    return slug[:40]


def build_catalog():
    catalog_by_key = {}  # key: normalized title -> merged record

    for store_name, base_url in SHOPIFY_STORES.items():
        print(f"Fetching {store_name} ({base_url}) ...")
        products = fetch_shopify_products(base_url)
        print(f"  found {len(products)} One Piece product(s)")

        for prod in products:
            key = prod["title"].strip().lower()
            if key not in catalog_by_key:
                catalog_by_key[key] = {
                    "id": slugify_id(prod["title"]),
                    "name": prod["title"],
                    "set": guess_set(prod["title"]),
                    "category": guess_category(prod["title"], prod["product_type"]),
                    "globalUsd": 0,
                    "stores": {},
                }
            # Only record a price if the item is in stock somewhere; an
            # out-of-stock 0 would wrongly drag down the "lowest price".
            if prod["in_stock"]:
                catalog_by_key[key]["stores"][store_name] = prod["price_zar"]

    return list(catalog_by_key.values())


def update_catalog():
    catalog = build_catalog()
    with open("catalog.json", "w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"\ncatalog.json written with {len(catalog)} product(s).")


if __name__ == "__main__":
    update_catalog()
