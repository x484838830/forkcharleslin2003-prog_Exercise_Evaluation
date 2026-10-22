# Code review of the fork, and a read-only check of the live question trees

> Source: code review by Claude Code at commit 6fbf608, plus read-only GET requests to the production config branch (commands run by Claude Code)
> Collected: 2026-10-22
> Published: 2026-10-22

Kind of file: an observation. The owner asked in chat: 「那你檢查一下這些程式有什麼問題？」

## Syntax check

Claude Code extracted every inline script and ran the macOS JavaScriptCore `checkSyntax` on it. A deliberately broken file confirmed that the checker reports errors. All 8 scripts passed: the 5 .gs files, the scripts of Start.dc.html, Analysis.html, ReportDialog.html and SetupDialog.html.

## Live question trees (read-only)

Claude Code fetched action=sessions and the config branch for the two sessions of tenant [removed: 醫院代號]. These are the same GET requests that an evaluator's phone sends. No request wrote data.

| Session | Structure | Leaves | Questions | Duplicate leaf names | Duplicate question IDs | Blank question IDs |
|---|---|---|---|---|---|---|
| 2026a | one-level | 4 | 21 | none | none | none |
| 2026b | two-level, 7 top nodes | 11 | 23 | none | none | none |

Both sessions returned the score levels 4, 3, 2, 1, 0. Both returned submitOpen false. No top-level node of 2026b came back as a leaf, so no 地點 lost its scenes.

Conclusion: the three latent defects about the question tree (blank 演練單元 cell, duplicate leaf name, duplicate question ID) do not occur in the live data on this date.
