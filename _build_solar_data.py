"""Build the Scotland solar place dataset and geocode it."""
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(r"D:\Tools\Solar\Scotland Solar Project Plan")
CACHE = OUT / "_solar_coords.json"

# place, primary volume, cpc, ads competition 0-1, region
# Primary keyword is "solar panels {place}" except Scotland.
PLACES = [
    ("scotland", 1300, 13.35, 0.93, "Scotland-wide"),
    ("glasgow", 320, 14.25, 0.90, "Glasgow & Clyde"),
    ("edinburgh", 260, 20.16, 0.88, "Edinburgh & Lothians"),
    ("aberdeen", 260, 16.03, 0.82, "Aberdeen & North East"),
    ("aberdeenshire", 260, 16.03, 0.82, "Aberdeen & North East"),
    ("inverness", 90, 10.30, 0.96, "Highlands"),
    ("perth", 90, 7.67, 0.65, "Tayside"),
    ("dundee", 70, 11.10, 0.83, "Tayside"),
    ("fife", 70, 25.01, 0.78, "Fife"),
    ("ayrshire", 30, 16.58, 0.66, "Ayrshire"),
    ("dumfries", 30, 8.37, 0.83, "Dumfries & Galloway"),
    ("stirling", 30, 15.24, 0.78, "Forth Valley"),
    ("dunfermline", 20, 12.22, 0.83, "Fife"),
    ("east lothian", 20, 12.30, 0.84, "Edinburgh & Lothians"),
    ("elgin", 20, 8.37, 0.90, "Aberdeen & North East"),
    ("falkirk", 20, 21.67, 0.83, "Forth Valley"),
    ("galashiels", 20, 19.69, 0.80, "Scottish Borders"),
    ("lanarkshire", 20, 8.52, 0.94, "Lanarkshire"),
    ("livingston", 20, 13.59, 0.74, "Edinburgh & Lothians"),
    ("midlothian", 20, 40.66, 0.93, "Edinburgh & Lothians"),
    ("moray", 20, 19.47, 0.70, "Aberdeen & North East"),
    ("ayr", 10, 23.49, 0.83, "Ayrshire"),
    ("bathgate", 10, 12.25, 0.93, "Edinburgh & Lothians"),
    ("cumbernauld", 10, 0.0, 0.50, "Lanarkshire"),
    ("east kilbride", 10, 13.61, 0.91, "Glasgow & Clyde"),
    ("forres", 10, 14.81, 0.82, "Aberdeen & North East"),
    ("hamilton", 10, 12.65, 0.90, "Lanarkshire"),
    ("highlands", 10, 4.69, 0.58, "Highlands"),
    ("kilmarnock", 10, 43.58, 0.89, "Ayrshire"),
    ("kinross", 10, 0.0, 0.50, "Tayside"),
    ("kirkcaldy", 10, 0.0, 0.29, "Fife"),
    ("motherwell", 10, 7.69, 1.0, "Lanarkshire"),
    ("paisley", 10, 25.15, 0.97, "Glasgow & Clyde"),
    ("perthshire", 10, 0.0, 0.07, "Tayside"),
    ("renfrewshire", 10, 0.0, 0.25, "Glasgow & Clyde"),
    ("tayside", 10, 0.0, 0.86, "Tayside"),
    ("west lothian", 10, 19.00, 0.80, "Edinburgh & Lothians"),
]

# Extra measured keywords to show on the site plan (not the town's primary volume).
EXTRAS = {
    "scotland": [
        ("solar panel grants scotland", 1900, "/solar-panel-grants/", "Content", "Largest Scotland intent cluster — one grants page"),
        ("home energy scotland grant", 1000, "/solar-panel-grants/", "Content", "Scheme name people actually search"),
        ("free solar panels scotland", 390, "/solar-panel-grants/", "Content", "Grant-seekers; answer with the loan, not a free install"),
        ("cost of solar panels scotland", 320, "/solar-panel-cost/", "Secondary", "Pricing page"),
        ("are solar panels worth it in scotland", 170, "/blog/are-solar-panels-worth-it/", "Content", "Weather and payback objection"),
        ("solar panel installation scotland", 110, "/solar-panel-installation/", "Secondary", "Installer-intent national term"),
        ("solar panel installers scotland", 50, "/", "Secondary", "Homepage support"),
        ("warmer homes scotland", 1600, "/solar-panel-grants/", "Content", "Related scheme; only mention if solar is in scope"),
    ],
    "glasgow": [
        ("solar panel installation glasgow", 210, "/solar-panel-installation/", "Secondary", "Measured"),
        ("solar panel installers glasgow", 170, "/", "Secondary", "Measured"),
    ],
    "edinburgh": [
        ("solar panel installation edinburgh", 170, "/solar-panel-installation/", "Secondary", "Measured"),
        ("solar panel installers edinburgh", 170, "/", "Secondary", "Measured"),
    ],
    "aberdeen": [
        ("solar panel installers aberdeen", 10, "/", "Supporting", "Measured, low volume"),
    ],
    "aberdeenshire": [
        ("solar panel installers aberdeenshire", 20, "/", "Secondary", "Measured"),
    ],
    "inverness": [
        ("solar panel installers inverness", 10, "/", "Supporting", "Measured"),
    ],
    "perth": [
        ("solar panels perth scotland", 30, "/", "Primary alt", "Disambiguates Perth, Australia"),
        ("solar panel installation perth", 20, "/solar-panel-installation/", "Secondary", "Measured"),
        ("solar panel installers perth", 20, "/", "Secondary", "Measured"),
    ],
    "dundee": [
        ("solar panel installers dundee", 10, "/", "Supporting", "Measured"),
    ],
    "fife": [
        ("solar panel installers fife", 10, "/", "Supporting", "Measured"),
    ],
    "stirling": [
        ("solar panel installation stirling", 10, "/solar-panel-installation/", "Supporting", "Measured"),
    ],
    "ayrshire": [
        ("solar panel installers ayrshire", 10, "/", "Supporting", "Measured"),
    ],
}

# Keep region markers off the main town pin.
GEO_ALIAS = {
    "scotland": None,
    "aberdeenshire": "Inverurie",
    "fife": "Glenrothes",
    "lanarkshire": "Wishaw",
    "highlands": "Aviemore",
    "moray": "Lossiemouth",
    "tayside": "Forfar",
    "perthshire": "Crieff",
    "east lothian": "Haddington",
    "midlothian": "Dalkeith",
    "west lothian": "Linlithgow",
    "renfrewshire": "Johnstone",
    "ayrshire": "Irvine",
    "perth": "Perth",
    "east kilbride": "East Kilbride",
    "dumfries": "Dumfries",
}

FIXED = {
    "scotland": {"lat": 56.49, "lng": -4.20, "display": "Scotland"},
}


def tier_for(vol: int) -> str:
    if vol >= 200:
        return "S"
    if vol >= 70:
        return "A"
    if vol >= 30:
        return "B"
    if vol >= 20:
        return "C"
    if vol >= 10:
        return "D"
    return "Skip"


def bucket_for(vol: int) -> str:
    if vol >= 500:
        return "500+"
    if vol >= 200:
        return "200-499"
    if vol >= 70:
        return "70-199"
    if vol >= 20:
        return "20-69"
    return "<20"


def compact(town: str) -> str:
    return "".join(ch for ch in town.lower() if ch.isalnum())


def geocode(name: str, cache: dict) -> dict:
    key = name.lower().strip()
    if key in FIXED:
        cache[key] = FIXED[key]
        return cache[key]
    if key in cache and cache[key].get("lat") is not None:
        return cache[key]
    query = GEO_ALIAS.get(key, name)
    if query is None:
        return FIXED["scotland"]
    url = "https://geocoding-api.open-meteo.com/v1/search?" + urllib.parse.urlencode(
        {"name": query, "count": 5, "language": "en", "format": "json", "countryCode": "GB"}
    )
    req = urllib.request.Request(url, headers={"User-Agent": "SolarScotlandPlan/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    results = payload.get("results") or []
    pick = None
    for r in results:
        admin = " ".join(
            str(r.get(k) or "")
            for k in ("admin1", "admin2", "admin3", "name")
        ).lower()
        if "scotland" in admin or (r.get("country_code") or "").upper() == "GB":
            pick = r
            if "scotland" in admin:
                break
    if pick is None and results:
        pick = results[0]
    if not pick:
        raise RuntimeError(f"no geocode for {name} ({query})")
    cache[key] = {
        "lat": float(pick["latitude"]),
        "lng": float(pick["longitude"]),
        "display": pick.get("name") or query,
    }
    time.sleep(0.15)
    return cache[key]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cache = {}
    if CACHE.exists():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    rows = []
    for town, vol, cpc, comp, region in PLACES:
        geo = geocode(town, cache)
        comp_pct = round((comp or 0) * 100, 1)
        score = round(vol * max(cpc or 0, 0.5) / (1 + comp_pct / 50), 1) if vol else 0.0
        slug = compact(town)
        suggested = f"solarpanels{slug}.co.uk"
        extras = [
            {"kw": kw, "vol": v, "page": page, "type": typ, "note": note}
            for kw, v, page, typ, note in EXTRAS.get(town, [])
        ]
        rows.append(
            {
                "keyword": "solar panels scotland" if town == "scotland" else f"solar panels {town}",
                "town": town,
                "volume": vol,
                "cpc": cpc or 0,
                "competition": comp_pct,
                "opportunity_score": score,
                "tier": tier_for(vol),
                "volume_bucket": bucket_for(vol),
                "region": region,
                "emd_primary": suggested,
                "emd_best_available": suggested,
                "emd_available": [suggested],
                "emd_available_count": 0,
                "emd_nohyphen": False,
                "lat": geo["lat"],
                "lng": geo["lng"],
                "extras": extras,
            }
        )
    CACHE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    rows.sort(key=lambda r: (-r["volume"], -r["cpc"], r["town"]))
    (OUT / "_solar_kw_data.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    csv_path = OUT / "scotland-solar-places.csv"
    fields = [
        "town", "keyword", "volume", "cpc", "competition", "opportunity_score",
        "tier", "volume_bucket", "region", "emd_primary", "lat", "lng",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "places")
    print(csv_path)


if __name__ == "__main__":
    main()
