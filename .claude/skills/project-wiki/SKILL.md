---
name: project-wiki
description: "Use at the start of any task in the Exercise_Evaluation repo (演習評核: Start.dc.html, Analysis.html, apps-script/, docs/), and whenever the user asks what the project does, asks to change the dashboard (分析平台), the evaluator form, the backend or the report, asks to sync or update the knowledge base, or names ai/, the wiki, 知識庫 or 工作區. The ai/ folder holds a compiled LLM wiki of this project with git-based incremental sync."
---

# Project wiki (ai/)

This repository has a compiled knowledge base in `ai/`. Use it before you read the large source files.

1. Read `ai/SCHEMA.md`. It is the only rule set. Obey it.
2. Read `ai/wiki/index.md` and `ai/wiki/glossary.md`.
3. Run `python3 ai/scripts/wiki.py status`. If an article is stale, sync it first (SCHEMA.md §6.1). Read only the diffs that the status report names.
4. Answer from the wiki articles, and check the code when the answer will drive a change. The code wins over the wiki.
5. When your work teaches something new or changes the code, update the wiki in the same session (SCHEMA.md §6.1 and §6.2), then run `python3 ai/scripts/wiki.py lint`.
6. For a task with more than one step or session, keep a note in `ai/work/active/` (SCHEMA.md §6.5).

The user is the maintainer of a fork. Pushes go to the fork only, through GitHub Desktop. Never push to `upstream`. The dashboard's constants point at production data: never run a write path against production for a test. Never write an absolute path into a file. Use relative paths (SCHEMA.md §9), because the maintainer works on more than one computer.
