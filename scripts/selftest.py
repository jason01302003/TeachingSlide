"""檢查腳本的自我測試：故意做一個有錯的小 Wiki，確認 lint 真的抓得到。

起因：2026-11-16 修改 lint 時把連結的正規表示式改壞，結果 lint 回報「通過」。
檢查工具本身出錯時，「通過」沒有意義，所以每次改檢查腳本後都要先跑這支。

執行：python scripts/selftest.py
"""
from __future__ import annotations

import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

import common

GOOD = """---
title: 好頁面
type: concept
sources: [DO2006]
status: 初稿
updated: 2026-11-16
---
這是一段夠長的事實敘述，長度超過三十個字，而且句尾有來源標註 [DO2006 §1]。

| 欄位 | 連結 |
|---|---|
| 表格內的別名連結也要被認得，這一列夠長所以需要標註 [DO2006 §2] | [[concepts/bad\\|壞頁面]] |
"""

BAD = """---
title: 壞頁面
type: concept
sources: [DO2006, EJOR2009]
status: 草稿
updated: 2026-11-16
---
這是一段夠長的事實敘述，長度超過三十個字，但是句尾完全沒有任何來源標註。

這一句引用了不存在的代號，長度同樣超過三十個字，用來測試代號檢查 [ABC2020 §1]。

連到不存在的頁面 [[concepts/missing]]，並且有一個沒有成對的 $ 符號 x_1 [DO2006 §1]。

> **待確認**：這裡有一件待確認的事，但是總表沒有連過來。見 [[concepts/good]]。

（自編例子 E99）這個例子不存在。

這一行的數學式被吃掉反斜線變成 Tab：$\theta=1$，要能被抓到，長度超過三十個字 [DO2006 §1]。
"""

EXPECT = [
    "status「草稿」不合法",
    "這段沒有來源標註也沒有標記",
    "的代號不存在",
    "[[concepts/missing]] 指向不存在的頁面",
    "$ 沒有成對",
    "sources 列了 EJOR2009，但內文沒有",
    "有待確認或已確認的註記，但總表沒有連到它",
    "引用了自編例子 E99",
    "孤兒頁",
    "沒有列出 concepts/orphan",
    "紀錄標題格式不符",
    "含有控制字元",
]
MUST_NOT = ["[[concepts/bad\\|壞頁面]]", "[[concepts/bad\\]]"]   # 表格內的別名連結不可被誤判成斷鏈


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        wiki, runs = root / "wiki", root / "runs"
        (wiki / "concepts").mkdir(parents=True)
        runs.mkdir()
        (wiki / "concepts" / "good.md").write_text(GOOD, encoding="utf-8")
        (wiki / "concepts" / "bad.md").write_text(BAD, encoding="utf-8")
        (wiki / "concepts" / "orphan.md").write_text(GOOD.replace("好頁面", "孤兒").replace("[[concepts/bad\\|壞頁面]]", "無"), encoding="utf-8")
        (wiki / "open-questions.md").write_text("---\ntitle: 待確認\ntype: overview\nsources: []\nstatus: 初稿\nupdated: 2026-11-16\n---\n空的\n", encoding="utf-8")
        (wiki / "index.md").write_text("# 目錄\n- [[concepts/good]]\n- [[concepts/bad]]\n- [[open-questions]]\n", encoding="utf-8")
        (wiki / "log.md").write_text("# 紀錄\n## 2026-11-16 亂寫的標題\n", encoding="utf-8")
        (runs / "examples.json").write_text("{}", encoding="utf-8")

        common.WIKI, common.RUNS = wiki, runs
        import lint_wiki
        lint_wiki.WIKI, lint_wiki.RUNS = wiki, runs
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = lint_wiki.main("selftest")
        out = buf.getvalue()

    sys.stdout.reconfigure(encoding="utf-8")
    failed = [e for e in EXPECT if e not in out] + [f"誤判：{m}" for m in MUST_NOT if m in out]
    if "concepts/good:" in out:
        failed.append("誤判：好頁面被報錯")
    if code != 1:
        failed.append("有錯的 Wiki 竟然回報通過")
    print(f"自我測試：預期抓到 {len(EXPECT)} 種錯誤，實際漏掉或誤判 {len(failed)} 項")
    for f in failed:
        print("  ✗", f)
    if failed:
        print("---- lint 的實際輸出 ----\n" + out)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
