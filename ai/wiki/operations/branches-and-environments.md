# Branches, environments and this fork

> Sources: CLAUDE.md branch sections; git observation of upstream branches; maintainer decisions in chat
> Repo: [CLAUDE.md](../../../CLAUDE.md)
> Synced: b1a765f
> Anchors: Branch state; Branch policy
> Raw: [Upstream branch state](../../raw/repo-observations/2026-10-20-upstream-branch-state.md); [Upstream branch state, 2026-10-22](../../raw/repo-observations/2026-10-22-upstream-branch-state.md); [Checkout moved to the GitHub folder](../../raw/owner-decisions/2026-10-22-checkout-moved-to-github-folder.md); [Relative paths only](../../raw/owner-decisions/2026-10-22-relative-paths-only.md); [Fork setup and the AI workspace](../../raw/owner-decisions/2026-10-20-fork-and-ai-workspace.md)
> Updated: 2026-10-22

## Overview

Upstream has two live branches. `master` is production: a push deploys the hospital's site. `dev` is the sandbox: a push deploys the test site, and its constants point at the developer's own spreadsheets. The branch `一版` is the rollback point. This checkout is a fork. It pushes only to the fork, so no push from here can deploy either site. The Apps Script backends are never deployed by a push, on any branch.

## Upstream branches

| Branch | Role | Tip on 2026-10-20 |
|---|---|---|
| `master` | production. Every constant holds a production value. | `18c41f4` |
| `dev` | sandbox. Same code, sandbox constants. | `04d51cb`, 3 commits ahead of `master` |
| `一版` | rollback point before the 2026-10-14 release | `a7d1871` |
| `chart-handoff` | old work branch, already merged into `master` | `bfee602` |

Branch tips on 2026-10-22 (the next fetch):

| Branch | Tip on 2026-10-22 | Change since 2026-10-20 |
|---|---|---|
| `master` | `b2c0914` | 1 new commit: the dashboard header names the hospital, not the session (see [Dashboard](../frontend/dashboard.md), Header) |
| `dev` | `4560a1e` | 4 commits ahead of `master`, 1 behind. `4560a1e` carries the same change as `b2c0914` as a separate commit. |
| `一版` | `a7d1871` | none |
| `chart-handoff` | `bfee602` | none |

History in short:

1. Until 2026-10-14, `master` was frozen at `a7d1871` and work happened on `dev`.
2. The 2026-10-14 release promoted `dev` onto `master`.
3. After the release, the owner asked for changes directly on production, so `master` took direct commits and `dev` stayed behind.
4. On 2026-10-20, upstream brought `dev` level with `master` again (`4c0aee5`) and added `scripts/sync-dev-from-master.sh` (`88d6a66`) on `dev` only.

> **Status: Outdated** (2026-10-20)
> The `master` copy of `CLAUDE.md` (Branch policy) says that `dev` is behind production. The git observation of 2026-10-20 shows `dev` 3 commits ahead and 0 behind. The `dev` copy of `CLAUDE.md` was updated. The `master` copy was not.

### The constant hazard

Each branch carries environment constants in `Start.dc.html`, `Analysis.html`, `ConfigWithSubmit.gs` and `Config.gs`: the spreadsheet IDs, the `/exec` URLs, the registry ID and the keys. A merge between `master` and `dev` carries the other branch's values across. The `dev` commit message of `88d6a66` says that the test site once read and wrote the hospital's real record spreadsheet, on 2026-10-14. The sync script exists to stop a repeat. Its order: merge without commit, pin the sandbox values, check, and commit only when every check passes.

`ANALYSIS_KEY` is the same on both branches (verified byte-identical on 2026-10-12). So the sandbox and production are not isolated at the key layer. See [Public exposure and keys](public-exposure.md).

## Environments

| Environment | Site | Deploys from |
|---|---|---|
| production | the Vercel project of the hospital's site | push to upstream `master` |
| sandbox | a second Vercel project, the test site | push to upstream `dev` |

The Vercel setting that picks the branch is under Settings → Environments → Production → Branch Tracking. Neither site has an `index.html`, so the root path returns 404. A URL must name the file, for example `/Start.dc.html?t=…`.

## This fork

| Remote | Points at | Push |
|---|---|---|
| `origin` | `x484838830/forkcharleslin2003-prog_Exercise_Evaluation` | yes. GitHub Desktop pushes here. |
| `upstream` | `charleslin2003-prog/Exercise_Evaluation` | blocked. The push URL is a dummy value. |

- On the maintainer's main computer, the checkout is in the folder `GitHub` on the Desktop, next to the maintainer's other repositories. It moved there on 2026-10-22.
- The maintainer works on more than one computer, and the folder can differ on each one. So no file in `ai/` or `.claude/` holds an absolute path (SCHEMA.md §9).
- The fork has all four upstream branches.
- The fork is not connected to Vercel, so a push to the fork deploys nothing.
- The fork is public. A fork of a public repository cannot be made private.
- The maintainer pushes with GitHub Desktop. Explain steps in GitHub Desktop terms.

### How to bring upstream changes into the fork

1. Fetch `upstream`: run `git fetch upstream`, or ask Claude to run it.
2. Merge `upstream/master` into the fork's `master`. In GitHub Desktop: Branch → Merge into current branch → `upstream/master`.
3. Run `python3 ai/scripts/wiki.py status` and follow SCHEMA.md §6.1 to sync the wiki.

Do not merge upstream `dev` into the fork's `master`. `dev` carries sandbox constants.

Merges done so far:

| Date | Upstream commit | Merge commit in the fork | Conflicts |
|---|---|---|---|
| 2026-10-22 | `b2c0914` | `b1a765f` | none |

## See Also

- [Deployment and paste order](deployment.md)
- [Public exposure and keys](public-exposure.md)
- [Testing](testing.md)
