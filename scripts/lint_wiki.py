"""檢查點 C1：Wiki 健康檢查。

執行：python scripts/lint_wiki.py <標籤>      例如 python scripts/lint_wiki.py do2006
"""
from __future__ import annotations

import json
import re
import sys

from common import (ANY_TAG_RE, PAGE_TYPES, RUNS, SOURCE_IDS, SPECIAL, TAG_RE, WIKI, Report,
                    all_pages, links_in, read_page, strip_code)

REQUIRED_META = ["title", "type", "sources", "status", "updated"]
FACT_TYPES = {"source", "concept", "algorithm", "comparison"}
MARKERS = ("（推論）", "（自編例子", "（白話說明）", "待確認")
EXEMPT_HEADINGS = ("相關頁面", "書目", "原文符號", "更新紀錄")
LOG_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] (discuss|schema|ingest|query|search|lint|check|fix|build) \| .+")
EXAMPLE_RE = re.compile(r"（自編例子\s*(E\d+)")


def blocks_of(body: str):
    """把內文切成 (所在標題, 區塊文字)。區塊＝段落、最上層清單項目（含子項）、表格的一列。"""
    heading, buf = "", []
    out = []

    def flush():
        if buf:
            out.append((heading, "\n".join(buf)))
            buf.clear()

    in_code = False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            flush()
            continue
        if in_code:
            continue
        if line.startswith("#"):
            flush()
            heading = line.lstrip("#").strip()
        elif not line.strip():
            flush()
        elif line.lstrip().startswith("|"):
            flush()
            if not re.fullmatch(r"\s*\|[\s:|-]+\|\s*", line):
                out.append((heading, line))
        elif re.match(r"(-|\*|\d+\.)\s", line):          # 最上層清單項目
            flush()
            buf.append(line)
        else:
            buf.append(line)                            # 段落續行或縮排的子項
    flush()
    return out


def is_table_header(block: str, body: str) -> bool:
    lines = body.splitlines()
    for i, line in enumerate(lines[:-1]):
        if line == block and re.fullmatch(r"\s*\|[\s:|-]+\|\s*", lines[i + 1]):
            return True
    return False


def main(label: str) -> int:
    rep = Report("C1", label)
    pages = all_pages()
    metas, bodies = {}, {}
    for pid, path in pages.items():
        metas[pid], bodies[pid] = read_page(path)

    # 1. frontmatter
    for pid, meta in metas.items():
        if pid in SPECIAL:
            continue
        for key in REQUIRED_META:
            if key not in meta:
                rep.error(pid, f"frontmatter 缺少 {key}")
        if meta.get("type") and meta["type"] not in PAGE_TYPES:
            rep.error(pid, f"type「{meta['type']}」不在允許清單")
        if meta.get("status") and meta["status"] not in ("初稿", "已確認"):
            rep.error(pid, f"status「{meta['status']}」不合法")
        for sid in meta.get("sources", []) if isinstance(meta.get("sources"), list) else []:
            if sid not in SOURCE_IDS:
                rep.error(pid, f"sources 含未知代號 {sid}")

    # 2. 連結存在；3. 孤兒頁；4. index 完整
    inbound = {pid: set() for pid in pages}
    for pid, body in bodies.items():
        for target in links_in(body):
            if target not in pages:
                rep.error(pid, f"連結 [[{target}]] 指向不存在的頁面")
            elif target != pid:
                inbound[target].add(pid)
    for pid in pages:
        if pid in SPECIAL or pid == "overview":
            continue
        if not (inbound[pid] - {"index", "log"}):
            rep.error(pid, "孤兒頁：除了 index 以外沒有任何頁面連到它")
        if "index" in pages and "index" not in inbound[pid]:
            rep.error("index", f"沒有列出 {pid}")

    # 5. 來源標註的代號；6. 事實性區塊都有標註
    marker_count = {m: 0 for m in MARKERS}
    for pid, body in bodies.items():
        meta = metas[pid]
        if pid in SPECIAL:
            continue
        clean = strip_code(body)
        for m in ANY_TAG_RE.finditer(clean):
            if m.group(1) not in SOURCE_IDS:
                rep.error(pid, f"來源標註 {m.group(0)} 的代號不存在")
        if meta.get("type") not in FACT_TYPES:
            continue
        declared = set(meta.get("sources", []))
        cited = {m.group(1) for m in TAG_RE.finditer(clean)}
        for sid in sorted(cited - declared):
            rep.error(pid, f"內文引用了 {sid}，但 frontmatter 的 sources 沒有列")
        for sid in sorted(declared - cited):
            rep.error(pid, f"sources 列了 {sid}，但內文沒有任何 [{sid} …] 標註")
        for heading, block in blocks_of(body):
            if any(h in heading for h in EXEMPT_HEADINGS):
                continue
            text = strip_code(block).strip()
            plain = re.sub(r"\[\[[^\]]*\]\]", "", text)        # 去掉 [[連結]] 後才算長度：純導覽句不算事實
            if len(plain) < 30 or text.endswith(("：", ":")) or is_table_header(block, body):
                continue
            if re.fullmatch(r"\$\$.*\$\$", text, flags=re.S):   # 獨立一行的數學式，標註寫在它所屬的那一點
                continue
            for mk in MARKERS:
                if mk in text:
                    marker_count[mk] += 1
            if TAG_RE.search(text) or any(mk in text for mk in MARKERS):
                continue
            rep.error(pid, f"這段沒有來源標註也沒有標記：「{text[:38]}…」")
    rep.info("非來源內容的標記數量：" + "、".join(f"{k} {v}" for k, v in marker_count.items()))

    # 7. 待確認事項要同步到 open-questions
    if "open-questions" in pages:
        listed = set(links_in(bodies["open-questions"]))
        for pid, body in bodies.items():
            if pid in SPECIAL or pid == "open-questions":
                continue
            if "**待確認**" in body and pid not in listed:
                rep.error("open-questions", f"{pid} 有待確認事項，但總表沒有連到它")

    # 8. 自編例子的關鍵數字
    ex_file = RUNS / "examples.json"
    examples = json.loads(ex_file.read_text(encoding="utf-8")) if ex_file.exists() else {}
    for pid, body in bodies.items():
        for eid in sorted(set(EXAMPLE_RE.findall(body))):
            if eid not in examples:
                rep.error(pid, f"引用了自編例子 {eid}，但 scripts/examples.py 沒有輸出這個例子")
                continue
            for key in examples[eid]["keys"]:
                if key not in body:
                    rep.error(pid, f"自編例子 {eid} 的關鍵數字「{key}」沒有出現在頁面上，可能與腳本輸出不一致")

    # 9. 數學式：$ 要成對；表格裡的數學式不可含 |；不可混入控制字元（例如 \theta 的 \t 被當成 Tab）
    for pid, body in bodies.items():
        for no, line in enumerate(strip_code(body).splitlines(), 1):
            if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", line) or "\t" in line.lstrip("\t"):
                rep.error(pid, f"第 {no} 行含有控制字元（可能是 LaTeX 指令的反斜線被吃掉）：{line.strip()[:40]!r}")
            if line.replace("\\$", "").count("$") % 2:
                rep.error(pid, f"第 {no} 行的 $ 沒有成對：{line.strip()[:40]}")
            if line.lstrip().startswith("|"):
                for math in re.findall(r"\$[^$]*\$", line):
                    if "|" in math:
                        rep.error(pid, f"第 {no} 行表格中的數學式含有 |：{math}")

    # 10. log 格式
    if "log" in pages:
        for line in bodies["log"].splitlines():
            if line.startswith("## ") and not LOG_RE.match(line):
                rep.error("log", f"紀錄標題格式不符：{line}")

    counts = {}
    for pid, meta in metas.items():
        counts[meta.get("type", "導覽")] = counts.get(meta.get("type", "導覽"), 0) + 1
    rep.info(f"共 {len(pages)} 頁：" + "、".join(f"{k} {v}" for k, v in sorted(counts.items())))
    return rep.finish()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "all"))
