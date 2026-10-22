# ai/ knowledge base — schema and rules

This file is the rule set for the ai/ knowledge base and workspace. Every agent that reads or writes ai/ obeys it. The file `.claude/skills/project-wiki/SKILL.md` only points here.

The design joins two methods:

- **Storage:** the LLM wiki method of [karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki). Sources go into `raw/`. The agent compiles them into articles in `wiki/`. The wiki grows and stays correct over time.
- **Writing:** the ASD-STE100 discipline of [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill). One term has one meaning. One sentence has one claim. The next agent must not misread an article.

The language of the wiki is English. Chinese words that are names in the product (sheet names, column headers, UI labels, potential values) stay in Chinese, because they are identifiers. `wiki/glossary.md` gives each one an English meaning.

## 1. Layout

```
ai/
├── SCHEMA.md            this file
├── README.md            for the human owner (Traditional Chinese)
├── raw/<topic>/         immutable sources that are NOT in the repo
├── wiki/
│   ├── index.md         one row per article, grouped by topic
│   ├── log.md           append-only operation log
│   ├── glossary.md      canonical terms and the words to avoid
│   └── <topic>/<article>.md
├── work/
│   ├── active/          one note per task in progress
│   └── done/            closed task notes
└── scripts/
    ├── wiki.py          status, diff, synced, evidence, terms, ste, lint
    ├── check_evidence.py   vendored (MIT), used by wiki.py
    ├── ste_lint.py         vendored (MIT), used by wiki.py
    └── gitattributes    lets git name the Markdown heading of each diff hunk
```

`wiki/` has one level of topic folders. Do not nest deeper.

## 2. Two kinds of source

| Kind | Where | Changes? | How an article cites it |
|---|---|---|---|
| Repo file | the repository itself (code, `CLAUDE.md`, `README.md`, `docs/`) | yes, with every commit | `> Repo:` links, plus `> Synced:` = the commit the article was checked against |
| Raw file | `ai/raw/<topic>/` | never | `> Raw:` links |

Do not copy repo files into `raw/`. Git already keeps every version. The `Synced` commit is the snapshot.

Put a source in `raw/` only when it is not in the repo. Examples: a decision the owner states in chat, a web page about the domain, a screenshot description, meeting notes.

## 3. The grounding rule

Every number, date and direct quote in an article must occur verbatim in a source that the article cites. For a repo file, the source is the file at the `Synced` commit.

1. Find the value in the source before you write it (grep or read).
2. Write it exactly as the source writes it.
3. For a value that you computed, show its parts. Each part must be in a source.
4. If you cannot find a value, do not write its exact form.

`wiki.py evidence` checks this. It reports suspects. You judge each suspect.

Write commit hashes, function names, constants, file paths and Chinese identifiers in `backticks`. The evidence check and the glossary check skip text in backticks.

## 4. Article format

```markdown
# <Title>

> Sources: <who or what, plain words>
> Repo: [CLAUDE.md](../../../CLAUDE.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs)
> Synced: <7-character commit hash>
> Anchors: <heading or function name>; <another>
> Raw: [<raw title>](../../raw/<topic>/<file>.md)
> Updated: YYYY-MM-DD

## Overview

<One paragraph: what this article says.>

## <Sections>

## See Also

- [<Other article>](../<topic>/<article>.md)
```

- `Repo`, `Synced`, `Anchors` and `Raw` are optional. An article needs `Repo` or `Raw`, or both.
- Paths are relative to the article file. From `wiki/<topic>/`, the repo root is `../../../` and `raw/` is `../../raw/`.
- `Anchors` lists the source headings and function names that the article depends on. Use the most specific heading (the `###` or `####` heading, not the `##` heading). `wiki.py status` searches the diff for each anchor.
- `Updated` is the date the knowledge changed. A typo fix does not change it. A sync with no content change does not change it.
- Status blocks go directly under a claim that is no longer true as written:

```markdown
> **Status: Outdated** (YYYY-MM-DD)
> <What changed. What is true now. Which source says so.>

> **Status: Disputed**
> <The two claims, each with its source.>
```

Never delete history silently. Mark it.

## 5. Writing rules (STE-flavored)

Articles use the STE-flavored mode. Procedures, checklists and task notes in `work/` use the strict mode.

Structural rules. Obey all of them:

1. Use active voice. Name the actor. Passive voice is permitted only when the actor is unknown or not important.
2. Write one claim per sentence. Write one instruction per sentence.
3. Keep a description sentence at 25 words or fewer. Keep an instruction at 20 words or fewer.
4. Do not use semicolons in prose.
5. Do not use phrasal verbs ("set up" → "configure", "find out" → "learn").
6. Do not stack more than three nouns ("record sheet header alias" → "the alias of a record-sheet header").
7. Keep subjects, verbs and articles. Do not drop words to save space.
8. Use a list for three or more steps or conditions.
9. Keep one topic per paragraph, six sentences or fewer.
10. Keep modality. "May", "can", "probably" carry information. Do not change "may fail" into "fails".
11. Do not add a fact, a cause or a frequency that the source does not state.
12. Use verbs, not nouns made from verbs ("perform an analysis" → "analyze").
13. Do not use marketing words (robust, seamless, powerful).

Lexical rules:

1. Use the term that `wiki/glossary.md` gives. Use it every time. Do not rotate synonyms.
2. A word in the glossary "Avoid" column may appear only in `backticks`, for example when an article names an old alias.
3. When a new concept needs a name, add it to the glossary first.

`wiki.py ste` runs the vendored STE linter on article prose. `wiki.py terms` checks the glossary. Both report. Neither edits.

## 6. Operations

### 6.1 Sync (the repo changed)

Use this after new commits arrive: your own edits, a pull from the fork, or a merge from `upstream` (the original repo). Do not re-read the whole repo.

1. Run `python3 ai/scripts/wiki.py status`.
2. For each changed file in the report, read the hunk headers and the anchor hits.
3. Run `python3 ai/scripts/wiki.py diff <file>` for each file that has an anchor hit or an article with no anchors. Read only that diff.
4. Update each affected article. Refresh its `Updated` date when the knowledge changed. Add a Status block when an old claim is no longer true.
5. Run `python3 ai/scripts/wiki.py synced <article>...` for every article that you reviewed, changed or not.
6. Look at "Repo files no article cites". Create an article, or add the file to an existing article's `Repo` field.
7. Update `wiki/index.md` for every article whose `Updated` date changed.
8. Append one entry to `wiki/log.md` (format in 6.6).

A large file (for example `CLAUDE.md` or `apps-script/Report.gs`) changes often. Many articles cite it. The anchors keep the work small: an article with no anchor hit usually needs only step 5.

### 6.2 Ingest (a new source that is not in the repo)

1. Save the source as `raw/<topic>/YYYY-MM-DD-<slug>.md`. Use the raw header in 6.7. Keep the original text. Remove only formatting noise.
2. Search `wiki/` for the key terms and their synonyms.
3. State the disposition: **New**, **Update**, **Disputed** or **No material**.
4. Compile: merge into an article with the same core subject, or create a new article. Obey section 3.
5. Search the whole wiki for other claims that the source changes (cascade). Update each affected article.
6. Update `wiki/index.md` and append to `wiki/log.md`.

For **No material**, keep the raw file, log it, and stop.

### 6.3 Query (answer a question)

1. Read `wiki/index.md`. Then search `wiki/` with the key terms and their synonyms.
2. Read the articles. Answer with links to them.
3. Prefer the wiki over memory. If the wiki and the code disagree, the code wins. Check the code, answer from the code, and then fix the wiki (6.1).
4. A query writes no file, unless the user asks to save the answer. A saved answer is an archive page: `> Archived: YYYY-MM-DD` instead of `> Updated:`, `> Sources:` links to the wiki articles, no `Repo` or `Raw`. Archive pages are never updated later.

### 6.4 Lint (health check)

1. Run `python3 ai/scripts/wiki.py lint`.
2. Fix broken links, index rows and absolute paths (section 9).
3. Judge each fidelity suspect. Fix the real ones.
4. Fix glossary hits and STE hard findings in the articles you touch.
5. Report contradictions, missing cross-links and concepts that need their own article. Do not fix them silently.
6. Append a lint entry to `wiki/log.md`.

### 6.5 Work (a task in progress)

1. Create `work/active/YYYY-MM-DD-<slug>.md` when a task needs more than one session or more than one step.
2. Write in it: the goal, the decisions with the reason for each, the steps, the open questions.
3. Write each decision of the owner into `raw/owner-decisions/` too. A task note is a working file. A raw file is evidence.
4. When the task closes, move the note to `work/done/`. Ingest what the task taught into the wiki.

### 6.6 Log format

```
## [YYYY-MM-DD] sync | <short subject>
- Range: <old commit>..<new commit>
- Reviewed: <article>, <article>
- Updated: <article> (<what changed>)

## [YYYY-MM-DD] ingest | <primary article title>
- Disposition: New | Update | Disputed
- Raw: raw/<topic>/<file>.md
- Updated: <cascade article>

## [YYYY-MM-DD] ingest | no material: raw/<topic>/<file>.md
- Disposition: No material

## [YYYY-MM-DD] query | Archived: <page title>

## [YYYY-MM-DD] lint | <N> issues found, <M> fixed
```

The log is append-only.

### 6.7 Raw file header

```markdown
# <Title>

> Source: <URL, or "owner in chat with Claude">
> Collected: YYYY-MM-DD
> Published: YYYY-MM-DD or Unknown

<original content>
```

## 7. Safety rules

The fork is a public GitHub repository. Everything in ai/ is public.

1. Do not write a key, a password, a token or a spreadsheet ID into ai/. Name the constant instead (`ANALYSIS_KEY`, `RECORD_SPREADSHEET_ID`).
2. Do not write a deployment `/exec` ID. Name the constant (`RECORD_URL`).
3. Do not write a real `醫院代號` value (the `?t=` code). The `?t=` code is the only barrier between a stranger and the score form. Write `<hid>` instead.
4. Do not write evaluator codes with their scores, or any observation text from a real drill.
5. Do not write personal data about a person.
6. If a source contains one of these items, leave the item out of the raw file and write `[removed: <kind>]`.

## 8. Precedence

1. The code is the final authority. A wiki article is a compiled summary, and a summary can be out of date.
2. The repo's own `CLAUDE.md` names an owner document for some facts ("Where each fact lives"). The wiki cites that owner. The wiki does not compete with it.
3. Do not edit `CLAUDE.md`, `README.md` or `docs/` to fix the wiki. Those files belong to the upstream project. Edit them only when the user asks for a change to the project.

## 9. Paths

The maintainer works on more than one computer. The checkout can be in a different folder on each computer. An absolute path works on one computer only.

1. Do not write an absolute path into `ai/` or `.claude/`. Examples: `/Users/<name>/…`, `/home/<name>/…`, `~/…`, `C:\…`.
2. In a Markdown link, use a path relative to the file that contains the link. Section 4 shows the form.
3. In prose, in a task note and in a command, use a path relative to the repository root. Example: `ai/scripts/wiki.py`.
4. Write each command so that it runs from the repository root.
5. In a script, find files from the location of the script. Do not write a fixed folder into a script. `wiki.py` uses `Path(__file__)`.
6. To name the location of the checkout itself, use words. Example: "the folder `GitHub` on the Desktop".
7. If a source contains an absolute path, write `[removed: absolute path]` in the raw file, or use words as in rule 6.
8. `wiki.py lint` reports each absolute path in `ai/` and `.claude/`. Fix each one before you commit.
