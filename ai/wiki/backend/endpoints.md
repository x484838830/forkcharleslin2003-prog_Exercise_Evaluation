# Backend endpoints and their red lines

> Sources: CLAUDE.md backend sections
> Repo: [CLAUDE.md](../../../CLAUDE.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [apps-script/Config.gs](../../../apps-script/Config.gs); [Start.dc.html](../../../Start.dc.html); [docs/handover-筆電.md](../../../docs/handover-筆電.md); [apps-script/README.md](../../../apps-script/README.md)
> Synced: 18c41f4
> Anchors: Config payload (`doGet` with no `action`); Admin / listing endpoints; The `action=sessions` exposure; Record spreadsheet (per-tenant; File roles; doPost; appendSubmission_; sessionSortable_; submitWindowState_; errorOut_
> Updated: 2026-10-20

## Overview

`ConfigWithSubmit.gs` is one Apps Script Web App behind `RECORD_URL`. Its `doGet` serves the config branch (no `action`) and five actions. Its `doPost` stores scores. Three branches have no authentication, and every evaluator's phone calls them: the config branch, `action=sessions` and `doPost`. Their payloads must never contain secrets. `Config.gs` is a second, read-only Web App behind `CONFIG_URL`. It serves only the config branch, for links with no parameters.

## Endpoint table

| Request | Auth | Returns |
|---|---|---|
| `doGet` with no action (config branch) | none | drill info, `codes`, `criteria`, `items`, plus tenant and window fields |
| `action=sessions` | none. `?t=` is required. | the sessions of that one tenant: label, status, window text |
| `doPost` | none | `{ok:true, rows, duplicate}` or `{ok:false, error, errorCode}` |
| `action=analysis` | `?key=` = the session's `分析金鑰` | the analysis payload (see [Analysis payload](analysis-payload.md)) |
| `action=exercises` | `?t=` + `?key=` | all sessions of the tenant with names and dates, archived ones included |
| `action=selftest` | `?adminKey=` = `ADMIN_KEY` | registry health, invalid-row reasons, record-sheet header check |
| `action=flush` | same as selftest | clears the registry cache key `reg:v2` only |

Production ships `ADMIN_KEY` as an empty string. So `selftest` and `flush` return `ADMIN_DISABLED`. `ADMIN_KEY` must not equal `ANALYSIS_KEY` and must not appear in either HTML file.

## Config branch

The original keys stay unchanged: `orgName`, `exerciseName`, `exerciseTopic`, `exerciseCategory`, `exerciseDate`, `exerciseDesc`, `codes`, `criteria`, `items`. Ten fields were added: `tenant`, `exercise`, `displayName`, `scenePrefix`, `commentEnabled`, `commentRequiredBelow`, `submitOpen`, `submitClosedReason`, `tenantSource`, `exerciseLocation`.

- `tenantSource` is diagnostic only. Clients must not branch on it for data.
- The branch is wrapped in try/catch and returns `CONFIG_READ_FAILED`. The evaluator form throws on `data.error` before it renders.

## doPost

Request body: `{ submissionId, fillerCode, itemName, answers: [{ id, score, comment }], tenant, exercise }`, sent as `text/plain;charset=utf-8`. The plain-text type avoids a CORS preflight that Apps Script cannot answer. Keep `submitScores()` in `Start.dc.html` and `appendSubmission_` in sync.

Deduplication: the cache key is `'sub_' + t.hid + '/' + t.exid + '_' + id` in registry mode and exactly `'sub_' + id` in fallback mode. The fallback form stayed byte-identical so that a retry across a deploy still deduplicates.

## action=sessions

`action=sessions` is a separate function from `action=exercises` on purpose:

1. The fallback branch of `exercises` ignores `?t=`. Without a key, it would expose the legacy tenant's names to anyone.
2. One function has one red line. A key check inside a shared function is hard to audit.
3. `exercises` opens one spreadsheet per row. `sessions` opens zero spreadsheets and reads only the cached registry. This is also why its label is `顯示名稱`, not `演習名稱`.

`sessions` gives a holder of a `?t=` code three new facts about the tenant's other sessions:

1. their codes and count
2. their display names
3. their status and window text
 It makes `演習代號` enumerable within one tenant. The owner side accepted this, because a session picker cannot exist without it. It is live in production since 2026-10-14.

Boundaries:

- No endpoint lists `醫院代號` values. There is no wildcard, so there is no path across tenants.
- `sessionSortable_` is the only place that builds a returned object. Sort-only fields sit outside its output, so they cannot leak into the JSON.

## Red line for the three unauthenticated branches

A payload of the config branch, `action=sessions` or `doPost` must never contain:

- `分析金鑰` or `ANALYSIS_KEY`, `ADMIN_KEY`
- any spreadsheet ID, the record sheet name, any sheet name
- registry row numbers, `registryWarning`, sanity-rule reason strings
- `檔案擁有者`, any file name
- for `sessions` also: another tenant's row, evaluator codes, question IDs, scores, comments, cell contents

Check this mechanically when you change any of these branches or add a fourth one. `doPost` once leaked the record sheet name through an error message (observed on 2026-10-08). The fix made that message generic.

## Config.gs

`Config.gs` has no registry code and no `nullSafeSheet_` or `safeHeaderCol_` guards. Seven functions were once byte-identical in both files. They are not any more. Some must stay equal: for example both copies of `readExerciseInfo_` return the same object, and the header alias arrays for 項目與問題 exist in both. A change to `Config.gs` needs its own paste and redeploy. `docs/handover-筆電.md` §3 says the live `Config.gs` was a hand-edited mix that matches no commit (state of 2026-10-12).

## See Also

- [Tenant routing](tenant-routing.md)
- [Analysis payload](analysis-payload.md)
- [Public exposure and keys](../operations/public-exposure.md)
- [Evaluator form](../frontend/evaluator-form.md)
