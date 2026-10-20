# Dashboard report view and the Doc button

> Sources: CLAUDE.md report view sections; Analysis.html code
> Repo: [CLAUDE.md](../../../CLAUDE.md); [Analysis.html](../../../Analysis.html)
> Synced: 18c41f4
> Anchors: Report view (`body.reportMode`); 優勢前三項／待改善前三項; Figure sizing for print; enterReport; exitReport; renderReport; renderReportSummary; renderReportQuality; renderReportAppendixC; rankedTop; abilityCells; docBtnBlockReason; docEndpoint; openDocOptions; runDocCheck; docStart; docOnStep; docAbandon; docStatus
> Updated: 2026-10-20

## Overview

The dashboard has two report paths. The button 產生報告 opens a print view of the same page (方案A, `body.reportMode`). `CLAUDE.md` says the page itself calls this view an internal review copy. The button 產生 Google 文件 asks the report Web App behind `REPORT_URL` to write a Doc and a PDF (方案B). The Doc report is the committee deliverable. Both paths use the session that the dashboard shows, because both read the in-memory `DATA`.

## The print view (方案A)

- `enterReport()` enters it. `#backBtn` leaves it. `?view=report` opens it on load. The button works only after `init()` succeeds.
- **Reuse is by CSS, never by cloning.** A clone would duplicate SVG ids such as `covGrad` and `covClip` and break one copy. `init()` fills every panel first. The report view changes only visibility and shows hidden `[data-reportonly]` wrappers. Section order is DOM order.

| Section | Content |
|---|---|
| R0 `#reportCover` | cover with editable fields (演習地點, 報告版次, 文件編號, 製表, 審核, 核定). Nothing saves them. 演習地點 is prefilled from `meta.exerciseLocation`. |
| R1 `#reportHint` | print hints, screen only. It holds two checkboxes. |
| R2 `#reportSummary` | overall mean, three potentials, drill coverage, agreement, within1, not-rated rate, top three and bottom three ability cells |
| R3–R6 | the panels `#overview`, `#s4`, `#radars`, `#coverage` as they are |
| R7 | `#ranking`, only when `#includeRanking` is checked (default off) |
| R8 `#reportComments` | the comments |
| R9 `#reportQuality` | data quality: missing questions, not-rated rate, row counts, label sources, excluded questions |
| R10 | `#method` |
| R11 `#reportAppendixC` | file names, sheet name, row count, tenant, session, time. No key, no spreadsheet ID, no URL. |

### The ability tables

`abilityCells()` reads `stats.potentialByS4`, the same data as the iso-3D chart. `rankedTop(cells, n, asc)` uses competition ranking and keeps every tie. "Top three" caps the rank, not the number of rows. The owner asked for this: the naive version dropped a fourth cell with the same score.

### Printing

- `:root{--figW:10cm;--figH:14.5cm}` sizes every figure in print. The orientation (10 wide, 14.5 tall) is literal and not yet checked on paper.
- `#coverageGauge` is not covered by the size rule.
- The user must tick Chrome's 背景圖形 option, or the iso-3D cubes and the color spectrum print white.
- Page numbers are not possible. Chrome supports no CSS page-margin boxes. Chrome's own header and footer would print the URL with the key. So `enterReport()` removes the query string with `history.replaceState`. A reload after that needs the key again.

## The Doc button (方案B)

`docBtnBlockReason()` keeps the button disabled while any of these is true:

1. a run is in progress
2. `REPORT_URL` is empty
3. no key
4. no data yet
5. the session is not routed by the tenant registry (`meta.tenant` or `meta.exercise` empty). The fallback tenant cannot get a Doc report from this button.

The flow:

1. `openDocOptions()` shows three options and a check button. The texts match `ReportDialog.html` word for word, because one `Report.gs` serves both paths. One deliberate difference: here every option is off by default since 2026-10-13.
2. `runDocCheck()` calls `reportCheck` and lists the checks.
3. `docStart()` starts a run. The identified mode needs a checkbox and a `window.confirm()`. `Report.gs` checks this again on the server.
4. The page calls `reportContinue` in a loop, one chapter batch per call, and shows progress, a timer and warnings.
5. `docAbandon()` and `docStatus()` handle a stuck run.

`docEndpoint(action)` builds `REPORT_URL?action=…&t=…&ex=…&key=…`. Because it sends the analysis key, `REPORT_URL` may only name a deployment that the owner controls.

## See Also

- [Dashboard](dashboard.md)
- [Doc report generator](../report/doc-report.md)
- [Public exposure and keys](../operations/public-exposure.md)
