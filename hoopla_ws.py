#!/usr/bin/env python3
# hoopla_ws.py — THE HOOPLA WINDOW-SHOPPER
# Check an audiobook's audio quality BEFORE spending a hoopla credit.
#
# Two ways to use:
#   python3 hoopla_ws.py <media_key> [<media_key> ...]     # direct: shop known keys
#   python3 hoopla_ws.py --url <hoopla title url>          # paste a hoopladigital.com
#                                                           # title URL — the tool finds
#                                                           # the mediaKey in the page
#                                                           # source itself
#
# How it works: hoopla's DASH manifests (dash.hoopladigital.com/<media_key>/Manifest.mpd)
# are PUBLIC — no account, no borrow. The manifest declares the audio bandwidth,
# and the bandwidth IS the quality: ~135kbps stereo = gorgeous, ~30-60kbps mono = mush.
# The borrow, by contrast, fires at download-start and spends a credit instantly.
# Window-shop first. Spend only on the good ones.
#
# Calibrated: The Confabulist — manifest 30,400 bps vs downloaded 31 kbps (measured live).
# The worst audiobook ever encountered died to calibrate this tool. Honored.

import re
import sys
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}


def verdict(bandwidth):
    if bandwidth >= 100000:
        return "🟢 GOOD — full stereo sound, worth the credit"
    if bandwidth >= 80000:
        return "🟡 okay — midrange encode"
    return "🟡 MUSH — thin radio sound, skip if you're iffy"


def shop_key(media_key):
    url = f"https://dash.hoopladigital.com/{media_key}/Manifest.mpd"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"  {media_key}: HTTP {r.status_code} — manifest not available")
            return
        bws = [int(b) for b in re.findall(r'bandwidth="(\d+)"', r.text)]
        if not bws:
            print(f"  {media_key}: manifest has no bandwidth numbers")
            return
        best = max(bws)
        print(f"  {media_key}: {best // 1000} kbps max — {verdict(best)}")
    except Exception as e:
        print(f"  {media_key}: ERROR {e}")


def mediakey_from_url(url):
    """Fetch a hoopla title page and pull the mediaKey out of its source.
    (The key hides inside escaped JSON: \"mediaKey\":\"xxx_978...\" )"""
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    keys = re.findall(r'mediaKey\\?":\\?"([a-z]{2,4}_[0-9]{9,15})', r.text)
    return keys


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    if args[0] == "--url":
        for url in args[1:]:
            print(f"title url: {url}")
            keys = mediakey_from_url(url)
            if not keys:
                print("  no mediaKey found in that page — try view-source manually")
                continue
            for k in keys:
                shop_key(k)
    else:
        for mk in args:
            shop_key(mk)


if __name__ == "__main__":
    main()
