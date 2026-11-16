---
title: 簡報稿｜加工順序固定的 relocation 排程
type: query
sources: [JOSH2016]
deck: josh2016
summary: 如果機器的指派與順序都已經定好，只決定「何時開始」，會變簡單嗎？答案要看目標：有的可以用動態規劃快速解決，有的仍然是 NP-hard。
status: 已確認
updated: 2026-11-16
---

# 順序都定好了，還有什麼好決定？

## 順序都定好了，還有什麼好決定？
kind:: title
wiki:: [[sources/josh2016]]

Lin, Hwang & Kononov（2016）導讀

## 把大問題拆成三步
kind:: motivation
wiki:: [[concepts/fixed-sequence]], [[concepts/relocation-problem]]

完整的問題要決定三件事：

1. 哪個工作給哪台機器
2. 每台機器上先做誰
3. 每個工作什麼時候開始

本文只研究第三步，因為如果這一步能快速算出，就能當作搜尋法的零件，替每個候選順序打分數。

## 問題定義：兩台專用機、順序固定
kind:: definition
wiki:: [[sources/josh2016]], [[concepts/parallel-machines]]

- 兩台專用機，每個工作只能在指定的機器上做，兩邊的順序都已經給定
- 共用一個資源池；兩台機器可以同時加工，前提是資源夠
- 同一時間點，先讓完成的工作歸還資源，再讓新工作取用
- 研究六種目標：$C_{\max}$、$\sum w_jC_j$、$L_{\max}$、$\sum w_jT_j$、$\sum w_jU_j$、$\sum U_j$

## 例子：資源逼機器等待
kind:: example
wiki:: [[concepts/fixed-sequence]]

$M_1$ 的順序 a1→a2→a3，$M_2$ 的順序 b1→b2→b3，初始資源 4。

- 不管資源，兩台各自連續做：makespan 是 7
- 加上資源限制後，最小 makespan 是 9，最小的總完工時間是 34
- 時間 3 時 b1 做完，$M_2$ 空了，但池中只有 4 單位，b2 要 5 單位，只能等

```gantt
{"example": "E5-sumc", "rows": [{"label": "M1", "bars": [{"job": "a1", "start": 0, "end": 2}, {"job": "a2", "start": 2, "end": 5}, {"job": "a3", "start": 7, "end": 9}]}, {"label": "M2", "bars": [{"job": "b1", "start": 0, "end": 3}, {"job": "b2", "start": 5, "end": 7}, {"job": "b3", "start": 7, "end": 8}]}], "caption": "最小總完工時間 = 34，這個排程的 makespan 是 9"}
```

## 主要結果：看目標而定
kind:: result
wiki:: [[comparisons/complexity-table]], [[sources/josh2016]]

| 目標 | 順序固定後 |
|---|---|
| $C_{\max}$、$\sum w_jC_j$、$L_{\max}$ | 多項式時間，$O(n_1n_2(n_1+n_2))$ |
| $\sum U_j$ | 多項式時間 |
| $\sum w_jT_j$、$\sum w_jU_j$ | NP-hard（普通意義） |
| $\sum T_j$ | 尚未解決 |

加工時間都相同時，六種目標全部是多項式時間。

## 方法：排程區塊與動態規劃
kind:: method
wiki:: [[algorithms/backward-dp]]

- 狀態 $(i,j)$：$M_1$ 還剩第 $i$ 個以後、$M_2$ 還剩第 $j$ 個以後的工作
- 由後往前，每次接上一個「排程區塊」，只有三種情形：只有 $M_1$ 做、只有 $M_2$ 做、兩台同時開始並重疊
- 前三個目標不用多記什麼：整段往後挪，目標值只加上固定的量
- 延遲類目標要把「已過的時間」記進狀態，所以時間跟加工時間的大小有關

## 為什麼有的目標難
kind:: caveat
wiki:: [[concepts/np-hardness]], [[algorithms/backward-dp]]

- $\sum w_jT_j$ 是普通意義的 NP-hard：數字不大時其實可以解
- 動態規劃的時間與加工時間總和成正比，加工時間都相同時就變成多項式時間
- strongly NP-hard 的問題沒有這種出路

## 回顧
kind:: recap
wiki:: [[sources/josh2016]], [[concepts/fixed-sequence]]

- 把決策拆開，單獨研究「何時開始」這一步
- 順序固定也不一定簡單：六種目標中，四種可快速解，兩種是 NP-hard
- 可以快速解的，能當作搜尋法的零件
- 與庫存限制排程相關，是作者提出的後續方向

## 延伸閱讀
kind:: further
wiki:: [[further-reading/josh2016]]

（由 further-reading 頁產生）
