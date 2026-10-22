# Record spreadsheet (演習評核_紀錄)

> Sources: README.md record-sheet section; CLAUDE.md Record spreadsheet section
> Repo: [README.md](../../../README.md); [CLAUDE.md](../../../CLAUDE.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs)
> Synced: b1a765f
> Anchors: 紀錄試算表填寫說明; 新增的選填欄; 關於「觀察紀錄」文字框; Record spreadsheet (per-tenant; appendSubmission_; RECORD_COMMENT_ALIASES_; sanitizeCell_; COMMENT_MAX_LENGTH_
> Updated: 2026-10-20

## Overview

The record sheet receives the scores. `appendSubmission_` appends one row per answered question. It matches columns by header text, not by position. So the owner decides which columns exist and in which order. Four columns are required. All other columns are optional: the backend writes them if they exist and skips them if they do not. Each session has its own record tab (`紀錄分頁名稱`, default `評核紀錄`). The analysis reads every row of that tab.

## Columns

Required. A missing required column makes a submission fail.

| Column (aliases) | Content |
|---|---|
| `問題ID` (`評核題號`) | the question ID, forced to plain-text format so Sheets does not turn it into a date |
| `分數` | the score as submitted. 0 is a real value (not-rated score). The backend does not check the range. |
| `人員代號` | the evaluator code |
| `送出時間` | the server time |

Optional, older:

| Column | Content |
|---|---|
| `演習名稱` | the drill name, for reference only |
| `項目名稱` | the leaf name picked at submit, for reference only |
| `地點` (old names accepted) | the top group of the question |
| `演練單元` | the scene of the question |
| `指標代號` | the indicator. The analysis reads it back since the label-snapshot change. |

Optional, newer. In the live sheet on 2026-10-12, only `觀察紀錄` existed of these.

| Column (aliases) | Content | Value |
|---|---|---|
| `觀察紀錄` (`觀察意見`, `質性觀察`, `備註`) | the evaluator's comment, trimmed and capped | the only qualitative data. The Doc report gets a 觀察紀錄 chapter from it. |
| `醫院代號` (`機構代號`) | the `?t=` code | lets rows from many sessions be told apart |
| `演習代號` (`場次代號`) | the `?ex=` code, plain-text format | same |
| `場景說明` (old names accepted) | label snapshot | see below |
| `評核潛能` (`潛能`) | label snapshot | see below |
| `4S 元素` (`4S元素`, `單一 4S 元素`) | label snapshot | see below |
| `評核題目` (`具體評核題目`, `問題內容`) | label snapshot | see below |

## Label snapshot (defect D3)

Without the snapshot columns, the analysis joins each record row to the current config spreadsheet when someone opens the dashboard. If the owner edits the questions for the next drill, an old report shows new labels, with no warning. With the snapshot columns, the backend writes the labels into the row at submit time. The analysis prefers a non-blank snapshot value (`labelSource:'snapshot'`), then the join (`'join'`), then nothing (`'none'`). A mix is permitted. The dashboard's data-quality section prints how many questions used each source.

Two fields keep the old precedence: `stage` and `itemName` come from the config join first and from the record column only as a fallback.

## Comments

- The comment box is optional by default. `啟用觀察紀錄` turns it off. `低分需說明門檻` makes it mandatory for low scores, on the phone only.
- The client trims a comment and caps it at 500 characters. The server caps it again at `COMMENT_MAX_LENGTH_`.
- The server never rejects a submission because of a comment.
- If the record sheet has no `觀察紀錄` column, the phone still shows the box, and the text is lost. Add the column first.
- `sanitizeCell_` escapes a formula prefix. This matters most for the comment column, the only free-text column.

## Duplicates and blanks

- The client sends one `submissionId` per submit attempt and reuses it for its 3 retries. The backend deduplicates with `CacheService` (6h) and `LockService`.
- The analysis keeps the last row per key (`醫院代號`, `演習代號`, `問題ID`). On a sheet without the first two columns, the key is the question ID alone, so the last write wins.
- Since 2026-10-16, the analysis skips a row with a blank `分數`. Before that, a blank cell counted as 0 and could overwrite an earlier real score.

## See Also

- [Config spreadsheet](config-spreadsheet.md)
- [Analysis payload](../backend/analysis-payload.md)
- [Tenant registry](tenant-registry.md)
