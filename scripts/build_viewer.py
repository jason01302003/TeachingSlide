"""把 wiki/ 的 Markdown 打包成單一檔案的瀏覽頁 wiki.html。Markdown 才是內容來源，wiki.html 不手改。

執行：python scripts/build_viewer.py
"""
from __future__ import annotations

import json
import sys

from common import ROOT, SLIDES, all_pages, links_in, read_page

TYPE_LABEL = [("overview", "總覽"), ("source", "來源（論文）"), ("concept", "概念"), ("algorithm", "演算法"),
              ("comparison", "跨論文比較"), ("query", "查詢回答與簡報稿"), ("external", "延伸閱讀（外部資料）")]

CSS = """
/* wiki.html 專用的版面；色票、字體與共用元件由 slides/assets/base.css 提供（見 CLAUDE.md 第 7.1 節） */
#app{display:grid;grid-template-columns:300px minmax(0,1fr);min-height:100vh}
aside{border-right:1px solid var(--line);padding:20px 16px;position:sticky;top:0;height:100vh;overflow:auto}
aside h1{font-size:19px;margin:0 0 4px}aside .sub{font-size:13px;color:var(--muted);margin:0 0 14px;line-height:1.6}
#q{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font:inherit;font-size:14px}
aside h2{font-size:12px;letter-spacing:.08em;color:var(--muted);margin:18px 0 6px}
aside ul{list-style:none;margin:0;padding:0}aside li a{display:block;padding:5px 8px;border-radius:6px;text-decoration:none;color:var(--ink);font-size:14.5px;line-height:1.4}
aside li a:hover{background:var(--accent-soft)}aside li a.on{background:var(--accent);color:var(--card)}
aside .tools a{display:inline-block;margin:0 10px 6px 0;font-size:14px}
main{padding:36px clamp(16px,5vw,64px) 80px;max-width:940px}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 6px;font-size:13px}
.pill{border:1px solid var(--line);border-radius:999px;padding:2px 10px;color:var(--muted)}
.pill.type{background:var(--accent-soft);color:var(--accent);border-color:transparent;font-weight:700}
.pill.draft{color:var(--warn);border-color:var(--warn)}
main h1{font-size:clamp(26px,4vw,36px);margin:.2em 0 .6em;text-wrap:balance}
article{--cite-size:.72em;--table-size:.92em;--caption-size:.85em;font-size:17px;line-height:1.8}article h1{display:none}
article h2{font-size:22px;margin:1.7em 0 .5em;padding-bottom:.25em;border-bottom:1px solid var(--line)}article h3{font-size:18px;margin:1.3em 0 .4em}
article li{margin:.25em 0}
blockquote{margin:.8em 0}
.tablewrap{margin:.8em 0}
figure{margin:1em 0}
.back{margin-top:48px;padding-top:16px;border-top:1px solid var(--line);font-size:14.5px;color:var(--muted)}
.back a{margin-right:12px;white-space:nowrap}
.slidemeta{font-size:13px;color:var(--muted);margin:-.3em 0 .6em}
@media (max-width:820px){#app{grid-template-columns:1fr}aside{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)}}
"""

JS = """
const DATA = JSON.parse(document.getElementById('wiki-data').textContent);
const titleOf = id => (DATA.pages[id] && DATA.pages[id].meta.title) || id;
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function nav(filter) {
  const f = (filter || '').toLowerCase();
  let html = '';
  for (const [type, label] of DATA.groups) {
    const ids = Object.keys(DATA.pages).filter(id => DATA.pages[id].meta.type === type &&
      (!f || (titleOf(id) + id + DATA.pages[id].body).toLowerCase().includes(f)));
    if (!ids.length) continue;
    html += `<h2>${label}（${ids.length}）</h2><ul>` + ids.map(id => `<li><a href="#${id}" data-id="${id}">${esc(titleOf(id))}</a></li>`).join('') + '</ul>';
  }
  document.getElementById('nav').innerHTML = html || '<p class="sub">找不到符合的頁面</p>';
  mark();
}
function mark() {
  const id = current();
  document.querySelectorAll('#nav a').forEach(a => a.classList.toggle('on', a.dataset.id === id));
}
const current = () => decodeURIComponent(location.hash.slice(1)) || 'overview';
function show() {
  const id = current(), page = DATA.pages[id], main = document.querySelector('main');
  if (!page) { main.innerHTML = `<h1>找不到頁面</h1><p>${esc(id)}</p>`; return; }
  const m = page.meta;
  let body = page.body;
  if (m.type === 'query' && m.deck) {   // 簡報稿：把 kind:: / wiki:: 兩行顯示成小字
    body = body.replace(/^kind:: *(.*)\\nwiki:: *(.*)$/gm, (x, kind, wiki) => `<p class="slidemeta">教學角色：${kind}　出處：${wiki}</p>`);
  }
  const pills = [];
  if (m.type) pills.push(`<span class="pill type">${esc((DATA.groups.find(g => g[0] === m.type) || [,m.type])[1])}</span>`);
  if (m.status) pills.push(`<span class="pill ${m.status === '已確認' ? '' : 'draft'}">${esc(m.status)}</span>`);
  (m.sources || []).forEach(s => pills.push(`<a class="pill" href="#sources/${s.toLowerCase()}">${esc(s)}</a>`));
  if (m.updated) pills.push(`<span class="pill">更新 ${esc(m.updated)}</span>`);
  if (m.deck) pills.push(`<a class="pill" href="slides/${esc(m.deck)}.html" target="_blank">開啟這份簡報 ↗</a>`);
  const back = (DATA.backlinks[id] || []).map(b => `<a href="#${b}">${esc(titleOf(b))}</a>`).join('');
  main.innerHTML = `<div class="meta">${pills.join('')}</div><h1>${esc(m.title || id)}</h1><article>` +
    renderMarkdown(body, { link: t => '#' + t, title: titleOf, cite: s => '#sources/' + s.toLowerCase() }) +
    `</article>` + (back ? `<div class="back">連到這一頁的頁面：<br>${back}</div>` : '');
  document.title = (m.title || id) + '｜排程論文 LLM Wiki';
  mark(); window.scrollTo(0, 0);
}
document.getElementById('q').addEventListener('input', e => nav(e.target.value));
window.addEventListener('hashchange', show);
nav(''); show();
"""


def main() -> None:
    pages = all_pages()
    data = {"pages": {}, "backlinks": {}, "groups": TYPE_LABEL + [("導覽", "導覽檔")]}
    for pid, path in pages.items():
        meta, body = read_page(path)
        if not meta:
            meta = {"title": {"index": "index（內容目錄）", "log": "log（操作紀錄）"}.get(pid, pid), "type": "導覽"}
        data["pages"][pid] = {"meta": meta, "body": body}
    for pid, page in data["pages"].items():
        for target in links_in(page["body"]):
            if target in pages and target != pid and pid not in data["backlinks"].setdefault(target, []):
                data["backlinks"][target].append(pid)
    render_js = (SLIDES / "assets" / "render.js").read_text(encoding="utf-8")
    base_css = (SLIDES / "assets" / "base.css").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>排程論文 LLM Wiki</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
<style>
{base_css}
</style>
<style>{CSS}</style>
</head>
<body>
<div id="app">
<aside>
<h1>排程論文 LLM Wiki</h1>
<p class="sub">五篇論文、{len(pages)} 個頁面。內容由 AI 依 CLAUDE.md 的規則撰寫與維護。</p>
<p class="tools"><a href="#overview">總覽</a><a href="#index">目錄</a><a href="#log">操作紀錄</a><a href="#open-questions">待確認</a><a href="slides/index.html" target="_blank">簡報 ↗</a></p>
<input id="q" type="search" placeholder="搜尋頁面內容…" aria-label="搜尋頁面">
<nav id="nav"></nav>
</aside>
<main></main>
</div>
<script id="wiki-data" type="application/json">{payload}</script>
<script>{render_js}</script>
<script>{JS}</script>
</body>
</html>
"""
    (ROOT / "wiki.html").write_text(html, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"已產生 wiki.html（{len(pages)} 頁）")


if __name__ == "__main__":
    main()
