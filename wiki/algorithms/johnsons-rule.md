---
title: Johnson's rule
type: algorithm
sources: [EJOR2009]
status: 已確認
updated: 2026-11-16
---

## 適用的問題

二機流程工廠最小化 makespan（$F2\mid\mid C_{\max}$），以及與它等價的單一工作隊 relocation problem 求最小初始資源量 [EJOR2009 §1, §5]。

## 規則

對任兩個工作 $J_i$、$J_j$，若 $\min\{p_i, q_j\} \le \min\{q_i, p_j\}$，就把 $J_i$ 排在 $J_j$ 前面 [EJOR2009 §1]。

## 兩種執行方式

### Form 1（教科書常見的寫法）

1. 在所有還沒排的工序中，找出加工時間最短的那一個 [EJOR2009 §1]。
2. 如果它是第一台機器的工序，把這個工作排到目前最前面的空位；如果是第二台機器的工序，排到目前最後面的空位 [EJOR2009 §1]。
3. 把這個工作移除，重複到全部排完 [EJOR2009 §1]。

### Form 2（分兩組排序）

1. 把工作分成兩組：$p_i \le q_i$ 的一組，$p_i > q_i$ 的一組 [EJOR2009 §1]。
2. 第一組依 $p_i$ 由小到大排，第二組依 $q_i$ 由大到小排 [EJOR2009 §1]。
3. 第一組在前、第二組在後接起來 [EJOR2009 §1]。

兩種方式都需要排序，所以時間複雜度是 $O(n\log n)$ [EJOR2009 §1]。

## 用 relocation problem 來理解 Form 2

把每個工作想成一個投資專案，要先投入 $\alpha_i$、完成後回收 $\beta_i$，目標是讓起始資金最少 [EJOR2009 §5]。

- 不賠錢的專案（$\beta_i \ge \alpha_i$）先做，依投入金額 $\alpha_i$ 由小到大 [EJOR2009 §5]。
- 會賠錢的專案（$\beta_i < \alpha_i$）後做，依回收金額 $\beta_i$ 由大到小 [EJOR2009 §5]。
- 為什麼這樣排合理：門檻低又會賺的先做，賺到的錢可以拿去做門檻高的；回收最少的留到最後，因為最後一個專案回收多少已經不影響別的專案。這兩句理由是本 Wiki 的解讀，原文只給出排法（推論）。

## 小例子

四個工作的 $(p_i, q_i)$：A (3, 5)、B (6, 2)、C (2, 4)、D (5, 4)（自編例子 E1）。

1. 分組：A、C 屬於 $p_i \le q_i$；B、D 屬於 $p_i > q_i$（自編例子 E1）。
2. 第一組依 $p_i$ 由小到大：C (2)、A (3)。第二組依 $q_i$ 由大到小：D (4)、B (2)（自編例子 E1）。
3. 接起來得到 C→A→D→B，makespan 為 18；若照 A→B→C→D 做則是 20（自編例子 E1）。
4. 換成 relocation problem 來看，同一個順序需要的最小初始資源量是 3，把 24 種順序全部試過也找不到更小的（自編例子 E1）。

```gantt
{"example": "E1-flowshop", "rows": [{"label": "M1", "bars": [{"job": "C", "start": 0, "end": 2}, {"job": "A", "start": 2, "end": 5}, {"job": "D", "start": 5, "end": 10}, {"job": "B", "start": 10, "end": 16}]}, {"label": "M2", "bars": [{"job": "C", "start": 2, "end": 6}, {"job": "A", "start": 6, "end": 11}, {"job": "D", "start": 11, "end": 15}, {"job": "B", "start": 16, "end": 18}]}], "caption": "Johnson 順序 C→A→D→B：makespan 18，M2 閒置共 3"}
```

## 為什麼是對的

標準的證明是交換論證：假設最佳順序中有兩個相鄰的工作違反規則，把它們對調後 makespan 不會變大 [EJOR2009 §3]。原文另外用 [[concepts/composite-job]] 把論證推廣到不相鄰的兩個工作，並在 relocation problem 的情境下分三種情形說明對調後仍然可行 [EJOR2009 §3, §5]。

## 相關頁面

- [[concepts/two-machine-flowshop]]、[[concepts/composite-job]]、[[concepts/relocation-problem]]
- [[sources/ejor2009]]
