# Phase 4 Initial Financial Investigation

## Scope

This initial investigation examined the first fourteen Tier 1 entities in the Phase 3 priority queue. The review compared the extracted JSON calculations with actual retained statement-page images or text and inspected whether the retained source population was complete for the failed check. It did not verify every figure or schedule for these entities.

## Result

Seventeen discrepancies were independently confirmed as inconsistencies printed in the source reports. One retained-source completeness defect and four validator false positives were also confirmed. No financial value was corrected, and the correction log remains empty.

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

Hickman is a different problem: the retained PDF does not include the governmental statements needed to establish beginning fund balance, so the check is `INCOMPLETE_SOURCE`, not a confirmed financial discrepancy.

The Municipal Energy Agency flag is a validator false positive. “Transfer from (provision for) rate stabilization” is printed as a regulatory adjustment within operating revenues, rather than an interfund transfer. The original label and negative operating-revenue treatment should remain, with a narrow exception to the generic transfer-word rule.

The October 22 Sargent Public Schools re-trim produced three more validator false positives. On retained PDF pages 22–23 (printed statement pages 49–50), “Athletic Transfer” and “Transfer” are Activities Fund account names. The flagged amounts are printed in the Receipts or Disbursements columns, while each row's Transfers in (out) value is zero. The $3,000 and $7,175 receipts and $7,281 disbursement should remain in their printed columns. The generic transfer-word rule needs statement-column context rather than reclassification of these amounts.

## Audit treatment

- Preserve the original lines and printed totals as separate source observations.
- Record the affected reconciliation dimension as `FAILED_VALIDATION` with evidence that the source report is internally inconsistent.
- Do not replace a printed amount with a calculated amount.
- Exclude affected reconciled measures from verified publication, or publish them only with a clear source-report-discrepancy label and separate printed-versus-calculated fields.
- Small differences remain documented discrepancies; they are not automatically dismissed as rounding.

## Pipeline assessment

The existing JSON already records the source-report discrepancies in `report_discrepancies`. For these checks, the extraction system accurately retained conflicting source representations and did not force them to balance. The Phase 3 queue should distinguish confirmed source-report discrepancies, incomplete source, and validator defects while keeping unresolved financial measures out of verified publication.

## Next investigation targets

The next group prioritizes remaining active validator flags and material transfer/classification cases, beginning with Boelus, Hall County, Leigh, Lower Loup NRD, Ord, Plattsmouth Airport Authority, and Twin Platte NRD. Sargent's three reviewed false positives have been removed from the active validation queue.
