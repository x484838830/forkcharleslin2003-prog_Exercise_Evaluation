# Tenant registry (租戶註冊表)

> Sources: CLAUDE.md registry and routing sections; owner guide
> Repo: [CLAUDE.md](../../../CLAUDE.md); [docs/owner-guide-多醫院多演習.md](../../../docs/owner-guide-多醫院多演習.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [apps-script/Setup.gs](../../../apps-script/Setup.gs)
> Synced: 18c41f4
> Anchors: 租戶註冊表 (`REGISTRY_SPREADSHEET_ID`; readRegistry_; assertRegistrySane_; REGISTRY_SCENEPREFIX_ALIASES_; 2. 欄位一覽; 9. 為什麼某一列會被判「無效」
> Updated: 2026-10-20

## Overview

The tenant registry is one spreadsheet with the tab `租戶註冊表`. Each row is one session of one tenant. The row names the config file, the record file and tab, the analysis key, and the submission window of that session. The backend reads it with `readRegistry_()` and caches it for 120 seconds under `reg:v2`. A sanity check marks bad rows invalid, and an invalid row is invisible to routing. The owner adds tenants, adds sessions, ends sessions and rotates keys by editing this sheet, with no redeploy. Production has used a registry since `f813130` (2026-10-14).

## Columns

The backend matches the columns by alias (`REGISTRY_*_ALIASES_`), never by position.

| Column | Meaning |
|---|---|
| `醫院代號` | the tenant code in `?t=`. It must pass `normSlug_`. |
| `演習代號` | the session code in `?ex=` |
| `顯示名稱` | the session label in pickers |
| `設定試算表ID` | the config spreadsheet of the session |
| `紀錄試算表ID` | the record spreadsheet |
| `紀錄分頁名稱` | the record tab. Blank means the default `評核紀錄`. |
| `分析金鑰` | the analysis key of the session |
| `啟用` | `N` disables the session for the form and for submissions. The analysis stays readable. |
| `開放送出起` / `開放送出迄` | the submission window. Only `doPost` enforces it. Blank means open forever. |
| `預設演習` | marks the session that a link with `?t=` only resolves to |
| `scenePrefix` | the prefix of scene names. Default `SCENE`. |
| `檔案擁有者` | documentation only. No code reads it, and no endpoint returns it. |

The setup wizard generates `醫院代號` as `<醫事機構代碼>-<6 hex>`. The bare institution code is public government data, so it must not be the whole code.

## Sanity rules

`assertRegistrySane_(rows)` marks rows invalid and never throws.

| # | Rule | Scope |
|---|---|---|
| 1 | Duplicate `醫院代號` + `演習代號`: every row of the group is invalid. | all rows |
| 2 | Duplicate `紀錄試算表ID` + `紀錄分頁名稱` (blank name = default): every row of the group is invalid. This blocks defect D1. | all rows |
| 3 | One `分析金鑰` under two different `醫院代號`: every sharing row is invalid. The same key for two sessions of one tenant is permitted. | all rows |
| 4 | A required cell is blank. | that row |
| 5 | A code, a spreadsheet ID or a date-time does not parse. | that row |

Rules 1 and 2 checked only `啟用=Y` rows until 2026-10-08. That was wrong, because an archived row is still routable for the analysis. The audit case: the owner copies last year's row, forgets to change `紀錄分頁名稱`, and the new drill overwrites last year's scores.

A request that matches an invalid row gets `ROW_INVALID` with a generic message. Only `action=selftest` returns the reasons.

## Hazards

- **Header edits.** If a header cell is broken, `findHeaderCol_` finds no column, and the registry has no usable rows. A request with `?t=` then gets `REGISTRY_BROKEN` (see [Tenant routing](../backend/tenant-routing.md)).
- **The cache.** An edit takes up to 120 seconds to show. `action=flush` clears it, but it needs `ADMIN_KEY`, and production ships `ADMIN_KEY` empty.
- **No 場景前綴 alias.** `REGISTRY_SCENEPREFIX_ALIASES_` is `['scenePrefix', '情境前綴']` (also copied in `Setup.gs`). If the owner retitles the header to 場景前綴, the prefix falls back to `SCENE` silently, and every scene-code match for that tenant can be wrong. `CLAUDE.md` calls this the worst kind of miss.
- **Archived keys.** An archived row's key is still a live credential. Rule 3 checks all rows for this reason.

## See Also

- [Tenant routing](../backend/tenant-routing.md)
- [Setup wizard](../operations/setup-wizard.md)
- [Config spreadsheet](config-spreadsheet.md)
