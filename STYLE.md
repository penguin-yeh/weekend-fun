# weekend-fun 頁面風格規範（雜誌風 editorial，v2／2026-10）

> 給負責產生本 repo 頁面的 bot：**每次用 `build_site.py`／`fetch_images.py` 產生或更新頁面之前，先讀完這份文件。**
> 這份文件是把 `README.md` 裡「設計（v2，2026-10）」一節的實際規則抽出來成獨立檔案，方便跟其他 repo 的
> `STYLE.md` 一致地被讀取；完整的資料欄位說明仍以 `README.md` 為準。

## 0. 硬性規則

1. 不要手改 `*.html`／`img/`：所有頁面都是 `build_site.py` 從 `data/*.json` 算出來的，手改會在下次重跑時被覆蓋，改法請改 `data/*.json` 再重跑腳本。
2. 圖片只能是 `fetch_images.py` 抓到的真實活動照（或 PIL 畫的灰階佔位圖，由 `image_placeholder` 標記），不可以手動塞一張不相關的圖片。
3. 展覽/活動卡片的 `sun`／`sat` 欄位要對應真實開放日期，不可以憑空假設。
4. 全部文字用繁體中文；連結、日期、地點要跟活動官方頁一致，不可編造。
5. 每個會被送到 GitHub Pages 的 HTML（含 `index.html`、週六日期頁、`concerts.html`、`hidden-spots.html`）的 `<head>` 在 `</title>` 之後必須有本站 favicon 這四行，並且**不要再輸出**原來那行企鵝 data-uri icon。`build_site.py` 產生頁面時也要這樣寫，否則下次重跑會把 icon 蓋掉：

```html
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="site.webmanifest">
```

## 1. 設計 token（色票與字型，取自 `index.html` 實際 CSS）

| 用途 | 值 |
|---|---|
| 紙色底 | `--paper: #f5f0e6` |
| 主文字／墨色 | `--ink: #1b1916` |
| 次要文字 | `--mute: #7b746a` |
| 分隔線 | `--rule: #d9d0c1` |
| 強調色 | `--acc: #d9481c` |
| 無襯線字體 | `"Noto Sans TC", -apple-system, BlinkMacSystemFont, "PingFang TC", "Microsoft JhengHei", sans-serif` |
| 襯線大標 | `"Noto Serif TC", "Songti TC", serif`（搭配 `Fraunces` 做數字／拉丁字） |

## 2. 版面語言

- 大封面（`.cover`）＋襯線超大標題，左下角漸層遮罩壓文字。
- 左右交錯、編號條目（01、02…）的 editorial 排版，不是對稱卡片網格。
- sticky 文字篩選列（類型、免費、台北／其他地方）。
- 捲動淡入動畫，**必須尊重 `prefers-reduced-motion`**。
- 私藏景點頁（`hidden-spots.html`）用苔綠／石色的安靜配色，跟主頁的暖紙色＋磚紅調區分開。

## 3. 圖片規則

- 封面圖優先取 `data/*.json` 裡 `cover` 指定的 `slug`；沒指定就用第一個 ★ 必去。
- 首頁「最新一期」自動挑一張橫幅、解析度夠的照片，避免海報圖放大變糊。
- 抓不到真實照片時 `fetch_images.py` 會畫 PIL 灰階佔位圖並標記 `image_placeholder`——**不要**手動換成隨便一張網路圖片去蓋掉佔位狀態，要去源頭補 `image_src` 再重跑腳本。

## 4. 執行方式

照 `README.md`「Weekly routine」：

```bash
python3 fetch_images.py data/YYYY-MM-DD.json
python3 build_site.py data/YYYY-MM-DD.json
git add -A && git commit -m "weekend YYYY-MM-DD" && git push origin main
```

資料欄位、`concerts.html`／`hidden-spots.html` 的欄位細節，見 `README.md`。

## 週數切換（必備）

每個 `YYYY-MM-DD.html`（週六日期）與 `index.html` 的封面 `</header>` 之後必須有「← 上一週／週數選單／下一週 →」。**不要手寫、不要改 `build_site.py` 去輸出它**：頁面產生後執行 `python3 scripts/add_week_nav.py`，它用 `<!--weeknav-->…<!--/weeknav-->` 標記插入或更新（行內樣式、顏色取 `--paper／--ink／--rule／--mute` 變數）。不准手改標記內的內容。
