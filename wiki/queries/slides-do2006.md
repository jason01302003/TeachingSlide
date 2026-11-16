---
title: 簡報稿｜多個工作隊的 relocation problem
type: query
sources: [DO2006]
deck: do2006
summary: 多一個工作隊可以同時施工，聽起來是好事，卻讓問題從容易變成 strongly NP-hard；這份簡報看研究者怎麼退一步，用近似演算法換取有保證的答案。
status: 已確認
updated: 2026-11-16
---

# 多個工作隊：人手變多，問題反而變難

## 多個工作隊：人手變多，問題反而變難
kind:: title
wiki:: [[sources/do2006]]

Kononov & Lin（2006）導讀

## 只有一個工作隊時很簡單
kind:: motivation
wiki:: [[concepts/parallel-machines]], [[concepts/relocation-problem]]

- 一個工作隊時，判斷計畫可不可行，只要 $O(n\log n)$ 時間
- 現實中常有好幾隊同時施工，只要有空閒的隊伍、也夠資源，就可以重疊
- 直覺：人手多應該更好排
- 事實：只要有兩個工作隊，要讓工期最短就已經很難

## 問題定義：加上時間與工作隊
kind:: definition
wiki:: [[sources/do2006]], [[concepts/parallel-machines]]

- 資源池、取用 $\alpha_i$、歸還 $\beta_i$ 的規則不變
- 多個相同的工作隊（機器）可以同時各做一個工作，條件是資源夠
- 工作不可中斷；本文假設每個工作的工時都是 1
- 目標：全部完成的時間（makespan）最小

## 例子：多一隊並沒有讓工期減半
kind:: example
wiki:: [[concepts/parallel-machines]]

六個工時為 1 的工作，初始資源 4：

- 一個工作隊：要 6 個時段
- 兩個工作隊：要 4 個時段
- 工作隊數不限：還是 4 個時段

卡住進度的是資源，不是人手。

```gantt
{"example": "E4-opt-m2", "rows": [{"label": "隊 1", "bars": [{"job": "A", "start": 0, "end": 1}, {"job": "C", "start": 1, "end": 2}, {"job": "F", "start": 2, "end": 3}, {"job": "D", "start": 3, "end": 4}]}, {"label": "隊 2", "bars": [{"job": "B", "start": 0, "end": 1}, {"job": "E", "start": 3, "end": 4}]}], "caption": "2 個工作隊的最佳排程：4 個時段"}
```

## 主要結果：兩個工作隊就是 strongly NP-hard
kind:: result
wiki:: [[concepts/np-hardness]], [[concepts/approximation-algorithm]], [[comparisons/complexity-table]]

- 兩台相同機器、工時為 1、淨貢獻為正：strongly NP-hard
- 兩台專用機也一樣；證明是從數字配對問題歸約
- 機器數不限時，問題等價於 Bin Packing
- 除非 P = NP，近似比不可能小於 $3/2$；漸近近似比不可能小於 $4/3$

白話：沒有已知的快速精確解法，連很接近最佳的答案都有極限。

## 方法：放寬、補整、拆開
kind:: method
wiki:: [[algorithms/rounding-and-splitting]]

1. **放寬**：假裝工作可以切成片段，每個時段挑能歸還最多資源的組合，這很好解
2. **Rounding**：被切開的工作，補成完整的一個時段
3. **Splitting**：時段裡的工作超過工作隊數時，拆成連續的幾個時段

## 例子：近似解 5、最佳解 4
kind:: example
wiki:: [[algorithms/rounding-and-splitting]]

- 放寬後得到 4 個時段，其中 C 與 E 被切開
- Rounding 把它們補整，變成 5 個時段
- 窮舉的最佳解是 4 個時段，近似比值 1.25

```gantt
{"example": "E4-rounded", "rows": [{"label": "隊 1", "bars": [{"job": "A", "start": 0, "end": 1}, {"job": "D", "start": 1, "end": 2}, {"job": "C", "start": 2, "end": 3}, {"job": "F", "start": 3, "end": 4}, {"job": "E", "start": 4, "end": 5}]}, {"label": "隊 2", "bars": [{"job": "B", "start": 0, "end": 1}]}], "caption": "Rounding 的結果（不限工作隊數）：5 個時段"}
```

## 保證有多好，以及要注意什麼
kind:: caveat
wiki:: [[algorithms/rounding-and-splitting]], [[sources/do2006]]

- Rounding：機器數不限時，近似比 2
- Splitting：$m$ 台機器時，近似比 $3-2/m$
- 兩個近似比都是緊的：原文構造出剛好達到的例子
- 原文結論把 $4/3$ 寫成一般近似比的下界，但定理講的是漸近近似比（待確認）

## 回顧
kind:: recap
wiki:: [[sources/do2006]], [[comparisons/complexity-table]]

- 單一工作隊容易；兩個工作隊就是 strongly NP-hard
- 難的來源是資源的限制，不是機器數量
- 退一步的做法：先放寬、再補整、再拆開，換到有倍數保證的答案
- 下一步：把目標換成跟時間有關的總加權完工時間（見 JOSH2010 簡報）

## 延伸閱讀
kind:: further
wiki:: [[further-reading/do2006]]

（由 further-reading 頁產生）
