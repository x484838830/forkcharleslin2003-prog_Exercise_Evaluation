# Setup wizard (Setup.gs, 新增一場演習)

> Sources: CLAUDE.md File roles (Setup.gs, QrLib.html); apps-script/README.md
> Repo: [CLAUDE.md](../../../CLAUDE.md); [apps-script/Setup.gs](../../../apps-script/Setup.gs); [apps-script/SetupDialog.html](../../../apps-script/SetupDialog.html); [apps-script/QrLib.html](../../../apps-script/QrLib.html); [apps-script/README.md](../../../apps-script/README.md)
> Synced: b1a765f
> Anchors: File roles; Setup.gs; SetupDialog.html; QrLib.html; 正式環境還需要指令碼屬性
> Updated: 2026-10-20

## Overview

The setup wizard opens a new session in one dialog. Without it, the owner must do five error-prone steps by hand. The steps are: copy the config spreadsheet, add a record tab, invent a key, fill the registry columns, and assemble two URLs. A mistake shows as a cryptic `ROW_INVALID` on the morning of the drill. The wizard is container-bound to the tenant registry spreadsheet and needs no deployment. It ends with the evaluator URL and a QR code. It calls no Web App.

## What it does

1. It checks the five registry sanity rules **before it writes anything**.
2. It copies the config spreadsheet.
3. It creates the record tab.
4. It appends the registry row.

The registry row comes last on purpose. A failure never leaves a row that points at a file that does not exist.

Other rules:

- 開放送出起 and 開放送出迄 are mandatory in the wizard, although the registry treats them as optional. A blank window means "open forever", and every past session would stay open for submissions.
- It generates `醫院代號` as `<醫事機構代碼>-<6 hex>`. The bare institution code is public data and must not be the whole code.
- It mints a new key per row (`randomKey_`).
- A new record tab copies the header of the first non-empty tab.

## Hidden coupling

`Setup.gs` copies `normSlug_`, `isSpreadsheetId_`, `findHeaderCol_`, `formatDateTime_` and the five sanity rules from `ConfigWithSubmit.gs`. When the backend copy changes, this file must change too. A differential harness once showed identical outputs. `REGISTRY_SCENEPREFIX_ALIASES_` is also copied here, with the same missing 場景前綴 alias.

## QR codes

`QrLib.html` is vendored verbatim from `kazuhikoarase/qrcode-generator` (MIT). Do not edit it. It generates the QR code in the browser. An online QR service would send every tenant code to a third party, which the `?t=` code must avoid. The output is an SVG path, so it prints even when Chrome's background-graphics option is off. The file lives in `apps-script/`, so the public site does not ship it.

## Script properties

| Property | Required | Purpose |
|---|---|---|
| `SETUP_SITE_BASE` | yes | the site base for the generated URLs. The example points at the test site. |
| `SETUP_CONFIG_TEMPLATE` | no | the config spreadsheet to copy |
| `SETUP_TARGET_FOLDER` | no | where the copy goes. Default: next to the template. |

## Known gaps

- The wizard folds 地點 into 說明. Since 2026-10-17 both backends read an optional `演習地點` row, but the wizard does not write it. So a wizard-made session prints 「—」 for `{{演習地點}}` until someone adds the row. A comment in `Setup.gs` and a hint in `SetupDialog.html` still say the backend has no such field.
- A session made by the wizard cannot get a Doc report from the container-bound menu. Script properties pin that menu to one session. The dashboard path has no such limit.
- Untested: the copy-template path, the automatic clear of the old default session, and a new tenant's first session.

## See Also

- [Tenant registry](../data/tenant-registry.md)
- [Doc report generator](../report/doc-report.md)
- [Open issues](open-issues.md)
