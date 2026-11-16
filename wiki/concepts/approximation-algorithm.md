---
title: 近似演算法與近似比
type: concept
sources: [DO2006, JOSH2010]
status: 已確認
updated: 2026-11-16
---

## 白話說明

既然最佳解太難找，就退一步：設計一個跑得快的方法，並且保證它的答案「不會比最佳解差超過某個倍數」。這個倍數就是近似比（白話說明）。

## 定義

- $\rho$-近似演算法：一個多項式時間的演算法，對最小化問題的任何例子 $I$，都輸出一個可行解，其 makespan 不超過 $\rho\times OPT(I)$ [DO2006 §2]。
- 漸近 $\rho$-近似演算法：存在一個常數 $c$，使得輸出的 makespan 不超過 $\rho\times OPT(I)+c$ [DO2006 §2]。當最佳值很大時，多出來的常數 $c$ 就不重要了（白話說明）。
- 近似比「是緊的」，是指找得到例子讓演算法真的差到那個倍數，所以分析無法再改進 [DO2006 §5]。

## 正面結果與負面結果

| 問題 | 結果 | 出處 |
|---|---|---|
| $RP_\infty$（機器數不限，UET） | Rounding Algorithm 的近似比為 2 | [DO2006 Thm 4] |
| $m$ 台相同機器的 $RP$（UET） | Splitting Algorithm 的近似比為 $3-2/m$ | [DO2006 Thm 5] |
| $RP_\infty$，即使 $\alpha_i=\beta_i$、$p_i=1$ | 除非 P = NP，近似比不可能小於 $3/2$ | [DO2006 §2] |
| $RP_\infty$，即使 $\alpha_i\le\beta_i$、$p_i=1$ | 除非 P = NP，漸近近似比不可能小於 $4/3$ | [DO2006 Thm 3] |
| 單機 $\sum w_iC_i$，$\delta_i\ge 0$、$p_i=1$ | Algorithm W 的近似比為 2，且是緊的 | [JOSH2010 Thm 4, §3] |
| 單機 $\sum w_iC_i$，$\delta_i\le 0$、$w_i=1$ | 由問題等價得到同樣的近似比 2 | [JOSH2010 §3] |
| 單機 $\sum w_iC_i$，另外兩個特例與一般情形 | 能否近似仍未解決 | [JOSH2010 §4] |

對 $RP_\infty$ 而言，已知做得到 2、做不到小於 $3/2$，中間還有空間（推論）。

## 相關頁面

- [[algorithms/rounding-and-splitting]]、[[algorithms/algorithm-w]]
- [[concepts/np-hardness]]
- [[sources/do2006]]、[[sources/josh2010]]

## 更新紀錄

- JOSH2010：新增 Algorithm W 的結果與尚未解決的情形。
