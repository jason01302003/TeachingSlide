# 操作紀錄

只能往後加。每筆標題格式：`## [日期] 操作 | 標題`。檢查的原始輸出在 `runs/`。

## [2026-11-16] discuss | 主題、來源與做法

- 使用者決定：延續排程論文主題，但不參考作業九，獨立製作；參考 Karpathy 的 LLM Wiki。
- 來源由使用者提供，五篇 PDF 已放在 `raw/`。
- 流程實作採「Claude Code 流程＋檢查腳本」；只做本機檔案。

## [2026-11-16] discuss | 讀完五篇後的重點與疑點

- AI 讀完五篇（含直接看 PDF 頁面確認被文字擷取弄丟的符號），回報每篇一句話摘要與五個疑點（見 `CLAUDE.md` 第 12 節）。
- 使用者決定：`TSWJ2014` 作為獨立分支，只連共通概念；Wiki 重點放在「複雜度結果總表」與「演算法步驟與小例子」；形式為 Markdown ＋自動產生的瀏覽頁。
- 使用者要求：正式執行前先檢查 `CLAUDE.md`。

## [2026-11-16] schema | CLAUDE.md 初稿與兩輪修改

- 初稿：三層架構、來源標註規則、Ingest／Query／Lint、三個檢查點的流程圖。
- 第一輪修改（使用者要求）：數學式改用 LaTeX；新增「延伸閱讀」操作，允許上網搜尋，並加上書目查證檢查點 C3。
- 第二輪修改（使用者更正 AI 的理解）：不是只做一份簡報，而是**每篇論文各一份**，共五份；流程圖改成兩個外圈（ingest 圈、簡報圈）。
- AI 的設計調整：簡報稿改由腳本轉成 HTML，數字核對從最後的簡報檢查提前到簡報稿檢查（C2）。

## [2026-11-16] build | 檢查與建置腳本

- 新增 `scripts/`：`common.py`、`examples.py`、`lint_wiki.py`（C1）、`check_outline.py`（C2）、`check_further_reading.py`（C3）、`build_slides.py`（N6）、`check_slides.py`（C4）、`build_viewer.py`。
- `examples.py` 第一次執行後調整了兩個自編例子的參數：E5 的初始資源由 3 改為 4（原本幾乎完全無法平行，看不出重疊）；E6 改成純 SPT 會讓 AG2 延遲的數字（原本純 SPT 剛好可行，顯示不出兩個代理人的衝突）。
- `CLAUDE.md` 第 4 節補上 `（白話說明）` 標記。

## [2026-11-16] ingest | DO2006

- 新增 `sources/do2006`；新增概念頁 `relocation-problem`、`resource-constrained-scheduling`、`parallel-machines`、`objective-functions`、`np-hardness`、`approximation-algorithm`；新增 `algorithms/rounding-and-splitting`、`comparisons/complexity-table`、`comparisons/papers-at-a-glance`、`overview`、`open-questions`、`index`。共 14 頁。
- 自編例子 E1（四棟建物的最小初始資源）、E4（六個工作、多個工作隊）由 `scripts/examples.py` 計算。
- 寫入 3 項待確認（Q1–Q3）。其中 Q3（Rounding 新時段的插入位置）是實作 E4 時才發現的，不在最初的清單裡。

## [2026-11-16] check | C1 第 1 輪（DO2006）：不通過，5 項錯誤

- 紀錄：`runs/20261116-013309-C1-ingest1-do2006.txt`
- 頁面格式問題 1 項：`rounding-and-splitting` 用粗體當小標題，被當成沒有來源的段落。
- 檢查工具認不得的寫法 4 項：表格裡的 `[[頁面\|別名]]` 被當成斷鏈；獨立一行的數學式、純導覽句（「完整列表見…」）、閱讀說明被當成沒有來源的事實。

## [2026-11-16] fix | 修正頁面與檢查工具；發現檢查工具被改壞

- 頁面：粗體小標題改成 `###` 標題；閱讀說明補上 `（白話說明）`。
- 檢查工具：連結的正規表示式支援 `\|`；去掉連結後不足 30 字的導覽句與獨立數學式不列入檢查。
- **事故**：第一次修改時，指令經過 shell 少了一層反斜線，連結的正規表示式被改壞。重跑檢查卻顯示「通過」（`runs/20261116-013327-C1-ingest1-do2006-retry1.txt`），這個通過是無效的。是在看修改後的檔案內容時才發現。
- 處置：用編輯工具重新修正正規表示式；新增 `scripts/selftest.py`，故意做一個含 11 種錯誤的小 Wiki，確認 lint 每一種都抓得到，而且不會誤判表格內的別名連結。之後每次修改檢查腳本都要先跑自我測試。

## [2026-11-16] check | C1 第 2、3 輪（DO2006）：通過

- 紀錄：`runs/20261116-013407-C1-ingest1-do2006-retry2.txt`（修正正規表示式後）、`runs/20261116-013421-C1-ingest1-do2006-retry3.txt`（自我測試 11 項全數抓到之後再跑一次）。
- 14 頁、0 錯誤。非來源內容的標記：推論 2、自編例子 11、白話說明 11、待確認 4。

## [2026-11-16] ingest | EJOR2009

- 新增 `sources/ejor2009`、`concepts/scheduling-basics`、`concepts/two-machine-flowshop`、`concepts/composite-job`、`algorithms/johnsons-rule`。
- 更新舊頁面：`concepts/relocation-problem`（加入「求最小初始資源量」的版本、與二機流程工廠的等價，並指出 E1 的最佳順序就是 Johnson 順序）、`concepts/objective-functions`、`comparisons/complexity-table`、`comparisons/papers-at-a-glance`、`overview`、`open-questions`（Q4、Q5）、`index`。被更新的概念頁加上「更新紀錄」一節。
- 自己發現並修正：`johnsons-rule` 初稿把「為什麼這樣排合理」的理由掛在 [EJOR2009 §5] 名下，但原文只給排法、沒有給這兩句理由，改標為（推論）。這一項 lint 抓不到，是寫完重讀時發現的。
- 更正上一筆 fix 的說法：正規表示式被改壞的原因只確定是修改指令裡的跳脫字元少了一層反斜線，不確定是哪一層造成的。

## [2026-11-16] check | C1 第 4 輪（EJOR2009）：通過

- 紀錄：`runs/20261116-013705-C1-ingest2-ejor2009.txt`。先跑 `selftest.py`（11 項全數抓到）再跑 lint。
- 19 頁、0 錯誤。標記：推論 4、自編例子 22、白話說明 14、待確認 6。

## [2026-11-16] ingest | JOSH2010

- 新增 `sources/josh2010`、`algorithms/algorithm-w`（含原文 4 個工作例子的逐步執行 E2、緊例族的實際計算 E3）。
- 更新舊頁面：`concepts/relocation-problem`（新增總加權完工時間的版本與「加上時間之後就變難」）、`resource-constrained-scheduling`、`objective-functions`、`np-hardness`、`approximation-algorithm`、`complexity-table`（4 列）、`papers-at-a-glance`、`overview`、`open-questions`（Q6、Q7）、`index`。
- 自己發現並修正：`sources/josh2010` 的書目初稿引用了 JOSH2016 參考文獻裡的卷期頁碼，但 JOSH2016 此時還沒 ingest，先拿掉，留到 ingest JOSH2016 時再補。
- Q6（緊例的封閉式）由 E3 的實際計算佐證：n = 6 時 Algorithm W 的值是 9，不是原文公式給的 7.5。

## [2026-11-16] check | C1 第 5 輪（JOSH2010）：通過

- 紀錄：`runs/20261116-013851-C1-ingest3-josh2010.txt`。自我測試 11 項全數抓到。
- 21 頁、0 錯誤。標記：推論 5、自編例子 32、白話說明 15、待確認 9。

## [2026-11-16] ingest | TSWJ2014

- 新增 `sources/tswj2014`、`concepts/two-agent-scheduling`、`algorithms/branch-and-bound`、`algorithms/simulated-annealing`；自編例子 E6（五個工作的雙代理人例子）。
- 更新舊頁面：`scheduling-basics`（交期、延遲、SPT、EDD、三欄記號）、`objective-functions`、`np-hardness`、`complexity-table`（新增獨立的一節）、`papers-at-a-glance`、`overview`（另一個分支）、`open-questions`（Q8–Q11）、`index`。
- 依使用者的決定，本篇是獨立分支：頁面中沒有寫任何它與 relocation problem 的直接關聯。
- 重讀時新發現兩項原文不一致，都不在最初的清單裡：Q9（內文說執行時間都小於 1 秒，Table 6 有幾組超過）、Q10（內文說誤差都小於 1%，Table 5 有一組 1.05%）。Q10 是在寫完「平均誤差都小於 1%」之後回頭核對表格才發現的，已把三個頁面的說法改成「作者表示…，表中實際有一組為 1.05%」。
- 自己修正：`two-agent-scheduling` 初稿寫「EDD 最保險」並掛上來源，原文沒有這句評語，改成只陳述原文用 EDD 做檢查。E6 補算兩個被頁面引用的數字（原本是心算的 12）。

## [2026-11-16] check | C1 第 6 輪（TSWJ2014）：不通過，1 項錯誤；另有 1 項 lint 沒抓到

- 紀錄：`runs/20261116-014138-C1-ingest4-tswj2014.txt`
- lint 抓到：`sources/tswj2014` 的定位說明沒有來源標註。
- lint **沒抓到**：`concepts/np-hardness` 的 `$\theta=1$` 被寫成「Tab 字元＋heta」。原因是更新舊頁面的指令裡 `\t` 被當成 Tab。這是寫完後主動搜尋才發現的；數學式壞掉但 `$` 成對，原本的 lint 看不出來。

## [2026-11-16] fix | 補上控制字元檢查

- 頁面：修正 `$\theta=1$`；定位說明補上來源標註並註明是使用者的決定。
- 檢查工具：lint 新增「行內含有控制字元」的檢查；`selftest.py` 加入對應的錯誤樣本（預期抓到的錯誤由 11 種增為 12 種）。
- 做法調整：之後用指令修改含 LaTeX 的頁面時一律用原始字串，避免反斜線被轉義。

## [2026-11-16] check | C1 第 7 輪（TSWJ2014）：通過

- 紀錄：`runs/20261116-014204-C1-ingest4-tswj2014-retry1.txt`。自我測試 12 項全數抓到。
- 25 頁、0 錯誤。標記：推論 8、自編例子 39、白話說明 19、待確認 16。

## [2026-11-16] ingest | JOSH2016

- 新增 `sources/josh2016`、`concepts/fixed-sequence`、`algorithms/backward-dp`；自編例子 E5（兩台專用機、順序固定）並補算水位變化，讓頁面上的每個時間點與資源量都有腳本輸出可對。
- 更新舊頁面 11 個：`sources/do2006`（後續研究）、`sources/josh2010`（卷期頁碼）、`relocation-problem`（三個決策階段）、`parallel-machines`、`objective-functions`（regular 的定義）、`np-hardness`（普通意義與 strong 的對照）、`resource-constrained-scheduling`、`complexity-table`（6 列）、`papers-at-a-glance`（引用關係）、`overview`、`open-questions`（Q12）、`index`。
- 操作上的問題：第一次用指令列更新舊頁面時指令本身因引號與反斜線而無法執行，沒有改到任何檔案。改成把更新內容寫成腳本檔再執行。

## [2026-11-16] check | C1 第 8 輪（JOSH2016）：通過

- 紀錄：`runs/20261116-014553-C1-ingest5-josh2016.txt`。自我測試 12 項全數抓到。
- 28 頁、0 錯誤。標記：推論 8、自編例子 47、白話說明 24、待確認 17。待確認事項共 12 項（Q1–Q12），最初清單只有 5 項，其餘 7 項是 ingest 過程中發現的。

## [2026-11-16] query | 五份簡報稿

- 依序寫 `queries/slides-ejor2009`、`do2006`、`josh2010`、`tswj2014`、`josh2016`（8–10 張，結構：動機 → 定義 → 例子 → 結果 → 方法 → 回顧 → 延伸閱讀）。圖表的數字一律貼 `examples.py` 輸出的資料。

## [2026-11-16] check | C2（簡報稿）

- ejor2009、do2006、josh2010、josh2016：第一次就通過。
- **tswj2014：不通過，2 項錯誤**（`runs/20261116-175019-C2-tswj2014.txt`）：(1) 我在甘特圖資料裡多加了一列「圖例」，與 `examples.py` 輸出不一致；(2) 「結果」那張排在兩張「方法」之後，教學結構順序不對。修正後通過（`runs/20261116-175024-C2-tswj2014.txt`）。
- 負向測試：暫時把一份簡報稿的「24 種順序」改成「987 種」，C2 報「數字 987 在所列出處頁面中找不到」。確認數字核對真的有作用，測試用的暫存檔已刪除。

## [2026-11-16] search | 延伸閱讀（五份各 3 篇）

- 用 Crossref 搜尋候選論文（只送論文關鍵字），共採用 9 篇不同論文，同一篇最多出現在兩份簡報。推薦理由只依書目、標題與五篇來源的引用脈絡；沒有任何一篇讀過全文。Lin & Liu (2008) 在五篇來源中都沒有被引用，推薦理由明講「只依標題」。

## [2026-11-16] check | C3（書目查證）：五份全數通過

- 15 個 DOI 逐一向 Crossref 查詢，標題相似度皆 1.00，年份與第一作者相符。紀錄：`runs/20261116-1748*-C3-*.txt`、`runs/20261116-1749*-C3-*.txt`。
- 這一關沒有抓到錯誤。原因可能是候選論文本來就是先用 Crossref 搜到的，書目沒有經過模型記憶這一手；C3 在這次的價值是「確認」，不是「攔截」。

## [2026-11-16] build | 產生簡報與瀏覽頁

- `build_slides.py all` 產生五份簡報與入口頁；`build_viewer.py` 產生 `wiki.html`（38 頁）。

## [2026-11-16] check | C4（簡報檢查）

- 第一輪：do2006、josh2016、tswj2014 通過；**ejor2009 與 josh2010 不通過**（`runs/20261116-175034-C4-ejor2009.txt`）：延伸閱讀的 DOI 與 Wiki 頁不一致。原因是 DOI `10.1016/0377-2217(88)90030-6` 含括號，轉成 Markdown 連結 `[..](url)` 時在第一個 `)` 被截斷，點下去會連到錯誤的網址。
- 修正：產生連結時把括號編成 `%28`、`%29`；檢查腳本比對前先還原。重新產生後五份全部通過。
- 瀏覽器實測：用本機伺服器實際開啟五份簡報，檢查數學式（0 個錯誤）、圖表（共 7 張）與內容是否超出投影片。**ejor2009 第 4 張與 josh2016 最後一張超出版面**，這是 HTML 檢查腳本看不出來的。修正：圖表限高、延伸閱讀字級縮小。重測五份皆無溢出；`wiki.html` 開啟後 38 頁導覽、數學式與圖表正常。

## [2026-11-16] check | C1（最終）：通過

- 紀錄：`runs/20261116-175035-C1-final.txt`。38 頁、0 錯誤。標記：推論 8、自編例子 47、白話說明 24、待確認 17。

## [2026-11-16] discuss | 使用者確認待確認事項

- 使用者指示：「各篇之間的不一致」不處理，因為各篇年份不同，可能有更新的結論；其餘待確認事項皆已確認。
- 處置：`open-questions` 的 Q1–Q4、Q6、Q8–Q11 狀態改為「已由使用者確認」；Q5、Q7、Q12（各篇之間的不一致）整節移除，並刪掉 `sources/ejor2009`、`josh2010`、`josh2016` 與 `slides-josh2016` 中對應的段落。
- 沒有做的事：各頁的 status 仍是「初稿」。使用者確認的對象是待確認事項，不是每一頁的全部內容，所以沒有擅自改成「已確認」。
- 同步更新後重跑：lint（38 頁、0 錯誤；待確認標記 17 → 14）、C2、C4（josh2016）皆通過，已重新產生簡報與 `wiki.html`。

## [2026-11-16] discuss | 使用者確認整個 Wiki

- 使用者指示：整個 Wiki 標為已確認。所有有 frontmatter 的頁面（36 頁）status 由「初稿」改為「已確認」；`index`、`log` 本來就沒有 frontmatter。
- 這是使用者的人工確認，不是 AI 自我檢查的結果；AI 的檢查範圍見上方各筆 check 紀錄。
- 使用者已把專案檔案移到 `TeachingSlide/` 資料夾，之後的操作都在該資料夾內進行。

## [2026-11-16] schema | 固定簡報風格

- 使用者確認目前的簡報風格不錯，要求寫進 `CLAUDE.md` 並固定。
- 新增 `CLAUDE.md` 第 7.1 節：色票（淺色與深色）、圖表色盤、字體、版面尺寸與字級、單一來源（`deck.css`、`render.js`）、超出版面的處理原則。內容取自現有檔案的實際數值，樣式檔本身沒有更動。

## [2026-11-16] schema | wiki.html 的樣式合併為單一來源

- 起因：使用者要求把 `wiki.html` 的樣式與簡報合併成單一來源。原本色票在 `deck.css` 與 `build_viewer.py` 各寫一份，只是剛好相同。
- 做法：新增 `slides/assets/base.css`（色票、字體、共用元件）；`deck.css` 與 `build_viewer.py` 的 CSS 只留版面；`wiki.html` 內嵌 `base.css`，簡報頁面先連結 `base.css` 再連結 `deck.css`。引用標籤、表格、圖表字級的差異改用三個 CSS 變數表示。新增 `CLAUDE.md` 第 7.1 節的對應規則。
- 視覺上的小變動：Wiki 瀏覽頁的 `blockquote` 外距、表格與圖表的間距等原本各自微調的數值，維持在 `wiki.html` 專用的 CSS 內，顯示效果沒有改變；簡報這邊字級與版面完全沿用。唯一統一的是原本 `deck.css` 內重複定義的 `further` 頁字級（20px 被後面的 17px 覆蓋，現在直接寫 17px，實際顯示相同）。
- 新增 `scripts/check_style.py`（檢查點 C5）。測試：故意在 `deck.css` 加一個色碼，以及改動 `base.css` 一個顏色但不重新產生 `wiki.html`，兩種都被抓到；之後已還原。測試時產生的幾份失敗紀錄我刪掉了，只留最後一份通過的，這是我的紀錄上的缺口，在這裡補記。
- 實測：用瀏覽器開啟簡報入口、五份簡報與 `wiki.html`：背景、文字色、字體、引用標籤顏色一致；五份簡報沒有內容超出版面、數學式 0 個錯誤；Wiki 導覽 38 頁。五份簡報 C4 與 `lint_wiki.py` 皆通過。
- 更正：上一筆說 wiki.html 的顯示效果沒有改變，說得太滿。引用標籤的內距、表格的列距在 wiki.html 與簡報原本略有不同，現在統一用 base.css 的數值，wiki.html 這兩處有極小的差異（不到 1px 級的內距），沒有逐一比對。

## [2026-11-17] build | 新增根目錄首頁 index.html

- 起因：使用者要把成果放上 GitHub Pages；根目錄沒有 `index.html`，只打 repo 網址會是 404。
- 做法：新增 `index.html`，用 `<meta http-equiv="refresh">` 自動導向 `slides/index.html`，並附兩個手動連結（簡報入口、Wiki）。樣式沿用 `slides/assets/base.css` 與 `deck.css`，沒有新增色碼或字體。`CLAUDE.md` 第 1 節的產出表加了一列。
- 這是手寫的檔案，不由腳本產生；內容沒有碰 Wiki 或簡報。
