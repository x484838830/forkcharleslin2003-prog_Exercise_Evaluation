# Knowledge Base Index

Read [SCHEMA.md](../SCHEMA.md) first. Terms: [glossary.md](glossary.md). History: [log.md](log.md).

## overview

What the system is for, its parts, and which documents to trust.

| Article | Summary | Updated |
|---------|---------|---------|
| [Project purpose and users](overview/project-purpose.md) | What the platform does in one drill, who uses it, and the design principles the code follows. | 2026-10-20 |
| [Source documents and how far to trust each](overview/source-documents.md) | The eleven upstream documents, their readers and freshness, and known stale claims. | 2026-10-20 |
| [System map](overview/system-map.md) | Components S1–W3, who calls whom, and the two deployment shapes. | 2026-10-20 |

## domain

The knowledge field: resilience potentials, 4S surge elements, the score scale and the statistics.

| Article | Summary | Updated |
|---------|---------|---------|
| [4S elements (Space, Staff, Stuff, System)](domain/4s-elements.md) | The 4-S surge framework, how the backend splits a 4S cell, and change rules. | 2026-10-20 |
| [Agreement statistics (r_wg, within1, ICC, leniency)](domain/agreement-statistics.md) | r_wg, within1, ICC(2,k) and leniency, with the domain formula. | 2026-10-20 |
| [Observed rate (有效觀察涵蓋率) and the 50% inclusion gate](domain/observed-rate-inclusion-gate.md) | 有效觀察涵蓋率 and the 50% gate; not the same as 演習覆蓋率. | 2026-10-20 |
| [Resilience potentials (評核潛能)](domain/resilience-potentials.md) | 反應/監測/預期/學習 as the four RAG potentials, row groups, and the ability matrix. | 2026-10-20 |
| [Score scale and the not-rated score 0](domain/score-scale.md) | 評分標準 drives the scale; 0 = 不予評分 is never averaged; hazards and client contract. | 2026-10-20 |

## data

The three spreadsheets and the column vocabulary.

| Article | Summary | Updated |
|---------|---------|---------|
| [Config spreadsheet (演習評核_設定)](data/config-spreadsheet.md) | The five tabs of 演習評核_設定 and the owner's rules. | 2026-10-20 |
| [Record spreadsheet (演習評核_紀錄)](data/record-spreadsheet.md) | Record-sheet columns, label snapshot, comments, deduplication. | 2026-10-20 |
| [Tenant registry (租戶註冊表)](data/tenant-registry.md) | Registry columns, the five sanity rules, and hazards. | 2026-10-20 |
| [Vocabulary renames and the alias pattern](data/vocabulary-renames.md) | The 2026-10-12 and 2026-10-16 renames, alias arrays, and the two folding layers. | 2026-10-20 |

## backend

The Apps Script backend: routing, endpoints, the analysis payload.

| Article | Summary | Updated |
|---------|---------|---------|
| [Analysis payload (action=analysis)](backend/analysis-payload.md) | meta, row arrays, stats keys, and the client contract. | 2026-10-20 |
| [Backend endpoints and their red lines](backend/endpoints.md) | Every doGet action and doPost, auth, and the red line for unauthenticated branches. | 2026-10-20 |
| [Tenant routing and the fallback rule](backend/tenant-routing.md) | resolveTenant_ order, REGISTRY_BROKEN, the fallback tenant, post-resolution gates. | 2026-10-20 |

## frontend

The evaluator form and the dashboard.

| Article | Summary | Updated |
|---------|---------|---------|
| [Dashboard report view and the Doc button](frontend/dashboard-report-view.md) | The print view (方案A) sections and the 產生 Google 文件 flow (方案B). | 2026-10-22 |
| [Dashboard (Analysis.html)](frontend/dashboard.md) | Analysis.html: header name helpers, tabs, hidden panels, session picker, anonymity, rules for changes. | 2026-10-22 |
| [Evaluator form (Start.dc.html)](frontend/evaluator-form.md) | Start.dc.html: DC template, screens, picker, comments, URL parameters, storage key. | 2026-10-20 |

## report

The Google Doc report generator.

| Article | Summary | Updated |
|---------|---------|---------|
| [Doc report generator (Report.gs, 方案B)](report/doc-report.md) | Report.gs: Web App and menu shapes, template modes, run mechanics, 報告快照, privacy. | 2026-10-20 |

## operations

Branches, deployment, exposure, testing, the setup wizard and open issues.

| Article | Summary | Updated |
|---------|---------|---------|
| [Branches, environments and this fork](operations/branches-and-environments.md) | master/dev/一版, the constant hazard, Vercel projects, this fork's remotes and its upstream merges. | 2026-10-22 |
| [Deployment and paste order](operations/deployment.md) | Paste and redeploy, deploy order per feature, and how to read what is live. | 2026-10-20 |
| [Open issues and known defects](operations/open-issues.md) | Open defects, code review findings, stale safety tooling, unverified behaviour, documentation drift. | 2026-10-22 |
| [Public exposure and keys](operations/public-exposure.md) | .vercelignore vs .gitignore, keys, unauthenticated branches, evaluator identity. | 2026-10-20 |
| [Setup wizard (Setup.gs, 新增一場演習)](operations/setup-wizard.md) | Setup.gs: what it writes and in which order, hidden coupling, QR codes, gaps. | 2026-10-20 |
| [Testing](operations/testing.md) | smoke.sh, the manual test documents, local viewing, untested paths. | 2026-10-20 |
