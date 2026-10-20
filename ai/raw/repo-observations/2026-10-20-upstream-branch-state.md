# Upstream branch state observed with git

> Source: git log of the upstream branches in the local clone (commands run by Claude Code)
> Collected: 2026-10-20
> Published: 2026-10-20

Kind of file: an observation of repository state, plus short summaries of three commit messages. Commit messages belong to the upstream author.

## Branch tips (fetched 2026-10-20)

| Branch | Tip | Note |
|---|---|---|
| master | 18c41f4 | production. The checkout of this wiki tracks it. |
| dev | 04d51cb | 3 commits ahead of master, 0 behind |
| 一版 | a7d1871 | the rollback point before the 2026-10-14 release |
| chart-handoff | bfee602 | already contained in master (0 commits ahead) |

## The 3 commits on dev that master does not have (all dated 2026-10-20)

1. 4c0aee5 "Bring dev level with production, keeping the sandbox data". Summary of its message: dev had been stuck at 4782edf since the 2026-10-14 release and was 20 commits behind. The commit fast-forwarded dev to 18c41f4, then switched the eight environment constants back to the sandbox. It rewrote the inline comments that said 正式分支（master）, because a comment that describes the wrong branch reads as confirmation. It changed the Branch state section of the dev copy of CLAUDE.md to say that the reader is on dev.
2. 88d6a66 "Add a script that keeps dev level with master without drifting to production". It adds scripts/sync-dev-from-master.sh (303 lines) and 17 lines in CLAUDE.md. Summary of its message:
   - The failure the script prevents: the test site silently reading and writing the hospital's real record spreadsheet. The message says this "already happened once on 2026-10-14".
   - Order of the script: merge --no-commit --no-ff, then pin the sandbox constants, then verify, then commit only when every check is green. A failure leaves the merge in progress, and git merge --abort undoes it.
   - It checks a whitelist: every /exec id in the shipped files must be one of the three sandbox deployments. It also pins ANALYSIS_KEY and detects conflict markers.
   - It notes that the smoke.sh guard is broken today because production moved to new deployments.
3. 04d51cb "Number the picker rows on single-level drills". It changes Start.dc.html only (11 lines added).
