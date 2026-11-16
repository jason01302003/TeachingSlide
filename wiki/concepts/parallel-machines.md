---
title: 平行機器：相同機與專用機
type: concept
sources: [DO2006, JOSH2016]
status: 已確認
updated: 2026-11-16
---

## 白話說明

「平行機器」是指有好幾台機器（或好幾個工作隊）可以同時各做一件工作。在 relocation problem 裡，就是好幾棟建物可以同時施工（白話說明）。

## 兩種平行機器

| 種類 | 意思 | 出處 |
|---|---|---|
| 相同機（identical parallel machines） | 任何工作可以交給任何一台機器，代號 $RP$ | [DO2006 §1, §4] |
| 專用機（dedicated parallel machines） | 每個工作事先指定只能在某一台機器上做，代號 $RPD$；$RPD_m$ 表示有 $m$ 台 | [DO2006 §3]、[JOSH2016 §1] |

## 為什麼多了機器反而變難

- 只有一個工作隊時，可行性可以在 $O(n\log n)$ 時間判定 [DO2006 §1]。
- 有兩個工作隊時，即使每個工作都只花 1 單位時間、淨貢獻都為正，要讓 makespan 最小就已經是 strongly NP-hard [DO2006 Thm 2]。
- 如果沒有資源限制，兩台專用機的問題是簡單的；加上資源限制之後才變成 strongly NP-hard [DO2006 §3, Thm 1]。
- 機器數不限、每個工作 $\alpha_i=\beta_i$ 且工時為 1 時，一個時段就像一個箱子，問題等價於 Bin Packing [DO2006 §2]。
- 專用機上如果連每台機器的加工順序都固定，問題是否變簡單要看目標函數：makespan 變成多項式時間可解，但加權的延遲類目標仍是 NP-hard [JOSH2016 Thm 1, Thm 2, Thm 3]。見 [[concepts/fixed-sequence]]。

## 小例子

六個工時為 1 的工作，初始資源 4（自編例子 E4）。窮舉的結果：一個工作隊要 6 個時段，兩個工作隊要 4 個時段，工作隊數不限也還是 4 個時段（自編例子 E4）。多一個工作隊並沒有讓工期減半，再多也沒有用，因為卡住進度的是資源而不是人手（自編例子 E4；推論）。若套用近似演算法，Rounding 會排出 5 個時段，細節見 [[algorithms/rounding-and-splitting]]（自編例子 E4）。

## 相關頁面

- [[concepts/relocation-problem]]、[[concepts/np-hardness]]、[[concepts/fixed-sequence]]
- [[algorithms/rounding-and-splitting]]
- [[sources/do2006]]、[[sources/josh2016]]

## 更新紀錄

- JOSH2016：補上 $RPD_m$ 的記號與「順序固定之後」的結果。
