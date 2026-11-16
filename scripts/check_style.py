"""檢查風格是否維持單一來源（CLAUDE.md 第 7.1 節）。

規則：
1. 色票與字體只能定義在 slides/assets/base.css；deck.css 與 build_viewer.py 的樣式不可出現色碼或字體名稱。
2. 圖表色盤只能定義在 slides/assets/render.js 的 PALETTE。
3. wiki.html 必須逐字內嵌目前的 base.css（base.css 改了卻沒重新產生 wiki.html 會被抓到）。
4. 每份簡報與入口頁都要連結 assets/base.css，且在 deck.css 之前。
5. 簡報與入口頁不可有 <style> 區塊或 style="" 屬性。

執行：python scripts/check_style.py
"""
from __future__ import annotations

import re
import sys

from common import ROOT, SLIDES, Report

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
FONT = re.compile(r"(Noto Sans|JhengHei|PingFang|Consolas|Cascadia|font-family\s*:\s*[^;]*\b(serif|sans-serif|monospace)\b)")


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def main() -> int:
    rep = Report("C5", "style")
    base = (SLIDES / "assets" / "base.css").read_text(encoding="utf-8")

    deck = strip_comments((SLIDES / "assets" / "deck.css").read_text(encoding="utf-8"))
    viewer_src = (ROOT / "scripts" / "build_viewer.py").read_text(encoding="utf-8")
    m = re.search(r'CSS = """(.*?)"""', viewer_src, flags=re.S)
    viewer = strip_comments(m.group(1)) if m else ""
    if not m:
        rep.error("build_viewer.py", "找不到 CSS 區塊")
    for name, css in (("deck.css", deck), ("build_viewer.py 的 CSS", viewer)):
        for hit in sorted(set(HEX.findall(css))):
            rep.error(name, f"出現色碼 {hit}；顏色只能寫在 base.css 的變數中")
        for hit in FONT.findall(css):
            rep.error(name, f"出現字體定義 {hit[0]!r}；字體只能寫在 base.css")

    # wiki.html 內嵌的 base.css
    wiki = (ROOT / "wiki.html").read_text(encoding="utf-8") if (ROOT / "wiki.html").exists() else ""
    if base.strip() not in wiki:
        rep.error("wiki.html", "沒有內嵌目前的 base.css（請重新執行 scripts/build_viewer.py）")

    # 簡報與入口頁
    pages = sorted(SLIDES.glob("*.html"))
    for page in pages:
        text = page.read_text(encoding="utf-8")
        a, b = text.find("assets/base.css"), text.find("assets/deck.css")
        if a == -1 or b == -1 or a > b:
            rep.error(page.name, "必須先連結 assets/base.css、再連結 assets/deck.css")
        if re.search(r"<style[\s>]", text) or re.search(r'\sstyle\s*=', text):
            rep.error(page.name, "不可有 <style> 區塊或 style 屬性")

    # 色盤只在 render.js
    for path in list(SLIDES.glob("assets/*.js")):
        if path.name != "render.js" and HEX.search(path.read_text(encoding="utf-8")):
            rep.error(path.name, "出現色碼；圖表色盤只能寫在 render.js 的 PALETTE")

    rep.info(f"base.css {len(base.splitlines())} 行；檢查 deck.css、build_viewer.py 的 CSS、wiki.html、{len(pages)} 個簡報頁面")
    return rep.finish()


if __name__ == "__main__":
    sys.exit(main())
