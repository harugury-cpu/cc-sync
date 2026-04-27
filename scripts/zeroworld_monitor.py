#!/usr/bin/env python3
import json, sys
from datetime import timedelta, date
from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode, unquote
from urllib.error import URLError
from http.cookiejar import CookieJar

THEME_PK   = 52
PAGE_URL   = "https://zerohongdae.com/reservation/51"
API_URL    = "https://zerohongdae.com/reservation/theme"
START_HOUR = 12
END_HOUR   = 20

cj = CookieJar()
opener = build_opener(HTTPCookieProcessor(cj))
try:
    opener.open(Request(PAGE_URL, headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read()
except URLError:
    sys.exit(0)

xsrf = next((unquote(c.value) for c in cj if c.name == "XSRF-TOKEN"), None)
if not xsrf:
    sys.exit(0)

today = date.today()
saturdays = [today + timedelta(days=i) for i in range(15) if (today + timedelta(days=i)).weekday() == 5]

available = []
for sat in saturdays:
    payload = urlencode({"reservationDate": sat.strftime("%Y-%m-%d"), "location": "1"}).encode()
    req = Request(API_URL, data=payload, headers={
        "User-Agent": "Mozilla/5.0",
        "X-XSRF-TOKEN": xsrf,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": PAGE_URL,
    })
    try:
        data = json.loads(opener.open(req, timeout=15).read().decode())
    except Exception:
        continue

    for slot in data.get("times", {}).get(str(THEME_PK), []):
        if slot.get("reservation"):
            continue
        h = int(slot["time"].split(":")[0])
        if START_HOUR <= h < END_HOUR:
            available.append((sat, slot["timeKO"]))

if not available:
    sys.exit(0)

lines = ["🟢 제로월드 홍대 [얼라이브] 토요일 빈자리 발견!"]
prev = None
for sat, tko in available:
    if sat != prev:
        lines.append("\n📅 " + sat.strftime("%m/%d") + "(토)")
        prev = sat
    lines.append("  • " + tko)
lines.append("\n👉 https://zerohongdae.com/reservation/51")
print("\n".join(lines))
