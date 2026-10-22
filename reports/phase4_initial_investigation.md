# Phase 4 Initial Financial Investigation

## Scope

This investigation covers the initial Tier 1 group plus subsequent source-flag and reconciliation batches. The review compared extracted JSON calculations with retained statement-page images or text and inspected whether the retained source population was complete for each failed check. It did not verify every figure or schedule for these entities.

## Result

Forty discrepancies were independently confirmed as inconsistencies printed in the source reports. Five retained-source completeness defects, six validator false positives, and one classification ambiguity were also confirmed. No financial value was corrected, and the correction log remains empty.

| Entity | Check | Difference | Confirmed source issue |
| --- | --- | ---: | --- |
| Oshkosh | Governmental expenditure lines vs printed total | $6,021.18 | Printed lines total $894,115.97; printed total is $900,137.15. |
| Oshkosh | Proprietary fund columns vs printed total | $2,676.25 | Fund-column operating expenses total $760,543.99; printed total is $757,867.74. |
| Wymore | Grants and donations columns vs printed total | $10,000.00 | Fund columns total $556,064; printed total is $566,064. |
| Wymore | Repairs and maintenance columns vs printed total | $5,000.00 | Fund columns total $222,748; printed total is $227,748. |
| Sutherland | Governmental roll-forward | $2.00 | Printed component and total lines contain small internal differences; ending balance cannot be reproduced from every printed line simultaneously. |
| Sutherland | Business-type roll-forward | $2.00 | Printed component and total lines contain $1 differences that accumulate in the line-based roll-forward. |
| Arlington | Business-type roll-forward | $66.00 | Beginning net position plus printed change equals $2,137,459, not the printed $2,137,525 ending balance. |
| Arlington | Balance-sheet equation | $3.00 | Printed liabilities plus net position exceeds printed assets by $3. |
| Pathfinder Irrigation District | Nonoperating detail vs printed total | $5,000.00 | Displayed nonoperating lines total $50,430; printed total is $55,430. |
| Gering Irrigation District | Cash roll-forward | $199,426.00 | Printed resources omit the beginning balance. |
| Gering Irrigation District | Ending cash composition | $173,642.00 | Printed cash and investments total $239,977; handwritten total is $66,335. |
| Central Irrigation District | Cash roll-forward | $99.98 | Printed activity implies about $9,127.01; handwritten ending is $9,027.03. |
| Laurel Housing Authority | Proprietary cash flow | $2,600.00 | Printed net decrease differs from the four section totals by the nonroutine-maintenance amount. |
| North Platte Airport Authority | Business-type roll-forward | $2.00 | Two $1 line-to-subtotal differences accumulate in the ending balance. |
| Panhandle Area Development District | Operating expense lines vs total | $73.00 | Displayed lines total $312,072; printed total is $312,145. |
| South Central Area Agency on Aging | Business-type roll-forward | $2.00 | Revenues less expenditures produces $114,108; printed change is $114,106. |
| Hall County Housing Authority | Balance-sheet equation | $5,337.00 | Enterprise noncurrent-assets total omits the displayed right-of-use asset. |
| Amherst Public Schools | Governmental disbursement lines vs total | $10,000.00 | Printed disbursement lines total $6,782,394; printed total is $6,772,394. |
| Arcadia | Balance-sheet equation | $270.00 | Governmental assets are $270 below governmental net position with zero liabilities. |
| Byron Community Building District | Total resources | $2,010.00 | Beginning balances plus receipts equal $93,515; handwritten total resources is $95,525. |
| Byron Community Building District | Cash roll-forward | $20.00 | Printed components imply $18,494; handwritten ending balance is $18,514. |
| Cuming County | Governmental disbursement total | $2,667.00 | Culture and Recreation fund columns exceed the printed total by $2,667. |
| Broken Bow Public Schools | Governmental disbursement lines vs total | $67.00 | Printed lines total $33,481,684; printed total is $33,481,751. |
| Elkhorn Public Schools | Governmental receipt lines vs total | $500.00 | Printed lines omit a $500 contribution included in the printed total. |
| Wilcox-Hildreth Public School | Nutrition Fund operating receipts | $12,622.00 | Receipt lines total $121,511; printed total is $134,133. |
| Douglas County SID 633 | Balance-sheet equation | $4,908.00 | Liabilities, deferred inflows, and net position exceed assets by $4,908. |
| Crofton Community Schools | Interfund transfer elimination | $200,000.00 | Governmental funds print $200,000 of net transfers in rather than eliminating internal transfers. |
| Doniphan-Trumbull Public Schools | Governmental disbursement lines vs total | $2.00 | Printed lines total $10,018,234; printed total is $10,018,236. |
| Springfield | Governmental roll-forward | $2.00 | Opposing $1 receipt and disbursement differences produce a $2 line-based ending difference. |
| Yutan | Governmental roll-forward | $3.00 | Printed lines imply $904,770; printed ending balance is $904,773. |
| Fairmont | Balance-sheet equation | $356,893.00 | Combined net position omits the governmental Street restriction. |
| Henderson | Balance-sheet equation | $2.00 | Printed assets and net position differ by $2; their lines meet at the midpoint. |
| Pilger | Balance-sheet equation | $3,460.00 | Business-type restricted cash is understated by $3,460 in the combined statement. |
| Sarpy County SID 373 | Balance-sheet equation | $9,798.00 | The imbalance is twice the $4,899 property-tax/deferred-inflow amount. |
| Sarpy County SID 374 | Balance-sheet equation | $6,684.00 | The imbalance is twice the $3,342 property-tax/deferred-inflow amount. |
| Elwood | Business-type roll-forward | $2.00 | Operating-expense lines are $2 below the printed total. |
| Elwood | Governmental balance statement | $28,000.00 | Governmental assets exceed liabilities and fund balance by $28,000. |
| Hay Springs | Governmental roll-forward | $2.00 | Receipt and disbursement rounding differences produce a $2 ending difference. |
| Hayes Center | Governmental roll-forward | $2.00 | Receipt and disbursement differences produce a $2 ending difference. |
| Lodgepole | Governmental roll-forward | $2.00 | Disbursement and ending-balance differences produce a $2 line-based gap. |

Hickman is a different problem: the retained PDF does not include the governmental statements needed to establish beginning fund balance, so the check is `INCOMPLETE_SOURCE`, not a confirmed financial discrepancy.

The Municipal Energy Agency flag is a validator false positive. “Transfer from (provision for) rate stabilization” is printed as a regulatory adjustment within operating revenues, rather than an interfund transfer. The original label and negative operating-revenue treatment should remain, with a narrow exception to the generic transfer-word rule.

The October 22 Sargent Public Schools re-trim produced three more validator false positives. On retained PDF pages 22–23 (printed statement pages 49–50), “Athletic Transfer” and “Transfer” are Activities Fund account names. The flagged amounts are printed in the Receipts or Disbursements columns, while each row's Transfers in (out) value is zero. The $3,000 and $7,175 receipts and $7,281 disbursement should remain in their printed columns. The generic transfer-word rule needs statement-column context rather than reclassification of these amounts.

Lower Loup NRD's $5,700 “Irrigation Rights Transfer Fees” is printed within its Schedule of Revenues and is fee revenue. Twin Platte NRD's $3,718 “Chemigation fee transfer” is printed within General Fund expenditures and is a fee remittance; its report presents only one fund. Both are confirmed false positives and are removed from active queues.

Plattsmouth Airport Authority remains incomplete because its retained page combines receipts and transfers into a single $1,245,009 inflow and the governmental funds operating statement needed to separate the components is missing. Hall County remains under review because its Insurance Fund labels $5,356,069 “Other Receipts Interfund Transfers,” separately reports $668,362 of “Interfund Transfers,” and presents the first amount as Other receipts in the county-wide statement.

Three remaining source flags are confirmed retained-source defects. Boelus lacks Exhibit A Page 2 with disbursements by function. Leigh lacks the continuation of its General Fund departmental schedule. Ord retains only the right half of its governmental expenditure schedule, leaving the row labels and major fund columns absent. These flags remain active until the source PDFs are re-trimmed and re-extracted.

## Audit treatment

- Preserve the original lines and printed totals as separate source observations.
- Record the affected reconciliation dimension as `FAILED_VALIDATION` with evidence that the source report is internally inconsistent.
- Do not replace a printed amount with a calculated amount.
- Exclude affected reconciled measures from verified publication, or publish them only with a clear source-report-discrepancy label and separate printed-versus-calculated fields.
- Small differences remain documented discrepancies; they are not automatically dismissed as rounding.

## Pipeline assessment

The existing JSON already records the source-report discrepancies in `report_discrepancies`. For these checks, the extraction system accurately retained conflicting source representations and did not force them to balance. The Phase 3 queue should distinguish confirmed source-report discrepancies, incomplete source, and validator defects while keeping unresolved financial measures out of verified publication.

## Next investigation targets

The remaining active source flags have now been classified. The next investigation group prioritizes unreviewed reconciliation failures and material classification risks. Sargent, Lower Loup NRD, Twin Platte NRD, and Municipal Energy Agency false positives have been removed from the active validation queue.
