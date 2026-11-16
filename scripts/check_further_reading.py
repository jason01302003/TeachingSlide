"""檢查點 C3：延伸閱讀的書目查證。每個 DOI 實際向 Crossref 查詢。

執行：python scripts/check_further_reading.py <代號>
"""
from __future__ import annotations

import difflib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from common import RAW_DOIS, WIKI, Report, all_pages, links_in, read_page

FIELDS = ["作者", "年份", "出處", "DOI", "定位", "對應頁面", "推薦理由", "查證"]
UA = "llm-wiki-homework-checker/1.0 (bibliography verification)"


def parse_entries(body: str):
    entries = []
    for part in re.split(r"^### ", body, flags=re.M)[1:]:
        lines = part.splitlines()
        entry = {"title": lines[0].strip(), "raw": part}
        for line in lines[1:]:
            m = re.match(r"-\s*([^：:]+)[：:]\s*(.*)", line)
            if m:
                entry[m.group(1).strip()] = m.group(2).strip()
        entries.append(entry)
    return entries


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def crossref(doi: str) -> dict | None:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)["message"]
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Crossref 連線失敗：{doi}")


def main(deck: str) -> int:
    rep = Report("C3", deck)
    path = WIKI / "further-reading" / f"{deck}.md"
    if not path.exists():
        rep.error(deck, f"找不到 further-reading/{deck}.md")
        return rep.finish()
    pages = all_pages()
    meta, body = read_page(path)
    if meta.get("type") != "external":
        rep.error(deck, "type 必須是 external")
    if "未讀全文" not in body:
        rep.error(deck, "頁面沒有標明「未讀全文」")
    entries = parse_entries(body)
    if not 2 <= len(entries) <= 3:
        rep.error(deck, f"列了 {len(entries)} 篇，應為 2–3 篇")

    # 同一篇外部論文最多出現在兩份簡報
    usage: dict[str, list[str]] = {}
    for other in sorted((WIKI / "further-reading").glob("*.md")):
        for e in parse_entries(read_page(other)[1]):
            usage.setdefault(e.get("DOI", "").lower(), []).append(other.stem)

    seen = set()
    for e in entries:
        where = f"「{e['title'][:40]}」"
        for f in FIELDS:
            if not e.get(f):
                rep.error(where, f"缺少欄位「{f}」")
        doi = e.get("DOI", "").strip().lower()
        if not doi:
            continue
        if not re.fullmatch(r"10\.\d{4,9}/\S+", doi):
            rep.error(where, f"DOI 格式不正確：{doi}")
            continue
        if doi in RAW_DOIS:
            rep.error(where, f"這篇就是 raw/ 裡的 {RAW_DOIS[doi]}，不可列為延伸閱讀")
        if doi in seen:
            rep.error(where, "同一份清單內重複")
        seen.add(doi)
        if len(usage.get(doi, [])) > 2:
            rep.error(where, f"同一篇出現在 {len(usage[doi])} 份簡報（{', '.join(usage[doi])}），上限為 2")
        targets = links_in(e.get("對應頁面", ""))
        if not targets:
            rep.error(where, "「對應頁面」沒有 [[連結]]")
        for t in targets:
            if t not in pages:
                rep.error(where, f"對應頁面 [[{t}]] 不存在")

        msg = crossref(doi)
        time.sleep(0.5)
        if msg is None:
            rep.error(where, f"Crossref 查不到 DOI {doi}")
            continue
        cr_title = (msg.get("title") or [""])[0]
        cr_year = None
        for key in ("published-print", "issued", "published-online"):
            parts = msg.get(key, {}).get("date-parts", [[None]])
            if parts and parts[0] and parts[0][0]:
                cr_year = parts[0][0]
                break
        cr_authors = [a.get("family", "") for a in msg.get("author", [])]
        cr_venue = (msg.get("container-title") or [""])[0]
        ratio = difflib.SequenceMatcher(None, norm(e["title"]), norm(cr_title)).ratio()
        rep.info(f"{doi} → Crossref：{cr_title} / {', '.join(cr_authors)} / {cr_venue} / {cr_year}（標題相似度 {ratio:.2f}）")
        if ratio < 0.9:
            rep.error(where, f"標題與 Crossref 不符：Crossref 為「{cr_title}」")
        year = re.search(r"\d{4}", e.get("年份", ""))
        if year and cr_year:
            diff = abs(int(year.group()) - cr_year)
            if diff > 1:
                rep.error(where, f"年份 {year.group()} 與 Crossref 的 {cr_year} 不符")
            elif diff == 1:
                rep.warn(where, f"年份 {year.group()} 與 Crossref 的 {cr_year} 差一年（可能是線上與紙本出版年不同）")
        if cr_authors:
            first = norm(cr_authors[0])
            if first and first not in norm(e.get("作者", "")):
                rep.error(where, f"第一作者與 Crossref 不符：Crossref 為 {cr_authors[0]}")
        if cr_venue and norm(cr_venue)[:12] not in norm(e.get("出處", "")):
            rep.warn(where, f"期刊名稱與 Crossref 的「{cr_venue}」寫法不同，請確認")
    rep.info(f"{deck}：{len(entries)} 篇")
    return rep.finish()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法：python scripts/check_further_reading.py <代號>")
    sys.exit(main(sys.argv[1]))
