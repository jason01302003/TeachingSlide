---
title: 五篇論文一覽
type: comparison
sources: [DO2006, EJOR2009, JOSH2010, TSWJ2014, JOSH2016]
status: 已確認
updated: 2026-11-16
---

## 比較表

| 論文 | 機器環境 | 資源限制 | 目標 | 方法 | 最重要的結果 |
|---|---|---|---|---|---|
| [[sources/do2006\|DO2006]] | 多台相同機器（工作隊） | 有（relocation） | $C_{\max}$ | 難度證明、近似演算法 | 兩台機器、UET 即為 strongly NP-hard；近似比 2 與 $3-2/m$ [DO2006 Thm 2, Thm 4, Thm 5] |
| [[sources/ejor2009\|EJOR2009]] | 單機（等價於二機流程工廠） | 有（relocation） | 最小初始資源量；$C_{\max}$ | 概念介紹、composite job、交換論證 | relocation problem 的投資觀點可以直觀解釋 Johnson's rule；composite job 能降低數個相關問題的計算時間 [EJOR2009 §2, §5] |
| [[sources/josh2010\|JOSH2010]] | 單機 | 有（relocation） | $\sum w_iC_i$ | 難度證明、問題等價、近似演算法 | 四個特例皆為 strongly NP-hard；Algorithm W 近似比 2 [JOSH2010 Thm 1, Thm 2, Thm 4] |
| [[sources/tswj2014\|TSWJ2014]] | 單機、兩個代理人 | 無 | $AG_1$ 的 $\sum(\theta T_j+(1-\theta)C_j)$，$AG_2$ 不得延遲 | branch-and-bound、模擬退火、數值實驗 | 最佳解可算到 24 個工作；模擬退火誤差約在 1% 上下 [TSWJ2014 §5, Table 5] |
| [[sources/josh2016\|JOSH2016]] | 2 台專用機、順序固定 | 有（relocation） | 六種：$C_{\max}$、$\sum w_jC_j$、$L_{\max}$、$\sum w_jT_j$、$\sum w_jU_j$、$\sum U_j$ | 動態規劃、難度證明 | 四種目標多項式時間可解，兩種 NP-hard；$\sum T_j$ 未解決 [JOSH2016 Thm 1, Thm 2, Thm 3, Thm 5] |

## 五篇之間的引用關係

- EJOR2009、JOSH2010、JOSH2016 都引用 DO2006 [EJOR2009 References]、[JOSH2010 §1]、[JOSH2016 §1]。
- JOSH2016 引用 JOSH2010 [JOSH2016 §1]。
- TSWJ2014 沒有引用其他四篇，其他四篇也沒有引用它 [TSWJ2014 References]。

## 相關頁面

- [[comparisons/complexity-table]]
- [[overview]]
