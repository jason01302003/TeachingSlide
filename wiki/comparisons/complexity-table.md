---
title: 複雜度結果總表
type: comparison
sources: [DO2006, EJOR2009, JOSH2010, TSWJ2014, JOSH2016]
status: 已確認
updated: 2026-11-16
---

## 怎麼讀這張表

每一列是一個問題版本。「結果」欄的意思：多項式時間＝有快速的精確解法；NP-hard／strongly NP-hard＝沒有已知的快速精確解法（見 [[concepts/np-hardness]]）；近似比＝快速方法保證不會比最佳解差超過的倍數（見 [[concepts/approximation-algorithm]]）（白話說明）。

## Relocation problem

| 機器 | 條件 | 目標 | 結果 | 出處 |
|---|---|---|---|---|
| 單一工作隊 | 不考慮時間 | 是否可行 | 多項式時間，$O(n\log n)$（Kaplan 與 Amir 的結果） | [DO2006 §1] |
| 單一工作隊 | 不考慮時間 | 最小初始資源量 $v_0$ | 多項式時間，$O(n\log n)$；等價於 $F2\mid\mid C_{\max}$，用 Johnson's rule | [EJOR2009 §1, §5] |
| 多個相同工作隊 | 一般加工時間 | $C_{\max}$ | NP-hard（Amir 與 Kaplan 的結果） | [DO2006 §1] |
| 2 台專用機 | UET、$\delta_i>0$ | $C_{\max}$ | strongly NP-hard | [DO2006 Thm 1] |
| 2 台相同機器 | UET、$\delta_i>0$ | $C_{\max}$ | strongly NP-hard | [DO2006 Thm 2] |
| 機器數不限 | UET | $C_{\max}$ | 近似比 2（Rounding） | [DO2006 Thm 4] |
| $m$ 台相同機器 | UET | $C_{\max}$ | 近似比 $3-2/m$（Splitting） | [DO2006 Thm 5] |
| 機器數不限 | UET、$\alpha_i=\beta_i$ | $C_{\max}$ | 近似比不可能小於 $3/2$（除非 P = NP） | [DO2006 §2] |
| 機器數不限 | UET、$\alpha_i\le\beta_i$ | $C_{\max}$ | 漸近近似比不可能小於 $4/3$（除非 P = NP） | [DO2006 Thm 3] |
| 單機 | $p_i=1$、$\delta_i\le 0$ | $\sum w_iC_i$ | strongly NP-hard | [JOSH2010 Thm 1] |
| 單機 | $p_i=1$、$\delta_i\ge 0$ | $\sum w_iC_i$ | strongly NP-hard；近似比 2（Algorithm W） | [JOSH2010 Thm 2, Thm 4] |
| 單機 | $w_i=1$、$\delta_i\ge 0$ | $\sum w_iC_i$ | strongly NP-hard | [JOSH2010 Cor. 1] |
| 單機 | $w_i=1$、$\delta_i\le 0$ | $\sum w_iC_i$ | strongly NP-hard；近似比 2（由等價關係） | [JOSH2010 Cor. 2, §3] |
| 2 台專用機 | 順序不固定 | $C_{\max}$、$\sum C_j$、與交期有關的目標 | strongly NP-hard（由前面幾列推得） | [JOSH2016 §1] |
| 2 台專用機 | 順序固定 | $C_{\max}$、$\sum w_jC_j$、$L_{\max}$ | 多項式時間，$O(n_1n_2(n_1+n_2))$ | [JOSH2016 Thm 1] |
| 2 台專用機 | 順序固定 | $\sum w_jT_j$、$\sum w_jU_j$ | NP-hard（普通意義）；pseudo-polynomial 動態規劃 | [JOSH2016 Thm 2, Thm 3, Thm 4] |
| 2 台專用機 | 順序固定 | $\sum U_j$ | 多項式時間，$O(n_1^2n_2^2(n_1+n_2)^2)$ | [JOSH2016 Thm 5] |
| 2 台專用機 | 順序固定 | $\sum T_j$ | 尚未解決 | [JOSH2016 §6] |
| 2 台專用機 | 順序固定、加工時間都相同 | 上述六種目標 | 全部多項式時間 | [JOSH2016 §6] |

## 二機流程工廠（與單一工作隊的 relocation problem 等價）

| 問題 | 結果 | 出處 |
|---|---|---|
| $F2\mid\mid C_{\max}$ | 多項式時間，$O(n\log n)$（Johnson's rule） | [EJOR2009 §1] |
| 交期指派問題（Birman 與 Mosheiov 提出） | 原解法 $O(n^2\log n)$，用 composite job 降為 $O(n\log n)$ | [EJOR2009 §2] |
| $F2\mid f\mid C_{\max}$、$F2\mid l\mid C_{\max}$（首位或末位禁排） | 原解法 $O(n^2)$，用 composite job 降為 $O(n\log n)$ | [EJOR2009 §2] |
| $F2\mid f,l\mid C_{\max}$（首末位同時禁排） | 原解法 $O(n^3)$，用 composite job 降為 $O(n^2)$ | [EJOR2009 §2] |

## 雙代理人排程（獨立分支，沒有資源限制）

| 問題 | 結果 | 出處 |
|---|---|---|
| 單機總延遲時間 $1\mid\mid\sum T_j$ | NP-hard（Du 與 Leung 的結果） | [TSWJ2014 §3] |
| $1\mid \sum_{AG_2}U_j=0\mid \sum_{AG_1}(\theta T_j+(1-\theta)C_j)$ | NP-hard（包含上一列為特例）；branch-and-bound 可解到 24 個工作；模擬退火用於 100、200 個工作 | [TSWJ2014 §3, §5] |

## 更新紀錄

- JOSH2016：新增兩台專用機、順序固定的六列。
- TSWJ2014：新增雙代理人排程一節。
- JOSH2010：新增單機總加權完工時間的四列。
- EJOR2009：新增「最小初始資源量」一列與二機流程工廠一節。

## 相關頁面

- [[comparisons/papers-at-a-glance]]
- [[concepts/np-hardness]]、[[concepts/approximation-algorithm]]
- [[sources/do2006]]、[[sources/ejor2009]]、[[sources/josh2010]]、[[sources/tswj2014]]、[[sources/josh2016]]
