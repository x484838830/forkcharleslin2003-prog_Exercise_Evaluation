# Analysis payload (action=analysis)

> Sources: CLAUDE.md analysis endpoint section
> Repo: [CLAUDE.md](../../../CLAUDE.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs)
> Synced: 18c41f4
> Anchors: Analysis endpoint (`doGet?action=analysis; buildAnalysis_; pickLabel; flattenScores_; summarize_; itemsDepth_
> Updated: 2026-10-20

## Overview

`doGet?action=analysis&key=…` returns one JSON object for one session. `buildAnalysis_(t)` builds it. It reads every row of the session's record sheet, keeps the last row per key, and joins each question ID to 對應指標 and 項目與問題. The payload has `meta`, three row arrays and `stats`. The dashboard and the Doc report both read this payload. Clients must not recompute what the payload already says. Every field added since the first version is additive, and clients must accept an old backend that lacks it.

## Authentication

The key is compared against the resolved row's `分析金鑰`, or `ANALYSIS_KEY` for the fallback tenant. A key rotation is a one-cell edit in the tenant registry, with no redeploy. `action=analysis` ignores `啟用=N`, because a finished drill still needs its report.

## Deduplication

The key is (`醫院代號`, `演習代號`, `問題ID`). The first two parts come from the record row when those columns exist, else they are empty. On a sheet without them, the key is the question ID, and the last write wins.

`buildAnalysis_` also skips a record row whose own `醫院代號` or `演習代號` is non-blank and different from the resolved tenant. Both conditions are needed: a blank value means an old row, and a blank tenant code means fallback mode.

## Row fields

`{ questionId, stage, itemName, goal, potential, s4, indicator, question, scores:[{code,score}], mean, sd }` plus:

| Field | Since | Meaning |
|---|---|---|
| `exerciseId` | — | the session code |
| `comments` | — | `[{code, comment}]`, non-empty only, sorted by code |
| `labelSource` | — | `snapshot`, `join` or `none` |
| `untriggered` | — | count of scores equal to `meta.scale.lowValue` |
| `s4List` | 2026-10-16 | the split 4S elements (see [4S elements](../domain/4s-elements.md)) |
| `ratedCount` | 2026-10-16 | number of rated scores (not 0) |
| `questionGoal` | 2026-10-16 | the question's own 場景說明 cell. No client reads it today. |
| `observedRate` | 2026-10-17 | `ratedCount / scores.length` |
| `included` | 2026-10-17 | passes the inclusion gate |

- `scores` lists every evaluator, 0 included. `mean` and `sd` use rated scores only. `mean` is `null` when every score is 0.
- Label precedence: `stage` and `itemName` take the config join first. `goal`, `potential`, `s4`, `indicator` and `question` take the snapshot first.

## Row arrays

| Array | Potential | In `stats` |
|---|---|---|
| `analysisRows` | 反應, 監測, 預期 | yes |
| `coverageRows` | contains 覆蓋率 | yes |
| `learningRows` | 學習 | no |

`consistencyRows` = `analysisRows` + `coverageRows`. The agreement statistics and the inclusion ledger use it.

## meta

`orgName`, `exerciseName`, `exerciseTopic`, `exerciseCategory`, `exerciseDate`, `exerciseDesc`, `generatedAt`, `evaluatorCodes`, plus `exerciseLocation`, `tenant`, `exercise`, `displayName`, `scenePrefix`, `tenantSource`, `configFileName`, `recordFileName`, `recordSheetName`, `recordRowCount`, `commentCount`, `labelSourceSummary`, `scale`, `levelCount`, `stageOrder`.

- File names are permitted here, because this branch needs a key. Spreadsheet IDs are never permitted.
- `stageOrder` lists the 地點 values in sheet order. Clients sort by it instead of the browser's collation.
- `levelCount` is the depth of the 項目與問題 tree (`itemsDepth_`).

## stats

The original seven keys: `overall`, `potentials`, `s4`, `coverage`, `icc2k`, `within1`, `potentialByS4`. Added keys: `untriggered`, `missingQuestions`, `unratedQuestions`, `inclusion`, `byEvaluator`, `rwg`.

- The five score summaries (`overall`, `potentials`, `s4`, `coverage`, `potentialByS4`) use rated scores of included rows only. Each can be `{n:0, mean:null}`, for three different causes: no question, every score 0, or every question excluded by the gate.
- `missingQuestions`: questions in 項目與問題 with no score at all.
- `unratedQuestions`: questions that were scored, but only with 0. The two lists are disjoint.
- `untriggered`: `{n, total, rate, value, label, excluded}`. On a 0–4 drill it is the 不予評分 rate. On a 1–5 drill it is the old 未觸發 rate. The key kept its old name for old clients.
- The agreement keys are explained in [Agreement statistics](../domain/agreement-statistics.md). The gate is explained in [Observed rate and the inclusion gate](../domain/observed-rate-inclusion-gate.md).

## Client contract

1. Guard `r.mean === null` and `{n:0, mean:null}` everywhere.
2. Read `meta.scale`. Never hardcode 5, "1 = 未觸發" or σ_E² = 2.
3. Read `r.s4List`. Never split a 4S cell.
4. Read `r.included` with `!== false`. Never recompute the threshold.
5. Treat each missing new field as the old behaviour.

## See Also

- [Backend endpoints](endpoints.md)
- [Dashboard](../frontend/dashboard.md)
- [Doc report generator](../report/doc-report.md)
- [Record spreadsheet](../data/record-spreadsheet.md)
