"""Monthly crude oil production by country, from the US EIA International Energy Data bulk file (free, no API key).

Writes web/data/production.json for the "Production data" section on /insights/.
Run monthly by .github/workflows/production-data.yml.
Series: "Crude oil including lease condensate production", monthly, thousand barrels per day.
(JODI was tried first: it has no production volumes for Iraq after 2024, UAE after 2018, Oman after 2016.)
"""
import csv, io, json, os, sys, calendar, datetime, urllib.request, collections

FIRST_YEAR = 2015
OUT = sys.argv[1] if len(sys.argv) > 1 else "web/data/production.json"

ME, CIS, AF, NA, LA, EU, AP = "Middle East", "CIS & Caspian", "Africa", "North America", "Latin America", "Europe", "Asia-Pacific"
COUNTRIES = {
    # Middle East
    "SA": ("Saudi Arabia", ME), "IQ": ("Iraq", ME), "AE": ("UAE", ME), "KW": ("Kuwait", ME), "IR": ("Iran", ME),
    "QA": ("Qatar", ME), "OM": ("Oman", ME), "BH": ("Bahrain", ME), "SY": ("Syria", ME), "YE": ("Yemen", ME),
    "JO": ("Jordan", ME), "IL": ("Israel", ME), "TR": ("Türkiye", ME),
    # CIS & Caspian
    "RU": ("Russia", CIS), "KZ": ("Kazakhstan", CIS), "AZ": ("Azerbaijan", CIS), "TM": ("Turkmenistan", CIS),
    "UZ": ("Uzbekistan", CIS), "UA": ("Ukraine", CIS), "BY": ("Belarus", CIS), "GE": ("Georgia", CIS),
    "KG": ("Kyrgyzstan", CIS), "TJ": ("Tajikistan", CIS), "MD": ("Moldova", CIS), "AM": ("Armenia", CIS),
    # Africa
    "NG": ("Nigeria", AF), "AO": ("Angola", AF), "LY": ("Libya", AF), "DZ": ("Algeria", AF), "EG": ("Egypt", AF),
    "CG": ("Congo", AF), "GA": ("Gabon", AF), "GQ": ("Equatorial Guinea", AF), "GH": ("Ghana", AF), "TD": ("Chad", AF),
    "SD": ("Sudan", AF), "SS": ("South Sudan", AF), "TN": ("Tunisia", AF), "CM": ("Cameroon", AF), "CI": ("Côte d'Ivoire", AF),
    "CD": ("DR Congo", AF), "NE": ("Niger", AF), "SN": ("Senegal", AF), "ZA": ("South Africa", AF), "MA": ("Morocco", AF),
    "MZ": ("Mozambique", AF), "MU": ("Mauritius", AF), "BW": ("Botswana", AF), "SZ": ("Eswatini", AF),
    "LS": ("Lesotho", AF), "NA": ("Namibia", AF), "BJ": ("Benin", AF), "MR": ("Mauritania", AF), "KE": ("Kenya", AF),
    # North America
    "US": ("United States", NA), "CA": ("Canada", NA), "MX": ("Mexico", NA),
    # Latin America
    "BR": ("Brazil", LA), "VE": ("Venezuela", LA), "CO": ("Colombia", LA), "AR": ("Argentina", LA), "EC": ("Ecuador", LA),
    "GY": ("Guyana", LA), "PE": ("Peru", LA), "TT": ("Trinidad & Tobago", LA), "BO": ("Bolivia", LA), "CL": ("Chile", LA),
    "CU": ("Cuba", LA), "GT": ("Guatemala", LA), "BZ": ("Belize", LA), "SR": ("Suriname", LA), "PY": ("Paraguay", LA),
    "UY": ("Uruguay", LA), "DO": ("Dominican Rep.", LA), "CR": ("Costa Rica", LA), "PA": ("Panama", LA),
    "SV": ("El Salvador", LA), "HN": ("Honduras", LA), "NI": ("Nicaragua", LA), "JM": ("Jamaica", LA), "BB": ("Barbados", LA),
    "GD": ("Grenada", LA),
    # Europe
    "NO": ("Norway", EU), "GB": ("United Kingdom", EU), "DK": ("Denmark", EU), "IT": ("Italy", EU), "RO": ("Romania", EU),
    "DE": ("Germany", EU), "NL": ("Netherlands", EU), "AL": ("Albania", EU), "AT": ("Austria", EU), "PL": ("Poland", EU),
    "HR": ("Croatia", EU), "HU": ("Hungary", EU), "FR": ("France", EU), "ES": ("Spain", EU), "RS": ("Serbia", EU),
    "CZ": ("Czechia", EU), "GR": ("Greece", EU), "SK": ("Slovakia", EU), "LT": ("Lithuania", EU), "BG": ("Bulgaria", EU),
    "EE": ("Estonia", EU), "LV": ("Latvia", EU), "SI": ("Slovenia", EU), "IE": ("Ireland", EU), "PT": ("Portugal", EU),
    "BE": ("Belgium", EU), "SE": ("Sweden", EU), "FI": ("Finland", EU), "CH": ("Switzerland", EU), "CY": ("Cyprus", EU),
    "MT": ("Malta", EU), "LU": ("Luxembourg", EU), "IS": ("Iceland", EU), "MK": ("North Macedonia", EU),
    "BA": ("Bosnia & Herzegovina", EU), "ME": ("Montenegro", EU), "XK": ("Kosovo", EU),
    # Asia-Pacific
    "CN": ("China", AP), "IN": ("India", AP), "ID": ("Indonesia", AP), "MY": ("Malaysia", AP), "AU": ("Australia", AP),
    "TH": ("Thailand", AP), "VN": ("Vietnam", AP), "BN": ("Brunei", AP), "PK": ("Pakistan", AP), "MM": ("Myanmar", AP),
    "PG": ("Papua New Guinea", AP), "NZ": ("New Zealand", AP), "JP": ("Japan", AP), "PH": ("Philippines", AP),
    "BD": ("Bangladesh", AP), "TW": ("Chinese Taipei", AP), "MN": ("Mongolia", AP), "KR": ("Korea", AP),
    "TL": ("Timor-Leste", AP), "AF": ("Afghanistan", AP), "LK": ("Sri Lanka", AP), "HK": ("Hong Kong", AP),
    "SG": ("Singapore", AP), "NP": ("Nepal", AP), "MO": ("Macau", AP), "BT": ("Bhutan", AP), "FJ": ("Fiji", AP),
}


def fetch_bytes(url):
    req = urllib.request.Request(url, headers={"user-agent": "evgeny-maradin.pages.dev production-data updater"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read()


EIA_BULK = "https://api.eia.gov/bulk/INTL.zip"
NAME = "crude oil including lease condensate production"


def main():
    import zipfile, pycountry
    raw = fetch_bytes(EIA_BULK)
    print(f"EIA bulk: {len(raw)//1024//1024} MB")
    z = zipfile.ZipFile(io.BytesIO(raw))
    data, units, skipped = {}, collections.Counter(), set()
    for member in z.namelist():
        with z.open(member) as fh:
            for line in io.TextIOWrapper(fh, encoding="utf-8"):
                if NAME not in line.lower() or '"f":"M"' not in line.replace(" ", ""):
                    continue
                try:
                    s = json.loads(line)
                except ValueError:
                    continue
                if s.get("f") != "M" or NAME not in s.get("name", "").lower():
                    continue
                unit = s.get("units", "")
                units[unit] += 1
                if "barrels per day" not in unit.lower():
                    continue
                iso3 = (s.get("geography") or "").split("-")[-1]
                c = pycountry.countries.get(alpha_3=iso3)
                if not c:
                    skipped.add(iso3); continue
                mult = 1000.0 if unit.lower().startswith("million") else 1.0
                for d, v in s.get("data", []):
                    if v is None or not isinstance(v, (int, float)):
                        continue
                    per = f"{str(d)[:4]}-{str(d)[4:6]}"
                    if int(per[:4]) >= FIRST_YEAR:
                        data[(c.alpha_2, per)] = v * mult
    print("units seen:", dict(units))
    print("skipped aggregates/unknown:", sorted(skipped))
    if not data:
        sys.exit("no data parsed - EIA bulk format changed?")

    months = sorted({p for _, p in data})
    by = collections.defaultdict(dict)
    for (area, per), v in data.items():
        by[area][per] = v

    # The latest months are incomplete (countries report with different lags). End the series at the
    # last month where countries producing >= 90% of output (vs. their trailing 12-month level) reported.
    def level(a, idx):
        vals = [by[a][m] for m in months[max(0, idx - 12):idx] if m in by[a]]
        return sum(vals) / len(vals) if vals else 0
    end = len(months) - 1
    while end > 12:
        tot = sum(level(a, end) for a in by)
        rep = sum(level(a, end) for a in by if months[end] in by[a])
        if tot and rep / tot >= 0.9:
            break
        end -= 1
    months = months[:end + 1]

    countries = {}
    for a, series in by.items():
        v = [round(series[m], 1) if m in series else None for m in months]
        if not any(x for x in v if x):  # never produced
            continue
        pc = pycountry.countries.get(alpha_2=a)
        name, region = COUNTRIES.get(a, (getattr(pc, "common_name", None) or getattr(pc, "name", a), "Other"))
        countries[a] = {"n": name, "r": region, "v": v}
    unknown = sorted(a for a in countries if a not in COUNTRIES)
    if unknown:
        print("codes without a name/region mapping:", unknown)

    out = {"source": "U.S. EIA International Energy Data", "source_url": "https://www.eia.gov/international/data/world",
           "series": "Crude oil incl. lease condensate production, thousand barrels per day",
           "updated": datetime.date.today().isoformat(), "months": months, "countries": countries}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    last = months[-1]
    top = sorted(countries.items(), key=lambda kv: -(kv[1]["v"][-1] or 0))[:10]
    print(f"months {months[0]}..{last}, countries {len(countries)}, file {os.path.getsize(OUT)//1024} KB")
    print("top 10 in", last, ":", ", ".join(f"{c['n']} {c['v'][-1]}" for _, c in top))


if __name__ == "__main__":
    main()
