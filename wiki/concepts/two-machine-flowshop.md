---
title: 二機流程工廠與 relocation problem 的等價
type: concept
sources: [EJOR2009, DO2006]
status: 已確認
updated: 2026-11-16
---

## 白話說明

想像一條只有兩站的生產線：每件產品都要先過第一站、再過第二站。第一站可以一件接一件不停地做，但第二站有時要「等」第一站把東西送過來，這段等待就是閒置時間（白話說明）。

## 問題

- $F2\mid\mid C_{\max}$：$n$ 個工作依序經過兩台機器，加工時間為 $p_i$、$q_i$，要找 makespan 最小的順序 [EJOR2009 §1]。
- 這是排程領域最早、最著名的結果之一，Johnson 在 1954 年給出解法 [EJOR2009 §1]。解法見 [[algorithms/johnsons-rule]]。

## 關鍵觀察

makespan 等於「第二台機器的加工時間總和」加上「第二台機器的閒置時間總和」。前者是固定的，所以要讓 makespan 最小，只要讓第二台機器的閒置時間最少 [EJOR2009 §2]。

## 與 relocation problem 的等價

把 relocation problem 的每個工作對應成流程工廠的一個工作：取用量 $\alpha_i$ 當作第一台機器的加工時間 $p_i$，歸還量 $\beta_i$ 當作第二台機器的加工時間 $q_i$。那麼對同一個順序 [EJOR2009 §5]：

$$\text{第二台機器的閒置時間總和} \;=\; \text{讓這個順序可行所需的初始資源量 } v_0$$

- 這個等價關係由 Kaplan 與 Amir 在 1988 年提出 [EJOR2009 §5]。
- 因此「找最小的 $v_0$」與「找最小的 makespan」是同一個問題，都可以用 Johnson's rule 在 $O(n\log n)$ 時間解決 [EJOR2009 §1, §5]。
- DO2006 也引用同一個結果，用來說明單一工作隊的可行性可以在 $O(n\log n)$ 時間判定 [DO2006 §1]。

## 小例子

四個工作 A、B、C、D，$(p_i, q_i)$ 分別是 (3, 5)、(6, 2)、(2, 4)、(5, 4)，與 [[concepts/relocation-problem]] 的四棟建物是同一組數字（自編例子 E1）。

| 順序 | makespan | 第二台機器閒置 | 對應的最小 $v_0$ |
|---|---|---|---|
| C→A→D→B（Johnson 順序）（自編例子 E1） | 18 | 3 | 3 |
| A→B→C→D（自編例子 E1） | 20 | 5 | 5 |

第二台機器的加工時間總和是 15，所以 makespan 分別是 15 + 3 = 18 與 15 + 5 = 20，閒置時間正好等於另一邊算出的初始資源量（自編例子 E1）。

```gantt
{"example": "E1-flowshop", "rows": [{"label": "M1", "bars": [{"job": "C", "start": 0, "end": 2}, {"job": "A", "start": 2, "end": 5}, {"job": "D", "start": 5, "end": 10}, {"job": "B", "start": 10, "end": 16}]}, {"label": "M2", "bars": [{"job": "C", "start": 2, "end": 6}, {"job": "A", "start": 6, "end": 11}, {"job": "D", "start": 11, "end": 15}, {"job": "B", "start": 16, "end": 18}]}], "caption": "Johnson 順序 C→A→D→B：makespan 18，M2 閒置共 3"}
```

```gantt
{"example": "E1-flowshop-abcd", "rows": [{"label": "M1", "bars": [{"job": "A", "start": 0, "end": 3}, {"job": "B", "start": 3, "end": 9}, {"job": "C", "start": 9, "end": 11}, {"job": "D", "start": 11, "end": 16}]}, {"label": "M2", "bars": [{"job": "A", "start": 3, "end": 8}, {"job": "B", "start": 9, "end": 11}, {"job": "C", "start": 11, "end": 15}, {"job": "D", "start": 16, "end": 20}]}], "caption": "順序 A→B→C→D：makespan 20，M2 閒置共 5"}
```

## 相關頁面

- [[algorithms/johnsons-rule]]、[[concepts/composite-job]]、[[concepts/relocation-problem]]、[[concepts/scheduling-basics]]
- [[sources/ejor2009]]、[[sources/do2006]]
