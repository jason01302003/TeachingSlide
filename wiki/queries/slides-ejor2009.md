---
title: 簡報稿｜Johnson's rule 與 relocation problem
type: query
sources: [EJOR2009]
deck: ejor2009
summary: 從公共住宅重建的故事出發，看為什麼「先做哪一個」會決定計畫做不做得成，以及一條簡單的規則如何找到最省資源的順序。
status: 已確認
updated: 2026-11-16
---

# Relocation Problem 是什麼？從 Johnson's rule 看起

## Relocation Problem 是什麼？
kind:: title
wiki:: [[sources/ejor2009]]

Cheng & Lin（2009）導讀：用「先做哪一棟」理解資源限制排程

## 為什麼先做哪一棟很重要
kind:: motivation
wiki:: [[concepts/relocation-problem]]

- 城市要重建好幾棟舊公寓，每棟動工前要先把住戶搬到臨時住宅
- 蓋好之後，新大樓能容納的人可能比原本多，也可能比原本少
- 臨時住宅有限，所以順序一錯，計畫就卡住
- 這個問題最早來自波士頓的公共住宅重建計畫

## 問題定義：水池與工作
kind:: definition
wiki:: [[concepts/relocation-problem]]

- 一個資源池，一開始有 $v_0$ 單位
- 工作 $J_i$ 開始時取走 $\alpha_i$，完成時歸還 $\beta_i$
- 池中不夠 $\alpha_i$ 就不能開始
- 淨貢獻 $\delta_i=\beta_i-\alpha_i$ 可正可負
- 問：最少要準備多少 $v_0$，才保證有可行的順序？

## 例子：四棟建物，順序決定成敗
kind:: example
wiki:: [[concepts/relocation-problem]]

(取用, 歸還)：A (3, 5)、B (6, 2)、C (2, 4)、D (5, 4)

- 依 A→B→C→D：初始資源至少要 5
- 24 種順序全部試過：最少只要 3，最差要 9
- 達到 3 的順序之一是 C→A→D→B

```levels
{"example": "E1-levels", "v0": 3, "steps": [{"job": "C", "alpha": 2, "beta": 4, "before": 3, "during": 1, "after": 5}, {"job": "A", "alpha": 3, "beta": 5, "before": 5, "during": 2, "after": 7}, {"job": "D", "alpha": 5, "beta": 4, "before": 7, "during": 2, "after": 6}, {"job": "B", "alpha": 6, "beta": 2, "before": 6, "during": 0, "after": 2}], "caption": "依 C→A→D→B 的順序，初始資源 3 就夠用"}
```

## 主要結果：它就是二機流程工廠
kind:: result
wiki:: [[concepts/two-machine-flowshop]]

把取用量當第一台機器的加工時間 $p_i$，歸還量當第二台機器的加工時間 $q_i$：

$$\text{第二台機器的閒置時間總和} = \text{該順序需要的初始資源量 } v_0$$

- 所以找最小 $v_0$，等於找最小的 makespan
- 同一組數字：C→A→D→B 的 makespan 是 18、閒置 3；A→B→C→D 是 20、閒置 5

```gantt
{"example": "E1-flowshop", "rows": [{"label": "M1", "bars": [{"job": "C", "start": 0, "end": 2}, {"job": "A", "start": 2, "end": 5}, {"job": "D", "start": 5, "end": 10}, {"job": "B", "start": 10, "end": 16}]}, {"label": "M2", "bars": [{"job": "C", "start": 2, "end": 6}, {"job": "A", "start": 6, "end": 11}, {"job": "D", "start": 11, "end": 15}, {"job": "B", "start": 16, "end": 18}]}], "caption": "Johnson 順序 C→A→D→B：makespan 18，M2 閒置共 3"}
```

## 方法：Johnson's rule
kind:: method
wiki:: [[algorithms/johnsons-rule]]

1. 把工作分成兩組：$p_i \le q_i$（不賠）與 $p_i > q_i$（會賠）
2. 不賠的依 $p_i$ 由小到大排在前面
3. 會賠的依 $q_i$ 由大到小排在後面

投資的說法：不賠錢的專案先做、門檻低的先；賠錢的專案後做、回收多的先。

四棟的例子：A、C 不賠 → C、A；B、D 會賠 → D、B；得到 C→A→D→B。

## Composite job：把一串工作打包
kind:: caveat
wiki:: [[concepts/composite-job]]

- 一串連續的工作，可以換成一個假想的工作，對第二台機器造成的閒置時間完全相同
- 例子中 C→A→D→B 打包後是 $(p^*, q^*) = (3, 2)$，$p^*=3$ 正是需要的最小初始資源量
- 用處：讓幾個相關問題的計算時間下降，例如 $O(n^2\log n)$ 降為 $O(n\log n)$

## 回顧
kind:: recap
wiki:: [[sources/ejor2009]], [[concepts/relocation-problem]]

- Relocation problem：先取用、後歸還的資源池，歸還量可多可少
- 只問最少初始資源時，它和二機流程工廠是同一個問題
- Johnson's rule 在 $O(n\log n)$ 時間找到最省資源的順序
- 一旦多一個工作隊或加上時間目標，問題就變難，這是其他幾份簡報的主題

## 延伸閱讀
kind:: further
wiki:: [[further-reading/ejor2009]]

（由 further-reading 頁產生）
