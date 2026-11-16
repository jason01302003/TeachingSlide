---
title: 總覽
type: overview
sources: [DO2006, EJOR2009, JOSH2010, TSWJ2014, JOSH2016]
status: 已確認
updated: 2026-11-16
---

## 這個 Wiki 是什麼

這是一個由 AI 依 `CLAUDE.md` 的規則撰寫與維護的排程論文知識庫。來源是使用者放在 `raw/` 的論文；每加入一篇，AI 會寫一頁來源摘要，並更新相關的概念頁、演算法頁與比較表。

## 目前收錄

- 已 ingest 5 篇：[[sources/do2006]]、[[sources/ejor2009]]、[[sources/josh2010]]、[[sources/tswj2014]]、[[sources/josh2016]]。

## 主線：Relocation problem

[[concepts/relocation-problem]] 來自公共住宅重建：每件工作開工要先取用資源，完工後歸還的資源量可多可少。只有一個工作隊時，判斷計畫可不可行是容易的，而且它和二機流程工廠是同一個問題，用 [[algorithms/johnsons-rule]] 就能找到最省資源的順序 [EJOR2009 §5]；一旦有兩個工作隊可以同時施工，要讓工期最短就變成 strongly NP-hard [DO2006 §1, Thm 2]。另一個讓問題變難的方向是把目標換成跟時間有關的總加權完工時間：即使只有一台機器也是 strongly NP-hard [JOSH2010 Thm 1, Thm 2]。面對這些難題，研究者改成設計有效能保證的近似演算法（[[algorithms/rounding-and-splitting]]、[[algorithms/algorithm-w]]）。

最後一塊是把問題拆小：如果機器的指派與順序都已經定了，只決定開始時間，會不會變簡單？答案是看目標而定，有的可以用動態規劃快速解決，有的仍然是 NP-hard [JOSH2016 Thm 1, Thm 2]。見 [[concepts/fixed-sequence]] 與 [[algorithms/backward-dp]]。

四篇 relocation problem 論文合起來的圖像是：問題本身很簡單（一台機器、只問可不可行），但往任何一個方向多走一步（多一台機器、多一個跟時間有關的目標）就變難；研究者的回應分別是近似演算法與「找出還能精確求解的特例」（推論）。

## 另一個分支：雙代理人排程

[[concepts/two-agent-scheduling]] 沒有資源限制，問的是兩位客戶共用一台機器時怎麼取捨：一方要早完成、少延遲，另一方要求完全不延遲 [TSWJ2014 §2]。這個問題同樣是 NP-hard，TSWJ2014 的對策是 [[algorithms/branch-and-bound]]（求最佳解）與 [[algorithms/simulated-annealing]]（求近似解）[TSWJ2014 §3, §4]。它和 relocation problem 的主線沒有直接關係，放在同一個 Wiki 是因為面對難題的思路可以互相對照（推論）。

## 從哪裡開始讀

- 想先懂問題：[[concepts/relocation-problem]]
- 想看結論：[[comparisons/complexity-table]]、[[comparisons/papers-at-a-glance]]
- 想知道哪些地方還不確定：[[open-questions]]
- 全部頁面：[[index]]；操作紀錄：[[log]]
