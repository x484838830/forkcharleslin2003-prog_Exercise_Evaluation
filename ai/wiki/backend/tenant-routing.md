# Tenant routing and the fallback rule

> Sources: CLAUDE.md tenant routing section
> Repo: [CLAUDE.md](../../../CLAUDE.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [Start.dc.html](../../../Start.dc.html)
> Synced: b1a765f
> Anchors: Tenant routing (方案 A; resolveTenant_; fallbackTenant_; normSlug_; isSpreadsheetId_; tenantSheetConfig_; tenantSheetRecord_; NO_RETRY_ERROR_CODES
> Updated: 2026-10-20

## Overview

`resolveTenant_(e, body)` decides which config file, record file and key a request uses. `CLAUDE.md` calls it the single most load-bearing behaviour of the backend. The rule has two goals that pull against each other. Old links without codes must keep working, so they fall back to a hardcoded tenant. A link with a tenant code must never write into another tenant's files, so a miss is a hard error.

## Resolution order

0. Read the codes. `hid` comes from `body.tenant`, else `?t=`. `exid` comes from `body.exercise`, else `?ex=`. The POST body wins over the query. A code that fails `normSlug_` is a hard `BAD_CODE` error. It is never blanked silently.
1. **No registry** (`REGISTRY_SPREADSHEET_ID === ''`): use `fallbackTenant_()`, even when codes were supplied. The codes are echoed back but do not route.
2. **Registry configured but unusable:**
   - `readable === false` (the open failed, for example a Drive hiccup): fall back, with `registryWarning`. A transient fault must not take a live drill down.
   - readable but no usable rows, and the caller supplied `?t=`: hard error `REGISTRY_BROKEN`.
   - readable but no usable rows, and no `?t=`: fall back.
3. **Registry usable, `hid === ''`:** fall back. This keeps old links alive.
4. **Registry usable, `hid !== ''`:** route by the codes. A miss is a hard error, never a fallback and never another row: `NO_TENANT`, `NO_DEFAULT`, `AMBIGUOUS_DEFAULT`, `NO_EXERCISE`, `ROW_INVALID`.

## Why `REGISTRY_BROKEN` exists

On 2026-10-09 a tester pasted over the registry's `分析金鑰` header cell and cleared it. The registry then had zero usable rows. Every `?t=` request fell through to the fallback tenant. For two minutes a link for one test tenant served another tenant's questions and would have written scores into that tenant's record sheet. Nothing looked wrong on screen. Since then, a readable but empty registry is a visible outage for coded links. The repo records no test against a really broken registry (see [Open issues](../operations/open-issues.md)).

`REGISTRY_BROKEN` is in `NO_RETRY_ERROR_CODES` of `Start.dc.html`. A retry cannot help: a person must fix the sheet, and the cache adds 120 seconds.

## The fallback tenant

`fallbackTenant_()` uses four constants: `CONFIG_SPREADSHEET_ID`, `RECORD_SPREADSHEET_ID`, `RECORD_SHEET_NAME`, `ANALYSIS_KEY`. They are the permanent legacy tenant. Do not delete them. The plan document proposed to delete them, and `CLAUDE.md` overrides that. The fallback tenant is enabled and has no submission window.

## The tenant object

`resolveTenant_` returns an object of 20 keys. Six of them were missing from older documentation and are load-bearing:

- `isDefault` decides the default session.
- `openFromText` and `openToText` are the window text that `windowText_` prints and `action=sessions` returns.
- `reasons` is what `action=selftest` reports per invalid row.
- `requestedHid` and `requestedExid` echo the caller's own codes back in fallback mode, where `hid` and `exid` are empty.

## Gates after resolution

| Gate | Config branch | `doPost` | `action=analysis` |
|---|---|---|---|
| `啟用=N` | `DISABLED` | `DISABLED` | allowed (the report is needed after the drill) |
| outside the submission window | served, with `submitOpen:false` and a reason | `OUT_OF_WINDOW` | allowed |

## Boundaries that must hold

1. A slug is never passed to `openById`. Spreadsheet IDs only come out of a registry row. This stops the Web App from becoming a Drive read proxy.
2. `tenantSheetConfig_(t)` and `tenantSheetRecord_(t)` are the only places that open a tenant's files.
3. Every error is HTTP 200 with JSON: `error` is a Traditional Chinese sentence that the UI prints, `errorCode` is the machine code. One exception: a bad analysis key returns exactly `{error:'unauthorized', errorCode:'UNAUTHORIZED'}`, because `Analysis.html` prints that string.

## See Also

- [Tenant registry](../data/tenant-registry.md)
- [Backend endpoints](endpoints.md)
- [Public exposure and keys](../operations/public-exposure.md)
