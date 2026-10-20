# AI 知識與工作區（給你看的說明）

這個資料夾是 Claude 用來「記住這個專案」的地方。你平常不用自己讀裡面的文章，只要知道它怎麼運作、要怎麼叫 Claude 用它就好。

## 裡面有什麼

| 位置 | 內容 | 誰在寫 |
|---|---|---|
| `wiki/` | 整理好的知識文章（目前 25 篇），分成 7 個主題：總覽、領域知識、試算表、後端、前端、報告、維運 | Claude |
| `wiki/index.md` | 目錄 | Claude |
| `wiki/glossary.md` | 用語表：每個概念固定一個說法，列出「不要用的別名」 | Claude |
| `wiki/log.md` | 操作紀錄，只會往後加 | Claude |
| `raw/` | 原始資料：你的決定、外部參考文獻、分支狀態紀錄。存進來就不改 | Claude（內容來自你或網路） |
| `work/` | 工作區：多步驟任務的進行中筆記 | Claude |
| `scripts/` | 檢查腳本 | — |
| `SCHEMA.md` | Claude 必須遵守的規則（英文） | — |

## 兩個方法各負責什麼

- **karpathy-llm-wiki（怎麼存）**：原始資料放 `raw/`，整理成文章放 `wiki/`。之後回答問題時讀整理好的文章，不必每次重讀整個專案。
- **ASD-STE100（怎麼寫）**：一個詞只有一個意思、一句只講一件事、不刪掉「可能」這類保留語氣、不加原文沒有的事實。用語表和檢查腳本會抓錯。

文章用英文寫（你 2026-10-20 決定的），產品裡的中文名稱（工作表名、欄名、畫面文字）保留中文。

## 為什麼不用每次全部重掃

每篇文章都記下兩件事：「根據哪些檔案寫的」以及「整理時的 commit 編號」。程式改了之後，腳本會用 git 比對：

1. 哪些檔案從那個 commit 之後改過
2. 改的是哪些段落或函式
3. 哪幾篇文章引用了那些段落（「錨點命中」）

Claude 只讀那些改動（diff），只更新受影響的文章。

## 你可以這樣跟 Claude 說

| 你說 | Claude 會做 |
|---|---|
| 「同步知識庫」 | 跑 `wiki.py status`，只讀改動，更新受影響的文章 |
| 「同步原 repo」 | 從原作者的 repo 拉最新版、合併到你的 fork，再同步知識庫 |
| 「檢查知識庫」 | 跑 `wiki.py lint`：檢查斷掉的連結、數字對不對得上出處、用語、句型 |
| 「這個功能怎麼運作？」 | 先查知識庫再回答，附上文章連結 |
| 「把這個存進知識庫」 | 把你給的資料存進 `raw/`，再整理進相關文章 |
| 「我決定……」 | 把你的決定記進 `raw/owner-decisions/` |

## 要注意的事

- **這個資料夾會跟著 push 到你的 fork，而 fork 是公開的。** 規則禁止在這裡寫入金鑰、試算表 ID、`/exec` 網址、醫院代號、評核官的分數或觀察紀錄。
- **程式碼永遠比知識庫準。** 兩者對不上時，Claude 會以程式為準，再回頭修文章。
- 原作者的 `CLAUDE.md`、`README.md`、`docs/` 不會因為知識庫而被修改。

## 自己跑檢查（選用）

在專案資料夾打開終端機：

```bash
python3 ai/scripts/wiki.py status
```

```bash
python3 ai/scripts/wiki.py lint
```

## 來源與授權

- 知識庫方法：[Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)（MIT）
- 寫作規則：[danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)（MIT）
- 兩支借用的腳本授權全文：`THIRD_PARTY_LICENSES.md`
