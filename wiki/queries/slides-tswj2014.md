---
title: 簡報稿｜雙代理人單機排程
type: query
sources: [TSWJ2014]
deck: tswj2014
summary: 兩位客戶共用一台機器，一方要快、一方不能晚；看研究者怎麼用分支定界求最佳解、用模擬退火處理大問題。這是 Wiki 裡與 relocation problem 無關的另一個分支。
status: 已確認
updated: 2026-11-16
---

# 兩位客戶共用一台機器

## 兩位客戶共用一台機器
kind:: title
wiki:: [[sources/tswj2014]]

Lee, Shiau, Chung & Ding（2014）導讀。這篇與 relocation problem 沒有直接關係，是 Wiki 裡的另一個分支。

## 當工作來自不同的客戶
kind:: motivation
wiki:: [[concepts/two-agent-scheduling]]

- 傳統排程假設所有工作有同一個目標
- 現實中，工作來自不同的客戶，各自在意不同的事
- 例：研發部門要快速回應，製造部門要準時交貨，兩邊共用同一個試作工場
- 排程者要在兩邊的要求之間取捨

## 問題定義
kind:: definition
wiki:: [[sources/tswj2014]], [[concepts/scheduling-basics]]

- 一台機器；每個工作屬於 $AG_1$ 或 $AG_2$，有加工時間 $p_j$ 與交期 $d_j$
- 延遲時間 $T_j=\max\{0, C_j-d_j\}$
- $AG_2$ 的工作一件都不能延遲
- 在此前提下，讓 $AG_1$ 的 $\sum(\theta T_j+(1-\theta)C_j)$ 最小
- 沒有 $AG_2$ 且 $\theta=1$ 時，就是已知 NP-hard 的總延遲時間問題，所以這個問題也難

## 例子：兩邊的要求會衝突
kind:: example
wiki:: [[concepts/two-agent-scheduling]]

五個工作，$\theta=1/2$。120 種順序中，只有 22 種讓 $AG_2$ 不延遲。

| 排法 | 可行嗎 | $AG_1$ 目標值 |
|---|---|---|
| 全部照 SPT | 不可行 | 14.5（若不管 $AG_2$） |
| $AG_2$ 先做完 | 可行 | 24.5 |
| 最佳解 | 可行 | 18 |

```gantt
{"example": "E6-opt", "rows": [{"label": "機器", "bars": [{"job": "a2", "start": 0, "end": 2, "group": 1}, {"job": "b1", "start": 2, "end": 6, "group": 2}, {"job": "a1", "start": 6, "end": 9, "group": 1}, {"job": "b2", "start": 9, "end": 12, "group": 2}, {"job": "a3", "start": 12, "end": 17, "group": 1}]}], "caption": "最佳順序 a2→b1→a1→b2→a3：目標值 18"}
```

## 實驗結果
kind:: result
wiki:: [[sources/tswj2014]], [[algorithms/branch-and-bound]], [[algorithms/simulated-annealing]]

- 分支定界可解到 24 個工作，最耗時的一組平均 47.37 秒
- 模擬退火的平均誤差，作者表示都小於 1%
- 工作數是 100、200 時，$SA_1$ 的表現優於 $SA_2$，作者建議工作數多時用 $SA_1$
- 越重視 $AG_2$ 的比例、或交期越寬鬆，分支定界越好解

## 方法一：分支定界法（求最佳解）
kind:: method
wiki:: [[algorithms/branch-and-bound]]

把所有順序想成一棵樹，提早剪掉不可能更好的分支：

1. **支配性質**：這樣排一定不會比較好
2. **可行性**：這樣排下去 $AG_2$ 一定會延遲
3. **下界**：這個分支最好也只能這樣，已經不比目前最好的解好

例：前兩個位置排 a1、a3，b1 最快也要到 12 才完成，超過交期 6，整枝剪掉。

## 方法二：模擬退火（求近似解）
kind:: method
wiki:: [[algorithms/simulated-annealing]]

- 從 $AG_2$ 依交期、再 $AG_1$ 依加工時間的順序出發
- 每次隨機對調兩個工作；變好就接受，變差也有機率接受，機率逐漸降低
- 執行 $400n$ 次迭代
- $SA_1$：不可行的鄰近解重新產生；$SA_2$：把 $AG_2$ 的延遲加進目標當懲罰

## 注意事項
kind:: caveat
wiki:: [[sources/tswj2014]]

這篇原文有幾處前後不一，Wiki 都標為「待確認」：

- 實驗參數 $P$ 一處說是 $AG_2$ 的比例、一處說是 $AG_1$ 的比例
- 內文說誤差都小於 1%，但 Table 5 有一組是 1.05%
- 內文說執行時間都小於 1 秒，Table 6 有幾組超過

## 回顧
kind:: recap
wiki:: [[sources/tswj2014]], [[concepts/two-agent-scheduling]]

- 雙代理人排程：在滿足一方要求的前提下，讓另一方的目標最好
- 難題的兩條路：能算就用分支定界求最佳，太大就用模擬退火求近似
- 它與 relocation problem 沒有直接關係，共通點是面對 NP-hard 時的思路

## 延伸閱讀
kind:: further
wiki:: [[further-reading/tswj2014]]

（由 further-reading 頁產生）
