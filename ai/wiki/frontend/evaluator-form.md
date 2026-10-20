# Evaluator form (Start.dc.html)

> Sources: CLAUDE.md sections on the mockup, screens and URL parameters; README.md
> Repo: [CLAUDE.md](../../../CLAUDE.md); [Start.dc.html](../../../Start.dc.html); [support.js](../../../support.js); [README.md](../../../README.md)
> Synced: 18c41f4
> Anchors: Editing the mockup; Screens; The picker is an accordion, not a grid; `showCriteria` is per-question, not a screen; Per-question 觀察紀錄 (free text); Identity header and submit gating; URL params and storage key; scenePrefix; renderVals; flattenRows; configRequestUrl; doneStorageKey; adoptDoneItems; scoreScale; submitScores
> Updated: 2026-10-20

## Overview

`Start.dc.html` is the phone page where evaluators score a drill. It is a Design Component (DC) exported from a visual design tool. A template block holds the markup. A script block holds one `Component` class with `constructor` and `renderVals()`. `support.js` is a generated runtime that compiles the template and renders it with the vendored React 18. All content comes from the backend at runtime. The page never reads or sends any key.

## How the file is built

- The `<x-dc>` template uses `{{ expr }}`, `<sc-if value="{{…}}">` and `<sc-for list="{{…}}" as="x">`. These two elements are the only control flow.
- A template expression can only use keys that `renderVals()` returns. There is no ref, effect or measurement mechanism. Do not add one.
- `support.js` is generated from a separate project. The repo has no source for it. Do not edit it by hand. Do not edit `vendor/`.
- Inline `style="…"` values carry the design tokens, for example `#161512`, `#7a4e0f`, `#f7f5ee`, error `#b00020`. Keep exact values.
- No build step exists. To view it, serve the folder (`python3 -m http.server`) and open the page. Some browsers block the scripts over `file://`.

## Screens

`this.state.screen` is `'sessions' | 'select' | 'survey' | 'done' | 'exit'`. There is no criteria screen.

| Screen | When |
|---|---|
| `sessions` | the first screen only in picker mode (`?t=` present, `?ex=` absent). It lists sessions from `action=sessions`. Past sessions are folded and cannot be picked. |
| `select` | the identity header, the evaluator-code dropdown, and the scene accordion |
| `survey` | the question cards of one scene |
| `done` | after a submit. If every leaf is done, it shows the END screen. |
| `exit` | after 離開頁面. `window.close()` works only on script-opened tabs, so the page always switches to this screen too. |

If `action=sessions` answers `REGISTRY_OFF`, or answers with no `sessions` array (an old backend), `fallBackToSingleSession()` goes to `select` with no error.

## The scene picker

The picker is an accordion. `flattenRows(...)` turns the item tree into visible rows. Only one group is open at a time (`openGroupKey`). This design assumes two levels. A third level makes the lowest items unreachable. A click on a leaf opens its survey and clears the answers and comments.

The done flags use the leaf name as the key. Two leaves with the same name share one flag (defect D4, still open).

## Question cards

- Each card has its own 評分標準 accordion (`criteriaOpenIds`).
- The score buttons come from `scoreScale()` over the 評分標準 rows, not a hardcoded 1–5. `optionsGridStyle` is `repeat(min(n, 6), minmax(0, 1fr))`, so a seventh button wraps on a 390-wide screen.
- The comment box (觀察紀錄) shows unless `commentEnabled === false`. With `commentRequiredBelow > 0`, a score at or below the threshold needs a comment, and the submit button stays disabled. Only the client enforces this.
- The client trims a comment and caps it at 500 characters.
- A scene can be submitted only when every question has a score or a 0.

## Identity header and submit gate

The select screen shows a three-line header: institution, drill, date. An evaluator who got the wrong link can see it. The drill name falls back in this order: `exerciseName`, `exerciseTopic`, `exerciseCategory`, `orgName`.

If the backend says `submitOpen === false`, the submit button is disabled and reads 目前未開放送出.

## URL parameters

| Link shape | Config request |
|---|---|
| no parameters | `CONFIG_URL`, byte-identical to the request before multi-tenancy |
| `?t=` and/or `?ex=` | `RECORD_URL?t=…&ex=…` |
| `?t=` only | first `action=sessions`, then the picked session |

The storage key for done flags:

```
no params   -> 'exerciseEvalDone:' + (exerciseName||exerciseTopic||exerciseCategory||'default') + ':' + code
with params -> 'exerciseEvalDone:' + T_PARAM + '/' + (exid || EX_PARAM) + ':' + code
```

- Every call must pass `exid`. Without it, two sessions of one tenant share done flags.
- The legacy branch must stay. An evaluator on an old link must not lose done flags at a deploy.
- The key has no random part. A test that reuses a session code starts with every scene done.
- `adoptDoneItems` copies an old `?t=`-only key into the picked default session once.

## Scene prefix

The scene regexes use `config.scenePrefix`, default `SCENE`. A tenant can set its own prefix in the registry.

## Submit

`submitScores()` posts the body described in [Backend endpoints](../backend/endpoints.md). It reuses one `submissionId` for 3 retries. `NO_RETRY_ERROR_CODES` lists the routing errors that a retry cannot fix.

## See Also

- [Config spreadsheet](../data/config-spreadsheet.md)
- [Score scale](../domain/score-scale.md)
- [Tenant routing](../backend/tenant-routing.md)
