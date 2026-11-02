#!/usr/bin/env python3
"""Rebuild episodes.json from the podcast RSS feed. Standard library only. Run by GitHub Actions daily."""
import json, re, urllib.request, xml.etree.ElementTree as ET, datetime, sys
cfg = json.load(open("config.json"))
src = sys.argv[1] if len(sys.argv) > 1 else cfg["feed"]
raw = open(src, "rb").read() if not src.startswith("http") else urllib.request.urlopen(
    urllib.request.Request(src, headers={"User-Agent": "edventures-site-builder"}), timeout=60).read()
root = ET.fromstring(raw)
IT = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
guest_names = [g["name"].lower() for g in cfg["guests"]]
eps = []
for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    m = re.search(r"(?:Episodes?|Ep\.?)\s*#?\s*(\d+)", title, re.I)
    n = int(m.group(1)) if m else None
    if n is None and it.findtext(IT + "episode"):
        n = int(it.findtext(IT + "episode"))
    clean = re.sub(r"^\s*(?:Episodes?|Ep\.?)\s*#?\s*\d+\s*[:\-–—]?\s*", "", title).strip() or title
    low = title.lower()
    typ = "interview" if any(g in low for g in guest_names) else (
        "live" if any(w in low for w in cfg["live_words"]) else "news")
    typ = cfg.get("type_overrides", {}).get(str(n), typ)
    d = it.findtext("pubDate") or ""
    try: date = datetime.datetime.strptime(d[:16], "%a, %d %b %Y").strftime("%b %-d, %Y")
    except ValueError: date = ""
    eps.append({"n": n, "title": clean, "type": typ, "date": date, "link": (it.findtext("link") or "").strip()})
if not eps:
    sys.exit("No episodes parsed; leaving episodes.json unchanged.")
out = {"updated": datetime.date.today().strftime("%b %-d, %Y"), "episodes": eps}
json.dump(out, open("episodes.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(eps)} episodes written")
