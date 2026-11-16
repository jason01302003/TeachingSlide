# 內容目錄

每次 ingest 後更新。查詢時先讀這一頁找相關頁面。

## 總覽

- [[overview]]：Wiki 的範圍、主線與閱讀入口
- [[open-questions]]：待確認與原文不一致之處的總表
- [[log]]：操作與檢查紀錄

## 來源（論文）

- [[sources/do2006]]：Kononov & Lin (2006)，多個工作隊的 relocation problem；兩台機器即 strongly NP-hard，近似比 2 與 3−2/m
- [[sources/ejor2009]]：Cheng & Lin (2009)，Johnson's rule、composite job，以及 relocation problem 與二機流程工廠的等價
- [[sources/josh2010]]：Kononov & Lin (2010)，單機 relocation problem 的總加權完工時間；四個特例 strongly NP-hard，Algorithm W 近似比 2
- [[sources/tswj2014]]：Lee 等 (2014)，雙代理人單機排程；branch-and-bound 與兩種模擬退火（獨立分支）
- [[sources/josh2016]]：Lin, Hwang & Kononov (2016)，兩台專用機、順序固定的 relocation 排程；六種目標的複雜度分界與動態規劃

## 概念

- [[concepts/relocation-problem]]：問題的故事、模型與小例子
- [[concepts/resource-constrained-scheduling]]：資源限制排程，以及 relocation problem 特別在哪裡
- [[concepts/parallel-machines]]：相同機與專用機；為什麼多了機器反而變難
- [[concepts/fixed-sequence]]：順序已定、只決定開始時間的問題，以及它為什麼不簡單
- [[concepts/scheduling-basics]]：工作、機器、流程工廠與三欄記號
- [[concepts/two-machine-flowshop]]：二機流程工廠，以及它為什麼等於單一工作隊的 relocation problem
- [[concepts/composite-job]]：把一串工作濃縮成一個等效工作
- [[concepts/two-agent-scheduling]]：兩位客戶共用一台機器時的取捨，含五個工作的小例子
- [[concepts/objective-functions]]：排程要最佳化什麼
- [[concepts/np-hardness]]：NP-hard 與 strongly NP-hard 的白話解釋與證明方式
- [[concepts/approximation-algorithm]]：近似比的定義、正面與負面結果

## 演算法

- [[algorithms/johnsons-rule]]：二機流程工廠的最佳排法、兩種寫法與投資觀點的解釋
- [[algorithms/algorithm-w]]：輪流依權重與淨貢獻挑工作的 2 倍近似演算法，含原文例子的逐步執行
- [[algorithms/backward-dp]]：用排程區塊做動態規劃的三種演算法（BDP-1、BDP-2、FDP）
- [[algorithms/branch-and-bound]]：用支配性質、可行性與下界剪枝來求最佳解
- [[algorithms/simulated-annealing]]：隨機對調加上逐漸降低的接受機率，兩個版本的差別
- [[algorithms/rounding-and-splitting]]：放寬、補整、拆開三步驟的近似演算法與小例子

## 跨論文比較

- [[comparisons/complexity-table]]：各問題版本的複雜度與近似結果
- [[comparisons/papers-at-a-glance]]：每篇論文的機器環境、目標、方法與主要結果

## 簡報稿與延伸閱讀

- [[queries/slides-ejor2009]]：Relocation Problem 是什麼？從 Johnson's rule 看起；延伸閱讀見 [[further-reading/ejor2009]]
- [[queries/slides-do2006]]：多個工作隊：人手變多，問題反而變難；延伸閱讀見 [[further-reading/do2006]]
- [[queries/slides-josh2010]]：重要的工作先做？資源說了算；延伸閱讀見 [[further-reading/josh2010]]
- [[queries/slides-josh2016]]：順序都定好了，還有什麼好決定？；延伸閱讀見 [[further-reading/josh2016]]
- [[queries/slides-tswj2014]]：兩位客戶共用一台機器；延伸閱讀見 [[further-reading/tswj2014]]
