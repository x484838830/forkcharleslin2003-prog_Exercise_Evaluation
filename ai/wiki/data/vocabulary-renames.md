# Vocabulary renames and the alias pattern

> Sources: CLAUDE.md rename section; README.md rename table
> Repo: [CLAUDE.md](../../../CLAUDE.md); [README.md](../../../README.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [apps-script/Config.gs](../../../apps-script/Config.gs); [Analysis.html](../../../Analysis.html)
> Synced: b1a765f
> Anchors: The 2026-10-12 renames; 2026-10-12 的兩個改名; normPotential_; normalisePotentials; RECORD_STAGE_ALIASES_; RECORD_GOAL_ALIASES_; GROUP_HEADER_ALIASES_; GOAL_HEADER_ALIASES_; SNAPSHOT_COLUMNS_
> Updated: 2026-10-20

## Overview

The owner renamed product words twice: on 2026-10-12 and on 2026-10-16. Each rename followed one pattern. The new name became canonical. The old names stayed accepted. The spreadsheets did not have to change on the same day. `CLAUDE.md` calls this the single most confusing thing in the codebase. Read this article before you compare against a potential value or a column header.

## The renames

| Date | Old | New | Where |
|---|---|---|---|
| 2026-10-12 | `情境` | 場景 | display words and column names |
| 2026-10-12 | `回應` | 反應 | a potential value in the 評核潛能 cells (not a header) |
| 2026-10-16 | `情境階段`, `場景階段` (層1) | 地點 | the top group column, and the 階段 column labels in the dashboard and the Doc report |
| 2026-10-16 | `測試情境`, `測試場景與目標` | 場景說明 | the scene description column |

`層2` was not renamed. It is still 演練單元.

## Headers: alias arrays

A header rename puts the new name first in each alias array and keeps every old name behind it. Four arrays carry the 層1 and 場景說明 names:

| Constant | Side |
|---|---|
| `RECORD_STAGE_ALIASES_` | record sheet |
| `RECORD_GOAL_ALIASES_` | record sheet |
| `GROUP_HEADER_ALIASES_` | config sheet (also copied in `Config.gs`) |
| `GOAL_HEADER_ALIASES_` | config sheet (also copied in `Config.gs`) |

`RECORD_GOAL_ALIASES_` and `GOAL_HEADER_ALIASES_` hold the same values today. They stay separate constants on purpose: one names a source column, the other a snapshot column. Do not share the variable.

On 2026-10-16 the owner renamed the sheet first. Every backend from before that date throws on the header 地點. So a new header works only after both `ConfigWithSubmit.gs` and `Config.gs` are pasted.

## Values: two folding layers for `回應` → 反應

The potential value lives in cells, not in a header. The owner did not edit the cells. So two layers fold the old value, and both are load-bearing:

1. `normPotential_(v)` in `ConfigWithSubmit.gs` strips a trailing 潛能 (since 2026-10-16) and maps `回應` to 反應. It runs in `readIndicatorFull_` and in the snapshot read of `buildAnalysis_`.
2. `normalisePotentials(DATA)` in `Analysis.html` rewrites `r.potential` on every row, then folds the keys of `stats.potentials` and `stats.potentialByS4`. The radars filter rows by `r.potential`, so the row rewrite is the important part. It protects the dashboard from an old backend.

The live 對應指標 sheet still contains `回應` (verified 2026-10-12). Always compare against 反應. A comparison against `回應` makes only the 反應 group vanish, which is harder to notice than a total failure.

## Deliberate leftovers

Do not "tidy up" these:

- The Doc report's chapter anchor is still `{{SEC_情境}}`. An anchor must match the text in the owner's template. A change without a template change on the same day removes chapter 9.
- `SNAPSHOT_COLUMNS_` (報告快照) still says 階段 and `測試場景與目標`. A renamed snapshot header makes every report run throw until someone edits the live sheet.

## One dangerous miss

`REGISTRY_SCENEPREFIX_ALIASES_` has no 場景前綴 alias. See [Tenant registry](tenant-registry.md).

## Rule for future renames

1. Put the new name first in every alias array that holds the old one, in every backend copy.
2. Keep every old name.
3. Paste the backends before the owner renames the sheet.
4. Update `README.md`, because it is the owner's contract.
5. Update `wiki/glossary.md`: add the old name to the Avoid column.

## See Also

- [Config spreadsheet](config-spreadsheet.md)
- [Resilience potentials](../domain/resilience-potentials.md)
- [Glossary](../glossary.md)
