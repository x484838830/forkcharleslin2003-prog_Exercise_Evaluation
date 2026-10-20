# Project purpose and users

> Sources: upstream repo documentation (CLAUDE.md, README.md, docs/build-from-scratch-從零建置.md, docs/setup-三支apps-script.md); maintainer request in chat
> Repo: [CLAUDE.md](../../../CLAUDE.md); [README.md](../../../README.md); [docs/build-from-scratch-從零建置.md](../../../docs/build-from-scratch-從零建置.md); [docs/setup-三支apps-script.md](../../../docs/setup-三支apps-script.md)
> Synced: 18c41f4
> Anchors: What this repo is; Report generator (方案B); 1-2. 誰呼叫誰; Panels with no tab button
> Raw: [Fork setup and the AI knowledge workspace](../../raw/owner-decisions/2026-10-20-fork-and-ai-workspace.md)
> Updated: 2026-10-20

## Overview

The system scores hospital emergency drills (演習評核). Evaluators score a drill on their phones. A Google Apps Script backend stores the scores in Google Sheets. A dashboard analyzes the scores per session. A report generator writes a Google Doc and a PDF for a committee. The hospital that the sources name is 萬芳醫院. The maintainer forked the project to add features to the dashboard without a change to the live platform.

## What happens in one drill

1. The owner prepares a config spreadsheet: drill info, evaluator codes, the score scale, the questions, and the indicator map.
2. The owner opens a session in the tenant registry. The setup wizard can do this step.
3. During the drill, each evaluator opens the evaluator form on a phone, picks an evaluator code, picks a scene, and scores each question.
4. The backend appends one record row per question to the record sheet.
5. After the drill, the quality department opens the dashboard. The dashboard reads the analysis payload of the session.
6. The dashboard can print a report view. It can also start the Doc report, which a separate Apps Script Web App writes.

## Who uses it

| Role | Uses | Source of the fact |
|---|---|---|
| evaluator | `Start.dc.html` on a phone, mobile size 390×844 | `CLAUDE.md`, What this repo is |
| owner | the spreadsheets. `README.md` is the owner's filling contract. | `CLAUDE.md`, File roles |
| quality department (品管中心) | `Analysis.html` | build manual §1-2 diagram. The setup manual is addressed to 品管中心. |
| advisor (老師) | sets scoring rules, for example the 50% inclusion gate on 2026-10-17 | `README.md` |
| committee | reads the Doc report. `CLAUDE.md` calls the Doc report the committee deliverable. | `CLAUDE.md`, Report generator |

`CLAUDE.md` describes the quality department as "a ten-person quality department". In a group of that size, an evaluator code is at best a pseudonym. This fact drives the privacy rules of the dashboard (see [Dashboard](../frontend/dashboard.md)).

## What the system measures

Each question maps to one potential and to one or more 4S elements.

- The potentials come from resilience thinking: 反應, 監測, 預期 and 學習. See [Resilience potentials](../domain/resilience-potentials.md).
- The 4S elements are Space, Staff, Stuff and System. See [4S elements](../domain/4s-elements.md).
- The owner's source document for the combination is a Word file named 「韌性潛能與 4S 擴容元素整合矩陣表」. Its twelve cell texts are the `ABILITY_NOTES` of the dashboard.

## Where the project came from

The project started as a design mockup. A visual design tool exported `Start.dc.html` as a standalone page. `CLAUDE.md` says the markup and inline styles hold the design's precise values. The data flow is real and in production use.

## Design principles that the code follows

These principles recur in `CLAUDE.md`. A change that breaks one of them needs a decision from the owner.

1. **A configuration mistake must not cost scores.** The server does not reject a submission because of a comment rule or a score range.
2. **Links that evaluators already have must keep working.** A link with no parameters sends byte-identical requests to the requests it sent before multi-tenancy.
3. **The spreadsheet is the configuration.** The config spreadsheet is never cached, so an edit takes effect when the phone reloads.
4. **A partial deployment must degrade, not break.** Clients accept an old backend. Deploy order rules exist for each change (see [Deployment and paste order](../operations/deployment.md)).
5. **A wrong answer that looks right is worse than a visible error.** For example, a broken tenant registry gives a hard `REGISTRY_BROKEN` error instead of a silent fallback.
6. **Evaluator identity stays hidden by default.** The per-evaluator table has no tab button, and reports are anonymous by default.

## See Also

- [System map](system-map.md)
- [Source documents](source-documents.md)
- [Glossary](../glossary.md)
