# Testing

> Sources: CLAUDE.md (smoke.sh and checklist entries); scripts/smoke.sh header; docs/manual-test-checklist.md; docs/dispatch-e2e-manual.md; docs/operator-test-manual.md
> Repo: [CLAUDE.md](../../../CLAUDE.md); [scripts/smoke.sh](../../../scripts/smoke.sh); [docs/manual-test-checklist.md](../../../docs/manual-test-checklist.md); [docs/dispatch-e2e-manual.md](../../../docs/dispatch-e2e-manual.md); [docs/operator-test-manual.md](../../../docs/operator-test-manual.md); [docs/handover-筆電.md](../../../docs/handover-筆電.md)
> Synced: 18c41f4
> Anchors: File roles; guard_production; 還沒驗證; 先搞清楚哪些不用人工做; 為什麼下面這些只能人工; 0. 紅線; Running / viewing
> Updated: 2026-10-20

## Overview

The project has no CI and no unit tests. `scripts/smoke.sh` is the only automated regression. It calls the sandbox backend with curl. Everything that needs Google's runtime (`SpreadsheetApp`, `DriveApp`, `DocumentApp`) or a real screen and camera is a manual test. Three manuals describe manual tests for three different testers. One known defect matters before any test: the production guard of `smoke.sh` no longer recognizes the current production deployments.

## Test tools

| Tool | Tester | What it covers |
|---|---|---|
| `scripts/smoke.sh` | an engineer with a shell | 18 checks against the sandbox. Read-only by default. `--with-write` adds write isolation and idempotency. Exit code 0 or 1. |
| `docs/manual-test-checklist.md` | an engineer | only what cannot be automated, with the reason for each item (M1–M6) |
| `docs/dispatch-e2e-manual.md` | a cloud agent that drives a browser | wizard → evaluator → dashboard → Doc report, with stop conditions |
| `docs/operator-test-manual.md` | the quality department | one full drill and report with no command line |

## smoke.sh

- Keys come from the environment variables `EVAL_KEY_MAIN` and `EVAL_KEY_CLINIC`, never from the file. Without them, the key checks are skipped, not failed.
- It asserts no statistic on purpose. So data drift (for example a longer record sheet) is invisible to it. Do not read a changed number as a regression without a check.
- It checks the red line of the unauthenticated `action=sessions` payload mechanically.
- It derives future and past sessions from the live registry instead of hardcoded codes.
- Run it after every Apps Script redeploy, before manual tests.

> **Status: Outdated** (2026-10-20)
> `CLAUDE.md` says `guard_production` is meant to refuse production `/exec` IDs. It still matches only the two retired production deployments, so it does not block the current production `RECORD_URL`, `CONFIG_URL` or `REPORT_URL`. The stop conditions of `docs/dispatch-e2e-manual.md` have the same stale pair, and its forbidden-spreadsheet row lacks the production registry. Fix all three before you run `--with-write` or a dispatched agent.

## Local viewing

1. Serve the repo folder: `python3 -m http.server`.
2. Open `http://localhost:8000/Start.dc.html` or `http://localhost:8000/Analysis.html`.
3. Add a real `?t=` code. Without it, the dashboard hides the session picker and the Doc button.

In this fork, both pages point at production constants. A local page reads real data. A submit from the local evaluator form writes a real score row. Use the sandbox (`dev` constants) or a copy with test constants for any write test.

## Known untested paths

- the registry hard error `REGISTRY_BROKEN` against a really broken registry
- the time-budget split and the chart fallbacks of `Report.gs`
- the setup wizard's copy-template path (M1), the automatic clear of the old default session (M2), QR printing (M5)
- a new tenant's first session in the wizard

See [Open issues](open-issues.md).

## See Also

- [Deployment and paste order](deployment.md)
- [Source documents](../overview/source-documents.md)
