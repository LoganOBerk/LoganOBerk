#!/usr/bin/env python3
"""Generate static SVG stat cards from the GitHub REST + GraphQL APIs.

Stdlib only. Writes assets/{stats,top-langs,streak,activity}.svg.
If any API call fails after retries the script exits non-zero BEFORE writing
anything, so the previously committed SVGs stay in place (nothing ever 404s).
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.request
from html import escape
from pathlib import Path

LOGIN = os.environ.get("PROFILE_LOGIN", "LoganOBerk")
TOKEN = os.environ.get("METRICS_TOKEN") or os.environ.get("GITHUB_TOKEN")
OUT = Path(os.environ.get("OUT_DIR", "assets"))

BG, BORDER, TEXT, MUTED = "#0d1117", "#30363d", "#c9d1d9", "#8b949e"
CYAN, PINK, PURPLE, ORANGE = "#00FFD1", "#FF2D78", "#BF5AF2", "#FF9500"
FONT = "font-family:'Segoe UI',Ubuntu,Helvetica,Arial,sans-serif"


# ---------- API helpers ----------
def _request(url, data=None):
    headers = {"User-Agent": "profile-stats", "Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # network, 5xx, rate limit
            last = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"GitHub API failed: {url}: {last}")


def rest(path):
    return _request(f"https://api.github.com{path}")


def gql(query, variables):
    d = _request("https://api.github.com/graphql",
                 json.dumps({"query": query, "variables": variables}).encode())
    if d.get("errors"):
        raise RuntimeError(d["errors"])
    return d["data"]


MAIN_Q = """
query($login:String!){ user(login:$login){
  followers{totalCount}
  repositories(ownerAffiliations:OWNER,isFork:false,first:100,privacy:PUBLIC){
    totalCount
    nodes{ name stargazerCount forkCount
      languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}} } }
  contributionsCollection{
    totalCommitContributions totalPullRequestContributions
    totalIssueContributions totalPullRequestReviewContributions } } }"""

YEAR_Q = """
query($login:String!,$from:DateTime!,$to:DateTime!){ user(login:$login){
  contributionsCollection(from:$from,to:$to){ contributionCalendar{
    totalContributions weeks{contributionDays{date contributionCount}} } } } }"""


def collect():
    profile = rest(f"/users/{LOGIN}")
    user = gql(MAIN_Q, {"login": LOGIN})["user"]

    created = dt.datetime.fromisoformat(profile["created_at"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    days = {}
    for year in range(created.year, now.year + 1):
        start = max(created, dt.datetime(year, 1, 1, tzinfo=dt.timezone.utc))
        end = min(now, dt.datetime(year, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc))
        cal = gql(YEAR_Q, {"login": LOGIN, "from": start.isoformat(), "to": end.isoformat()})
        for w in cal["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]

    langs = {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            n = e["node"]["name"]
            cur = langs.get(n, [0, e["node"]["color"] or MUTED])
            cur[0] += e["size"]
            langs[n] = cur

    cc = user["contributionsCollection"]
    repos = user["repositories"]
    return {
        "days": days,
        "langs": langs,
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "issues": cc["totalIssueContributions"],
        "reviews": cc["totalPullRequestReviewContributions"],
        "stars": sum(r["stargazerCount"] for r in repos["nodes"]),
        "forks": sum(r["forkCount"] for r in repos["nodes"]),
        "repos": profile["public_repos"],
        "followers": user["followers"]["totalCount"],
        "since": created.year,
    }


# ---------- calculations ----------
def streaks(days):
    ordered = sorted(days)
    longest = run = 0
    prev = None
    for d in ordered:
        date = dt.date.fromisoformat(d)
        if days[d] > 0:
            run = run + 1 if prev and (date - prev).days == 1 and days[prev.isoformat()] > 0 else 1
            longest = max(longest, run)
        else:
            run = 0
        prev = date
    today = dt.datetime.now(dt.timezone.utc).date()
    cursor = today if days.get(today.isoformat(), 0) > 0 else today - dt.timedelta(days=1)
    current = 0
    while days.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= dt.timedelta(days=1)
    return current, longest


# ---------- SVG rendering ----------
def card(w, h, title, body, title_color=CYAN):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<rect x=".5" y=".5" rx="16" width="{w-1}" height="{h-1}" fill="{BG}" stroke="{BORDER}"/>'
            f'<text x="25" y="35" style="{FONT};font-size:18px;font-weight:600" fill="{title_color}">{escape(title)}</text>'
            f'{body}</svg>')


def stats_svg(s):
    total = sum(s["days"].values())
    rows = [("Total Contributions", total, CYAN), ("Commits (last 12 mo)", s["commits"], PINK),
            ("Pull Requests", s["prs"], PURPLE), ("Issues", s["issues"], ORANGE),
            ("PR Reviews", s["reviews"], CYAN), ("Public Repos", s["repos"], PINK),
            ("Stars Earned", s["stars"], PURPLE), ("Followers", s["followers"], ORANGE)]
    body = ""
    for i, (label, val, color) in enumerate(rows):
        y = 70 + i * 25
        body += (f'<circle cx="32" cy="{y-5}" r="5" fill="{color}"/>'
                 f'<text x="48" y="{y}" style="{FONT};font-size:14px" fill="{TEXT}">{label}</text>'
                 f'<text x="440" y="{y}" text-anchor="end" style="{FONT};font-size:14px;font-weight:700" fill="{TEXT}">{val:,}</text>')
    return card(467, 280, f"{LOGIN}'s GitHub Stats", body)


def langs_svg(s):
    top = sorted(s["langs"].items(), key=lambda kv: kv[1][0], reverse=True)[:6]
    total = sum(v[0] for _, v in top) or 1
    body, x = "", 25.0
    bar_w = 417
    body += '<clipPath id="c"><rect x="25" y="52" width="417" height="10" rx="5"/></clipPath><g clip-path="url(#c)">'
    for _, (size, color) in top:
        w = bar_w * size / total
        body += f'<rect x="{x:.2f}" y="52" width="{w:.2f}" height="10" fill="{color}"/>'
        x += w
    body += "</g>"
    for i, (name, (size, color)) in enumerate(top):
        cx, cy = 25 + (i % 2) * 210, 95 + (i // 2) * 28
        body += (f'<circle cx="{cx+5}" cy="{cy-5}" r="5" fill="{color}"/>'
                 f'<text x="{cx+18}" y="{cy}" style="{FONT};font-size:13px" fill="{TEXT}">{escape(name)} '
                 f'<tspan fill="{MUTED}">{size*100/total:.1f}%</tspan></text>')
    return card(467, 190, "Most Used Languages", body, PURPLE)


def streak_svg(s):
    cur, longest = streaks(s["days"])
    total = sum(s["days"].values())
    cols = [(f"{total:,}", "Total Contributions", f"since {s['since']}", CYAN),
            (str(cur), "Current Streak", "days", PINK),
            (str(longest), "Longest Streak", "days", ORANGE)]
    body = ""
    for i, (big, label, sub, color) in enumerate(cols):
        cx = 83 + i * 165
        body += (f'<text x="{cx}" y="85" text-anchor="middle" style="{FONT};font-size:32px;font-weight:700" fill="{color}">{big}</text>'
                 f'<text x="{cx}" y="112" text-anchor="middle" style="{FONT};font-size:14px" fill="{TEXT}">{label}</text>'
                 f'<text x="{cx}" y="132" text-anchor="middle" style="{FONT};font-size:12px" fill="{MUTED}">{sub}</text>')
        if i:
            body += f'<line x1="{cx-82}" y1="55" x2="{cx-82}" y2="140" stroke="{BORDER}"/>'
    return card(495, 165, "Contribution Streak", body)


def activity_svg(s):
    today = dt.datetime.now(dt.timezone.utc).date()
    series = [(today - dt.timedelta(days=i)) for i in range(29, -1, -1)]
    vals = [s["days"].get(d.isoformat(), 0) for d in series]
    peak = max(max(vals), 1)
    x0, x1, y0, y1 = 45, 780, 60, 210
    pts = [(x0 + i * (x1 - x0) / 29, y1 - v / peak * (y1 - y0)) for i, v in enumerate(vals)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{x0},{y1} {line} {x1},{y1}"
    body = f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient></defs>'
    for frac in (0, .5, 1):
        gy = y1 - frac * (y1 - y0)
        body += (f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{BORDER}" stroke-dasharray="3"/>'
                 f'<text x="{x0-8}" y="{gy+4:.1f}" text-anchor="end" style="{FONT};font-size:11px" fill="{MUTED}">{round(peak*frac)}</text>')
    body += f'<polygon points="{area}" fill="url(#g)"/><polyline points="{line}" fill="none" stroke="{CYAN}" stroke-width="2.5" stroke-linejoin="round"/>'
    for (x, y), v in zip(pts, vals):
        if v:
            body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{PINK}"/>'
    for i in (0, 7, 14, 21, 29):
        body += f'<text x="{pts[i][0]:.1f}" y="232" text-anchor="middle" style="{FONT};font-size:11px" fill="{MUTED}">{series[i].strftime("%b %d")}</text>'
    return card(825, 250, "Contributions · Last 30 Days", body)


def main():
    if not TOKEN:
        sys.exit("No GITHUB_TOKEN / METRICS_TOKEN provided")
    data = collect()
    rendered = {"stats.svg": stats_svg(data), "top-langs.svg": langs_svg(data),
                "streak.svg": streak_svg(data), "activity.svg": activity_svg(data)}
    OUT.mkdir(parents=True, exist_ok=True)
    for name, svg in rendered.items():  # write only after everything succeeded
        (OUT / name).write_text(svg, encoding="utf-8")
    print("Wrote", ", ".join(rendered))


if __name__ == "__main__":
    main()
