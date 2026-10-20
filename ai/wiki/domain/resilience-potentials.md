# Resilience potentials (評核潛能)

> Sources: Chuang, Ou, Hollnagel, Hou 2020 (ED-RAG, PLoS One); CLAUDE.md; README.md; backend and dashboard code
> Repo: [CLAUDE.md](../../../CLAUDE.md); [README.md](../../../README.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [Analysis.html](../../../Analysis.html)
> Synced: 18c41f4
> Anchors: normPotential_; buildAnalysis_; ABILITY_NOTES; 優勢前三項／待改善前三項; 設定試算表填寫說明（對應指標
> Raw: [ED-RAG paper notes](../../raw/domain/2020-09-21-ed-rag-resilience-assessment-grid.md)
> Updated: 2026-10-20

## Overview

Each question has one potential in the 評核潛能 column of 對應指標. The accepted values are 反應, 監測, 預期 and 學習, plus any value that contains 覆蓋率. The first four match the four potentials of resilient performance in resilience engineering: respond, monitor, anticipate and learn. Hollnagel's resilience assessment grid (RAG) measures these four potentials. The repo does not name its theoretical source. But the live indicator header contains the text `(RAG / 覆蓋率)`, so the indicators probably come from a RAG adaptation. The analysis uses 反應, 監測 and 預期 (the three potentials) for most statistics. It excludes 學習 from them.

## The domain: four potentials of resilient performance

The ED-RAG paper (Chuang, Ou, Hollnagel, Hou, 2020) gives these definitions:

| Potential | Question it asks | Value in this system |
|---|---|---|
| respond | What does the organization need to respond timely and effectively to what happens? | 反應 |
| monitor | How well does the organization detect changes, and are its indicators meaningful? | 監測 |
| anticipate | Can the organization look ahead to future events, threats and opportunities? | 預期 |
| learn | What are the learning bases and targets, and how are the effects verified? | 學習 |

The mapping in the third column is an inference from the words. The owner's Word file uses `預見` where the system uses 預期 (`CLAUDE.md`).

Hollnagel's RAG has one set of questions per potential and must be tailored to each organization. The ED-RAG translated it into Chinese and adapted it to emergency departments. Its authors work at Taipei Medical University and Jönköping University. It replaced the five named RAG classes with a four-point scale (1 to 4) without names. The reason: the evidence at an early stage was too thin for five classes.

### A caution from the domain

The ED-RAG paper says the RAG was never meant as a rating tool. A single score does not show where the problems are or what to do. The RAG gives a profile to compare over time. Keep this in mind when a feature ranks potentials or compares sessions.

## How the system treats each value

| Value in the cell | Row group | In statistics? |
|---|---|---|
| 反應, 監測, 預期 | `analysisRows` | yes: overall, per potential, 4S, ability cells |
| contains 覆蓋率 (for example 演習覆蓋率) | `coverageRows` | yes, as drill coverage. Not in the three potentials and not in 4S. |
| 學習 | `learningRows` | no. A code comment says this follows the exclusion rule of the owner's reference demo. |

Notes:

- `normPotential_` folds two variants before the split. It strips a trailing 潛能 (since 2026-10-16) and maps the old value `回應` to 反應. See [Vocabulary renames](../data/vocabulary-renames.md).
- 學習 questions do not appear in any chart. They still count in the 評核總數 card in the dashboard header. They appear in the hidden ranking panel and in the optional report section R7.
- Any other value falls into no group, with no warning. Before 2026-10-16, the value 反應潛能 did this, and every radar was empty.
- The potential column has exactly one accepted header: `評核潛能`.

## Potential × 4S: the ability matrix

The owner combined the potentials with the 4S elements in a Word file named 「韌性潛能與 4S 擴容元素整合矩陣表」. The three potentials × four 4S elements give 12 ability cells.

- `ABILITY_NOTES` in `Analysis.html` holds one fixed sentence per cell. The text is the body of each cell of the owner's Word file (second version, 2026-10-13).
- `Report.gs` holds a second copy, `ABILITY_NOTES_`. Change both copies in one commit. Nothing at runtime detects a mismatch. A change to the `Report.gs` copy also needs a new `REPORT_BUILD_` and a paste.
- The keys use the canonical 4S names, for example `反應×Space (空間)`. A rename of a canonical name in `S4_VALUE_ALIASES_` blanks every note silently.
- The data for the cells is `stats.potentialByS4`. The iso-3D chart, the ability ranking card and the report's top-three tables all read it, so they cannot disagree.

## See Also

- [4S elements](4s-elements.md)
- [Score scale](score-scale.md)
- [Observed rate and the inclusion gate](observed-rate-inclusion-gate.md)
- [Config spreadsheet](../data/config-spreadsheet.md)
