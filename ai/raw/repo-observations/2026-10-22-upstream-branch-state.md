# Upstream branch state observed with git, and the first merge into the fork

> Source: git fetch and git log of the upstream branches in the local clone (commands run by Claude Code)
> Collected: 2026-10-22
> Published: 2026-10-22

Kind of file: an observation of repository state, plus a short summary of one commit message. The commit message belongs to the upstream author.

## Branch tips (fetched 2026-10-22)

| Branch | Tip | Note |
|---|---|---|
| master | b2c0914 | production. 1 commit after 18c41f4. |
| dev | 4560a1e | 4 commits ahead of master, 1 behind |
| 一版 | a7d1871 | unchanged |
| chart-handoff | bfee602 | unchanged, already contained in master |

The commit that dev lacks is b2c0914. Dev carries the same change as its own commit 4560a1e, with the same subject.

## The new commit on master (dated 2026-10-21)

b2c0914 "Head the dashboard with 機構名稱, not the registry's 顯示名稱". It changes Analysis.html (15 lines) and CLAUDE.md (16 lines). Summary of its message:

- The dashboard header showed the registry's 顯示名稱. In the owner's sheet that value carries version suffixes such as _R7 and _V2.
- The header now shows the 機構名稱 row of the 演習資訊 tab.
- The change splits one helper into two: orgTitle() for which hospital, displayName() for which session.
- orgTitle() feeds #orgTitle, document.title and the report cover's 機構 line. displayName() feeds the CSV filename and the 產生 Google 文件 dialog.
- Each helper falls back to the other when its own field is blank.
- The author records one cost: two sessions of the same hospital now propose the same "Save as PDF" filename.

## The merge into the fork

On 2026-10-22, Claude Code merged upstream/master into the fork's master as commit b1a765f. Git reported no conflicts. The fork's master then contained b2c0914 plus the ai/ workspace commit eed21d0.
