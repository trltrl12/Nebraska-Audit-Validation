# Phase 4 Initial Financial Investigation

## Scope

This initial investigation examined the four entities with two independent failed checks in the Phase 3 priority queue: Oshkosh, Wymore, Sutherland, and Arlington. The review compared the extracted JSON calculations with the actual retained statement-page images. It did not verify every figure or schedule for these entities.

## Result

Eight discrepancies were independently confirmed as inconsistencies printed in the source reports. The inspected values match the displayed pages; the pipeline did not manufacture these differences. No financial value was corrected, and the correction log remains empty.

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

## Audit treatment

- Preserve the original lines and printed totals as separate source observations.
- Record the affected reconciliation dimension as `FAILED_VALIDATION` with evidence that the source report is internally inconsistent.
- Do not replace a printed amount with a calculated amount.
- Exclude affected reconciled measures from verified publication, or publish them only with a clear source-report-discrepancy label and separate printed-versus-calculated fields.
- Small differences remain documented discrepancies; they are not automatically dismissed as rounding.

## Pipeline assessment

The existing JSON already records each of these discrepancies in `report_discrepancies`. For these eight checks, the extraction system accurately retained the conflicting source representations and did not force them to balance. The Phase 3 queue should therefore distinguish confirmed source-report discrepancies from extraction or classification defects while keeping both as publication blockers.

## Next investigation targets

The next group combines an explicit failure with incomplete reconciliation or unresolved classification: Pathfinder Irrigation District, Gering Irrigation District, Hickman, Municipal Energy Agency of Nebraska, Central Irrigation District, Laurel Housing Authority, North Platte Airport Authority, Panhandle Area Development District, South Central Area Agency on Aging, and Hall County Housing Authority.
