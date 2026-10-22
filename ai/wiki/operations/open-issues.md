# Open issues and known defects

> Sources: CLAUDE.md warnings; handover §5; README.md; git observation of upstream; code review by Claude Code
> Repo: [CLAUDE.md](../../../CLAUDE.md); [docs/handover-筆電.md](../../../docs/handover-筆電.md); [README.md](../../../README.md); [Analysis.html](../../../Analysis.html); [Start.dc.html](../../../Start.dc.html); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [apps-script/Config.gs](../../../apps-script/Config.gs); [apps-script/Setup.gs](../../../apps-script/Setup.gs); [apps-script/Report.gs](../../../apps-script/Report.gs); [docs/owner-guide-多醫院多演習.md](../../../docs/owner-guide-多醫院多演習.md)
> Synced: 6fbf608
> Anchors: 已知沒做完的小缺口; 還沒驗證; 還沒實作（確認仍壞著）; 一個獨立的小待辦; Figure sizing for print; guard_production; REGISTRY_SCENEPREFIX_ALIASES_; submitScores; resolveTenant_; readRegistry_; readItems_; findLeafByName_; clearOtherDefaults_; duplicateTemplateRow_; enterReport
> Raw: [Upstream branch state](../../raw/repo-observations/2026-10-20-upstream-branch-state.md); [Code review and live check](../../raw/repo-observations/2026-10-22-code-review-live-check.md)
> Updated: 2026-10-22

## Overview

This article collects the problems that the sources record as open at commit `18c41f4`. Each item names its source article. Before you fix an item, check the code: an item may already be fixed upstream. When an item closes, mark it with a Status block here and in its source article.

## Defects that can give wrong data silently

| # | Issue | Effect | Details |
|---|---|---|---|
| 1 | No 場景前綴 alias in `REGISTRY_SCENEPREFIX_ALIASES_` | a renamed header makes every scene-code match of a tenant wrong, with no visible error | [Tenant registry](../data/tenant-registry.md) |
| 2 | D4: done flags keyed by leaf name | two scenes with the same name share one done flag | [Evaluator form](../frontend/evaluator-form.md) |
| 3 | The scale is never frozen per drill | a change to 評分標準 re-scales finished drills | [Score scale](../domain/score-scale.md) |
| 4 | The 評分標準 read failure falls back to 1–5 silently | a header typo re-scales a 0–4 drill | [Score scale](../domain/score-scale.md) |
| 5 | The observed-rate denominator counts only evaluators who submitted | an assigned evaluator who never submitted is invisible | [Observed rate](../domain/observed-rate-inclusion-gate.md) |

## Code review findings (fork review)

Claude Code reviewed the code at `6fbf608` and found the items below. Each item names the code that shows it. "Latent" means that the live data does not trigger the item today (see the raw file).

| # | Issue | Effect | Where |
|---|---|---|---|
| R1 | After a failed submit, the form keeps the same `submissionId`. A changed score or comment does not reset it. | If the first attempt was written on the server, the resend returns `duplicate:true`. The form shows success, but the server keeps the old scores. | `Start.dc.html` `submitScores`, the score `pick` handler. `ConfigWithSubmit.gs` `appendSubmission_` cache check |
| R2 | When `openById` of the registry fails (`readable` false), a request with `?t=` gets the fallback tenant. `readRegistry_` caches that result for `120` seconds. | A link to one session can show and accept the form of the fallback session. The dashboard shows the fallback data. `Report.gs` aborts, because it compares `meta.tenant`. | `ConfigWithSubmit.gs` `resolveTenant_` case (ii), `readRegistry_` |
| R3 | `Setup.gs` reads 啟用 with `isYes_`, so a blank cell means "disabled". The backend and the owner guide treat a blank cell as "enabled". `Setup.gs` also does not accept the 預設 text that the backend accepts. | The wizard does not clear an old default row. The hospital then has two defaults, and every link without `?ex=` gets `AMBIGUOUS_DEFAULT`. The wizard check still reports one default. | `Setup.gs` row reader, `clearOtherDefaults_`. `ConfigWithSubmit.gs` `parseRegistryRow_` |
| R4 | Latent. In a two-level sheet, a row with 地點 but a blank 演練單元 attaches its question to the 地點 node. `stripGroupInternals_` then returns that node as a leaf. | All other scenes of that 地點 disappear from the form and the analysis, with no error. | `readItems_` in both backends |
| R5 | Latent. `findLeafByName_` matches a leaf by name only. | If two 地點 have a scene with the same name, the second scene cannot be submitted (未知的問題ID). This adds to defect D4. | `ConfigWithSubmit.gs` `appendSubmission_` |
| R6 | Latent. No code checks that 問題ID is unique. The analysis key holds no scene. | Two questions with the same ID merge into one row, and one evaluator's score overwrites the other. | `buildAnalysis_` |
| R7 | Latent. `Config.gs` reads 評分標準 headers with a plain `indexOf` and has no `try`/`catch` in `doGet`. | On links with no parameters, a header typo gives no criteria, so the form falls back to 1–5 buttons on a 0–4 drill. A missing tab shows an Apps Script error page. | `Config.gs` `readCriteria_`, `doGet` |
| R8 | The fill-mode defect 1 of handover §0.3 is still in the code: each inserted row is a copy of the row that holds the token. | A run that stops between insert and fill leaves token rows, and a retry fills them again. | `Report.gs` `duplicateTemplateRow_` |
| R9 | `?view=report` stays in effect after the first load. | Every refresh or session switch enters the report view again. | `Analysis.html` `init`, `enterReport` |
| R10 | A render error in `init()` reaches the `catch` of `load()`. | The page tells the user to check the network connection. | `Analysis.html` `load` |
| R11 | `docs/owner-guide-多醫院多演習.md` says that rules 1 and 2 compare only rows with 啟用=Y. The backend compares all rows. | An owner can expect an archived row to be safe, but the backend marks both rows invalid. | owner guide §9, `assertRegistrySane_` |

## Safety tooling that is out of date

| # | Issue | Details |
|---|---|---|
| 6 | `guard_production` in `smoke.sh` and the stop conditions of the dispatch manual name only retired production deployments | [Testing](testing.md) |
| 7 | `dev` and `master` share one `ANALYSIS_KEY` | [Public exposure and keys](public-exposure.md) |
| 8 | `ADMIN_KEY` is empty, so `selftest` and `flush` are off. The handover calls setting it a small task that makes other checks easier. | [Backend endpoints](../backend/endpoints.md) |

## Unverified behaviour

- `REGISTRY_BROKEN` against a really broken registry. The handover describes a two-step test: break the header, wait 120 seconds, check a `?t=` link and a no-parameter request to `RECORD_URL`.
- The time-budget split and every chart fallback of `Report.gs`.
- Three wizard paths and a new tenant's first session.

## Small open items in the dashboard

- `#coverageGauge` is outside the print size rule.
- The figure orientation (10 cm wide, 14.5 cm tall) is not yet checked on paper.
- The handover asks to check with the owner what 垂直置中 (vertical centering) meant in one request.
- `questionGoal` is in the payload, but no client reads it.

## Documentation drift found while building this wiki

- `CLAUDE.md` names `anonCode()` in the dashboard. The code has `buildAnonMap()` and `anonLabel()` instead.
- The `master` copy of `CLAUDE.md` says `dev` is behind production. On 2026-10-20, `dev` was 3 commits ahead.
- The comment at `Setup.gs` and the hint in `SetupDialog.html` say the backend reads no 演習地點 row. That is stale since 2026-10-17.
- See also the stale claims list in [Source documents](../overview/source-documents.md).

## See Also

- [Testing](testing.md)
- [Source documents](../overview/source-documents.md)
