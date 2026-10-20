# Config spreadsheet (演習評核_設定)

> Sources: README.md (owner contract); CLAUDE.md backend section; owner guide §11
> Repo: [README.md](../../../README.md); [CLAUDE.md](../../../CLAUDE.md); [docs/owner-guide-多醫院多演習.md](../../../docs/owner-guide-多醫院多演習.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs)
> Synced: 18c41f4
> Anchors: 設定試算表填寫說明; 選填欄：場景說明; Config spreadsheet (per-tenant; Config payload; readExerciseInfo_; readItems_; readIndicatorFull_; readIndicatorMap_; readCriteria_; levelHeaderCol_; 11. ⛔ 鐵則
> Updated: 2026-10-20

## Overview

The config spreadsheet defines one drill. It has five tabs: 演習資訊, 人員代號, 評分標準, 項目與問題 and 對應指標. The backend reads it on every request and never caches it. So an edit takes effect when a phone reloads. Each session in the tenant registry names its own config spreadsheet (`設定試算表ID`). The fallback tenant uses `CONFIG_SPREADSHEET_ID`. `README.md` is the owner's contract for this file. The `*_ALIASES_` constants in `ConfigWithSubmit.gs` own the exact accepted header texts.

## Tabs

| Tab | Shape | Read by | Becomes |
|---|---|---|---|
| 演習資訊 | key/value rows: column A label, column B value, no header row | `readExerciseInfo_` (in both backends) | `orgName`, `exerciseName`, `exerciseTopic`, `exerciseCategory`, `exerciseDate`, `exerciseDesc`, `exerciseLocation`, `commentEnabled`, `commentRequiredBelow` |
| 人員代號 | header `代號` | config branch | `codes` (the evaluator-code dropdown) |
| 評分標準 | headers `分數`, `標籤`, `說明`, one row per level | `readCriteria_` | `criteria`, and the drill's scale (see [Score scale](../domain/score-scale.md)) |
| 項目與問題 | `層1`, `層2`, … or `項目名稱`, plus question ID, question text, optional 場景說明 | `readItems_` | `items` (a tree) |
| 對應指標 | five columns, matched by alias | `readIndicatorMap_` (write path, three columns), `readIndicatorFull_` (analysis path, five columns) | not in the config payload. It feeds the record snapshot and the analysis. |

## 演習資訊

All nine labels are optional.

- `演習主題` (or `主題`) and `演習類別` are two different fields. The sheet has both rows. Do not merge them.
- `演習地點` (or `地點`) became a field on 2026-10-17. It feeds the Doc report token `{{演習地點}}` and the cover of the dashboard report view.
- `啟用觀察紀錄` turns the comment box off only for a literal `N`, `n`, `否`, `關閉` or a false value. A blank cell or a missing row means on. Hazard: an unticked checkbox in column B reads as false and turns off every comment box of the drill.
- `低分需說明門檻` makes a comment mandatory for a score at or below the value. The phone enforces it. The server does not.

## 項目與問題

- One grouping column (`項目名稱`) gives a flat list. `層1`, `層2`, … give a tree of any depth.
- `層1` also accepts `地點` and the old names. `層2` also accepts `演練單元`. Since 2026-10-16 the backend also accepts `層一` and full-width digits (`levelHeaderCol_`).
- The phone shows at most two levels. A third level makes the lowest items unreachable. A change to `Start.dc.html` must come first.
- A leaf name must be unique in the whole sheet. The phone keys the "done" flag by leaf name (defect D4). Two leaves with the same name share one flag.
- The optional 場景說明 column: the backend takes the first non-blank value under each leaf as `goal`. Since 2026-10-16 it also takes each question's own value as `questionGoal`.

## 對應指標

This tab maps each question to an indicator, a potential and 4S elements. All five columns are mandatory. If one column does not resolve, `action=analysis` fails, and the dashboard and the Doc report both fail to open. If the record sheet has a snapshot column, `doPost` can fail too.

The live sheet uses the second alias of most columns, not the first. `CLAUDE.md` records the live header row of 2026-10-12. Two traps:

1. The potential column accepts exactly one header text: `評核潛能`. `INDICATOR_POTENTIAL_ALIASES_` has one element.
2. The 4S header is `單一 4S 元素`. It must keep the space between 4S and 元素. Do not rename it to fix the word 單一. A renamed header resolves only if it starts with an alias.

The indicator header contains a line break. It resolves only through the prefix pass of `findHeaderCol_`.

The cell values of the potential column and the 4S column have their own rules. See [Resilience potentials](../domain/resilience-potentials.md) and [4S elements](../domain/4s-elements.md).

## Rules for the owner

1. Do not edit the config spreadsheet between the start of a drill and the archive of its report (owner guide §11).
2. Do not change the `分數` column after a drill starts. The analysis reads the current scale every time. A new scale belongs in a new config spreadsheet.
3. Change table headers only to names in the alias arrays. A new name works only after the backend that knows it is pasted.

## See Also

- [Record spreadsheet](record-spreadsheet.md)
- [Vocabulary renames](vocabulary-renames.md)
- [Tenant registry](tenant-registry.md)
- [Score scale](../domain/score-scale.md)
