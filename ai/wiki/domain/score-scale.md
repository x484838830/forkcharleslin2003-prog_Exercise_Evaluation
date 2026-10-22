# Score scale and the not-rated score 0

> Sources: CLAUDE.md scale section; README.md 評分標準 section; ED-RAG paper (domain context)
> Repo: [CLAUDE.md](../../../CLAUDE.md); [README.md](../../../README.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [Start.dc.html](../../../Start.dc.html); [Analysis.html](../../../Analysis.html)
> Synced: b1a765f
> Anchors: The score scale follows 評分標準; 設定試算表填寫說明（評分標準）; 0 分＝不予評分，不算進任何平均; scaleOf_; readCriteria_; scoreScale; ratedOnly_; NOT_RATED_SCORE_
> Raw: [ED-RAG paper notes](../../raw/domain/2020-09-21-ed-rag-resilience-assessment-grid.md)
> Updated: 2026-10-20

## Overview

Each drill's own 評分標準 sheet defines its score scale. The `分數` column lists the levels. On 2026-10-16 the owner changed the scale from 1–5 to 0–4, where 0 means 不予評分 (not rated). Two owner decisions are final. First, 0 is not a rating. It enters no average, no SD and no agreement statistic. It appears only as a count or a rate. Second, the scale follows each drill's sheet automatically, so old 1–5 drills render as before.

## The two scales

| Scale | Levels (from `README.md`) | Low level |
|---|---|---|
| 0–4 (since 2026-10-16) | 4 完整達成, 3 輕微缺點但達成, 2 部分達成, 1 未達成, 0 不予評分 | 0, excluded from every average |
| 1–5 (older drills) | 5 完整達成 … 1 未觸發 (劇本未走到此條件) | 1, averaged with 2–5, and reported as a rate too |

The meaning of 0 is that no evaluator could rate the question (`README.md`: 這一題沒辦法評). The script did not reach it, the evidence was too thin, or it did not apply. It does not mean "worst".

Domain note: the ED-RAG adaptation of Hollnagel's RAG also moved from five named classes to a four-point scale. Its reason was that thin evidence could not be split into five levels (see [Resilience potentials](resilience-potentials.md)). The repo does not say whether this influenced the owner.

## One sheet, two derivations

| Where | Function | Output |
|---|---|---|
| backend | `scaleOf_(readCriteria_(configSs))` in `buildAnalysis_` | `meta.scale` |
| evaluator form | `scoreScale(criteria)` in `Start.dc.html` | the score buttons |

Both derivations remove duplicates, sort ascending, skip a non-numeric `分數`, and fall back to 1–5. Change one, and change the other. Nothing at runtime compares them.

`meta.scale` fields: `values`, `rated`, `min`, `max`, `lowValue`, `lowLabel`, `lowExcluded`, `expectedVar`, `levels`, `source`. Read the comment above `scaleOf_` for each field.

| Field | 0–4 sheet | 1–5 sheet |
|---|---|---|
| `rated` | 1..4 | 1..5 |
| `min` / `max` | 1 / 4 | 1 / 5 |
| `lowValue` | 0 | 1 |
| `lowExcluded` | true | false |
| `expectedVar` | 1.25 | 2 |

## The fixed rule: 0 is never averaged

- `NOT_RATED_SCORE_ = 0` and `ratedOnly_` remove 0 everywhere, whether or not the scale lists 0. This rule is code, not sheet data.
- Only 0 gets this treatment. If the owner puts 不予評分 on another number, the analysis averages it.
- A question that every evaluator scored 0 has `mean: null`. It is listed in `stats.unratedQuestions` and drawn in no chart.
- Since 2026-10-16 a blank `分數` cell is skipped. It used to count as 0.

## What the backend does not check

`doPost` writes the score as received and does not check the range. Reason: a check would read 評分標準 on every submission, and a broken sheet would then refuse every score in the middle of a drill. The score buttons are the only gate.

## Hazards

1. **Re-scaling.** The analysis reads the current 評分標準 every time. Nothing freezes the scale per drill. A change after a drill re-scales that drill's dashboard and report. A change during a drill mixes two scales. Use a new config spreadsheet for a new scale.
2. **Silent fallback.** `readCriteria_` throws if any of the three headers is wrong, `說明` included. The scale then falls back to 1–5 with `source:'error'`. The dashboard does not show this. Only the 檢查設定 row 評分量尺 of the Doc report shows it, and that row is green either way. Read its text.
3. **Old evaluator form on a 0–4 sheet.** It shows 1–5 buttons. Evaluators can submit 5 and never 0. That is wrong data, and no later deploy fixes it.

## Contract for every client

- Guard `r.mean === null` before `toFixed`, sorting or plotting.
- Treat a missing `ratedCount` as `scores.length`.
- Treat a missing `meta.scale` (old backend) as the 1–5 default.
- Branch any prose about the scale on `lowExcluded`. The 1–5 sentence is false on a 0–4 drill.

## Interaction with the comment rule

The evaluator form compares `score <= commentRequiredBelow`. On a 0–4 scale, a threshold of 1 requires a comment for 0 and for 1. No integer threshold requires a comment for 0 alone.

## See Also

- [Observed rate and the inclusion gate](observed-rate-inclusion-gate.md)
- [Agreement statistics](agreement-statistics.md)
- [Config spreadsheet](../data/config-spreadsheet.md)
