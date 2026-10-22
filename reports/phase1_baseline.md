# Phase 1 Baseline Audit

Generated from source commit `e3487afa0a6953a428bea997359aa257fd97882c` on `2026-10-22T19:54:26.869816+00:00`.

> Scope: structural inventory, cross-table checks, and reproduction of the existing validator's status. This is not comprehensive verification against every PDF.

## Executive findings

- 2,658 summarized reports are represented in the published summary; 2,649 are marked done and 9 are flagged in progress.
- 20 summary records explicitly fail the governmental roll-forward and 339 have no affirmative result.
- 52,469 review items remain, including 12,275 amounts not found by the automated cited-page check and 532 explicit decision items.
- The current flagged output contains 9 issues. These remain publication blockers until resolved or explicitly excluded with evidence.
- Exact whole-row duplication was not found in the three primary CSV outputs; this does not rule out semantic double counting across statements, funds, or schedules.

## Inventory

| Artifact | Count |
| --- | --- |
| Listed filings | 2672 |
| Manifest rows | 2669 |
| Trimmed PDFs | 2659 |
| Extraction JSON reports | 2658 |
| Independent verifier JSON reports | 2658 |
| Summary rows | 2658 |
| Normalized line items | 53220 |
| Detailed financial lines | 71964 |
| Review items | 52469 |
| Needs Decision items | 532 |

## Existing validation coverage

| Check | Yes | No | Blank / not recorded |
| --- | --- | --- | --- |
| Governmental roll-forward | 2299 | 20 | 339 |
| Proprietary cash flow | 366 | 2 | 2290 |
| Business-type roll-forward | 855 | 14 | 1789 |
| Balance sheet | 1656 | 9 | 993 |

A blank result can mean the statement or measure was not applicable, unavailable, or not extracted. The current output does not always encode those cases separately, so blanks cannot be treated as passes or zeros.

## Cross-table and source checks

- Summary rows missing source URLs: 0.
- Detail rows missing source URLs: 0.
- Detail rows missing cited source pages: 0.
- JSON reports without a trimmed PDF: 0.
- Trimmed PDFs without extraction JSON: 1: Grand_Island_Public_Schools_Foundation_FY2025.
- JSON reports without verifier output: 0.
- Listed filings without a manifest record: 3: J_Precinct_Mt_Pleasant_Cemetery_District_B2526, Nebraska_Statewide_Workforce_and_Educational_Reporting_System_NSWERS_FY2025, Union_Lincoln_Precinct_Cemetery_District_FY2025.
- Manifest records without a retained trimmed PDF: 10: Central_Community_College_FTESE_FY2025, Metropolitan_Community_College_FTESE_FY2025, Mid_Plains_Community_College_FTESE_FY2025, Northeast_Community_College_FTESE_FY2025, Otoe_County_Rural_Water_District_3_FY2025, Rock_County_Historical_Society_FY2025, SA854-07222026-January_1_2025_through_December_31_2025_Audit_Report, Sarpy_County_SID_234_B2526, Southeast_Community_College_FTESE_FY2025, Western_Community_College_FTESE_FY2025.

## Current flagged issues

| File | Check | Reason |
| --- | --- | --- |
| Boelus_FY2025 | verifier | missing: verifier: trimmed PDF lacks the disbursements page (p1 says 'Page 1 of 2'; pp2-3 are struck-through earlier versions of page 1, p4 is the schedules). Disbursements are fund totals from line 23 with assumed functions, so function-level lines are missing; needs re-trim and re-extraction (page shows Exhibit A (Page 2 of 2), lines 29-52 disbursements by function per fund, is not in the trimmed PDF) |
| Hall_County_FY2025 | category | detail[160] 'Other Receipts Interfund Transfers' 5,356,069: transfer recorded as revenue; transfers belong in transfers_in/out (detail section 'other financing') |
| Hickman_FY2025 | reconcile | missing beginning_fund_balance or ending_fund_balance |
| Leigh_FY2025 | verifier | missing: verifier: the more detailed object-level schedule for the General Fund departments is not in the JSON, and the trimmed PDF lacks its continuation page (report p40). The extractor's choice to keep the p9 budget lines and avoid double counting is reasonable for now, but the trim must be fixed and the departmental schedule recorded (replacing the p9 expenditure lines) once all columns are available (page shows Combining Statement of Revenues and Expenditures - General Fund Departments (report p39), columns General / Street / Police: revenues by source (e.g. Street property taxes 21,197, sales tax 26,584, intergovernmental 84,786) and expenditures by object (e.g. Street repairs and maintenance 163,735, capital outlay 75,113; Police contracted services 55,369; General salaries, taxes and benefits 30,701). Column totals 68,429 / 298,142 / 55,369 tie to p9. The remaining department columns (Housing project, Park, Pool, Library) and any total column are on a page not in the trimmed PDF) |
| Lower_Loup_NRD_FY2025 | category | detail[17] 'Irrigation Rights Transfer Fees' 5,700: transfer recorded as revenue; transfers belong in transfers_in/out (detail section 'other financing') |
| Municipal_Energy_Agency_of_Nebraska_FY2025 | category | receipts[1] 'Transfer from (provision for) rate stabilization' -1,500,000: transfer recorded as a receipt; transfers belong in transfers_in/out (detail section 'other financing') |
| Ord_FY2025 | verifier | missing: verifier: Trimmed p22 is only the right half of this schedule. The left half with row labels and the General/Public Health/Culture and Recreation/Debt Service/Public Works columns (report p61, PDF page 65) was not trimmed, so the schedule's lines are missing from detail[]. This is a trim problem (find_pages): re-trim to include PDF p65, then re-extract. (page shows Schedule of Expenditures - Modified Cash Basis - Governmental Funds (report p62), Total column: 754,343; 227,893; 119,361; 553,321; 268,053; 450,749; 319,543; 91,472; total 2,784,735) |
| Plattsmouth_Airport_Authority_FY2025 | category | receipts[0] 'Receipts and transfers (resource inflows)' 1,245,009: transfer recorded as a receipt; transfers belong in transfers_in/out (detail section 'other financing') |
| Twin_Platte_NRD_FY2025 | category | detail[15] 'Chemigation fee transfer' 3,718: transfer recorded as expenditure; transfers belong in transfers_in/out (detail section 'other financing') |

## Baseline risk assessment

1. **Source confirmation remains incomplete.** The page-presence check produces 12,275 review items, and the existing verifier shares the same trimmed-PDF population. A second method must verify statement context, period, fund, and column before publication status can be granted.
2. **Arithmetic coverage is uneven.** Failed and blank roll-forward/balance checks must be separated into true failures, not-applicable cases, and incomplete-source cases.
3. **Classification exceptions remain material.** Transfer classifications appear in current flagged output, and catch-all category mappings dominate parts of the review queue.
4. **The retained PDF set is curated rather than complete.** Validation can only confirm pages present in `trimmed/`; known missing schedules require source reacquisition or re-trimming.
5. **Duplicate detection is currently structural.** No exact duplicate primary rows were found, but semantic duplicate and double-count tests still need statement/fund/schedule inclusion rules.

## Phase 1 conclusion

The snapshot is reproducible and internally traceable at the row-to-URL/page level for the primary outputs, but it is not publication-ready as a fully verified database. Existing flags, missing affirmative reconciliations, unresolved decisions, and page-check exceptions require explicit resolution or publication exclusions.

Artifact hashes and the complete machine-readable metrics are stored in `baseline_metrics.json` so future runs can distinguish source changes from validation-rule changes.
