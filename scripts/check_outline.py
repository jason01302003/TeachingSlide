"""檢查點 C2：簡報稿檢查。

執行：python scripts/check_outline.py <代號>      例如 python scripts/check_outline.py do2006
"""
from __future__ import annotations

import json
import re
import sys

from common import RUNS, WIKI, Report, all_pages, links_in, read_page, strip_code

KINDS = ["title", "motivation", "background", "definition", "example", "result", "method", "caveat", "recap", "further"]
REQUIRED_ORDER = ["title", "motivation", "definition", "example", "result", "method", "recap", "further"]
NUM_RE = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w]|\.\d)")
BLOCK_RE = re.compile(r"```(gantt|levels)\n(.*?)```", re.S)


def parse_deck(deck: str):
    """回傳 (meta, 簡報標題, [投影片 dict])。"""
    path = WIKI / "queries" / f"slides-{deck}.md"
    meta, body = read_page(path)
    parts = re.split(r"^## ", body, flags=re.M)
    head = parts[0]
    title = next((l[2:].strip() for l in head.splitlines() if l.startswith("# ")), "")
    slides = []
    for part in parts[1:]:
        lines = part.splitlines()
        slide = {"title": lines[0].strip(), "kind": "", "wiki": [], "body": ""}
        rest = []
        for line in lines[1:]:
            if line.startswith("kind::"):
                slide["kind"] = line.split("::", 1)[1].strip()
            elif line.startswith("wiki::"):
                slide["wiki"] = links_in(line)
            else:
                rest.append(line)
        slide["body"] = "\n".join(rest).strip()
        slides.append(slide)
    return meta, title, slides


def numbers_in(text: str) -> set[str]:
    text = BLOCK_RE.sub("", text)
    text = re.sub(r"\[\[[^\]]*\]\]", "", text)
    text = re.sub(r"^\s*\d+\.\s", "", text, flags=re.M)          # 編號清單的序號
    text = re.sub(r"_\{?[\w,+\-]*\}?", "", text)                 # 下標裡的數字（如 J_1、C_{k,h}）
    text = re.sub(r"\^\{?[\w+\-]*\}?", "", text)                 # 上標
    return set(NUM_RE.findall(text))


def main(deck: str) -> int:
    rep = Report("C2", deck)
    path = WIKI / "queries" / f"slides-{deck}.md"
    if not path.exists():
        rep.error(deck, f"找不到簡報稿 {path.name}")
        return rep.finish()
    pages = all_pages()
    meta, title, slides = parse_deck(deck)
    if not title:
        rep.error(deck, "簡報稿缺少 # 簡報標題")
    if meta.get("deck") != deck:
        rep.error(deck, "frontmatter 的 deck 欄位與檔名不符")
    if not 8 <= len(slides) <= 14:
        rep.error(deck, f"投影片 {len(slides)} 張，應在 8–14 張之間")

    examples_file = RUNS / "examples.json"
    examples = json.loads(examples_file.read_text(encoding="utf-8")) if examples_file.exists() else {}
    known_blocks = {bid: blk for ex in examples.values() for bid, blk in ex.get("blocks", {}).items()}

    kinds = []
    cited_all = set()
    for no, s in enumerate(slides, 1):
        where = f"第 {no} 張「{s['title']}」"
        kinds.append(s["kind"])
        if s["kind"] not in KINDS:
            rep.error(where, f"kind「{s['kind']}」不在允許清單")
        if not s["wiki"]:
            rep.error(where, "沒有 wiki:: 出處")
        missing = [w for w in s["wiki"] if w not in pages]
        for w in missing:
            if s["kind"] == "further" and w == f"further-reading/{deck}":
                rep.warn(where, f"延伸閱讀頁 {w} 尚未建立（由 N5 產生，C4 會再檢查）")
            else:
                rep.error(where, f"出處 [[{w}]] 不存在")
        cited_all.update(s["wiki"])
        for target in links_in(s["body"]):
            if target not in pages:
                rep.error(where, f"內文連結 [[{target}]] 不存在")

        # 圖表區塊必須與 examples.py 的輸出完全相同
        for kind, raw in BLOCK_RE.findall(s["body"]):
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                rep.error(where, f"{kind} 區塊不是合法 JSON：{exc}")
                continue
            bid = data.get("example")
            if bid not in known_blocks:
                rep.error(where, f"{kind} 區塊的 example「{bid}」不在 scripts/examples.py 的輸出中")
            elif data != known_blocks[bid]:
                rep.error(where, f"{kind} 區塊「{bid}」的內容與 scripts/examples.py 的輸出不一致")

        # 數字要能在出處頁面找到
        if s["kind"] not in ("title", "further"):
            source_text = "\n".join(pages[w].read_text(encoding="utf-8") for w in s["wiki"] if w in pages)
            source_nums = set(re.findall(r"\d+(?:\.\d+)?", source_text))
            for num in sorted(numbers_in(strip_code(s["body"])) - source_nums):
                rep.error(where, f"數字 {num} 在所列出處頁面中找不到")

        body_lines = [l for l in BLOCK_RE.sub("", s["body"]).splitlines() if l.strip()]
        if len(body_lines) > 12:
            rep.warn(where, f"內文 {len(body_lines)} 行，可能塞不進一張投影片")
        if s["kind"] != "title" and not s["body"]:
            rep.error(where, "沒有內文")

    # 教學結構：必要段落依序出現
    pos = 0
    for need in REQUIRED_ORDER:
        try:
            pos = kinds.index(need, pos) + 1
        except ValueError:
            rep.error(deck, f"教學結構缺少「{need}」，或順序不對（目前順序：{' → '.join(kinds)}）")
            break
    if kinds and kinds[0] != "title":
        rep.error(deck, "第一張必須是 title")
    if kinds and kinds[-1] != "further":
        rep.error(deck, "最後一張必須是 further（延伸閱讀）")
    if f"sources/{deck}" not in cited_all:
        rep.error(deck, f"沒有任何一張投影片以 [[sources/{deck}]] 為出處")
    if slides and f"further-reading/{deck}" not in slides[-1]["wiki"]:
        rep.error(deck, f"最後一張的出處必須是 [[further-reading/{deck}]]")

    rep.info(f"{len(slides)} 張；結構：{' → '.join(kinds)}")
    rep.info(f"引用的 Wiki 頁面 {len(cited_all)} 個：{', '.join(sorted(cited_all))}")
    return rep.finish()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法：python scripts/check_outline.py <代號>")
    sys.exit(main(sys.argv[1]))
