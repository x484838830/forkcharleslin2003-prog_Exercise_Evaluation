# Wiki Log

<!-- Format: ## [YYYY-MM-DD] <action> | <subject>. Actions: sync / ingest / query / lint. Append-only. See SCHEMA.md §6.6. -->

## [2026-10-20] ingest | Initial build of the whole-project wiki
- Disposition: New
- Repo: every tracked file of upstream master at 18c41f4 (CLAUDE.md, README.md, apps-script/README.md, docs/*, code files)
- Raw: raw/owner-decisions/2026-10-20-fork-and-ai-workspace.md
- Raw: raw/repo-observations/2026-10-20-upstream-branch-state.md
- Raw: raw/domain/2020-09-21-ed-rag-resilience-assessment-grid.md
- Raw: raw/domain/2023-09-26-4s-surge-capacity-framework.md
- Raw: raw/domain/rwg-within-group-agreement-index.md
- Created: 25 articles in 7 topics, glossary.md, index.md
- Noted drift: CLAUDE.md names anonCode() (code has buildAnonMap/anonLabel); master CLAUDE.md says dev is behind (dev is ahead on 2026-10-20)

## [2026-10-22] sync | Merge of upstream b2c0914 (dashboard header names the hospital)
- Range: 18c41f4..b1a765f
- Raw: raw/repo-observations/2026-10-22-upstream-branch-state.md
- Reviewed: all 25 articles (CLAUDE.md is cited by every article)
- Updated: frontend/dashboard.md (orgTitle() vs displayName(), the PDF filename cost, Status block for the old title expression)
- Updated: frontend/dashboard-report-view.md (R0 cover line uses orgTitle())
- Updated: operations/branches-and-environments.md (branch tips on 2026-10-22, table of upstream merges into the fork)

## [2026-10-22] ingest | Branches, environments and this fork
- Disposition: Update
- Raw: raw/owner-decisions/2026-10-22-checkout-moved-to-github-folder.md
- Updated: operations/branches-and-environments.md (location of the local checkout)

## [2026-10-22] ingest | Branches, environments and this fork
- Disposition: Update
- Raw: raw/owner-decisions/2026-10-22-relative-paths-only.md
- Updated: SCHEMA.md (new section 9 Paths; 6.4 step 2), scripts/wiki.py (lint reports absolute paths)
- Updated: operations/branches-and-environments.md (checkout folder differs per computer)
- Raw edit under SCHEMA.md §9 rule 7: replaced 3 absolute paths in raw/owner-decisions/2026-10-20-fork-and-ai-workspace.md and raw/owner-decisions/2026-10-22-checkout-moved-to-github-folder.md with words and a [removed] marker
