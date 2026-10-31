# 週末去哪玩 🐧 — static site

Live: https://penguin-yeh.github.io/weekend-fun/ · Repo: https://github.com/penguin-yeh/weekend-fun
Local git repo = `site/` (branch `main`, Pages serves repo root; `.nojekyll` present). Push auth = `gh auth git-credential` (box `~/.gitconfig`, gh logged in as penguin-yeh).

## Layout
- `data/YYYY-MM-DD.json` — one weekend (date = Saturday). Same format as `samples/2026-10-31.json` plus per event:
  `url` (活動頁), `slug` (image filename stem, e.g. `2026-11-07-xxx`), optional `image_src` (remote photo URL;
  if omitted, `fetch_images.py` uses the og:image of `url`), `image` (set by fetch_images.py → `img/<slug>.jpg`),
  optional `credit` (e.g. "Wikimedia Commons"), `image_placeholder` (set when a PIL gradient placeholder was drawn).
  Events: `name, city, venue, time, price, free, kind(萬聖節|展覽|市集|美食|音樂表演|藝術祭), hi, pick, sat, sun`.
  Sections: label `台北` → filter 台北; every other label → 其他地方.
- `data/hidden-spots.json` — 私藏清幽景點 (`groups[].spots[]`: name, area, ride, cost, why, caution, ok, url, slug, image_src).
- `fetch_images.py` — downloads each item's photo, resizes to ≤800px JPEG into `site/img/`, falls back to a placeholder.
- `build_site.py` — renders pages + regenerates `index.html` (latest weekend + archive + hidden spots link).
- `weekend_card.py` — the PNG card (separate; same JSON works).

## Weekly routine
```bash
cd /workspace/weekend-fun
# 1. write data/2026-11-07.json (events with url + slug [+ image_src])
python3 fetch_images.py data/2026-11-07.json     # fills "image"; prints placeholders
# 2. eyeball site/img/2026-11-07-*.jpg — never keep a photo of a different place
python3 build_site.py data/2026-11-07.json       # writes site/2026-11-07.html + index.html
cd site && git add -A && git commit -m "weekend 2026-11-07" && git push origin main
# 3. wait ~1 min, then: curl -sI https://penguin-yeh.github.io/weekend-fun/2026-11-07.html
```
`python3 build_site.py` with no args rebuilds every page from `data/`.
`python3 build_site.py --spots data/hidden-spots.json` rebuilds the hidden-spots page.

## 設計（v2，2026-10）
雜誌風 editorial 版面：大封面＋襯線大標題（Noto Serif TC 900 + Fraunces）、紙色底、細線分隔、左右交錯的編號條目（01、02…）、sticky 文字篩選列、捲動淡入（尊重 prefers-reduced-motion）。私藏景點頁用苔綠／石色的安靜配色。
- JSON 可選欄位 `"cover": "<slug>"` 指定封面圖（預設是第一個 ★ 必去）。
- 首頁「最新一期」會自動挑一張橫幅、解析度夠的照片（避免海報放大變糊）。
- v1 舊版樣式備份在 raw/build_site.v1.py。

## 展覽（2026-10-30 起）
- 事件可加的欄位：`date_range`（展期，例如 `"10/1–10/31"`）、`last_day` / `opening`（ISO 日期；剛好落在這個週末時，會自動標上「週六最後一天」或「週日開幕」）、`ticket_url`（加一個「購票 →」連結）。
- `kind: "展覽"` 的事件：當某區有 ≥4 檔展覽、同時也有其他活動時，會分成「活動 / 展覽」兩個小標。篩選列多了「展覽 / 活動」類型 chip。
- 只開週六（或週日公休）的展覽要把 `sun` 設成 `false`，這樣「週日」篩選才會正確。
- 10/31 這一期的 19 檔展覽已經併入 `data/2026-10-31.json`（原始研究檔在 `data/2026-10-31-exhibits.json`，合併前的備份在 `raw/2026-10-31.pre-exhibits.json`）。

## 演唱會登記頁（concerts.html）
- 資料：`data/concerts.json` = `{"updated": "YYYY-MM-DD", "note": "...", "items": [...]}`（也接受舊的純陣列）。
- 每個 item：`artist, name, dates, venue, city, reg_window, sale_time, platform, price, requirements, status ("open" | "soon"), url, slug, image ("img/concert-<slug>.jpg")`，加上：
  - `keydates`: `[{"at": "2026-10-31T13:00", "label": "實名登記抽選截止"}, ...]`（台灣時間）。用來排序（最近的在前）、產生「下一關」標籤、上方時間軸和倒數。已過去的時間點 build 時自動略過，所以每週重跑就會更新。
  - `feature: true`（可選）：封面「Next Deadline」大字顯示這一場的下一個時間點；沒有就用全部裡最近的一個。
- 圖片：放 `raw/concerts/<slug>.jpg`，縮到 ≤800px 存成 `site/img/concert-<slug>.jpg`（同其他圖片的 PIL 設定）。
- 指令：`python3 build_site.py --concerts`（或不帶參數全部重建）。首頁和週末頁導覽都有連結。

## 每週要看的來源（sources to check weekly）
IG／Threads 帳號只拿來找線索，一定要到官方或活動頁確認日期、地點、票價之後才放上網站。
- **@taipei_gan_ma 台北要幹嘛**：https://www.instagram.com/taipei_gan_ma/ （Threads：https://www.threads.net/@taipei_gan_ma）。約 10.6 萬人追蹤。每週四、五發「台北週末活動」清單，主打大型熱門活動（市集、音樂祭、園區大展、遊行），也會發特價、百貨週年慶和小眾樂團。IG 不登入看不到貼文，Threads 不登入可以看到最近大約 10 篇。
- **@taipei.selected 台北精選｜城市提案**：https://www.instagram.com/taipei.selected/ （Threads：https://www.threads.net/@taipei.selected）。約 1 萬人追蹤。偏小眾的免費藝廊展、光影展、品牌快閃和老屋展覽，很對「靜態展覽」的口味。每週也會發週末清單。
- 官方場館頁：華山 huashan1914.com、松菸 songshanculturalpark.org、北美館 tfam.museum、MOCA mocataipei.org.tw、故宮 npm.gov.tw、忠泰美術館、國美館 ntmofa.gov.tw、高美館 kmfa.gov.tw、衛武營 npac-weiwuying.org。
- 展覽活動：南港展覽館 tainex.com.tw、世貿 twtc.com.tw、臺北市政府文化局 culture.gov.taipei、台灣觀光 taiwan.net.tw。
- 演唱會：concert.nericlab.com/month/YYYY-MM（各場開賣日曆）、arena.taipei、KKTIX、ibon、拓元 tixcraft、Ticket Plus。

## 資料欄位補充（免費標記）

- `free: true`：卡片標題列顯示綠框「免費」標籤，「免費」篩選鈕只顯示這些項目。
- `reg_required: true`：免費但要先線上取票或預約，標籤改成「免費・需先取票」。
- `reg_url` / `reg_label`：取票或預約連結（預設文字「免費取票」）。`reg_note` 寫名額、截止日等條件，例如「限量 1,000 張，送完為止」。
- `free_note`：本身要收費、但有免費時段的項目（例如北美館 17:00 後免費），顯示虛線標籤，不會被算進免費篩選。
- `source`：線索來源（例如 `@taipei_gan_ma`）。只有核對過官方頁面才會加上這個項目。
