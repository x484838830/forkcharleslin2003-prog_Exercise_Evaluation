# Public exposure and keys

> Sources: CLAUDE.md exposure sections; .vercelignore; .gitignore; handover §1
> Repo: [CLAUDE.md](../../../CLAUDE.md); [.vercelignore](../../../.vercelignore); [.gitignore](../../../.gitignore); [docs/handover-筆電.md](../../../docs/handover-筆電.md)
> Synced: b1a765f
> Anchors: Open on `master`: Vercel serves the whole repo; Branch state; The `action=sessions` exposure; 1. ⚠️ 先看這個：沙箱與正式站共用同一把分析金鑰; 7. 工作習慣
> Updated: 2026-10-20

## Overview

The upstream repo is public, and so is the fork. So the project has two outward interfaces with different repair costs. Vercel serves files from the repo, and `.vercelignore` controls which ones. Git history is public on GitHub, and `.gitignore` controls what enters it. A Vercel setting takes effect on the next deploy. Git history cannot be cleaned. The dashboard's access control is an unshared URL plus an analysis key that the page itself contains. So the key is public by design, and the real secrets are the evaluator data and the write path.

## Two layers

| Layer | File | Controls | Repair |
|---|---|---|---|
| website | `.vercelignore` | which repo files the site serves | the next deploy |
| git | `.gitignore` | which files enter the public history | not possible after a push |

- The site needs only `Start.dc.html`, `Analysis.html`, `support.js`, `vendor/` and `assets/`.
- `.vercelignore` excludes `apps-script/`, `docs/`, `*.md`, `scripts/` and scratch files. Before the 2026-10-14 release, production served `CLAUDE.md` and the backend source. They returned 404 when re-checked on 2026-10-16.
- `.gitignore` excludes `*.tsv` spreadsheet exports. The owner chose on 2026-10-12 to keep them out of git.
- Any new backend file, internal document or scratch file needs a rule in `.vercelignore`. A file with real data also needs a rule in `.gitignore`.

For this fork: the `ai/` folder is public on GitHub. The fork has no website. If anyone connects the fork to Vercel, add `ai/` and `.claude/` to `.vercelignore` first.

## Keys and what they protect

| Secret | Where | Status |
|---|---|---|
| `ANALYSIS_KEY` | embedded in `Analysis.html` and the backend | public by design. It guards `action=analysis` for the fallback tenant. |
| `分析金鑰` per session | the tenant registry | the key a dashboard link carries. Rotation is a one-cell edit. |
| `ADMIN_KEY` | the backend | empty in production, so `selftest` and `flush` are off |
| `REPORT_ANALYSIS_KEY` and others | script properties of the report project | never in the repo |
| `醫院代號` (`?t=`) | registry, evaluator links | the only barrier between a stranger and the score form |

Problem recorded in `CLAUDE.md` and the handover: `dev` and `master` hold the same `ANALYSIS_KEY` (verified byte-identical on 2026-10-12). A sandbox tester holds production's key. The designed repair is one key per registry row, with the constant only for the fallback tenant.

## Unauthenticated branches

The config branch, `action=sessions` and `doPost` need no key. Every evaluator's phone calls them. Their payloads must never carry IDs, keys, sheet names, row numbers or file names. See the red line in [Backend endpoints](../backend/endpoints.md).

`action=sessions` lets a holder of one tenant's `?t=` code list that tenant's sessions. This is accepted, because the session picker needs it. No endpoint lists tenant codes.

## Evaluator identity

- The dashboard hides the per-evaluator table (`#detail`) and shows anonymous labels by default.
- The Doc report is anonymous by default. Identified output needs three deliberate steps.
- 報告快照 never stores evaluator codes, per-evaluator scores or comments.

## Rules for the wiki

SCHEMA.md §7 applies. Name a constant, never its value. Never copy a tenant code, an ID, a key or an e-mail address into `ai/`.

## See Also

- [Backend endpoints](../backend/endpoints.md)
- [Branches and environments](branches-and-environments.md)
- [Dashboard](../frontend/dashboard.md)
