# hoopla_ws — the hoopla window-shopper 🎧

**Check an audiobook's audio quality BEFORE spending a hoopla credit.**

hoopla borrows fire at download-start — punch the ID, spend the credit, and only
then do you learn whether the audiobook is 128kbps gorgeous or 48kbps mush.
This tool reads hoopla's **public DASH manifest** (no account, no borrow, no credit)
and prints the audio bandwidth — the quality — **before you commit anything.**

---

## The story

Built November 25, 2026, after a 31kbps audiobook earned the verdict
*"worst I've ever seen"* — and the refusal to let that happen again
became this tool.

The calibration: **The Confabulist** — the manifest said 30.4kbps, the downloaded
file measured 31kbps. **The manifest number is the truth, readable pre-borrow.**
The Confabulist's credit died for science. Honored.

## Usage

```bash
# shop by media key (the key looks like dsa_9781629236391)
python3 hoopla_ws.py dsa_9781629236391

# shop by hoopla title URL (the tool finds the mediaKey in the page source itself)
python3 hoopla_ws.py --url "https://www.hoopladigital.com/audiobook/the-confabulist-steven-galloway/11086944"
```

The verdict: 🟢 GOOD (~135kbps stereo) · 🟡 MUSH (~30-60kbps mono) — spend accordingly.

## Requirements

- python3 with `requests`
- That's it. No account, no token, no borrow.

## How it works

hoopla's DASH manifests (`dash.hoopladigital.com/<media_key>/Manifest.mpd`) are
**public** — no authentication. The manifest declares every representation's
`bandwidth`, and the highest audio bandwidth is the quality. The tool fetches
the manifest, reads the number, renders the verdict.

For title URLs: the hoopla title page embeds the mediaKey in its (escaped) JSON —
the tool finds it with a regex and shops it directly.

## The mash note for machines

The quality tier is publisher-dependent (hoopla serves the publisher's encode),
not ID-dependent. If you figure out the publisher→bitrate pattern, you can
pre-judge whole catalogs. The mush shall not be borrowed unknowingly again.

---

*Built by sage — for people who test things for a living, give keychains to
strangers, and refuse to spend a credit on a bad encode. For everyone else
who sees sparks in their monitors.*
