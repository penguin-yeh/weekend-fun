#!/usr/bin/env bash
# 把某個 claude/* 分支上「最新一週」的頁面同步進目前所在的分支（main）。
# 用法：scripts/sync_latest.sh <來源分支名>
# 搬：最新的 YYYY-MM-DD.html、index.html、對應的 data/YYYY-MM-DD.json，
# 以及該週所有 img/YYYY-MM-DD-*.jpg（週末活動照片）。
# 不搬 build_site.py／fetch_images.py 等程式（那些要走正常 review）。來源日期比 main 舊就略過。
set -euo pipefail
BRANCH="${1:?usage: sync_latest.sh <source-branch>}"
SRC="origin/${BRANCH}"

newest() { git ls-tree -r --name-only "$1" | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}\.html$' | sort | tail -1 || true; }

src_latest="$(newest "$SRC")"
main_latest="$(newest HEAD)"
if [ -z "$src_latest" ]; then echo "來源分支沒有日期頁面，略過"; exit 0; fi
if [ -n "$main_latest" ] && [[ "$src_latest" < "$main_latest" ]]; then
  echo "來源最新 $src_latest 比 main 的 $main_latest 舊，略過"; exit 0
fi

date="${src_latest%.html}"
paths=("$src_latest")
for p in index.html "data/${date}.json"; do
  if git cat-file -e "${SRC}:${p}" 2>/dev/null; then paths+=("$p"); fi
done
# 該週對應的圖片：img/<date>-*.jpg
while IFS= read -r img; do
  [ -n "$img" ] && paths+=("$img")
done < <(git ls-tree -r --name-only "$SRC" | grep -E "^img/${date}-.*\.jpg$" || true)

git checkout "$SRC" -- "${paths[@]}"
git add -- "${paths[@]}"
if git diff --cached --quiet; then echo "沒有變更"; exit 0; fi
git -c user.name="github-actions[bot]" -c user.email="41898282+github-actions[bot]@users.noreply.github.com" \
  commit -q -m "Sync ${date} from ${BRANCH}"
echo "synced ${date}"
