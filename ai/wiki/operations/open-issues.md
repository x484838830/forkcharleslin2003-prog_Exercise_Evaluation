# Open issues and known defects

> Sources: CLAUDE.md warnings; handover §5; README.md; git observation of upstream
> Repo: [CLAUDE.md](../../../CLAUDE.md); [docs/handover-筆電.md](../../../docs/handover-筆電.md); [README.md](../../../README.md); [Analysis.html](../../../Analysis.html)
> Synced: 18c41f4
> Anchors: 已知沒做完的小缺口; 還沒驗證; 還沒實作（確認仍壞著）; 一個獨立的小待辦; Figure sizing for print; guard_production; REGISTRY_SCENEPREFIX_ALIASES_
> Raw: [Upstream branch state](../../raw/repo-observations/2026-10-20-upstream-branch-state.md)
> Updated: 2026-10-20

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
