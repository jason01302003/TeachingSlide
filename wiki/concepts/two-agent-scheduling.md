---
title: 雙代理人排程（Two-agent scheduling）
type: concept
sources: [TSWJ2014]
status: 已確認
updated: 2026-11-16
---

## 白話說明

傳統排程假設所有工作有同一個目標。雙代理人排程則是兩位「客戶」共用同一台機器，各自有自己的一批工作、各自在意不同的事。排程者要在兩邊的要求之間取捨（白話說明）。

## 設定

- 傳統排程中所有工作有共同的目標；多代理人排程中，工作來自不同的客戶，各有各的目標 [TSWJ2014 §1]。
- 常見的問法是：在第二個代理人的要求被滿足的前提下，讓第一個代理人的目標最好 [TSWJ2014 §1, §2]。
- TSWJ2014 研究的版本：$AG_1$ 要讓總延遲時間與總完工時間的加權組合 $\sum(\theta T_j+(1-\theta)C_j)$ 最小，$AG_2$ 要求自己的工作都不延遲 [TSWJ2014 §2]。

## 兩邊的要求為什麼會衝突

- 只看 $AG_1$ 的總完工時間，短的工作先做（SPT）最好 [TSWJ2014 §4]。
- 要檢查 $AG_2$ 的工作會不會延遲，TSWJ2014 用的是交期早的先做（EDD）[TSWJ2014 Property 2]。
- 兩個規則排出來的順序通常不一樣，所以需要搜尋 [TSWJ2014 §3]；「通常不一樣」是本 Wiki 的補充（推論）。

## 小例子

五個工作，$\theta=1/2$：$AG_1$ 有 a1 (工時 3, 交期 6)、a2 (2, 9)、a3 (5, 12)；$AG_2$ 有 b1 (4, 6)、b2 (3, 16)（自編例子 E6）。

| 排法 | 順序 | 可行嗎 | $AG_1$ 的目標值 |
|---|---|---|---|
| 全部照 SPT（自編例子 E6） | a2→a1→b2→b1→a3 | 不可行，b1 在 12 才完成，超過交期 6 | 14.5（若不管 $AG_2$） |
| $AG_2$ 先做完再做 $AG_1$（自編例子 E6） | b1→b2→a2→a1→a3 | 可行 | 24.5 |
| 最佳解（窮舉）（自編例子 E6） | a2→b1→a1→b2→a3 | 可行 | 18 |

120 種順序中只有 22 種可行（自編例子 E6）。最佳解把 a2 插在 b1 前面、把 a1 插在 b2 前面，剛好讓 b1 在交期 6 完成：既不讓 $AG_2$ 延遲，也不讓 $AG_1$ 全部排到最後（自編例子 E6）。

```gantt
{"example": "E6-opt", "rows": [{"label": "機器", "bars": [{"job": "a2", "start": 0, "end": 2, "group": 1}, {"job": "b1", "start": 2, "end": 6, "group": 2}, {"job": "a1", "start": 6, "end": 9, "group": 1}, {"job": "b2", "start": 9, "end": 12, "group": 2}, {"job": "a3", "start": 12, "end": 17, "group": 1}]}], "caption": "最佳順序 a2→b1→a1→b2→a3：目標值 18"}
```

## 怎麼解

- 求最佳解：[[algorithms/branch-and-bound]]，在 TSWJ2014 的實驗中可處理到 24 個工作 [TSWJ2014 §5]。
- 求近似解：[[algorithms/simulated-annealing]]，可處理 100、200 個工作 [TSWJ2014 §5]。

## 與本 Wiki 其他部分的關係

這個分支沒有資源限制，與 [[concepts/relocation-problem]] 沒有直接關係；共通之處只有都是機器排程、都用到完工時間這類目標、都面對 NP-hard 的問題（推論）。

## 相關頁面

- [[sources/tswj2014]]
- [[concepts/objective-functions]]、[[concepts/scheduling-basics]]、[[concepts/np-hardness]]
