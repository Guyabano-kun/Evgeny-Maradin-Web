"""One-off probe: list STEO monthly production series (name, units, last points)."""
import io, json, zipfile, urllib.request, sys
req = urllib.request.Request("https://api.eia.gov/bulk/STEO.zip", headers={"user-agent": "evgeny-maradin.pages.dev"})
raw = urllib.request.urlopen(req, timeout=600).read()
z = zipfile.ZipFile(io.BytesIO(raw)); out = []; keys = set()
for m in z.namelist():
    for line in io.TextIOWrapper(z.open(m), encoding="utf-8"):
        try: s = json.loads(line)
        except ValueError: continue
        keys |= set(s.keys())
        n = s.get("name", "")
        if s.get("f") == "M" and "production" in n.lower():
            d = sorted(s.get("data", []))
            out.append({"id": s.get("series_id"), "name": n, "units": s.get("units"), "last": d[-1] if d else None,
                        "pts": [p for p in d if "202605" <= str(p[0]) <= "202612"],
                        "extra": {k: s[k] for k in s if k not in ("data", "name", "series_id", "units", "f")}})
json.dump({"keys": sorted(keys), "n": len(out), "series": out}, open(sys.argv[1], "w"), indent=0)
print(len(out), "production series")
