# System map

> Sources: upstream build manual §1 (dev @ da22841); CLAUDE.md File roles
> Repo: [docs/build-from-scratch-從零建置.md](../../../docs/build-from-scratch-從零建置.md); [CLAUDE.md](../../../CLAUDE.md); [apps-script/README.md](../../../apps-script/README.md)
> Synced: 18c41f4
> Anchors: 1-1. 元件一覽; 1-2. 誰呼叫誰; 1-3. 兩種部署形態能做什麼; File roles; Which deployment serves the config branch
> Updated: 2026-10-20

## Overview

The platform has three Google spreadsheets, up to four Apps Script projects, and three static web assets on Vercel. The evaluator form and the dashboard call the backend `ConfigWithSubmit.gs` through `RECORD_URL`. Only a link with no parameters calls the second backend `Config.gs` through `CONFIG_URL`. The report Web App calls the backend's analysis endpoint itself. The setup wizard calls no Web App.

## Components

The build manual names each component with a code. This wiki uses the same codes.

| Code | Component | Kind | Required for one drill |
|---|---|---|---|
| S1 | config spreadsheet | Google Sheet, five tabs | yes |
| S2 | record spreadsheet | Google Sheet, one record tab per session | yes |
| S3 | tenant registry | Google Sheet, tab `租戶註冊表` | no (only for several tenants or sessions) |
| D1 | report template | Google Doc (not a Word file) | no |
| F1 | report output folder | Google Drive folder | no |
| P1 | `ConfigWithSubmit.gs` | standalone Apps Script Web App → `RECORD_URL` | yes |
| P2 | `Config.gs` | standalone Apps Script Web App → `CONFIG_URL` | yes (it can be retired) |
| P3 | report Web App | standalone Apps Script with `Report.gs` → `REPORT_URL` | no, and it needs S3 |
| P4 | setup wizard | `Setup.gs` + `SetupDialog.html` + `QrLib.html`, bound to S3, not deployed | no, and it needs S3 |
| W1 | `Start.dc.html` | static page on Vercel (evaluator form) | yes |
| W2 | `Analysis.html` | static page on Vercel (dashboard) | yes |
| W3 | `support.js`, `vendor/`, `assets/` | static files on Vercel | yes |

The build manual does not recommend a container-bound `Report.gs` under S1 any more. The code still supports it. The only report path in use is the dashboard button 「產生 Google 文件」 → P3.

## Who calls whom

```
Evaluator phone: Start.dc.html
  no parameters        GET  CONFIG_URL                  → P2 Config.gs → S1 (fallback copy)
  ?t= or ?ex=          GET  RECORD_URL?t=&ex=           → P1
  ?t= only             GET  RECORD_URL?action=sessions  → P1
  submit               POST RECORD_URL                  → P1

Quality department: Analysis.html
  GET RECORD_URL?action=analysis&key=                   → P1
  GET RECORD_URL?action=exercises&t=&key=               → P1
  GET REPORT_URL?action=report*&t=&ex=&key=             → P3

P1 ConfigWithSubmit.gs
  reads S3 (cache reg:v2, 120 seconds)
  reads S1 of the resolved registry row
  writes and reads S2 (the resolved record tab)

P3 report Web App
  reads S3 (its own cache rptreg:v1, 120 seconds)
  UrlFetch RECORD_URL?action=analysis                   → P1
  writes 報告快照 and _報告暫存 in S1
  copies D1 to a new Doc and a PDF in F1

P4 setup wizard (bound to S3, calls no Web App)
  copies S1 → adds a record tab in S2 → appends a row in S3 → shows URLs and a QR code
```

## Two deployment shapes

`REGISTRY_SPREADSHEET_ID` decides the shape. An empty value turns the registry off, and every request uses the fallback tenant.

| Feature | Registry off (one session) | Registry on (many tenants and sessions) |
|---|---|---|
| evaluator form with no parameters | works (fallback tenant) | works (fallback tenant) |
| session list with `?t=` only | falls back to one session silently (`REGISTRY_OFF`) | works |
| `?t=&ex=` picks a session | parameters are echoed only | works |
| dashboard | works | works |
| session picker in the dashboard | hidden | works |
| 「產生 Google 文件」 (Doc report) | always disabled | works, if P3 exists and the dashboard URL has `?t=` |
| print view (dashboard report view) | works | works |
| setup wizard | not possible | works |

So the Doc report needs the tenant registry. Production has had a registry since `f813130` (see [Branches and environments](../operations/branches-and-environments.md)).

## Why two config backends exist

`Start.dc.html` keeps both `CONFIG_URL` and `RECORD_URL`. With no `?t=` and no `?ex=`, it calls `CONFIG_URL`. With either parameter, it calls `RECORD_URL`. `Config.gs` has no registry code. If it received a `?t=`, it would serve the hardcoded tenant silently. Do not merge the two URLs into one.

`Config.gs` has drifted from `ConfigWithSubmit.gs`. Some functions must stay equal in both files, for example `readExerciseInfo_`. See [Backend endpoints](../backend/endpoints.md).

## See Also

- [Project purpose](project-purpose.md)
- [Tenant routing](../backend/tenant-routing.md)
- [Deployment and paste order](../operations/deployment.md)
