"""共用工具：路徑、frontmatter、連結擷取、檢查結果輸出。只用標準函式庫。"""
from __future__ import annotations

import datetime as _dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RUNS = ROOT / "runs"
SLIDES = ROOT / "slides"

SOURCE_IDS = ["DO2006", "EJOR2009", "JOSH2010", "TSWJ2014", "JOSH2016"]
RAW_DOIS = {
    "10.1016/j.disopt.2006.06.003": "DO2006",
    "10.1016/j.ejor.2007.11.035": "EJOR2009",
    "10.1007/s10951-009-0151-7": "JOSH2010",
    "10.1155/2014/596306": "TSWJ2014",
    "10.1007/s10951-015-0455-8": "JOSH2016",
}
PAGE_TYPES = {"source", "concept", "algorithm", "comparison", "query", "overview", "external"}
SPECIAL = {"index", "log"}          # 沒有 frontmatter 的導覽檔

# 表格裡的別名要寫成 [[頁面\|別名]]（Obsidian 的慣例），所以分隔符號前允許一個反斜線
LINK_RE = re.compile(r"\[\[([^\]|#\\]+)(?:#[^\]|\\]*)?(?:\\?\|([^\]]*))?\]\]")
TAG_RE = re.compile(r"\[((?:DO|EJOR|JOSH|TSWJ)\d{4})(?:\s+[^\]\[]*)?\]")
ANY_TAG_RE = re.compile(r"\[([A-Z]{2,5}\d{4})(?:\s+[^\]\[]*)?\]")


def page_id(path: Path) -> str:
    """wiki/concepts/x.md -> concepts/x"""
    return path.relative_to(WIKI).with_suffix("").as_posix()


def all_pages() -> dict[str, Path]:
    return {page_id(p): p for p in sorted(WIKI.rglob("*.md"))}


def split_frontmatter(text: str) -> tuple[dict, str]:
    """回傳 (meta, body)。只支援本專案用到的簡單 YAML：key: value 與 [a, b] 清單。"""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta: dict = {}
    for line in text[3:end].strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.split(" #", 1)[0].strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key.strip()] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        else:
            meta[key.strip()] = value
    body = text[end + 4:].lstrip("\n")
    return meta, body


def read_page(path: Path) -> tuple[dict, str]:
    return split_frontmatter(path.read_text(encoding="utf-8"))


def strip_code(body: str) -> str:
    """移除程式碼區塊與行內程式碼，避免把範例當成內容檢查。"""
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", body)


def links_in(body: str) -> list[str]:
    return [m.group(1).strip() for m in LINK_RE.finditer(strip_code(body))]


class Report:
    """收集錯誤與警告，印出並存成 runs/ 下的紀錄檔。"""

    def __init__(self, check: str, label: str):
        self.check, self.label = check, label
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.infos: list[str] = []

    def error(self, where: str, msg: str):
        self.errors.append(f"[錯誤] {where}: {msg}")

    def warn(self, where: str, msg: str):
        self.warnings.append(f"[警告] {where}: {msg}")

    def info(self, msg: str):
        self.infos.append(f"[資訊] {msg}")

    def finish(self) -> int:
        now = _dt.datetime.now()
        verdict = "通過" if not self.errors else "不通過"
        lines = [
            f"檢查點 {self.check} | {self.label} | {now:%Y-%m-%d %H:%M:%S}",
            f"結果：{verdict}（錯誤 {len(self.errors)}、警告 {len(self.warnings)}）",
            "",
            *self.errors, *self.warnings, *self.infos,
        ]
        text = "\n".join(lines) + "\n"
        RUNS.mkdir(exist_ok=True)
        out = RUNS / f"{now:%Y%m%d-%H%M%S}-{self.check}-{self.label}.txt"
        out.write_text(text, encoding="utf-8")
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(text + f"（已存檔：runs/{out.name}）")
        return 1 if self.errors else 0
