---
title: 資源限制排程（Resource-constrained scheduling）
type: concept
sources: [DO2006, JOSH2010, JOSH2016]
status: 已確認
updated: 2026-11-16
---

## 白話說明

一般的排程只問「機器什麼時候有空」。資源限制排程多了一個條件：除了機器之外，工作還需要另一種數量有限的東西（錢、空間、庫存）才能開始（白話說明）。

## Relocation problem 特別在哪裡

- 傳統的資源限制排程中，工作用完資源後歸還的量與取用的量相同；relocation problem 允許歸還量 $\beta_i$ 與取用量 $\alpha_i$ 不同，所以淨貢獻可以是正、零或負 [DO2006 §1]。
- 也因此資源池的水位會隨著完成的工作而上升或下降，先做哪個工作會影響後面的工作能不能開始 [DO2006 §1]。
- JOSH2010 把這一點說成：relocation problem 是傳統資源限制的推廣，因為歸還量可以小於、等於或大於取用量 [JOSH2010 §1]。
- JOSH2016 所說的資源，指的是機器以外的東西，例如資金、住宅容量或庫存 [JOSH2016 §1]。庫存限制排程與 relocation problem 互有包含關係，視問題的定義而定 [JOSH2016 §6]。

## 更新紀錄

- JOSH2016：補上資源的例子與庫存限制排程。
- JOSH2010：補上「傳統資源限制的推廣」的說法。

## 相關頁面

- [[concepts/relocation-problem]]
- [[sources/do2006]]、[[sources/josh2010]]、[[sources/josh2016]]
