---
title: NP-hard 與 strongly NP-hard
type: concept
sources: [DO2006, JOSH2010, TSWJ2014, JOSH2016]
status: 已確認
updated: 2026-11-16
---

## 白話說明

說一個問題是 NP-hard，意思是目前沒有人知道能在合理時間內保證找到最佳解的方法，而且一般相信這種方法不存在。工作數一多，把所有可能都試一遍的時間會爆炸性成長（白話說明）。

strongly NP-hard 是更強的說法：即使題目裡的數字都不大，問題仍然很難。只是「普通意義下」NP-hard 的問題，有時可以用執行時間跟數字大小有關的演算法（pseudo-polynomial）解決；strongly NP-hard 的問題連這條路都走不通（白話說明）。

## 怎麼證明

證明的方式是「歸約」：拿一個已知很難的問題，說明只要能解眼前的排程問題，就能解那個已知的難題（白話說明）。

| 已知的難題 | 被用來證明什麼 | 出處 |
|---|---|---|
| Numerical Matching with Target Sums（由 Numerical 3-Dimensional Matching 得到） | 兩台專用機、淨貢獻為正、UET 的 relocation problem 是 strongly NP-hard | [DO2006 Thm 1] |
| Partition | 機器數不限時，沒有漸近近似比小於 $4/3$ 的演算法 | [DO2006 Thm 3] |
| Ordered Numerical 3-Dimensional Matching（由 Numerical 3-Dimensional Matching 得到） | 單機、UET 的總加權完工時間問題是 strongly NP-hard | [JOSH2010 Thm 1, Thm 2] |
| Partition | 兩台專用機、順序固定時，最小化 $\sum w_jT_j$ 或 $\sum w_jU_j$ 是 NP-hard（普通意義） | [JOSH2016 Thm 2, Thm 3] |

## 普通意義與 strong 的差別，用一個例子看

順序固定的問題中，$\sum w_jT_j$ 是普通意義下的 NP-hard，而且有一個執行時間與加工時間總和成正比的動態規劃 [JOSH2016 Thm 2, Thm 4]。當所有工作的加工時間都相同時，這個演算法就變成多項式時間 [JOSH2016 §4]。這正是「數字不大時其實可以解」的意思；strongly NP-hard 的問題沒有這種出路（白話說明）。

## 本 Wiki 收錄的難度結果

完整列表見 [[comparisons/complexity-table]]。

- 兩台相同機器、UET、淨貢獻為正：strongly NP-hard [DO2006 Thm 2]。原文結論把同一件事寫成 unary NP-hard，兩個說法指的是同一個性質 [DO2006 §6]。
- 單機、最小化 $\sum w_iC_i$：$\delta_i\le 0$ 或 $\delta_i\ge 0$ 搭配 $p_i=1$，以及 $\delta_i\ge 0$ 或 $\delta_i\le 0$ 搭配 $w_i=1$，四個特例都是 strongly NP-hard [JOSH2010 Thm 1, Thm 2, Cor. 1, Cor. 2]。
- 後兩個特例不是另外證明的，而是由「UET 情形與單位權重情形完全等價」直接推得 [JOSH2010 Thm 3]。把一個問題轉成另一個已經知道答案的問題，是省力的常見做法（白話說明）。
- 雙代理人單機排程：它包含單機總延遲時間問題這個已知的 NP-hard 問題作為特例（沒有第二個代理人、$\theta=1$），所以也是 NP-hard [TSWJ2014 §3]。這是最簡單的一種難度論證：指出問題裡面藏著一個已知的難題（白話說明）。
- 兩台專用機、順序不固定：由 DO2006 與 JOSH2010 的結果可推得最小化 makespan 與總完工時間都是 strongly NP-hard，與交期有關的目標也是 [JOSH2016 §1]。

## 更新紀錄

- JOSH2016：新增固定順序問題的難度結果，以及普通意義與 strong 的對照例子。
- TSWJ2014：新增雙代理人單機排程的難度說明。
- JOSH2010：新增單機總加權完工時間的四個難度結果與所用的歸約。

## 相關頁面

- [[concepts/approximation-algorithm]]、[[concepts/parallel-machines]]
- [[sources/do2006]]、[[sources/josh2010]]、[[sources/tswj2014]]、[[sources/josh2016]]
