# Dashboard (Analysis.html)

> Sources: CLAUDE.md "Analysis.html UI structure"; Analysis.html code
> Repo: [CLAUDE.md](../../../CLAUDE.md); [Analysis.html](../../../Analysis.html); [assets/imdl-logo.png](../../../assets/imdl-logo.png)
> Synced: b1a765f
> Anchors: Analysis.html UI structure; Tabs (five buttons); Panels with no tab button; 場次下拉 (`#exPicker`); 場景說明浮層 (`SCENE_GOALS`); orgTitle; displayName; loadExercises; syncPickerSelection; renderRadars; renderCoverage; renderS4; renderRanking; renderDetail; renderMethod; renderAbilityRank; renderNotRated; renderIso3D; buildAnonMap; anonLabel; svgRadar; barsSVG; stackedHBarsSVG; radarTable; shortScene; normalisePotentials; ANALYSIS_KEY; RECORD_URL; REPORT_URL
> Raw: [Upstream branch state, 2026-10-22](../../raw/repo-observations/2026-10-22-upstream-branch-state.md)
> Updated: 2026-10-22

## Overview

`Analysis.html` is one standalone page with no framework. On load it fetches `RECORD_URL?action=analysis&key=…` and keeps the payload in one global `DATA`. `init()` calls one `render*()` function per panel. Nothing re-renders by itself: after `DATA` changes, call the render functions again. The page is not linked from the evaluator form. Its access control is an unshared URL plus the key. The maintainer's fork exists to add features to this page.

## Warning for local work

The constants `RECORD_URL`, `ANALYSIS_KEY` and `REPORT_URL` in the file point at production. A local copy of the page therefore reads real drill data. The button 產生 Google 文件 writes a real Doc into the owner's Drive. Do not test write paths against production. Do not write the constant values into the wiki (SCHEMA.md §7).

## URL parameters

| Parameter | Effect |
|---|---|
| `?t=` / `?ex=` | forwarded to `action=analysis` |
| `?key=` | overrides the built-in `ANALYSIS_KEY` |
| `?view=report` | opens the report view on load |

With no parameters, the request is byte-identical to the request before multi-tenancy. A local test needs a real `?t=` code, or the session picker stays hidden.

## Header

- The title is `orgTitle() + '｜演習評核分析平台'`. `orgTitle()` is `meta.orgName || meta.displayName || '演習評核'`, so the title names the hospital.
- Two name helpers exist on purpose. Do not merge them.

| Helper | Expression | Answers | Feeds |
|---|---|---|---|
| `orgTitle()` | `meta.orgName \|\| meta.displayName \|\| '演習評核'` | which hospital (the 演習資訊 row 機構名稱) | `#orgTitle`, `document.title`, the report cover's `.coverOrg` |
| `displayName()` | `meta.displayName \|\| meta.orgName \|\| '演習評核'` | which session (the registry column 顯示名稱) | the CSV filename, `docRun.sessionLabel` in the 產生 Google 文件 dialog |

- Each helper falls back to the other when its own field is blank. A config sheet with no 機構名稱 row therefore shows the same title as before the split.
- The reason for the split: the owner's 顯示名稱 carries version suffixes such as `_R7` and `_V2`. Those suffixes help in a session picker. They are wrong in a page heading.
- Chrome's "Save as PDF" takes the file name from `document.title`. So two sessions of the same hospital now propose the same PDF file name. The cover still names the session. The CSV filename still uses `displayName()`, so the CSV names the session.

> **Status: Outdated** (2026-10-22)
> Before commit `b2c0914`, the title was `meta.displayName || meta.orgName || '演習評核'`, and the CSV filename used the same expression. Since `b2c0914`, the title uses `orgTitle()` and only the CSV filename keeps the old expression. Source: `Analysis.html` `orgTitle`, and `CLAUDE.md` "Analysis.html UI structure".
- The logo is `assets/imdl-logo.png`. Replace the file and keep the path to change it.
- Four KPI pills sit in the header (`#kpis`): 主題/說明, 評核官人數, 評核總數. 評核總數 counts all three row arrays, 學習 included.
- The session picker `#exPicker` (see below).

## Tabs (five buttons)

| Tab | Panel | Content |
|---|---|---|
| 綜合評比 | `#overview` | first card: iso-3D chart of potential × 4S (`svgIso3D`), the drill coverage gauge, the 4S bar chart (`barsSVG`, sorted by mean). Second row: `#abilityRankCard` (all ability cells ranked, ties share a rank) and `#notRatedCard` (questions excluded by the gate). |
| 4S 分析 | `#s4` | stacked horizontal bars per 4S element (`stackedHBarsSVG`). Bar length = the element's real mean. Segments = scenes, colored along an HSL spectrum. Next to it: the scene code table `#s4ScenarioTable`. |
| 三項潛能雷達圖 | `#radars` | one radar per potential (`svgRadar`, axes sorted low → high), each followed by a separate card with `radarTable()` |
| 演習覆蓋率 | `#coverage` | the drill coverage radar and its table |
| 統計方法 | `#method` | method text. Parts follow `meta.scale`. It also holds the inclusion-gate cards. |

Details that matter for changes:

- `svgRadar` wraps an axis label longer than 7 full-width characters (`RADAR_LABEL_UNITS`) and grows the `viewBox`.
- A row with `mean === null` stays off the radar. `unratedRadarNote()` says so, and the table lists the row last with `—`.
- `#notRatedCard` shows one row per question. One-level drills and two-level drills use different columns (`isSingleLevel()`). Rows sort by `meta.stageOrder`, then by a natural `'en'` sort.
- The 綜合評比 panel is reused as section R3 of the report view, so it prints.

## Panels with no tab button

`#ranking` (排序視圖) and `#detail` (評核官明細) render on load but have no tab button. Commit `54b33dd` removed the buttons on purpose. `#detail` shows scores per evaluator and has a CSV export. In a small quality department an evaluator code is at best a pseudonym. **Do not add tab buttons for these panels.** Re-exposing them needs its own decision with a consent mechanism. `#detail` is also hidden by force in the report view and in print.

## Session picker (`#exPicker`)

- `loadExercises()` fills the picker from `action=exercises` the first time `meta.tenant` is non-empty. Each option reads `顯示名稱｜日期`. Archived sessions stay selectable.
- A switch must not change the URL. `currentExid` holds the session. The old link list wrote the key into the address bar, which the report view must avoid.
- `load()` disables the picker during a fetch. This prevents a late response from showing a session that differs from the picker.
- Every failure hides the picker silently. The current drill must stay usable.
- The old button 當次演習 was removed. Do not add it back.

## Scene popover

`buildSceneGoals()` maps each scene code to its 場景說明. `sceneCell()` makes the code a button only when a real description exists. A popover that only repeats the code is useless.

## Anonymous mode

`#anonMode` is on by default. `buildAnonMap()` maps each evaluator code to 評核官 N by its index in the sorted `meta.evaluatorCodes`, and `anonLabel()` prints the label. `CLAUDE.md` names this function `anonCode()`, but no function of that name exists in the code at `18c41f4`. The code wins. The Doc report uses the same rule, so screen and paper name the same person. Turning it off needs a `window.confirm()`.

## Rules for changes

1. Follow the client contract of the payload (see [Analysis payload](../backend/analysis-payload.md)).
2. Use `shortScene()` for scene codes. It is the one function the three code-using places share.
3. `ABILITY_NOTES` has a second copy in `Report.gs`.
4. The page must still render with an old backend. Test with fields missing.
5. Hand-written method text does not update itself. Change it when a statistic changes.

## See Also

- [Dashboard report view and the Doc button](dashboard-report-view.md)
- [Analysis payload](../backend/analysis-payload.md)
- [Observed rate and the inclusion gate](../domain/observed-rate-inclusion-gate.md)
- [Resilience potentials](../domain/resilience-potentials.md)
