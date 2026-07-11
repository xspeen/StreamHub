#!/usr/bin/env python3
"""
StreamHub Channel Scanner
Fetches M3U playlists from iptv-org, parses channels, handles deduplication,
caching, and follows redirects for token refresh.
Uses only Python standard library - no external packages.
"""

import json
import os
import sys
import re
import time
import urllib.request
import urllib.error
import urllib.parse


# ---- Category definitions ----

BASE_URL = "https://iptv-org.github.io/iptv/"

# African country codes for DStv aggregation
R_AFRICA = "za,ng,ke,gh,ug,tz,zm,zw,et,sn,cm,ci,mw,mz,na,bw,sz,ls,mg,ao,rw,so,sd,ne,ml,bj,tg,bf,cg,cd,lr,sl,gn,eq,st,cv,km,dj,er,td,cf,mr,ss"

# Regional groupings
R_EUROPE = "gb,de,fr,it,es,pt,nl,se,no,dk,pl,ua,ru,ro,bg,hu,cz,sk,si,hr,rs,ba,me,mk,al,gr,cy,mt,ie,is,fi,ee,lv,lt,lu,be,at,ch,li"
R_ASIA = "in,jp,kr,tr,sa,ae,pk,bd,id,ph,my,th,vn,cn,tw,sg,lk,np,mm,kh,la,mv,bt,mn,kz,uz,kg,tj,tm,af,iq,ir,sy,jo,lb,ps,ye,om,kw,bh,qa,ge,am,az"
R_AMER = "us,ca,mx,br,ar,co,cl,pe,ve,ec,uy,py,bo,cr,pa,gt,hn,sv,ni,cu,do,pr,jm,tt,bs,bb,bz,gy,sr"
R_ME = "sa,ae,iq,ir,tr,jo,lb,ps,ye,om,kw,bh,qa,sy"
R_OCE = "au,nz,fj,pg,ws,to,vu,sb,ki,tv,nr,pw,fm,mh"

GENRES = [
    "sports", "news", "movies", "entertainment", "kids", "music",
    "documentary", "lifestyle", "religion", "education", "science",
    "travel", "cooking"
]

GENRE_ICONS = {
    "sports": "fa-futbol",
    "news": "fa-newspaper",
    "movies": "fa-film",
    "entertainment": "fa-tv",
    "kids": "fa-child-reaching",
    "music": "fa-music",
    "documentary": "fa-earth-americas",
    "lifestyle": "fa-heart",
    "religion": "fa-place-of-worship",
    "education": "fa-graduation-cap",
    "science": "fa-flask",
    "travel": "fa-plane",
    "cooking": "fa-utensils"
}

COUNTRY_NAMES = {
    "za": "S. Africa", "ng": "Nigeria", "ke": "Kenya", "gh": "Ghana",
    "ug": "Uganda", "tz": "Tanzania", "zm": "Zambia", "zw": "Zimbabwe",
    "et": "Ethiopia", "sn": "Senegal", "cm": "Cameroon", "ci": "Ivory Coast",
    "us": "USA", "gb": "UK", "in": "India", "br": "Brazil", "de": "Germany",
    "fr": "France", "jp": "Japan", "kr": "S. Korea", "tr": "Turkey",
    "sa": "Saudi Arabia", "pk": "Pakistan", "bd": "Bangladesh", "id": "Indonesia",
    "ph": "Philippines", "mx": "Mexico", "ar": "Argentina", "co": "Colombia",
    "it": "Italy", "es": "Spain", "pt": "Portugal", "nl": "Netherlands",
    "se": "Sweden", "no": "Norway", "dk": "Denmark", "pl": "Poland",
    "ua": "Ukraine", "ru": "Russia", "au": "Australia", "nz": "New Zealand",
    "ca": "Canada", "ae": "UAE", "ir": "Iran", "iq": "Iraq", "my": "Malaysia",
    "th": "Thailand", "vn": "Vietnam", "cn": "China", "tw": "Taiwan",
    "ro": "Romania", "bg": "Bulgaria", "hu": "Hungary", "cz": "Czechia",
    "sk": "Slovakia", "si": "Slovenia", "hr": "Croatia", "rs": "Serbia",
    "ba": "Bosnia", "me": "Montenegro", "mk": "N. Macedonia", "al": "Albania",
    "gr": "Greece", "cy": "Cyprus", "mt": "Malta", "ie": "Ireland",
    "is": "Iceland", "fi": "Finland", "ee": "Estonia", "lv": "Latvia",
    "lt": "Lithuania", "lu": "Luxembourg", "be": "Belgium", "at": "Austria",
    "ch": "Switzerland", "cl": "Chile", "pe": "Peru", "ve": "Venezuela",
    "ec": "Ecuador", "uy": "Uruguay", "py": "Paraguay", "bo": "Bolivia",
    "cr": "Costa Rica", "pa": "Panama", "gt": "Guatemala", "hn": "Honduras",
    "sv": "El Salvador", "ni": "Nicaragua", "cu": "Cuba", "do": "Dominican Rep.",
    "jm": "Jamaica", "tt": "Trinidad", "bs": "Bahamas", "bb": "Barbados",
    "sg": "Singapore", "lk": "Sri Lanka", "np": "Nepal", "mm": "Myanmar",
    "kh": "Cambodia", "la": "Laos", "fj": "Fiji", "pg": "Papua NG",
    "ge": "Georgia", "am": "Armenia", "az": "Azerbaijan", "kz": "Kazakhstan",
    "uz": "Uzbekistan", "kg": "Kyrgyzstan", "tj": "Tajikistan",
    "tm": "Turkmenistan", "af": "Afghanistan", "sy": "Syria", "jo": "Jordan",
    "lb": "Lebanon", "ps": "Palestine", "ye": "Yemen", "om": "Oman",
    "kw": "Kuwait", "bh": "Bahrain", "qa": "Qatar"
}


def build_categories():
    """Build the full list of categories for the API."""
    cats = []

    # DStv - aggregates all African sources
    cats.append({"id": "dstv", "name": "DStv", "icon": "fa-satellite-dish", "type": "dstv"})

    # Regions
    regions = [
        ("africa", "Africa", "fa-globe-africa", R_AFRICA),
        ("europe", "Europe", "fa-globe-europe", R_EUROPE),
        ("asia", "Asia", "fa-globe-asia", R_ASIA),
        ("americas", "Americas", "fa-globe-americas", R_AMER),
        ("mideast", "Middle East", "fa-mosque", R_ME),
        ("oceania", "Oceania", "fa-water", R_OCE),
    ]
    for rid, rname, ricon, rcodes in regions:
        cats.append({
            "id": rid,
            "name": rname,
            "icon": ricon,
            "type": "region",
            "codes": rcodes.split(",")
        })

    # Genres
    for g in GENRES:
        cats.append({
            "id": g,
            "name": g[0].upper() + g[1:],
            "icon": GENRE_ICONS.get(g, "fa-tv"),
            "type": "cat"
        })

    # Individual countries - deduplicate
    all_codes = set()
    for code_list in [R_AFRICA, R_EUROPE, R_ASIA, R_AMER, R_ME, R_OCE]:
        for c in code_list.split(","):
            all_codes.add(c.strip())

    for c in sorted(all_codes):
        cats.append({
            "id": c,
            "name": COUNTRY_NAMES.get(c, c.upper()),
            "icon": "fa-tower-broadcast",
            "type": "country"
        })

    return cats


def get_urls_for_category(cat):
    """Get the list of M3U URLs for a given category."""
    if cat["type"] == "dstv":
        return [f"{BASE_URL}countries/{c}.m3u" for c in R_AFRICA.split(",")]
    elif cat["type"] == "region":
        return [f"{BASE_URL}countries/{c}.m3u" for c in cat.get("codes", [])]
    elif cat["type"] == "cat":
        return [f"{BASE_URL}categories/{cat['id']}.m3u"]
    elif cat["type"] == "country":
        return [f"{BASE_URL}countries/{cat['id']}.m3u"]
    return []


def parse_m3u(text):
    """Parse M3U playlist text into a list of channel dicts."""
    channels = []
    lines = text.split("\n")
    name = ""
    group = ""

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            # Extract channel name (after last comma)
            comma_idx = line.rfind(",")
            if comma_idx > -1:
                name = line[comma_idx + 1:].strip()
            else:
                name = "Unknown"

            # Extract group-title
            group_match = re.search(r'group-title="([^"]*)"', line, re.IGNORECASE)
            group = group_match.group(1).strip() if group_match else ""
        elif line.startswith("http") and name:
            channels.append({
                "name": name,
                "group": group,
                "url": line
            })
            name = ""
            group = ""

    return channels


def fetch_url(url, timeout=15, max_redirects=5):
    """
    Fetch a URL with redirect following and proper headers.
    Mimics a set-top box User-Agent for HLS streams.
    Returns the response text or None on failure.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; STB Emulator) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
    }

    current_url = url
    for _ in range(max_redirects):
        try:
            req = urllib.request.Request(current_url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                # Check for redirect
                final_url = resp.geturl()
                if final_url != current_url:
                    current_url = final_url
                    continue
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            # Follow redirects manually
            if e.code in (301, 302, 303, 307, 308):
                location = e.headers.get("Location")
                if location:
                    if location.startswith("http"):
                        current_url = location
                    else:
                        parsed = urllib.parse.urlparse(current_url)
                        current_url = f"{parsed.scheme}://{parsed.netloc}{location}"
                    continue
            return None
        except (urllib.error.URLError, OSError, TimeoutError):
            return None

    return None


def fetch_category_channels(cat, max_channels=3000):
    """Fetch and parse all channels for a category. Returns deduplicated list."""
    urls = get_urls_for_category(cat)
    all_channels = []
    seen_urls = set()

    for url in urls:
        if len(all_channels) >= max_channels:
            break
        text = fetch_url(url)
        if text:
            channels = parse_m3u(text)
            for ch in channels:
                if ch["url"] not in seen_urls:
                    seen_urls.add(ch["url"])
                    all_channels.append(ch)
                    if len(all_channels) >= max_channels:
                        break

    return all_channels


def main():
    """CLI entry point for the scanner."""
    if len(sys.argv) < 3:
        print("Usage: scanner.py <data_dir> <category_id>")
        sys.exit(1)

    data_dir = sys.argv[1]
    cat_id = sys.argv[2]

    # Import db module
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from db import StreamHubDB

    db = StreamHubDB(data_dir)

    # Check cache first
    cached = db.get_cached_channels()
    if cached and cat_id in cached:
        print(json.dumps(cached[cat_id]))
        return

    # Build categories and find the requested one
    cats = build_categories()
    cat = None
    for c in cats:
        if c["id"] == cat_id:
            cat = c
            break

    if not cat:
        print(json.dumps([]))
        return

    # Fetch channels
    channels = fetch_category_channels(cat)

    # Cache the result
    cache = db.get_cached_channels() or {}
    cache[cat_id] = channels
    db.save_channel_cache(cache)

    # Output
    print(json.dumps(channels))


if __name__ == "__main__":
    main()
