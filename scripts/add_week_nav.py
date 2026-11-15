#!/usr/bin/env python3
"""add_week_nav.py — 幫每一期週末頁面（YYYY-MM-DD.html，日期為週六）與 index.html 加上「上一週／週數選單／下一週」。

用法：python3 scripts/add_week_nav.py      （在 repo 根目錄執行；冪等，可重複執行）

- 導覽列用 <!--weeknav-->…<!--/weeknav--> 標記，重跑只會替換標記內的內容。
- 插在封面 </header> 之後、<main> 之前；樣式全部行內，顏色取頁面既有的 CSS 變數（附預設值）。
- index.html 視為「最新一期」的入口，選單選到最新一期、下一週停用。
- 翻週用一般連結、週數選單用行內 onchange，不需要額外 <script>。
- 每次產生新一期頁面後都要執行；sync-main.yml 也會自動補跑。
"""
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})\.html$")
START, END = "<!--weeknav-->", "<!--/weeknav-->"
SANS = "'Noto Sans TC',-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei',sans-serif"
NUM = "Fraunces,'Noto Serif TC',serif"


def span(d: str) -> str:
    sat = datetime.strptime(d, "%Y-%m-%d")
    sun = sat + timedelta(days=1)
    return f"{sat.month}.{sat.day:02d} — {sun.month}.{sun.day:02d}"


def btn(href, text, on):
    base = ("display:inline-block;padding:8px 14px;border:1px solid var(--rule,#d9d0c1);border-radius:999px;"
            f"font:500 .86rem {SANS};text-decoration:none;")
    if on:
        return f'<a href="{href}" style="{base}color:var(--ink,#1b1916)">{text}</a>'
    return f'<span style="{base}color:var(--mute,#7b746a);opacity:.4">{text}</span>'


def block(dates, cur):
    i = dates.index(cur)                      # dates 為新到舊
    older = dates[i + 1] if i + 1 < len(dates) else None
    newer = dates[i - 1] if i > 0 else None
    n = len(dates) - i
    opts = "".join(
        f'<option value="{d}.html"{" selected" if d == cur else ""}>{span(d)}</option>' for d in dates
    )
    sel = (f'<select aria-label="切換週數" onchange="location.href=this.value" '
           f'style="font:600 .95rem {NUM};color:var(--ink,#1b1916);background:var(--paper,#f5f0e6);'
           f'border:1px solid var(--rule,#d9d0c1);border-radius:999px;padding:8px 14px;min-width:10.5em">{opts}</select>')
    label = (f'<span style="font:500 .68rem {SANS};letter-spacing:.22em;text-transform:uppercase;'
             f'color:var(--mute,#7b746a)">Issue {n:02d} / {len(dates):02d}</span>')
    return (
        f'{START}<div style="border-bottom:1px solid var(--rule,#d9d0c1);background:var(--paper,#f5f0e6)">'
        f'<div style="max-width:1180px;margin:0 auto;padding:12px clamp(20px,5vw,56px);display:flex;'
        f'flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between">'
        f'{btn(older + ".html", "← 上一週", True) if older else btn("", "← 上一週", False)}'
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px">{label}{sel}</div>'
        f'{btn(newer + ".html", "下一週 →", True) if newer else btn("", "下一週 →", False)}'
        f'</div></div>{END}'
    )


def apply(path: Path, dates, cur) -> bool:
    s = original = path.read_text(encoding="utf-8")
    s = re.sub(re.escape(START) + r".*?" + re.escape(END), "", s, flags=re.S)
    m = re.search(r"</header>", s)
    if not m:
        return False
    s = s[: m.end()] + block(dates, cur) + s[m.end():]
    if s == original:
        return False
    path.write_text(s, encoding="utf-8")
    return True


def main() -> None:
    dates = sorted((m.group(1) for f in ROOT.iterdir() if (m := DATED.match(f.name))), reverse=True)
    if not dates:
        print("no dated pages"); return
    changed = [f"{d}.html" for d in dates if apply(ROOT / f"{d}.html", dates, d)]
    idx = ROOT / "index.html"
    if idx.exists() and apply(idx, dates, dates[0]):
        changed.append("index.html")
    print("updated:", ", ".join(changed) or "(none)")


if __name__ == "__main__":
    sys.exit(main())
