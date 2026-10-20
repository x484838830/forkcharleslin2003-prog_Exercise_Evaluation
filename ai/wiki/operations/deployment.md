# Deployment and paste order

> Sources: CLAUDE.md branch-state warning and deploy-order bullets; apps-script/README.md; setup manual §4; handover §6
> Repo: [CLAUDE.md](../../../CLAUDE.md); [apps-script/README.md](../../../apps-script/README.md); [docs/setup-三支apps-script.md](../../../docs/setup-三支apps-script.md); [docs/handover-筆電.md](../../../docs/handover-筆電.md); [docs/build-from-scratch-從零建置.md](../../../docs/build-from-scratch-從零建置.md)
> Synced: 18c41f4
> Anchors: Branch state; Backend / data architecture; 4. 重新部署的規矩; 6. 會浪費你時間的坑; 4-2. 順序; 4-6. 回滾
> Updated: 2026-10-20

## Overview

The platform has two deploy channels, and they do not move together. A push to an upstream branch deploys the static pages through Vercel. The Apps Script code deploys only when a person pastes it into each project by hand. Apps Script has no deploy hook. So after every backend change there is a window with a new frontend and an old backend, or the reverse. Each feature has a deploy order that keeps that window safe.

## Paste and redeploy

| Project | Kind | After a paste |
|---|---|---|
| `ConfigWithSubmit.gs` (behind `RECORD_URL`) | Web App | redeploy |
| `Config.gs` (behind `CONFIG_URL`) | Web App | redeploy |
| `Report.gs` as the report Web App (behind `REPORT_URL`) | Web App | redeploy |
| `Setup.gs` + `SetupDialog.html` + `QrLib.html` | bound to the tenant registry | save and reload the sheet. No deployment. |
| `Report.gs` + `ReportDialog.html` bound to the config spreadsheet | container-bound (only if a copy exists) | save and reload the sheet |

How to redeploy a Web App:

1. In the Apps Script editor, open Deploy → Manage deployments.
2. Edit the **existing** deployment.
3. Set Version to "New version". Execute as "Me". Access "Anyone".
4. Deploy.

Never pick 新增部署 (`New deployment`). It creates a different `/exec` URL. The pages keep calling the old URL, and the old URL keeps serving the old version. Nothing shows an error.

A Web App serves its pinned version until someone redeploys it. A paste without a redeploy changes nothing for users.

A container-bound script must be pasted from the sheet's own menu (擴充功能 → Apps Script). A project created from the Apps Script home page is standalone and fails with `Cannot call SpreadsheetApp.getUi()`.

## Deploy order

The general rule is: the side that tolerates the other side's old version goes first.

| Change | Order |
|---|---|
| 4S split (2026-10-16) | push the pages → paste `Report.gs` and redeploy, confirm `REPORT_BUILD_` → paste `ConfigWithSubmit.gs` and redeploy |
| score scale (2026-10-16) | the same order. `Config.gs` needs nothing for the scale. |
| inclusion gate (2026-10-17) | push the pages → (`Report.gs` first if it changed) → paste `ConfigWithSubmit.gs` and redeploy |
| new report template | paste `Report.gs` and redeploy → confirm with 檢查設定 → switch `REPORT_TEMPLATE_DOC_ID` |
| header rename | paste both config backends → then the owner renames the sheet |

The 2026-10-14 release showed the risk of the reverse order. With a new frontend and an old backend, evaluators saw the comment box, and the old backend dropped the text. Close such a window fast, and never during a live drill.

The evaluator form must never lag the 評分標準 sheet. An old form on a 0–4 sheet produces wrong data that no deploy repairs.

## How to know what is deployed

Read the live endpoints, not the commits. `CLAUDE.md` says its table "records repo constants, not deploy state".

- The config branch returns `exerciseLocation` in new versions.
- `action=analysis` returns `meta.scale`, `r.s4List`, `stats.unratedQuestions` (2026-10-16), and `meta.exerciseLocation`, `stats.inclusion`, `r.included` (2026-10-17).
- The report Web App's `reportCheck` echoes `REPORT_BUILD_`. It is the only direct version read.

On 2026-10-20 `CLAUDE.md` recorded all three Web Apps as current with the 2026-10-17 pastes.

A field fingerprint proves only that the live code is at least that new. It does not prove that the whole file equals a commit. The live `Config.gs` was once a hand-edited mix.

## Static site

- Vercel builds after a push. The build time varies. To confirm, compare a hash of the file in git with a hash of the file that the site serves.
- `.vercelignore` decides which files the site serves (see [Public exposure and keys](public-exposure.md)).

## Rollback

The rollback point for the pages is the branch `一版` (`a7d1871`). It has no `.vercelignore`, so a rollback re-opens the file exposure. The build manual §4-6 describes the full rollback.

## See Also

- [Branches and environments](branches-and-environments.md)
- [System map](../overview/system-map.md)
- [Testing](testing.md)
