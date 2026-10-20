# Source documents and how far to trust each

> Sources: the upstream repo's own documents and their stated dates
> Repo: [CLAUDE.md](../../../CLAUDE.md); [README.md](../../../README.md); [apps-script/README.md](../../../apps-script/README.md); [docs/build-from-scratch-從零建置.md](../../../docs/build-from-scratch-從零建置.md); [docs/handover-筆電.md](../../../docs/handover-筆電.md); [docs/multi-tenant-and-report-plan.md](../../../docs/multi-tenant-and-report-plan.md); [docs/owner-guide-多醫院多演習.md](../../../docs/owner-guide-多醫院多演習.md); [docs/setup-三支apps-script.md](../../../docs/setup-三支apps-script.md); [docs/operator-test-manual.md](../../../docs/operator-test-manual.md); [docs/manual-test-checklist.md](../../../docs/manual-test-checklist.md); [docs/dispatch-e2e-manual.md](../../../docs/dispatch-e2e-manual.md)
> Synced: 18c41f4
> Anchors: Where each fact lives; 0-4. 文件與程式不一致時; 實作進度; 線上狀態不等於 repo; 還沒開始：把「產生評核報告」搬到分析平台
> Updated: 2026-10-20

## Overview

The upstream repo has eleven documents besides the code. They have different readers and different dates. Several of them contain claims that newer documents or the code have replaced. Read this article before you trust a claim from one of them. The code is the final authority. The build manual states this rule itself (§0-4, 程式贏).

## The documents

| Document | Reader | Purpose | Freshness |
|---|---|---|---|
| `CLAUDE.md` | developers and agents | architecture, design reasons, contracts between files | the most complete and the most current. Its Branch state table records repo constants, not deploy state. |
| `README.md` | the owner | the spreadsheet-filling contract for each sheet and column | current. A backend change that changes what is read or written must update it. |
| `apps-script/README.md` | developers | where each `.gs` file is pasted, script properties | partly stale: it lists `Report.gs` as container-bound only. `CLAUDE.md` and the build manual describe the report Web App. |
| `docs/build-from-scratch-從零建置.md` | developers | build the platform from zero. Promote `dev` to `master`. | based on `dev` @ `da22841` (2026-10-13). Line numbers drift. |
| `docs/handover-筆電.md` | developers | state that git cannot show: what runs live, sheet contents, next steps | written 2026-10-12 and 2026-10-13. §0 is newer than the rest. Parts of §5 are older than the 2026-10-14 release. |
| `docs/multi-tenant-and-report-plan.md` | developers | the decision record: tenancy options, report options, defects D1–D5, cheap fixes §6 | 實作進度 at the top is current. The rest is written in the future tense about code before the change. |
| `docs/owner-guide-多醫院多演習.md` | the owner | tenant registry procedures: add a tenant, add a session, end a session, rotate a key | current for procedures |
| `docs/setup-三支apps-script.md` | the quality department | set up the Apps Script projects with no engineering skills | marks each claim 〔實測〕 (tested) or 〔推論〕 (read from code). It contains real sandbox IDs. |
| `docs/operator-test-manual.md` | the quality department | run one full drill and report, step by step, with no command line | tested on 10-13 |
| `docs/manual-test-checklist.md` | developers | tests that only a human can do, with the reason for each | M3 is done. Other items are open. |
| `docs/dispatch-e2e-manual.md` | a cloud agent that drives a browser | end-to-end test from wizard to report | its stop conditions name retired `/exec` IDs (see [Testing](../operations/testing.md)) |

## Where each fact lives

`CLAUDE.md` names one owner for each kind of fact. Other documents must cite the owner and not restate it. The wiki follows the same rule.

| Fact | Owner |
|---|---|
| column names, aliases, accepted potential values | the `*_ALIASES_` constants in `apps-script/ConfigWithSubmit.gs` |
| how a 4S cell is split, and which words map to which 4S element | `S4_VALUE_ALIASES_` and `splitS4_` in `ConfigWithSubmit.gs` |
| the score scale | each drill's own 評分標準 sheet, derived by `scaleOf_` (server) and `scoreScale()` (evaluator form). The fixed rule "0 is never averaged" is `NOT_RATED_SCORE_`. |
| the 50% inclusion gate | `OBSERVED_RATE_MIN_` in `ConfigWithSubmit.gs` |
| the chapter count and the chart fallback layers of the Doc report | `apps-script/Report.gs` (`REPORT_SECTIONS_`, `emitChart_`) |
| live spreadsheet state | `docs/handover-筆電.md` §4 |
| Apps Script script properties | `apps-script/README.md` |
| constants per branch and key state | the Branch state table in `CLAUDE.md` |

## Known stale claims

Each item below is a claim in an older document that a newer source replaced.

1. `docs/handover-筆電.md` §5 says that the Doc report is not yet available from the dashboard. The build manual (2026-10-13) and `CLAUDE.md` say that the dashboard calls the report Web App through `REPORT_URL`, and that 產生 Google 文件 is enabled.
2. `docs/handover-筆電.md` §5 says that all work is on `dev` and that `master` has none of it. The 2026-10-14 release promoted `dev` onto `master`. Since then, `master` took direct commits and `dev` is behind (`CLAUDE.md`, Branch policy).
3. `docs/multi-tenant-and-report-plan.md` says that report option B never ran. It ran on 2026-10-09.
4. `apps-script/README.md` says that `Report.gs` is container-bound under 演習評核_設定. The production setup uses a standalone report Web App (`CLAUDE.md`, File roles).

## Rules for agents

1. When two documents disagree, check the code. Then record the result in the wiki with a Status block.
2. Do not edit upstream documents to fix the wiki. The wiki records the conflict.
3. Do not copy IDs, keys or e-mail addresses from these documents into the wiki (SCHEMA.md §7).

## See Also

- [Project purpose](project-purpose.md)
- [Testing](../operations/testing.md)
- [Open issues](../operations/open-issues.md)
