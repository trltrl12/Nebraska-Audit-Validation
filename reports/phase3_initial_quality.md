# Phase 3 Initial Quality Scan

Generated `2026-10-22T20:29:34.708379+00:00` from read-only source outputs.

> These are automated findings and review candidates. A candidate is not a confirmed financial error until source evidence establishes it.

## Findings

- Failures: 57
- Incomplete checks: 339
- Review candidates: 204

| Rule | Count |
| --- | ---: |
| CLASS-TRANSFER-001 | 182 |
| DUP-SOURCE-001 | 22 |
| REC-BAL-001 | 9 |
| REC-BT-001 | 14 |
| REC-GOV-001 | 20 |
| REC-GOV-002 | 339 |
| REC-PROP-001 | 2 |
| SOURCE-FLAG-001 | 12 |

## Highest-priority entities

Tier 1 has an explicit failure, Tier 2 has an incomplete governmental roll-forward, Tier 3 has review-only findings, and Tier 4 has no finding from this scanner.

| Tier | File | Entity | Failures | Incomplete | Scanner reviews | Existing reviews | Page checks | Decisions |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Sargent_Public_Schools_FY2025 | Sargent School District No. 84 | 3 | 0 | 3 | 46 | 15 | 0 |
| 1 | Oshkosh_FY2025 | City of Oshkosh | 2 | 0 | 0 | 56 | 4 | 1 |
| 1 | Wymore_FY2025 | City of Wymore | 2 | 0 | 0 | 39 | 4 | 1 |
| 1 | Sutherland_FY2025 | Village of Sutherland | 2 | 0 | 0 | 80 | 2 | 0 |
| 1 | Arlington_FY2025 | Village of Arlington | 2 | 0 | 0 | 45 | 0 | 0 |
| 1 | Pathfinder_Irrigation_District_FY2025 | Pathfinder Irrigation District | 1 | 1 | 0 | 15 | 0 | 2 |
| 1 | Gering_Irrigation_District_FY2025 | Gering Irrigation District | 1 | 1 | 0 | 22 | 10 | 1 |
| 1 | Hickman_FY2025 | City of Hickman | 1 | 1 | 0 | 14 | 2 | 1 |
| 1 | Municipal_Energy_Agency_of_Nebraska_FY2025 | Municipal Energy Agency of Nebraska | 1 | 1 | 0 | 13 | 0 | 1 |
| 1 | Central_Irrigation_District_FY2025 | Central Irrigation District | 1 | 1 | 0 | 25 | 11 | 0 |
| 1 | Laurel_Housing_Authority_FY2025 | Housing Authority of the City of Laurel, Nebraska | 1 | 1 | 0 | 7 | 3 | 0 |
| 1 | North_Platte_Airport_Authority_FY2025 | North Platte Airport Authority | 1 | 1 | 0 | 73 | 1 | 0 |
| 1 | Panhandle_Area_Development_District_FY2025 | Panhandle Area Development District | 1 | 1 | 0 | 27 | 0 | 0 |
| 1 | South_Central_Area_Agency_on_Aging_FY2025 | South Central Nebraska Area Agency on Aging | 1 | 1 | 0 | 17 | 0 | 0 |
| 1 | Hall_County_Housing_Authority_FY2025 | Hall County Housing Authority | 1 | 1 | 0 | 12 | 0 | 0 |
| 1 | Arcadia_FY2025 | Village of Arcadia | 1 | 0 | 1 | 39 | 0 | 3 |
| 1 | Springfield_FY2025 | City of Springfield | 1 | 0 | 0 | 39 | 0 | 3 |
| 1 | Plattsmouth_Airport_Authority_FY2025 | Plattsmouth Airport Authority | 1 | 0 | 0 | 15 | 5 | 2 |
| 1 | Hall_County_FY2025 | Hall County | 1 | 0 | 1 | 83 | 0 | 2 |
| 1 | Hay_Springs_FY2025 | City of Hay Springs | 1 | 0 | 0 | 50 | 0 | 2 |
| 1 | Nebraska_Cooperative_Republican_Platte_Enhancement_Project_N-CORPE_FY2025 | Nebraska Cooperative Republican Platte Enhancement Project (N-CORPE) | 1 | 0 | 0 | 28 | 0 | 2 |
| 1 | Fairmont_FY2025 | Village of Fairmont | 1 | 0 | 0 | 26 | 0 | 2 |
| 1 | Twin_Platte_NRD_FY2025 | Twin Platte Natural Resources District | 1 | 0 | 1 | 17 | 3 | 1 |
| 1 | Weston_FY2025 | Village of Weston | 1 | 0 | 0 | 27 | 2 | 1 |
| 1 | Byron_Community_Building_District_B2526 | Byron Community Building District (Thayer County) | 1 | 0 | 0 | 14 | 2 | 1 |
| 1 | Ord_FY2025 | City of Ord | 1 | 0 | 1 | 33 | 1 | 1 |
| 1 | Elwood_FY2025 | Village of Elwood | 1 | 0 | 0 | 74 | 0 | 1 |
| 1 | Oakland_FY2025 | City of Oakland | 1 | 0 | 0 | 49 | 0 | 1 |
| 1 | Pilger_FY2025 | Village of Pilger | 1 | 0 | 0 | 45 | 0 | 1 |
| 1 | Lodgepole_FY2025 | Village of Lodgepole | 1 | 0 | 0 | 16 | 0 | 1 |
| 1 | Yutan_FY2025 | City of Yutan | 1 | 0 | 0 | 3 | 0 | 1 |
| 1 | Boelus_FY2025 | Village of Boelus | 1 | 0 | 0 | 42 | 19 | 0 |
| 1 | Cuming_County_FY2025 | Cuming County | 1 | 0 | 0 | 38 | 5 | 0 |
| 1 | Rushville_FY2025 | City of Rushville | 1 | 0 | 0 | 47 | 2 | 0 |
| 1 | Doniphan_Trumbull_Public_Schools_FY2025 | Doniphan-Trumbull Public School District No. 40-0126 | 1 | 0 | 0 | 48 | 1 | 0 |
| 1 | Lower_Loup_NRD_FY2025 | Lower Loup Natural Resources District | 1 | 0 | 1 | 38 | 1 | 0 |
| 1 | Leigh_FY2025 | Village of Leigh | 1 | 0 | 0 | 14 | 1 | 0 |
| 1 | Millard_Public_Schools_FY2025 | School District No. 17 - Millard Public Schools | 1 | 0 | 1 | 76 | 0 | 0 |
| 1 | Crofton_Community_Schools_FY2025 | Crofton Community Schools District No. 96 | 1 | 0 | 0 | 60 | 0 | 0 |
| 1 | Minden_Public_Schools_FY2025 | Minden Public Schools District No. 503 | 1 | 0 | 2 | 60 | 0 | 0 |
| 1 | Broken_Bow_Public_Schools_FY2025 | Broken Bow Public Schools District No. 25 | 1 | 0 | 1 | 58 | 0 | 0 |
| 1 | Elkhorn_Public_Schools_FY2025 | Douglas County School District No. 10 (Elkhorn Public Schools) | 1 | 0 | 1 | 53 | 0 | 0 |
| 1 | Wilcox-Hildreth_Public_Schools_FY2025 | Wilcox-Hildreth Public School | 1 | 0 | 3 | 47 | 0 | 0 |
| 1 | Henderson_FY2025 | City of Henderson | 1 | 0 | 0 | 35 | 0 | 0 |
| 1 | Amherst_Public_Schools_FY2025 | Amherst Public Schools District No. 119 | 1 | 0 | 0 | 32 | 0 | 0 |
| 1 | Minatare_FY2025 | City of Minatare | 1 | 0 | 0 | 30 | 0 | 0 |
| 1 | Hayes_Center_FY2025 | Village of Hayes Center | 1 | 0 | 0 | 25 | 0 | 0 |
| 1 | Sarpy_County_SID_23_FY2025 | Sanitary and Improvement District No. 23 of Sarpy County | 1 | 0 | 0 | 17 | 0 | 0 |
| 1 | Sarpy_County_SID_373_FY2025 | Sanitary and Improvement District No. 373 of Sarpy County | 1 | 0 | 0 | 9 | 0 | 0 |
| 1 | Douglas_County_SID_633_FY2025 | Sanitary and Improvement District No. 633 of Douglas County | 1 | 0 | 0 | 8 | 0 | 0 |

## Interpretation limits

- Matching amounts alone are never treated as duplicates. Duplicate candidates require the same source file, page, schedule, fund, department, original label, and amount.
- Transfer-word findings require context review; labels such as transfer fees may describe external revenue rather than interfund activity.
- Blank reconciliation results remain incomplete until applicability and source completeness are established.
- The queue prioritizes investigation; it does not assign publication eligibility by itself.
