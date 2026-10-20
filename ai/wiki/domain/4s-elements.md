# 4S elements (Space, Staff, Stuff, System)

> Sources: 4-S surge capacity framework (Barbisch and Koenig 2006, as described in Health Security 2023); CLAUDE.md; README.md; backend constants
> Repo: [CLAUDE.md](../../../CLAUDE.md); [README.md](../../../README.md); [apps-script/ConfigWithSubmit.gs](../../../apps-script/ConfigWithSubmit.gs); [Analysis.html](../../../Analysis.html); [apps-script/Report.gs](../../../apps-script/Report.gs)
> Synced: 18c41f4
> Anchors: A 4S cell can name several elements; S4_VALUE_ALIASES_; S4_BLANK_VALUES_; splitS4_; s4CanonicalOf_; s4ListOf; S4_PREFERRED_ORDER
> Raw: [4-S surge capacity framework notes](../../raw/domain/2023-09-26-4s-surge-capacity-framework.md)
> Updated: 2026-10-20

## Overview

The 4S elements come from the 4-S framework of hospital surge capacity: staff, stuff, space (originally structures) and systems. Each question in 對應指標 names one or more 4S elements. Since 2026-10-16 the backend splits a cell such as `Staff / System` into canonical names, and the question counts in full under each element. Only the backend splits. The clients read the result `s4List`.

## The domain: surge capacity

Surge capacity is a concept of disaster medicine. The 4-S framework (Barbisch and Koenig, 2006) divides the essential elements of surge capacity in healthcare into four domains:

| Domain | Meaning in the framework | Canonical name in this system |
|---|---|---|
| staff | appropriately trained personnel | `Staff (人員)` |
| stuff | durable and perishable supplies and equipment | `Stuff (物資)` |
| structures, in a common modified version space | physical facilities where healthcare happens | `Space (空間)` |
| systems | management policies and procedures that integrate operations | `System (系統)` |

This explains an alias: the backend maps the words `structure` and 結構 to Space. A code comment says 結構 comes from the owner's matrix (空間/結構) and structure from the original 4S text.

## How the backend reads a 4S cell

`splitS4_(v)` and `s4CanonicalOf_` in `ConfigWithSubmit.gs` do the work. `S4_VALUE_ALIASES_` and `S4_BLANK_VALUES_` drive them.

1. A cell can name one or more elements. Separators: `/`, `、`, `,`, `;`, `+`, `&` and a line break.
2. Each piece must **equal** a recognition word, case-insensitive. Text in brackets after the word is permitted, for example `Staff (人員)`. A piece that only **contains** a word does not match. The first version used substring matching and counted `Workspace` as Space. That was rejected.
3. An unrecognized piece becomes its own category, with its text unchanged. It shows as an extra bar in the 4S chart. This is deliberate: a visible odd bar is better than a silent wrong count.
4. A cell that contains only a blank word (`N/A`, `-`, `無` and others) joins no element.
5. A question with several elements counts in full under each one, not 1/k. So the sum of n over the 4S elements can exceed the score count of the three potentials.

The result rides on each analysis row as `s4List`. `r.s4` keeps the raw cell text, which the tables and the CSV show. `stats.s4` and `stats.potentialByS4` group by membership in `s4List`.

## Rules for code changes

- **Clients never split.** `s4ListOf(r)` in `Analysis.html` and `s4ListOf_(r)` in `Report.gs` return `r.s4List`, or `[r.s4]` for an old backend.
- **A new canonical name, or a fifth element,** needs one commit that changes `S4_VALUE_ALIASES_`, `S4_PREFERRED_ORDER` and `ABILITY_NOTES` in `Analysis.html`, and `S4_PREFERRED_ORDER_` and `ABILITY_NOTES_` in `Report.gs`. Nothing at runtime notices a mismatch.
- **Deploy order:** clients first, backend last. A new backend with an old client drops rows from the per-scene 4S segments.
- **Do not rename the header** `單一 4S 元素`. A renamed header resolves only if it starts with an alias. If it fails, `action=analysis` fails, and `doPost` can fail too.
- 報告快照 freezes the raw 4S text, not the split result.
- `S4_COLORS` in `Analysis.html` is defined but never read.

## Which questions enter the 4S statistics

Only the three potentials (反應, 監測, 預期). Drill coverage questions and 學習 questions stay out of the 4S averages. Since 2026-10-17 a question must also pass the inclusion gate (see [Observed rate and the inclusion gate](observed-rate-inclusion-gate.md)).

## See Also

- [Resilience potentials](resilience-potentials.md)
- [Analysis payload](../backend/analysis-payload.md)
- [Dashboard](../frontend/dashboard.md)
