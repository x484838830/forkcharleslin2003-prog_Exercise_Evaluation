# Glossary

One concept has one term. Use the **Term** column in all wiki prose. The **Avoid** column lists words that caused confusion or that name a different concept. `wiki.py terms` reports an Avoid word in prose. An Avoid word is permitted in `backticks`, for example when an article names an old alias.

Chinese words in the 中文 column are product identifiers. Write them exactly as shown.

## People and organisations

| Term | 中文 | Code name | Meaning | Avoid |
|---|---|---|---|---|
| owner | 業主 | — | The person who runs the platform for the hospital, edits the spreadsheets and requests changes. | customer |
| advisor | 老師, 顧問 | — | The owner's advisor. The advisor set the 有效觀察涵蓋率 rule. | teacher, consultant |
| evaluator | 評核官 | `fillerCode` | A person who scores a drill on a phone with the evaluator form. | assessor, scorer, judge |
| evaluator code | 人員代號 | `codes`, `fillerCode` | The code that an evaluator picks in the form. It is the evaluator's only identity in the data. | user ID |
| maintainer | — | GitHub `x484838830` | The person who owns the fork and works in this checkout with Claude. The wiki does not record whether the maintainer is also the owner. | — |
| tenant | 醫院 | `hid`, `醫院代號`, `?t=` | One hospital in the tenant registry. | customer hospital |

## Drills and their structure

| Term | 中文 | Code name | Meaning | Avoid |
|---|---|---|---|---|
| drill | 演習 | `exercise`, `exerciseName` | One emergency exercise event that evaluators score. | exercise, drill event |
| session | 場次 | `exid`, `演習代號`, `?ex=` | One tenant-registry row for one drill of one tenant. | — |
| default session | 預設演習 | `isDefault` | The session that a link with `?t=` and no `?ex=` resolves to. | default drill |
| location | 地點 | `stage`, `層1` | The top group in 項目與問題. Old header names are still accepted. | `情境階段`, `場景階段`, phase |
| scene | 演練單元, SCENE | `itemName`, `層2` | The lowest group in 項目與問題 (a leaf). Its short code is, for example, A1. | scenario |
| scene description | 場景說明 | `goal` | The optional text that describes a scene. | `測試情境`, `測試場景與目標`, `測試場景`, `測試情境與目標`, test scenario |
| question | 評核題目, 問題 | `問題ID`, `questionId` | One scored question inside a scene. | — |
| indicator | 指標 | `indicator`, `指標代號` | The indicator that 對應指標 maps a question to. | — |

## Scoring concepts

| Term | 中文 | Code name | Meaning | Avoid |
|---|---|---|---|---|
| score | 分數 | `score` | Any value an evaluator submits, 0 included. | — |
| rated score | 有效給分 | `ratedCount` | A score that is not 0. Only rated scores enter averages. | valid score, effective score, real rating |
| not-rated score | 不予評分 | `NOT_RATED_SCORE_` | The score 0. It means "this question could not be judged". | zero rating |
| scale | 評分標準 | `meta.scale`, `scaleOf_` | The score levels of one drill, read from the 評分標準 sheet. | rubric |
| potential | 評核潛能 | `potential` | The resilience capacity that a question tests: 反應, 監測, 預期 or 學習, or the 演習覆蓋率 group. | capability, `回應`, `預見` |
| three potentials | 三項潛能 | `analysisRows` | The potentials 反應, 監測 and 預期 together. | — |
| drill coverage | 演習覆蓋率 | `coverageRows`, `stats.coverage` | A group of questions whose potential contains 覆蓋率. It is a score, not a ratio. | — |
| observed rate | 有效觀察涵蓋率 | `observedRate` | Per question: rated scores ÷ evaluators who submitted that question. | observation coverage, observed coverage, rating coverage, coverage ratio |
| inclusion gate | 納入門檻 | `OBSERVED_RATE_MIN_`, `included` | The rule that a question enters the totals only if its observed rate is at least the threshold. | coverage gate, coverage threshold |
| 4S element | 4S 元素 | `s4`, `s4List` | Space, Staff, Stuff or System. | 4S dimension |
| ability cell | 綜合能力 | `abilityCells()`, `potentialByS4` | One potential × one 4S element. | — |
| leniency | 寬嚴傾向 | `byEvaluator`, `deviation` | How far one evaluator's scores sit from the mean of the rows that evaluator scored. | severity bias |

## Data and files

| Term | 中文 | Code name | Meaning | Avoid |
|---|---|---|---|---|
| config spreadsheet | 演習評核_設定 | `CONFIG_SPREADSHEET_ID`, `設定試算表ID` | The spreadsheet that defines a drill: info, codes, scale, questions, indicators. | settings sheet |
| record spreadsheet | 演習評核_紀錄 | `RECORD_SPREADSHEET_ID`, `紀錄試算表ID` | The spreadsheet that receives scores. Its tab 評核紀錄 is the record sheet. | results sheet, response sheet |
| tenant registry | 租戶註冊表 | `REGISTRY_SPREADSHEET_ID` | The spreadsheet that maps 醫院代號 + 演習代號 to a config file, a record file and a key. | tenant table |
| fallback tenant | — | `fallbackTenant_()` | The legacy tenant that the hardcoded constants define. | default tenant |
| alias array | 別名 | `*_ALIASES_` | A list of accepted header texts for one column. The first entry is the new name. | — |
| label snapshot | 標籤快照 | `labelSource` | Labels that the backend writes into the record row at submit time. | — |
| report snapshot | 報告快照 | sheet `報告快照` | The append-only sheet where the Doc report freezes its numbers. | — |
| analysis payload | — | `action=analysis` | The JSON that `buildAnalysis_` returns: `meta`, row arrays, `stats`. | — |

## Programs and deployment

| Term | 中文 | Code name | Meaning | Avoid |
|---|---|---|---|---|
| evaluator form | 評核單 | `Start.dc.html` | The phone page where evaluators score. | questionnaire |
| dashboard | 分析平台, 分析頁 | `Analysis.html` | The page that shows the analysis of one session. | analysis platform, analysis page |
| dashboard report view | 產生報告 (方案A) | `body.reportMode` | The printable mode of the dashboard. | print report |
| Doc report | 評核報告 (方案B) | `Report.gs` | The Google Doc and PDF report that the report generator writes. | PDF report |
| backend | 後端 | `ConfigWithSubmit.gs` | The main Apps Script Web App behind `RECORD_URL`. `Config.gs` is a second, read-only backend. | server script |
| client | — | — | A program that reads the analysis payload: the dashboard or `Report.gs`. | — |
| setup wizard | 新增一場演習 | `Setup.gs` | The dialog that creates a session in the tenant registry. | — |
| paste | 貼上 | — | Copy a `.gs` file into its Apps Script project by hand. | — |
| redeploy | 部署新版本 | — | In Apps Script: edit the existing deployment and pick "New version". It keeps the `/exec` URL. | new deployment |
| production | 正式版 | branch `master` | The hospital's live site and backends. | live version |
| sandbox | 測試版, 沙箱 | branch `dev` | The test site and test spreadsheets. | staging |
| upstream | 原 repo | remote `upstream` | The original repository `charleslin2003-prog/Exercise_Evaluation`. | — |
| fork | — | remote `origin` | The copy of upstream under the GitHub account `x484838830`: `x484838830/forkcharleslin2003-prog_Exercise_Evaluation`. This checkout pushes here. | — |
