"""檢查點 C4：HTML 簡報檢查（轉換是否忠於簡報稿）。顯示是否正常另外用瀏覽器實際開啟確認。

執行：python scripts/check_slides.py <代號>
"""
from __future__ import annotations

import re
import sys
from urllib.parse import unquote
from html.parser import HTMLParser

from check_further_reading import parse_entries
from check_outline import parse_deck
from common import SLIDES, WIKI, Report, all_pages, read_page

ALLOWED_EXTERNAL = ("https://cdnjs.cloudflare.com/ajax/libs/", "https://doi.org/")
VOID = {"meta", "link", "br", "img", "hr", "input"}


class DeckParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.problems: list[str] = []
        self.slides: list[dict] = []
        self.urls: list[str] = []
        self._in_h2 = self._in_md = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            if a.get(key, "").startswith(("http://", "https://", "//")):
                self.urls.append(a[key])
        if tag == "section" and "slide" in a.get("class", ""):
            self.slides.append({"kind": a.get("data-kind", ""), "wiki": [w for w in a.get("data-wiki", "").split(",") if w],
                                "title": "", "md": "", "footer_links": []})
        if tag == "h2" and self.slides:
            self._in_h2 = True
        if tag == "script" and a.get("type") == "text/markdown":
            self._in_md = True
        if tag == "a" and self.slides and "footer" in self.stack:
            self.slides[-1]["footer_links"].append(a.get("href", ""))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "h2":
            self._in_h2 = False
        if tag == "script":
            self._in_md = False
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.problems.append(f"</{tag}> 沒有對應的開始標籤（目前在 <{self.stack[-1] if self.stack else '無'}> 內）")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()

    def handle_data(self, data):
        if self._in_h2:
            self.slides[-1]["title"] += data
        elif self._in_md:
            self.slides[-1]["md"] += data


def main(deck: str) -> int:
    rep = Report("C4", deck)
    path = SLIDES / f"{deck}.html"
    if not path.exists():
        rep.error(deck, f"找不到 slides/{deck}.html")
        return rep.finish()
    pages = all_pages()
    text = path.read_text(encoding="utf-8")
    parser = DeckParser()
    parser.feed(text)
    for p in parser.problems:
        rep.error(deck, f"HTML 結構：{p}")
    if parser.stack:
        rep.error(deck, f"HTML 結構：標籤沒有關閉 {parser.stack}")

    _, title, slides = parse_deck(deck)
    if len(parser.slides) != len(slides):
        rep.error(deck, f"HTML 有 {len(parser.slides)} 張，簡報稿有 {len(slides)} 張")
    for no, (h, s) in enumerate(zip(parser.slides, slides), 1):
        where = f"第 {no} 張"
        if h["title"].strip() != s["title"]:
            rep.error(where, f"標題不一致：HTML「{h['title'].strip()}」／簡報稿「{s['title']}」")
        if h["kind"] != s["kind"]:
            rep.error(where, f"kind 不一致：{h['kind']}／{s['kind']}")
        if h["wiki"] != s["wiki"]:
            rep.error(where, f"出處不一致：{h['wiki']}／{s['wiki']}")
        for w in h["wiki"]:
            if w not in pages:
                rep.error(where, f"出處 {w} 不存在於 Wiki")
        expected = [f"../wiki.html#{w}" for w in s["wiki"]]
        if h["footer_links"] != expected:
            rep.error(where, "頁尾的出處連結與 data-wiki 不一致")
        if s["kind"] != "further" and h["md"].strip() != s["body"].replace("</script", "<\\/script").strip():
            rep.error(where, "內文與簡報稿不一致（HTML 產生後簡報稿又被修改，或有人手改了 HTML）")

    # 延伸閱讀那張的 DOI 必須與 further-reading 頁一致
    fr = WIKI / "further-reading" / f"{deck}.md"
    if not fr.exists():
        rep.error(deck, f"further-reading/{deck}.md 不存在")
    elif parser.slides:
        want = sorted(e.get("DOI", "").lower() for e in parse_entries(read_page(fr)[1]))
        got = sorted(unquote(d).lower() for d in re.findall(r"https://doi\.org/(10\.[^)\s]+)", parser.slides[-1]["md"]))
        if want != got:
            rep.error("延伸閱讀", f"DOI 與 further-reading 頁不一致：投影片 {got}／Wiki {want}")
        if "未讀全文" not in parser.slides[-1]["md"]:
            rep.error("延伸閱讀", "沒有標明「未讀全文」")
        rep.info(f"延伸閱讀 {len(got)} 篇")

    all_urls = parser.urls + re.findall(r"\]\((https?://[^)\s]+)\)", text)
    for url in sorted(set(all_urls)):
        if not url.startswith(ALLOWED_EXTERNAL):
            rep.error(deck, f"不允許的外部連結：{url}")
    rep.info(f"{len(parser.slides)} 張；外部連結 {len(set(all_urls))} 個")
    return rep.finish()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法：python scripts/check_slides.py <代號>")
    sys.exit(main(sys.argv[1]))
