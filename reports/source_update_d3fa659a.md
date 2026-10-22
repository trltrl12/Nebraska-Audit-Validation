# Source Update Impact — `d3fa659a`

## Scope

This review compares Nebraska-Audit source commit `e3487afa0a6953a428bea997359aa257fd97882c` with `d3fa659a9a62f6ba11fd35154f168f466e70b683`. The update targeted a re-trim and re-extraction of Sargent Public Schools, then rebuilt the repository-wide CSV and workbook outputs. The validation repository treats the direct Sargent change separately from projection changes exposed by that rebuild.

## Dataset-level changes

| Output | Before | After | Change |
| --- | ---: | ---: | ---: |
| Entity summaries | 2,658 | 2,658 | 0 |
| Long-form rows | 53,220 | 53,238 | +18 |
| Detail rows | 71,964 | 72,674 | +710 |
| Review rows | 52,469 | 52,724 | +255 |
| Source validator flags | 9 | 12 | +3 |
| Progress rows | 2,672 | 2,672 | 0 |
| Manifest rows | 2,669 | 2,669 | 0 |

The refreshed independent quality scan contains 57 failures, 339 incomplete checks, and 204 review findings. The increase consists of three source-flag failures, four transfer-label review findings, and two provenance-aware duplicate candidates. The baseline also now records 368 affirmative proprietary cash-flow reconciliations, up from 366.

## Direct Sargent re-trim effect

Sargent Public Schools gained one retained report page: report page 54, represented as retained PDF page 23. The extraction attempt advanced from 1 to 2, and the entity moved from `done` to `flagged`.

| Sargent output | Before | After | Change |
| --- | ---: | ---: | ---: |
| Detail rows | 76 | 153 | +77 |
| Long-form rows | 24 | 25 | +1 |
| Review rows | 36 | 46 | +10 |
| Validator flags | 0 | 3 | +3 |

The entity's core cash summary did not change:

| Measure | Amount |
| --- | ---: |
| Beginning balance | $2,266,606 |
| Receipts | $4,577,760 |
| Disbursements | $4,385,175 |
| Transfers out | $52,028 |
| Ending balance | $2,407,163 |
| Reconciles | Yes |

The three new flags are validator false positives. “Athletic Transfer” and “Transfer” are Activities Fund account names. The underlying schedule prints $3,000 and $7,175 in the Receipts column and $7,281 in the Disbursements column; the Transfers in (out) column is zero for all three rows. The extraction should retain those printed classifications, and the validator should use statement-column context before treating the word “transfer” as interfund activity.

## Repository-wide rebuild effect

Only the Sargent entity JSON changed in the targeted extraction commit. The later output rebuild also refreshed generated rows for entities whose JSON already differed from the previously committed projections. The largest detail-row changes were Hastings Public Schools (+219), Crete Public Schools (+212), Hemingford Public Schools (+115), Sargent Public Schools (+77), Waterloo (+53), and Platte County (-33). These changes should not be attributed to the Sargent re-trim itself.

The rebuild also populated previously blank proprietary cash-flow fields for Plainview and Waterloo and updated Hemingford's business-type measure and liabilities representation. Those are projection-refresh effects from existing source JSON and need their own evidence review before they are treated as newly verified data.

## Validation treatment

- Use `d3fa659a9a62f6ba11fd35154f168f466e70b683` as the current source baseline.
- Preserve Sargent's printed receipt and disbursement values and record the three flags as validator false positives.
- Do not infer that all 710 added detail rows came from the Sargent re-trim; 633 of the net increase arose elsewhere during output regeneration.
- Review the refreshed Plainview, Waterloo, Hemingford, Hastings, Crete, and Platte County projections against retained evidence before granting verified publication status.
