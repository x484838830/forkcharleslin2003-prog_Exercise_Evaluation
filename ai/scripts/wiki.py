#!/usr/bin/env python3
"""Maintenance tool for the ai/ knowledge base. Standard library only, Python 3.9+.

The wiki compiles knowledge from two kinds of source:

- Repo files (code and docs of this repository). They change. Each article
  records them in its `> Repo:` field and records the commit it was checked
  against in its `> Synced:` field. Git is the snapshot, so nothing is copied.
- Raw files under ai/raw/. They never change (karpathy-llm-wiki rule).

This tool answers "what must I re-read?" without a full scan:
git diff from each article's Synced commit to HEAD, limited to that
article's Repo files. Optional `> Anchors:` (headings or function names)
narrow it further: an anchor that occurs in the diff marks a likely hit.

Commands (run from anywhere):
  status                 Articles that are stale, grouped by changed repo file.
                         Also: uncommitted changes, uncovered repo files.
  diff FILE [--since S]  Diff of one repo file since the oldest Synced commit
                         of the articles that cite it (or since S).
  synced ART... [--to S] Set the Synced field of articles to HEAD (or S).
                         Run it only after you reviewed the diff.
  evidence [ART...]      Numbers, dates and long quotes in articles must occur
                         in their Repo files (at Synced) or Raw files.
  terms                  Words that wiki/glossary.md lists as "Avoid".
  ste [ART...]           ASD-STE100 structural lint of article prose.
  lint                   links + index + evidence + terms + ste summary.

ART is a path to an article (absolute, or relative to the current
directory, the repo root, or ai/wiki/).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_evidence as ce  # noqa: E402  (vendored, MIT)
import ste_lint  # noqa: E402  (vendored, MIT)

ROOT = HERE.parents[1]
AI = ROOT / "ai"
WIKI = AI / "wiki"
RAW = AI / "raw"
ATTRIBUTES = HERE / "gitattributes"
SPECIAL = {"index.md", "log.md", "glossary.md"}

# Repo paths that need no article. Everything else that git tracks should be
# cited by at least one article, or `status` lists it as uncovered.
COVERAGE_IGNORE = ("ai/", ".claude/", ".idea/", "vendor/", "assets/")

# Our extra header fields are bookkeeping, not evidence.
ce.METADATA_RE = re.compile(
    r"^>\s*(Sources?|Raw|Repo|Synced|Anchors|Collected|Published|Updated|Archived):"
)
FIELD_RE = re.compile(r"^>\s*([A-Za-z]+):\s*(.*)$")
LINK_TARGET_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
TABLE_LINK_RE = re.compile(r"\]\(([^)\s#]+\.md)\)")


# ---------------------------------------------------------------- git helpers

def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", "-c", f"core.attributesFile={ATTRIBUTES}", "-c", "core.quotePath=false", *args],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout


def resolve_sha(ref: str) -> str | None:
    proc = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", ref + "^{commit}"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return proc.stdout.strip() or None


def short(sha: str) -> str:
    return git("rev-parse", "--short=7", sha).strip()


def exists_at(sha: str, path: str) -> bool:
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}:{path}"], cwd=ROOT, capture_output=True
    )
    return proc.returncode == 0


_names_cache: dict[str, set[str]] = {}
_diff_cache: dict[tuple[str, str], str] = {}


def changed_names(sha: str) -> set[str]:
    if sha not in _names_cache:
        out = git("diff", "--name-only", sha, "HEAD")
        _names_cache[sha] = {line for line in out.splitlines() if line}
    return _names_cache[sha]


def diff_text(sha: str, path: str, context: int = 0) -> str:
    key = (sha + f"/U{context}", path)
    if key not in _diff_cache:
        _diff_cache[key] = git("diff", f"-U{context}", sha, "HEAD", "--", path)
    return _diff_cache[key]


def hunk_headers(diff: str) -> list[str]:
    seen: list[str] = []
    for line in diff.splitlines():
        if line.startswith("@@"):
            parts = line.split("@@", 2)
            ctx = parts[2].strip() if len(parts) > 2 else ""
            if ctx and ctx not in seen:
                seen.append(ctx)
    return seen


IDENT_RE = re.compile(r"[A-Za-z_$][\w$]*")


def anchor_in(anchor: str, diff: str) -> bool:
    """An identifier anchor must match as a whole word. Any other anchor
    (a heading, a phrase) matches as a substring."""
    if IDENT_RE.fullmatch(anchor):
        return re.search(r"(?<![\w$])" + re.escape(anchor) + r"(?![\w$])", diff) is not None
    return anchor in diff


def oldest(shas: list[str]) -> str:
    """The commit that is an ancestor of all the others (best effort)."""
    best = shas[0]
    for sha in shas[1:]:
        proc = subprocess.run(
            ["git", "merge-base", "--is-ancestor", sha, best], cwd=ROOT
        )
        if proc.returncode == 0:
            best = sha
    return best


# ------------------------------------------------------------------ articles

@dataclass
class Article:
    path: Path
    text: str
    fields: dict[str, str]
    repo_files: list[str] = field(default_factory=list)
    raw_files: list[Path] = field(default_factory=list)
    anchors: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return self.path.relative_to(AI).as_posix()

    @property
    def synced(self) -> str:
        return self.fields.get("Synced", "").strip().strip("`")

    @property
    def archived(self) -> bool:
        return "Archived" in self.fields


def strip_anchor(link: str) -> str:
    return link.split("#", 1)[0]


def load_article(path: Path) -> Article:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for line in ce.parse_document(text).header:
        m = FIELD_RE.match(line.strip())
        if m:
            name, value = m.group(1), m.group(2).strip()
            fields[name] = (fields[name] + " " + value).strip() if name in fields else value
    art = Article(path=path, text=text, fields=fields)
    for link in LINK_TARGET_RE.findall(fields.get("Repo", "")):
        target = (path.parent / strip_anchor(link)).resolve()
        if not target.is_relative_to(ROOT) or target.is_relative_to(AI):
            art.errors.append(f"Repo link is outside the repo or inside ai/: {link}")
            continue
        art.repo_files.append(target.relative_to(ROOT).as_posix())
    for link in LINK_TARGET_RE.findall(fields.get("Raw", "")):
        target = (path.parent / strip_anchor(link)).resolve()
        if not target.is_relative_to(RAW):
            art.errors.append(f"Raw link is outside ai/raw/: {link}")
        elif not target.is_file():
            art.errors.append(f"Raw link does not resolve: {link}")
        else:
            art.raw_files.append(target)
    art.anchors = [a.strip().strip("`") for a in fields.get("Anchors", "").split(";") if a.strip()]
    if art.repo_files and not art.synced:
        art.errors.append("has Repo links but no Synced field")
    return art


def article_paths() -> list[Path]:
    return [p for p in sorted(WIKI.rglob("*.md")) if p.relative_to(WIKI).as_posix() not in SPECIAL]


def load_all() -> list[Article]:
    return [load_article(p) for p in article_paths()]


def find_article(arg: str) -> Path:
    candidates = [Path(arg), ROOT / arg, WIKI / arg, AI / arg]
    for c in candidates:
        if c.is_file():
            return c.resolve()
    raise SystemExit(f"article not found: {arg}")


def body_lines(text: str) -> list[str]:
    """Title + body, without the metadata header. Keeps line count small."""
    doc = ce.parse_document(text)
    return ([doc.title] if doc.title else []) + list(doc.body)


# -------------------------------------------------------------------- status

def cmd_status(_args) -> int:
    head = resolve_sha("HEAD")
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    print(f"# Wiki status — HEAD {short(head)} on {branch}\n")
    arts = load_all()
    errors: list[str] = []
    per_file: dict[str, list[tuple[Article, str, list[str]]]] = defaultdict(list)
    stale: dict[str, list[str]] = defaultdict(list)
    current, no_repo = [], []
    for a in arts:
        errors += [f"{a.label}: {e}" for e in a.errors]
        if a.archived:
            continue
        if not a.repo_files:
            no_repo.append(a.label)
            continue
        sha = resolve_sha(a.synced) if a.synced else None
        if a.synced and not sha:
            errors.append(f"{a.label}: Synced commit {a.synced} is unknown to git")
            continue
        if not sha:
            continue
        for f in a.repo_files:
            if not exists_at(head, f):
                errors.append(f"{a.label}: Repo file {f} does not exist at HEAD (renamed or deleted?)")
            elif f in changed_names(sha):
                d = diff_text(sha, f)
                hits = [x for x in a.anchors if anchor_in(x, d)]
                per_file[f].append((a, sha, hits))
                stale[a.label].append(f)
        if a.label not in stale:
            current.append(a.label)

    print("## Changed repo files since the articles were synced\n")
    if not per_file:
        print("(none — every article is synced with HEAD for the files it cites)\n")
    for f in sorted(per_file):
        entries = per_file[f]
        since = oldest([sha for _, sha, _ in entries])
        stat = git("diff", "--shortstat", since, "HEAD", "--", f).strip()
        commits = git("rev-list", "--count", f"{since}..HEAD", "--", f).strip()
        print(f"### {f}")
        print(f"- since {short(since)}: {commits} commit(s), {stat or 'no line change'}")
        headers = hunk_headers(diff_text(since, f))
        if headers:
            print("- changed sections/functions (hunk headers):")
            for h in headers[:25]:
                print(f"  - {h}")
            if len(headers) > 25:
                print(f"  - … {len(headers) - 25} more")
        print("- cited by:")
        for a, sha, hits in sorted(entries, key=lambda e: e[0].label):
            if hits:
                mark = "ANCHOR HIT: " + ", ".join(hits)
            elif a.anchors:
                mark = "no anchor hit (skim the hunk headers, then usually just mark synced)"
            else:
                mark = "no anchors (review the diff)"
            print(f"  - {a.label} (synced {short(sha)}) — {mark}")
        print(f"- read: `python3 ai/scripts/wiki.py diff {f}`\n")

    print(f"## Articles to review ({len(stale)})\n")
    for label in sorted(stale):
        print(f"- {label}: {', '.join(stale[label])}")
    if not stale:
        print("(none)")
    print(f"\n## Articles synced with HEAD ({len(current)})\n")
    print(", ".join(sorted(current)) or "(none)")
    if no_repo:
        print(f"\n## Articles with no Repo field ({len(no_repo)}) — raw-only, not tracked by git diff\n")
        print(", ".join(sorted(no_repo)))

    porcelain = git("status", "--porcelain").splitlines()
    dirty = [line[3:] for line in porcelain if not line[3:].startswith(("ai/", ".claude/"))]
    print("\n## Uncommitted changes outside ai/ (info — the wiki syncs to commits)\n")
    if dirty:
        cited = defaultdict(list)
        for a in arts:
            for f in a.repo_files:
                cited[f].append(a.label)
        for f in dirty:
            print(f"- {f}" + (f" — cited by {', '.join(cited[f])}" if cited.get(f) else ""))
    else:
        print("(none)")

    tracked = [p for p in git("ls-files").splitlines() if p]
    cited_all = {f for a in arts for f in a.repo_files}
    uncovered = [p for p in tracked if not p.startswith(COVERAGE_IGNORE) and p not in cited_all]
    print(f"\n## Repo files no article cites ({len(uncovered)})\n")
    print("\n".join(f"- {p}" for p in uncovered) or "(none)")

    print(f"\n## Errors ({len(errors)})\n")
    print("\n".join(f"- {e}" for e in errors) or "(none)")
    return 0


# ---------------------------------------------------------------------- diff

def cmd_diff(args) -> int:
    f = args.file
    if args.since:
        since = resolve_sha(args.since)
        if not since:
            raise SystemExit(f"unknown commit: {args.since}")
    else:
        shas = []
        for a in load_all():
            if f in a.repo_files and a.synced and resolve_sha(a.synced):
                shas.append(resolve_sha(a.synced))
        if not shas:
            raise SystemExit(f"no article cites {f}; pass --since")
        since = oldest(shas)
    print(git("diff", f"-U{args.context}", since, "HEAD", "--", f), end="")
    return 0


# -------------------------------------------------------------------- synced

def cmd_synced(args) -> int:
    target = resolve_sha(args.to or "HEAD")
    if not target:
        raise SystemExit(f"unknown commit: {args.to}")
    value = short(target)
    for arg in args.articles:
        path = find_article(arg)
        lines = path.read_text(encoding="utf-8").split("\n")
        done = False
        for i, line in enumerate(lines):
            if re.match(r"^>\s*Synced:", line):
                lines[i] = f"> Synced: {value}"
                done = True
                break
        if not done:
            for i, line in enumerate(lines):
                if re.match(r"^>\s*Repo:", line):
                    lines.insert(i + 1, f"> Synced: {value}")
                    done = True
                    break
        if not done:
            print(f"skip {arg}: no Repo field")
            continue
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"{path.relative_to(AI).as_posix()}: Synced -> {value}")
    return 0


# ------------------------------------------------------------------ evidence

BINARY_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".woff", ".woff2")
_show_cache: dict[str, str] = {}
LEADING_MARKER_RE = re.compile(r"^[ \t]*(?:>[ \t>]*|//+[ \t]*)", re.M)


def repo_text(ref: str, path: str) -> str:
    key = f"{ref}:{path}"
    if key not in _show_cache:
        text = git("show", key)
        # A quote may wrap across lines of a Markdown blockquote or a code
        # comment. Drop the line-leading markers so the wrapped text joins.
        text = LEADING_MARKER_RE.sub("", text)
        _show_cache[key] = ce.normalize(text)
    return _show_cache[key]


def evidence_corpus(a: Article) -> list[str]:
    corpus = []
    sha = resolve_sha(a.synced) if a.synced else None
    for f in a.repo_files:
        ref = sha or "HEAD"
        if not f.lower().endswith(BINARY_SUFFIXES) and exists_at(ref, f):
            corpus.append(repo_text(ref, f))
    for p in a.raw_files:
        corpus.append(ce.source_content(p))
    return corpus


def evidence_report(arts: list[Article]) -> tuple[int, int]:
    suspects = errors = 0
    print("## Fidelity suspects (judge each one; derived values may be fine)\n")
    for a in arts:
        if a.archived:
            continue
        if not a.repo_files and not a.raw_files:
            continue
        corpus = evidence_corpus(a)
        misses = []
        for cand in ce.extract_candidates(a.text):
            cand = ce.Candidate(cand.kind, ce.normalize(cand.value))
            if not any(ce.contains(src, cand) for src in corpus):
                misses.append(cand.value)
        if misses:
            print(a.label)
            for m in misses:
                print(f"- {m}")
            print()
            suspects += len(misses)
    if not suspects:
        print("(none)\n")
    print("## Evidence errors\n")
    for a in arts:
        if a.archived:
            continue
        problems = list(a.errors)
        if not a.repo_files and not a.raw_files:
            problems.append("article has neither Repo nor Raw sources")
        for p in problems:
            print(f"- {a.label}: {p}")
            errors += 1
    if not errors:
        print("(none)")
    orphans = ce.unreferenced_raws(AI)
    print("\n## Raw files no article cites\n")
    print("\n".join(f"- {p}" for p in orphans) or "(none)")
    return suspects, errors


def cmd_evidence(args) -> int:
    arts = [load_article(find_article(a)) for a in args.articles] if args.articles else load_all()
    print("# Evidence check\n")
    s, e = evidence_report(arts)
    print(f"\n{s} suspect(s), {e} error(s)")
    return 0


# --------------------------------------------------------------------- terms

def glossary_avoid() -> list[tuple[str, str]]:
    path = WIKI / "glossary.md"
    if not path.is_file():
        return []
    rules = []
    header = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        row = dict(zip(header, cells))
        avoid = row.get("Avoid", "")
        use = row.get("Term", "").replace("*", "")
        for word in avoid.split(","):
            word = word.strip().strip("`").strip()
            if word and word not in ("—", "-"):
                rules.append((word, use))
    return rules


def prose_lines(text: str) -> list[tuple[int, str]]:
    """(line number, text) for the title and body. The metadata header, fenced
    code, inline code and link targets are removed."""
    out = []
    state = "before_title"
    fence = None
    for n, line in enumerate(text.splitlines(), 1):
        if fence:
            if ce.is_fence_closer(line, *fence):
                fence = None
            continue
        opener = ce.fence_opener(line)
        if opener:
            fence = opener
            state = "body"
            continue
        stripped = line.strip()
        if state == "before_title" and line.startswith("# "):
            state = "after_title"
        elif state in ("after_title", "header"):
            if not stripped and state == "after_title":
                continue
            if stripped.startswith(">"):
                state = "header"
                continue
            state = "body"
        out.append((n, ce.strip_noise(line)))
    return out


def terms_report(arts: list[Article]) -> int:
    rules = glossary_avoid()
    hits = 0
    for a in arts:
        for lineno, line in prose_lines(a.text):
            for word, use in rules:
                if word.isascii():
                    found = re.search(r"(?<![\w-])" + re.escape(word) + r"(?![\w-])", line, re.I)
                else:
                    found = word in line
                if found:
                    print(f"- {a.label}:{lineno}: \"{word}\" — glossary says use: {use}")
                    hits += 1
    if not hits:
        print("(none)")
    return hits


def cmd_terms(_args) -> int:
    print("# Glossary avoid-list check\n")
    n = terms_report(load_all())
    print(f"\n{n} hit(s). Quote a forbidden word in `backticks` when you must name it.")
    return 0


# ----------------------------------------------------------------------- ste

def ste_findings(a: Article) -> tuple[list[dict], int]:
    lines = body_lines(a.text)
    findings, words = ste_lint.lint("\n".join(lines), a.label)
    return findings, words


def cmd_ste(args) -> int:
    arts = [load_article(find_article(a)) for a in args.articles] if args.articles else load_all()
    total_hard = 0
    for a in arts:
        findings, words = ste_findings(a)
        hard = sum(1 for f in findings if f["level"] != "advisory")
        total_hard += hard
        if args.articles:
            for f in findings:
                print(f"{f['file']}:{f['line']}:{f['col']} {f['rule']} [{f['match']}] {f['message']}")
        print(f"{a.label}: {hard} hard, {len(findings) - hard} advisory, {words} words")
    print(f"\n{total_hard} hard finding(s). Line numbers count from the title (header removed).")
    return 0


# ---------------------------------------------------------------------- lint

def links_report() -> int:
    broken = 0
    for path in sorted(WIKI.rglob("*.md")):
        text = ce.strip_fences(path.read_text(encoding="utf-8"))
        for link in LINK_TARGET_RE.findall(text):
            if re.match(r"^[a-z]+:", link) or link.startswith("#"):
                continue
            target = (path.parent / strip_anchor(link)).resolve()
            if not target.exists():
                print(f"- {path.relative_to(AI).as_posix()}: broken link {link}")
                broken += 1
    if not broken:
        print("(none)")
    return broken


def index_report(arts: list[Article]) -> int:
    index = WIKI / "index.md"
    problems = 0
    listed: dict[str, str] = {}
    if index.is_file():
        for line in index.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            m = TABLE_LINK_RE.search(line)
            if m:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                listed[(WIKI / m.group(1)).resolve().as_posix()] = cells[-1] if cells else ""
    for a in arts:
        key = a.path.resolve().as_posix()
        want = (a.fields.get("Archived") or a.fields.get("Updated") or "").strip()
        if key not in listed:
            print(f"- not in index: {a.label}")
            problems += 1
        elif want and listed[key] != want:
            print(f"- index date {listed[key]} != article date {want}: {a.label}")
            problems += 1
    known = {a.path.resolve().as_posix() for a in arts}
    for key in listed:
        if key not in known:
            print(f"- index entry has no file: {key}")
            problems += 1
    if not problems:
        print("(none)")
    return problems


def cmd_lint(_args) -> int:
    arts = load_all()
    print("# Wiki lint\n\n## Broken links\n")
    b = links_report()
    print("\n## Index consistency\n")
    i = index_report(arts)
    print("\n# Evidence\n")
    s, e = evidence_report(arts)
    print("\n## Glossary avoid-list\n")
    t = terms_report(arts)
    print("\n## STE structural lint (hard findings per article)\n")
    hard_total = 0
    for a in arts:
        findings, _ = ste_findings(a)
        hard = sum(1 for f in findings if f["level"] != "advisory")
        hard_total += hard
        if hard:
            print(f"- {a.label}: {hard}")
    if not hard_total:
        print("(none)")
    print(
        f"\n## Summary\n{b} broken link(s), {i} index problem(s), {s} fidelity suspect(s), "
        f"{e} evidence error(s), {t} glossary hit(s), {hard_total} STE hard finding(s).\n"
        "Freshness is a separate check: python3 ai/scripts/wiki.py status"
    )
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="wiki.py", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(func=cmd_status)
    p = sub.add_parser("diff")
    p.add_argument("file")
    p.add_argument("--since")
    p.add_argument("--context", type=int, default=3)
    p.set_defaults(func=cmd_diff)
    p = sub.add_parser("synced")
    p.add_argument("articles", nargs="+")
    p.add_argument("--to")
    p.set_defaults(func=cmd_synced)
    p = sub.add_parser("evidence")
    p.add_argument("articles", nargs="*")
    p.set_defaults(func=cmd_evidence)
    sub.add_parser("terms").set_defaults(func=cmd_terms)
    p = sub.add_parser("ste")
    p.add_argument("articles", nargs="*")
    p.set_defaults(func=cmd_ste)
    sub.add_parser("lint").set_defaults(func=cmd_lint)
    args = parser.parse_args(argv[1:])
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
