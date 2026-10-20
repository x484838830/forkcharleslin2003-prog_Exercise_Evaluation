# Doc report generator (Report.gs, 方案B)

> Sources: CLAUDE.md report generator section; Report.gs constants
> Repo: [CLAUDE.md](../../../CLAUDE.md); [apps-script/Report.gs](../../../apps-script/Report.gs); [apps-script/ReportDialog.html](../../../apps-script/ReportDialog.html); [docs/owner-guide-多醫院多演習.md](../../../docs/owner-guide-多醫院多演習.md)
> Synced: 18c41f4
> Anchors: Report generator (方案B); REPORT_BUILD_; REPORT_SECTIONS_; COVER_TOKENS_; COVER_TOKENS_SILENT_; FILL_IMAGE_TOKENS_; FILL_ROW_TOKENS_; scanTemplate_; scanAnchors_; planFillSlots_; chartCapability_; emitChart_; legacyChartBlob_; verifyIcc_; finalizeRun_; leftoverTokens_; plainToken_; SNAPSHOT_COLUMNS_; 14. 產生正式評核報告
> Updated: 2026-10-20

## Overview

`Report.gs` writes the committee report. It reads `action=analysis` over `UrlFetchApp`, copies an owner-owned template Doc, fills it, and exports a PDF. It never recomputes the statistics, so the Doc and the dashboard cannot disagree. In production it runs as a standalone report Web App behind `REPORT_URL`, which the dashboard button 產生 Google 文件 calls. The file still supports a container-bound copy under the config spreadsheet with a 演習評核報告 menu. No container-bound copy is recorded for production. `REPORT_BUILD_` (now `'2026-10-17 template'`) is the only version string that anyone can read from outside.

## Two ways to run the same file

| Shape | How it starts | Which session |
|---|---|---|
| report Web App (production path) | `doGet` serves `reportCheck`, `reportStart`, `reportContinue`, `reportStatus`, `reportAbandon` | the `t` and `ex` that the dashboard sends. The Web App resolves the config spreadsheet through the registry. |
| container-bound under 演習評核_設定 | the 演習評核報告 menu and `ReportDialog.html` | fixed by the script properties `REPORT_TENANT` and `REPORT_EXERCISE` |

The container-bound shape has a product gap. A session that the setup wizard creates gets a fresh key. So the menu cannot report on that session until someone edits three properties.

## Configuration

- The `.gs` code is ES5 only (`var`, function declarations, no arrow functions, no template literals). `ReportDialog.html` is browser JS and is exempt.
- No key is in the file. Script properties hold `REPORT_ANALYSIS_KEY`, `REPORT_API_URL`, `REPORT_TEMPLATE_DOC_ID` (required) and `REPORT_OUTPUT_FOLDER_ID`, `REPORT_TENANT`, `REPORT_EXERCISE`, `REPORT_TIME_BUDGET_MS` (optional). `REPORT_RUN_STATE` is maintained by the program.
- Bump `REPORT_BUILD_` on every edit. The 檢查設定 check (`reportCheck`) echoes it.

## Template: two shapes

The template Doc is required, not optional: `DocumentApp` has no page-number API. Page numbers, logo, fonts, margins, heading styles and the signature block live in the template.

| Shape | Tokens | Rule |
|---|---|---|
| anchor mode | `{{SEC_*}}` paragraphs, one per chapter | delete an anchor to skip a chapter. Six anchors are required. An anchor must be a bare top-level paragraph. |
| fill mode (the owner's shape) | `{{圖_*}}` image tokens alone in a 1×1 table, `{{列_*}}` row tokens in the sample row of a two-row table | `FILL_IMAGE_TOKENS_` and `FILL_ROW_TOKENS_` own the token list and the column contract |

The two shapes are mutually exclusive (`scanTemplate_`). Cover tokens (`COVER_TOKENS_`) are plain text and valid anywhere. `COVER_TOKENS_SILENT_` lists those whose absence must not warn.

The owner's final template (2026-10-17) uses fill mode. It places 8 of the 15 cover tokens, so each run logs one warning about seven missing tokens. That is by design. The template file lives in the owner's OneDrive, not in the repo.

**Deploy order for a new template:** paste `Report.gs` and redeploy first, check `REPORT_BUILD_` with 檢查設定, then point `REPORT_TEMPLATE_DOC_ID` at the new template. An older `Report.gs` refuses a template with unknown row tokens.

## Run mechanics

- **Steps.** Apps Script stops a call after 6 minutes. So the run is split across calls, each with its own quota. Each call stops at `REPORT_TIME_BUDGET_MS` (default 240000). A partial run is labelled in three places:
  - a draft banner in the Doc
  - the suffix （部分完成） in the file name
  - the status column of 報告快照
- **No overwrite.** Four layers protect against a double click. The main one: every run copies a new Doc, so the code never writes into an existing report.
- **Charts degrade, never fail.** `chartCapability_()` probes once per run. The fallback chain per figure:
  1. native chart
  2. COLUMN redraw (only for RADAR and BAR figures)
  3. the older Charts service (`legacyChartBlob_`)
  4. a Docs table of the same numbers
  5. a paragraph that names the failure Every degradation lands in the warnings and in 附錄C. No run is known to have reached a fallback.
- The iso-3D chart is not reproduced. A grouped column chart carries the same numbers.

## 報告快照

An append-only sheet in the config spreadsheet, text format. Each run freezes its labels and aggregates there before it writes the Doc. It closes defect D3 for reports and is the only data source for a future comparison with an earlier drill. It records **no evaluator code, no per-evaluator score and no comment text, ever**. Do not rename its headers in code without editing the live sheet on the same day (`SNAPSHOT_COLUMNS_`).

## Privacy

- Anonymous is the default: 評核官 1…N by index in the sorted `meta.evaluatorCodes`, the same rule as the dashboard. The code-to-number table is never printed.
- Identified output needs three things: a dialog checkbox, a `window.confirm()`, and a `{{SEC_評核官差異}}` anchor. The choice is marked on the cover, in 附錄C and in `REPORT_RUN_STATE`.
- 附錄B (per question × per evaluator) is off by default.
- 附錄C may print file names but never keys, spreadsheet IDs or the `/exec` URL.

## Verified runs

- 2026-10-09: the first end-to-end run. 檢查設定 passed all 14 items. The run wrote 21/21 chapters and appendices A–D, a 35-page PDF. Native charts worked.
- 2026-10-20: `reportCheck` reported `2026-10-17 template`, matching the repo. 檢查設定 passed 23/23 on the fill-mode template.
- Still unverified: the time-budget split across calls and every chart fallback.

## Lessons recorded in CLAUDE.md

1. **A wrong hint is worse than no hint.** Three wrong error hints each sent a tester to check the one thing that was not broken. When the cause is not provable, list the candidates.
2. **A warning printed into 附錄C must not contain a complete token** such as `{{機構名稱}}`. The leftover-token scan would find the report's own text. Pass it through `plainToken_`.

## See Also

- [Dashboard report view and the Doc button](../frontend/dashboard-report-view.md)
- [Analysis payload](../backend/analysis-payload.md)
- [Deployment and paste order](../operations/deployment.md)
- [Observed rate and the inclusion gate](../domain/observed-rate-inclusion-gate.md)
