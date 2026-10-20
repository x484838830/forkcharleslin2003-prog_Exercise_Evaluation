# Observed rate (有效觀察涵蓋率) and the 50% inclusion gate

> Sources: CLAUDE.md inclusion-gate section; README.md (owner explanation with the advisor's example)
> Repo: [CLAUDE.md](../../../CLAUDE.md); [README.md](../../../README.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [Analysis.html](../../../Analysis.html); [apps-script/Report.gs](../../../apps-script/Report.gs)
> Synced: 18c41f4
> Anchors: 有效觀察涵蓋率 and the 50% inclusion gate; 有效觀察涵蓋率：一題要有一半以上的人; OBSERVED_RATE_MIN_; flattenScores_; inclusionApplies; isExcludedFromScoring; isIncluded_; rankableRows_
> Updated: 2026-10-20

## Overview

On 2026-10-17 the advisor added a rule. A question's scores enter the totals and averages only if the question's observed rate is at least 50%. The totals are 綜合評比, the three potentials, 4S and drill coverage. The observed rate of a question is: rated scores ÷ evaluators who scored the question × 100%. The backend sets `r.included` once per row with the threshold `OBSERVED_RATE_MIN_`. Clients read `r.included`. They never compute the rate or the threshold themselves.

## Do not confuse the two "coverage" words

| Term | 中文 | What it is |
|---|---|---|
| drill coverage | 演習覆蓋率 | a potential group. Its questions have scores, and the gauge and a radar show their average. |
| observed rate | 有效觀察涵蓋率 | a ratio per question: how many evaluators gave a rated score |

The advisor warned about this mix-up explicitly. The backend names the ratio `observedRate` and never uses the word coverage for it. The gate applies to the drill coverage questions like any other questions.

## The advisor's table (four evaluators)

| Rated scores | Observed rate | Judgement | Enters totals |
|---|---|---|---|
| 4 | 100% | 充分 | yes |
| 3 | 75% | 可接受 | yes |
| 2 | 50% | 有條件接受 | yes |
| 1 | 25% | 待確認 | no |
| 0 | 0% | 未觸發 | no |

For other group sizes, the words follow the rate. The words are text to show. Only `r.included` decides.

The test is `>=`. So 2 of 4 is in, 1 of 2 is in, 1 of 3 is out, and 2 of 3 is in. A row with no rated score is never included.

## The denominator and its limit

The denominator (原指定評核官人數) is `scores.length`: every evaluator code with a stored score on that question, 0 included. The evaluator form refuses to submit a scene until every question has a score or a 0. So each evaluator who submitted a scene answered every question in it.

The limit: no sheet lists which evaluators were assigned to a scene. So "assigned" really means "submitted this scene". Example: four evaluators were assigned, one submitted with a rated score. The system computes 1/1 = 100%, not 25%.

## What the gate changes

Gated (only through `flattenScores_`): `stats.overall`, `stats.potentials`, `stats.s4`, `stats.potentialByS4`, `stats.coverage`.

Not gated: `rwg`, `within1`, `icc2k`, `byEvaluator`, `untriggered`, `missingQuestions`, `unratedQuestions`. These ask whether evaluators agree or what went unscored. `rwg` keeps its own cut: it skips a question with fewer than 2 rated scores.

An excluded row keeps its own `mean` and `sd`. Exclusion removes a row from aggregates and rankings, not from listings.

`stats.inclusion` is the ledger: `threshold`, `total`, `included`, `excluded`, and `excludedQuestions` with `rated`, `assigned` and `rate` per question. Its scope is the three potentials and drill coverage.

## Client contract

- Test `r.included !== false`, never truthiness. An old backend sends no `included`, and every row must then count.
- Anything a client sums, averages, plots or ranks from rows must apply the same test. In `Analysis.html`: the radars, the per-scene 4S segments, `renderRanking`. In `Report.gs`: the radar specs, `sceneS4Buckets_`, and every top/bottom ranking.
- An empty cell caused by the gate must not carry the caption 「分數全部為 0 分」. `abilityEmptyReason()` tells the causes apart.
- On a scale with no 0 level, the dashboard hides every gate element (`inclusionApplies()` = `meta.scale.lowExcluded`). A 1–5 drill is 100% everywhere.

## Where the dashboard shows the rule

- the 統計方法 tab: the `#inclusionMethod` cards (formula, the advisor's table, the warning, the excluded-question table)
- a 有效觀察 column in every `radarTable`
- `#inclusionNote` under the first overview card when a question was excluded
- `#notRatedCard` 「不納入綜合評比計算項目」, which lists the excluded questions

The Doc report applies the same gate but keeps its format, as the advisor asked.

## Recomputed, never frozen

The analysis computes inclusion every time it runs. A 0–4 drill that already ran changes its totals when the new backend is pasted. The record rows do not change.

## See Also

- [Score scale](score-scale.md)
- [Agreement statistics](agreement-statistics.md)
- [Analysis payload](../backend/analysis-payload.md)
- [Dashboard](../frontend/dashboard.md)
