# Fork notes for Claude

This checkout is the maintainer's fork of `charleslin2003-prog/Exercise_Evaluation`. The root `CLAUDE.md` belongs to upstream. Do not edit it for fork matters.

- Knowledge base and workspace: `ai/`. Start with `ai/SCHEMA.md`, then `ai/wiki/index.md`. The skill `project-wiki` describes the routine.
- Before you rely on the wiki, run `python3 ai/scripts/wiki.py status`. Sync stale articles from the git diff only. Do not rescan the whole repo.
- Remotes: `origin` = the fork (push here, via GitHub Desktop). `upstream` = the original repo (push is blocked on purpose).
- Never write an absolute path (`/Users/<name>/…`, `~/…`, `C:\…`) into any file. Use paths relative to the repo root, or to the file for Markdown links. The maintainer works on more than one computer, and the checkout folder differs between them. Rules: `ai/SCHEMA.md` §9. `python3 ai/scripts/wiki.py lint` reports violations in `ai/` and `.claude/`.
- The maintainer writes in Traditional Chinese. Answer in Traditional Chinese. Wiki articles are in English (STE-flavored), as the maintainer decided on 2026-10-20.
