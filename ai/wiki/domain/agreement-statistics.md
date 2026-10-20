# Agreement statistics (r_wg, within1, ICC, leniency)

> Sources: CLAUDE.md analysis endpoint section; Analysis.html 統計方法 text; R package multilevel documentation of rwg (James, Demaree and Wolf 1984)
> Repo: [CLAUDE.md](../../../CLAUDE.md); [Analysis.html](../../../Analysis.html); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [apps-script/Report.gs](../../../apps-script/Report.gs)
> Synced: 18c41f4
> Anchors: Analysis endpoint (`doGet?action=analysis; rwgLocal; rwgStat; rwgScale; renderMethod; verifyIcc_; verifyRwg_; byEvaluator
> Raw: [rwg notes](../../raw/domain/rwg-within-group-agreement-index.md)
> Updated: 2026-10-20

## Overview

The system reports how much evaluators agree. Since 2026-10-13 the dashboard shows r_wg (the within-group agreement index) instead of ICC(2,k). It also shows the share of evaluator pairs whose scores differ by 1 or less (`within1`). It computes leniency per evaluator (寬嚴傾向). None of these statistics passes through the inclusion gate. All of them ignore the not-rated score 0.

## r_wg

The domain formula (James, Demaree and Wolf, 1984): r_wg = 1 − observed variance ÷ expected random variance. The usual expected variance assumes a rectangular (uniform) distribution over A response options: (A² − 1) / 12. For 5 options this is 2. A negative value is truncated to 0, which means no agreement.

How this system computes it (`stats.rwg`, and the dashboard copy `rwgLocal`):

1. Per question, S_x² is the sample variance of the rated scores (denominator n − 1).
2. σ_E² is `meta.scale.expectedVar`. A is the number of rated levels. On a 1–5 scale σ_E² is 2. On a 0–4 scale A is 4 and σ_E² is 1.25.
3. A question with fewer than 2 rated scores is skipped.
4. A negative r_wg is clamped to 0.
5. The result is the mean over the questions. `skipped` and `clamped` count the questions that were skipped or clamped, because both push the mean up. The dashboard prints these counts next to the value.
6. The scope is the three potentials and drill coverage (`consistencyRows`). 學習 questions stay out.

Rough reading that the dashboard prints: ≥ 0.90 very high agreement, 0.70–0.90 acceptable, < 0.70 low.

Before 2026-10-16 the code had a hardcoded 5-point scale (`RWG_SCALE_POINTS_ = 5`).

The dashboard keeps its own implementation on purpose. With an old backend that sends no `stats.rwg`, the page can still show a value.

## within1

The share of same-question evaluator pairs whose scores differ by 1 or less. It is computed per question, so it needs no rectangular matrix. A 0 is never paired. The dashboard text explains the difference: r_wg asks how concentrated the scores are, and within1 asks how many pairs scored close together. The dashboard report view shows within1 in its summary.

## ICC(2,k)

`stats.icc2k` is the Shrout–Fleiss ICC(2,k) over the evaluators that every row has in common.

- It is `null` with fewer than 2 common evaluators or fewer than 2 questions.
- One question that only one evaluator scored makes the whole dataset `null`. This is not an edge case.
- A 0 counts as "did not rate", so one 0 drops that evaluator from the common set. Expect `null` more often on 0–4 drills.
- On a handful of questions ICC is not a quality signal. A test run with two evaluators and four questions returned exactly 0.00, which is arithmetically correct and meaningless.

`Report.gs` recomputes it locally in `verifyIcc_` as a check, and names the questions that collapsed the common set when the value is `null`.

## Leniency (寬嚴傾向)

`stats.byEvaluator` lists `{code, n, mean, deviation}` per evaluator. `deviation` is the evaluator's mean minus the mean of the row means of the rows that this evaluator scored. So an evaluator who scored only hard questions does not look strict. A 0 is skipped on both sides. The output must be renderable with anonymous labels.

## See Also

- [Score scale](score-scale.md)
- [Observed rate and the inclusion gate](observed-rate-inclusion-gate.md)
- [Analysis payload](../backend/analysis-payload.md)
