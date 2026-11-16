"""把 loop / graph 流程圖畫成 PNG（給繳交說明用）。

流程內容與 `繳交說明草稿.md` 第 4 節的 mermaid 圖一致；色票取自 slides/assets/base.css 的淺色版本。
執行：python scripts/draw_flow.py        輸出：loop_graph.png
"""
from __future__ import annotations

import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from common import ROOT

INK, MUTED, LINE = "#1c2530", "#5b6673", "#dcd8cc"
TEAL, TEAL_SOFT = "#0f766e", "#d9efec"
AMBER, AMBER_SOFT = "#b45309", "#fbeedb"
RED = "#9f1239"

FONT = "Microsoft JhengHei"
if FONT not in {f.name for f in font_manager.fontManager.ttflist}:
    sys.exit(f"找不到字體 {FONT}，請改用系統有的繁體中文字體")
plt.rcParams["font.family"] = FONT

W_NODE, H_NODE = 3.9, 0.74
# 代號 -> (y, 標題, 說明, 種類)
NODES = {
    "N1": (0, "N1 取得資料", "五篇論文放在 raw/（唯讀）", "p"),
    "N2": (1, "N2 Ingest 一篇", "讀論文 → 寫 Wiki 頁面（附出處標註）", "p"),
    "C1": (2, "C1 lint_wiki.py", "格式、連結、出處、例子數字", "c"),
    "N3": (3, "N3 查詢 Wiki", "只用 Wiki 內容，不回頭翻原文", "p"),
    "N4": (4, "N4 撰寫簡報稿", "每張標 wiki:: 出處", "p"),
    "C2": (5, "C2 check_outline.py", "結構順序、數字須出現在 Wiki", "c"),
    "N5": (6, "N5 搜尋延伸閱讀", "Wiki 以外唯一的內容來源", "p"),
    "C3": (7, "C3 check_further_reading.py", "用 Crossref 核對 DOI 與書目", "c"),
    "N6": (8, "N6 build_slides.py", "腳本轉成 HTML，模型不重寫內容", "p"),
    "C4": (9, "C4 check_slides.py + 瀏覽器實測", "轉換是否忠於簡報稿、版面有無溢出", "c"),
    "N7": (10, "N7 使用者確認", "人工審閱後才算完成", "p"),
}
YS = 1.25  # 列距


def Y(name_or_y):
    y = NODES[name_or_y][0] if isinstance(name_or_y, str) else name_or_y
    return -y * YS


def draw() -> None:
    fig, ax = plt.subplots(figsize=(10.4, 15.6), dpi=200)
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(Y(10) - 1.9, 1.6)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # 外圈底色
    for (y0, y1, label, tint) in ((1, 2, "外圈一：每篇論文一輪（N2 → C1）", "#e8f1ef"), (3, 9, "外圈二：每份簡報一輪（N3 → C4）", "#f4f1e8")):
        top, bot = Y(y0) + 0.62, Y(y1) - 0.5
        ax.add_patch(Rectangle((-4.95, bot), 9.9, top - bot, facecolor=tint, edgecolor="none", zorder=0))
        ax.text(4.72, (top + bot) / 2, label, rotation=90, ha="center", va="center", fontsize=10.5, color=MUTED)

    # 節點
    for key, (row, title, sub, kind) in NODES.items():
        y = Y(row)
        fc, ec = (TEAL_SOFT, TEAL) if kind == "p" else (AMBER_SOFT, AMBER)
        ax.add_patch(FancyBboxPatch((-W_NODE / 2, y - H_NODE / 2), W_NODE, H_NODE,
                                    boxstyle="round,pad=0,rounding_size=0.14", facecolor=fc, edgecolor=ec, linewidth=2, zorder=2))
        ax.text(0, y + 0.13, title, ha="center", va="center", fontsize=13, fontweight="bold", color=ec, zorder=3)
        ax.text(0, y - 0.18, sub, ha="center", va="center", fontsize=9.5, color=MUTED, zorder=3)

    def arrow(points, color=INK, dashed=False):
        # 前面的線段不畫箭頭，最後一段畫箭頭
        xs, ys = zip(*points)
        ax.plot(xs[:-1], ys[:-1], color=color, linewidth=1.8, linestyle="--" if dashed else "-", zorder=1, solid_capstyle="round")
        ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle="-|>", mutation_scale=16, color=color, linewidth=1.8,
                                     linestyle="--" if dashed else "-", shrinkA=0, shrinkB=0, zorder=1))

    half = W_NODE / 2
    # 往下的主流程
    order = ["N1", "N2", "C1", "N3", "N4", "C2", "N5", "C3", "N6", "C4", "N7"]
    for a, b in zip(order, order[1:]):
        arrow([(0, Y(a) - H_NODE / 2), (0, Y(b) + H_NODE / 2)])

    def side(label, x, y, color, ha):
        ax.text(x, y, label, ha=ha, va="center", fontsize=10.5, color=color, fontweight="bold", zorder=4,
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none"))

    # 通過的標籤（放在主流程箭頭旁）
    for a, b, lab in (("C1", "N3", "五篇都完成"), ("C2", "N5", "通過"), ("C3", "N6", "通過"), ("C4", "N7", "通過")):
        side(lab, 0.12, (Y(a) + Y(b)) / 2, TEAL, "left")

    # 回退箭頭（虛線，紅色）
    def back(frm, to, xchan, label, y_from=0.0, y_to=0.0, right=False, label_at=None):
        sgn = 1 if right else -1
        x0, x1 = sgn * half, sgn * half
        yf, yt = Y(frm) + y_from, Y(to) + y_to
        pts = [(x0, yf), (sgn * abs(xchan), yf), (sgn * abs(xchan), yt), (x1, yt)]
        arrow(pts, color=RED, dashed=True)
        ly = label_at if label_at is not None else (yf + yt) / 2
        side(label, sgn * abs(xchan), ly, RED, "center")

    back("C1", "N2", 3.15, "不通過，或\n還有下一篇", right=True)
    back("C2", "N4", 3.0, "有誤", y_from=-0.12, y_to=0.0)
    back("C2", "N2", 3.95, "Wiki 內容不足", y_from=0.12, y_to=0.12, label_at=(Y("C2") + Y("N2")) / 2)
    back("C3", "N5", 3.0, "書目不符")
    back("C4", "N6", 3.0, "轉換或顯示錯誤", label_at=(Y("C4") + Y("N6")) / 2)
    back("C4", "N4", 3.15, "內容有問題", right=True, label_at=(Y("C4") + Y("N4")) / 2 + 1.3)

    # 標題與圖例
    ax.text(0, 1.2, "loop / graph 設計：Wiki → 教學簡報", ha="center", va="center", fontsize=18, fontweight="bold", color=INK)
    ax.text(0, 0.85, "處理節點產出內容，檢查點用腳本或外部資料庫核對；檢查不過就退回前面的節點", ha="center", va="center", fontsize=10.5, color=MUTED)

    ly = Y(10) - 1.0
    ax.add_patch(FancyBboxPatch((-4.6, ly - 0.17), 0.5, 0.34, boxstyle="round,pad=0,rounding_size=0.07", facecolor=TEAL_SOFT, edgecolor=TEAL, linewidth=1.8))
    ax.text(-3.95, ly, "處理節點（N）", va="center", fontsize=10.5, color=INK)
    ax.add_patch(FancyBboxPatch((-2.15, ly - 0.17), 0.5, 0.34, boxstyle="round,pad=0,rounding_size=0.07", facecolor=AMBER_SOFT, edgecolor=AMBER, linewidth=1.8))
    ax.text(-1.5, ly, "檢查點（C）", va="center", fontsize=10.5, color=INK)
    ax.plot([0.35, 0.95], [ly, ly], color=INK, linewidth=1.8)
    ax.text(1.05, ly, "往下一步", va="center", fontsize=10.5, color=INK)
    ax.plot([2.45, 3.05], [ly, ly], color=RED, linewidth=1.8, linestyle="--")
    ax.text(3.15, ly, "退回重做", va="center", fontsize=10.5, color=INK)
    ax.text(0, ly - 0.55, "同一個檢查點最多重試 3 次。C5（check_style.py）只在改動樣式、重新產生簡報與 wiki.html 之後才跑，不在主流程內。",
            ha="center", va="center", fontsize=9.5, color=MUTED)

    out = ROOT / "loop_graph.png"
    fig.savefig(out, bbox_inches="tight", pad_inches=0.25, facecolor="white")
    print(f"已輸出 {out}")


if __name__ == "__main__":
    draw()
