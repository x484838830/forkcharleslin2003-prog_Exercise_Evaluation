# Relative paths only, so the checkout works on any computer

> Source: owner in chat with Claude
> Collected: 2026-10-22
> Published: 2026-10-22

> 另外也要寫進知識庫一個規則，都不要用絕對路徑，都用相對路徑，不然跨電腦無法操作。

Decision: no file in the knowledge base or the fork's Claude settings may hold an absolute path. Every path is relative: to the repository root in prose and commands, and to the containing file in Markdown links. The reason the owner gave: the owner operates the project from more than one computer, and an absolute path breaks on another computer.

Done on 2026-10-22:

- ai/SCHEMA.md got section 9 (Paths). Section 6.4 now lists absolute paths among the lint fixes.
- .claude/CLAUDE.md and .claude/skills/project-wiki/SKILL.md each got one line that points at section 9.
- ai/scripts/wiki.py lint got a check that reports absolute paths in ai/ and .claude/. On its first run it found 3, all in two raw files under owner-decisions. Claude Code replaced them with words and a [removed: …] marker.
- The scripts already found their files from their own location, so no script needed a change.
