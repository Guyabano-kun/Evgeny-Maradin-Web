"""One-off probe: list STEO monthly series for selected countries (name, units, May/Sep 2026 points)."""
import io, json, zipfile, urllib.request, sys
C = ["Canada", "Brazil", "United Arab", "Qatar", "China", "Norway", "Guyana", "Argentina", "Colombia", "United Kingdom",
     "Egypt", "India", "Indonesia", "Angola", "Ecuador", "Australia", "Oman", "Kazakhstan", "Russia", "Saudi"]
req = urllib.request.Request("https://api.eia.gov/bulk/STEO.zip", headers={"user-agent": "evgeny-maradin.pages.dev"})
z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(req, timeout=600).read())); out = []
for m in z.namelist():
    for line in io.TextIOWrapper(z.open(m), encoding="utf-8"):
        try: s = json.loads(line)
        except ValueError: continue
        n = s.get("name", "")
        if s.get("f") == "M" and any(c in n for c in C):
            d = dict(s.get("data", []))
            out.append({"id": s.get("series_id"), "name": n, "units": s.get("units"), "lh": s.get("lastHistoricalPeriod"),
                        "may": d.get("202605"), "sep": d.get("202609"), "jun": d.get("202606")})
json.dump(out, open(sys.argv[1], "w"), indent=0)
print(len(out))
