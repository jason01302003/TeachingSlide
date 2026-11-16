---
title: 簡報稿｜relocation problem 的總加權完工時間
type: query
sources: [JOSH2010]
deck: josh2010
summary: 重要的工作想先做，卻因為資源不夠而不能開始；單機、工時都是 1 的情形就已經 strongly NP-hard，這份簡報看 Algorithm W 怎麼保證不會差超過兩倍。
status: 已確認
updated: 2026-11-16
---

# 重要的工作先做？資源說了算

## 重要的工作先做？資源說了算
kind:: title
wiki:: [[sources/josh2010]]

Kononov & Lin（2010）導讀

## 沒有資源限制時，答案很簡單
kind:: motivation
wiki:: [[concepts/objective-functions]], [[algorithms/algorithm-w]]

- 每個工作有權重 $w_i$，權重大代表越早完成越好
- 沒有資源限制時，WSPT 規則（權重大又快做完的先做）就能得到最佳解
- 加上資源限制後：想先做的工作，可能因為資源不夠而不能開始

## 問題定義：單機、加權完工時間
kind:: definition
wiki:: [[sources/josh2010]], [[concepts/objective-functions]]

- 一台機器；工作有加工時間 $p_i$、權重 $w_i$、取用 $\alpha_i$、歸還 $\beta_i$
- 初始資源 $v_0$；順序必須可行
- 目標：總加權完工時間 $\sum w_iC_i$ 最小
- 作者說，這個目標在 relocation problem 裡是第一次被研究

## 例子：WSPT 排出不可行的順序
kind:: example
wiki:: [[algorithms/algorithm-w]]

四個工作，工時都是 1，初始資源 0。$J_4$ 權重 5，但需要 10 單位資源。

- WSPT 想先做 $J_4$，但池子是空的，做不了
- 若不管資源硬排，總加權完工時間是 14
- 可行排程的最佳值是 26：先做完 $J_1$、$J_2$、$J_3$ 湊到 10 單位，才輪到 $J_4$

## 主要結果：四個特例都是 strongly NP-hard
kind:: result
wiki:: [[sources/josh2010]], [[concepts/np-hardness]], [[comparisons/complexity-table]]

- 工時為 1 且淨貢獻非正：strongly NP-hard
- 工時為 1 且淨貢獻非負：strongly NP-hard
- 「工時都是 1」與「權重都是 1」完全等價，所以另外兩個特例也是
- 證明從 Ordered Numerical 3-Dimensional Matching 歸約

只有一台機器，就已經很難。

## 方法：Algorithm W
kind:: method
wiki:: [[algorithms/algorithm-w]]

兩個理由值得先做：比較重要，或能生出比較多資源。兩個理由輪流用：

1. 準備兩份名單：$\pi_1$ 依權重由大到小，$\pi_2$ 依淨貢獻由大到小
2. 奇數位置：從 $\pi_1$ 挑第一個資源夠的工作
3. 偶數位置：從 $\pi_2$ 挑第一個資源夠的工作
4. 找不到資源夠的工作，就代表真的沒有可行排程

執行時間 $O(n^2)$。

## 例子：Algorithm W 一步步排
kind:: example
wiki:: [[algorithms/algorithm-w]]

| 位置 | 看哪份名單 | 選到 | 資源 |
|---|---|---|---|
| 1 | 權重 | $J_1$ | 0 → 2 |
| 2 | 貢獻 | $J_3$ | 2 → 7 |
| 3 | 權重 | $J_2$ | 7 → 10 |
| 4 | 貢獻 | $J_4$ | 10 → 10 |

順序 J1→J3→J2→J4，總加權完工時間 26，剛好是最佳值。

## 保證與注意事項
kind:: caveat
wiki:: [[algorithms/algorithm-w]], [[sources/josh2010]]

- 近似比 2，而且是緊的：$n$ 越大，比值越接近 2
- 例如 $n=6$ 時 Algorithm W 得到 9、最佳 6；$n=100$ 時是 2500 對 1275
- 原文緊例的封閉式印成 $(n^2-n)/4$，但實際算出來是 $n^2/4$（待確認）
- 另外兩個特例與一般情形，能不能近似仍是未解問題

## 回顧
kind:: recap
wiki:: [[sources/josh2010]], [[algorithms/algorithm-w]]

- 只問可不可行時，單機很簡單；一旦在意「多快做完」，就變 strongly NP-hard
- 規則好用與否取決於目標：WSPT 在沒有資源限制時最佳，加上資源限制就可能不可行
- Algorithm W 輪流考慮「重要」與「會生資源」，得到 2 倍保證
- 下一步：如果機器與順序都先固定，只決定開始時間呢？（見 JOSH2016 簡報）

## 延伸閱讀
kind:: further
wiki:: [[further-reading/josh2010]]

（由 further-reading 頁產生）
