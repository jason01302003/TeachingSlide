"""節點 N6：把簡報稿（wiki/queries/slides-<代號>.md）轉成 HTML 簡報。內容不經模型重寫。

執行：python scripts/build_slides.py <代號>|all
"""
from __future__ import annotations

import html
import sys

from check_further_reading import parse_entries
from check_outline import parse_deck
from common import SLIDES, WIKI, all_pages, read_page

CDN = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>"""

KIND_LABEL = {"title": "", "motivation": "為什麼要關心", "background": "背景知識", "definition": "問題定義",
              "example": "例子", "result": "主要結果", "method": "方法", "caveat": "注意", "recap": "回顧",
              "further": "延伸閱讀"}
DECK_ORDER = ["ejor2009", "do2006", "josh2010", "josh2016", "tswj2014"]


def page_title(pid: str, pages) -> str:
    return read_page(pages[pid])[0].get("title", pid) if pid in pages else pid


def further_markdown(deck: str) -> str:
    """延伸閱讀那一張的內容直接由 further-reading 頁產生，不另外手寫。"""
    path = WIKI / "further-reading" / f"{deck}.md"
    if not path.exists():
        return "（延伸閱讀尚未建立）"
    out = ["> 以下為 Wiki 以外的資料，依書目與摘要推薦，未讀全文。", ""]
    for e in parse_entries(read_page(path)[1]):
        doi = e.get("DOI", "")
        out.append(f"**{e['title']}**  ")
        out.append(f"{e.get('作者', '')}（{e.get('年份', '')}）．*{e.get('出處', '')}*．[doi:{doi}](https://doi.org/{doi.replace('(', '%28').replace(')', '%29')})  ")
        out.append(f"〔{e.get('定位', '')}〕{e.get('推薦理由', '')}")
        out.append("")
    return "\n".join(out)


def build(deck: str) -> str:
    pages = all_pages()
    meta, title, slides = parse_deck(deck)
    sections = []
    for no, s in enumerate(slides, 1):
        body = further_markdown(deck) if s["kind"] == "further" else s["body"]
        body = body.replace("</script", "<\\/script")
        refs = " · ".join(
            f'<a href="../wiki.html#{html.escape(w)}" target="wiki">{html.escape(page_title(w, pages))}</a>' for w in s["wiki"])
        label = KIND_LABEL.get(s["kind"], "")
        sections.append(f"""<section class="slide" data-kind="{html.escape(s['kind'])}" data-wiki="{html.escape(','.join(s['wiki']))}">
<header><span class="kind">{html.escape(label)}</span><h2>{html.escape(s['title'])}</h2></header>
<div class="body"><script type="text/markdown">
{body}
</script></div>
<footer><span class="src">出處：Wiki › {refs}</span><span class="no">{no} / {len(slides)}</span></footer>
</section>""")
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="assets/deck.css">
{CDN}
</head>
<body class="deck" data-deck="{html.escape(deck)}">
<div id="stage">
{chr(10).join(sections)}
</div>
<nav id="bar"><a href="index.html" title="回簡報入口">☰</a><button id="prev" aria-label="上一張">‹</button><div id="progress"><i></i></div><button id="next" aria-label="下一張">›</button></nav>
<script src="assets/render.js"></script>
<script src="assets/deck.js"></script>
</body>
</html>
"""


def build_index(decks: list[str]) -> str:
    cards = []
    for i, deck in enumerate(decks, 1):
        meta, title, slides = parse_deck(deck)
        src_meta, _ = read_page(WIKI / "sources" / f"{deck}.md")
        branch = "另一個分支：雙代理人排程" if deck == "tswj2014" else "Relocation problem"
        cards.append(f"""<a class="card" href="{deck}.html"><span class="step">{i}</span>
<small>{html.escape(branch)}</small><h2>{html.escape(title)}</h2>
<p>{html.escape(meta.get('summary', ''))}</p>
<em>{html.escape(src_meta.get('citation', src_meta.get('title', '')))} · {len(slides)} 張</em></a>""")
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Relocation Problem 是什麼？五篇排程論文導讀</title>
<link rel="stylesheet" href="assets/deck.css">
</head>
<body class="hub">
<main>
<p class="eyebrow">排程論文 LLM Wiki · 教學簡報</p>
<h1>Relocation Problem 是什麼？</h1>
<p class="lead">五篇論文各一份簡報，內容全部來自 <a href="../wiki.html">LLM Wiki</a>。建議依下列順序閱讀：先看 relocation problem 與 Johnson's rule 的關係，再看多個工作隊、加權完工時間與固定順序三個延伸；最後一份是 Wiki 裡的另一個分支。</p>
<div class="cards">
{chr(10).join(cards)}
</div>
<p class="note">每張投影片頁尾的「出處」可以點回 Wiki 對應的頁面。每份簡報最後一張是延伸閱讀，列的是 Wiki 以外的論文。</p>
</main>
</body>
</html>
"""


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    existing = [d for d in DECK_ORDER if (WIKI / "queries" / f"slides-{d}.md").exists()]
    targets = existing if arg == "all" else [arg]
    SLIDES.mkdir(exist_ok=True)
    for deck in targets:
        (SLIDES / f"{deck}.html").write_text(build(deck), encoding="utf-8")
        print(f"已產生 slides/{deck}.html")
    (SLIDES / "index.html").write_text(build_index(existing), encoding="utf-8")
    print(f"已產生 slides/index.html（{len(existing)} 份）")
