# Current data flow

This documents the inspected `Nebraska-Audit` source snapshot at commit `e3487afa0a6953a428bea997359aa257fd97882c`.

1. `scripts/download.py` obtains the Nebraska Auditor filing list, records it in `output/file_list.csv`, and downloads source PDFs to the ignored `audits/` directory.
2. `scripts/find_pages.py` selects financial-statement and schedule pages, writes retained PDFs to `trimmed/`, and records provenance in `output/manifest.csv`.
3. The extraction workflow writes one report-level JSON file per extracted filing to `output/json/`. Each monetary value is intended to retain an original label and cited page. Independent verifier findings are stored in `output/json/verify/`.
4. `scripts/pagecheck.py` checks whether extracted amounts appear on cited retained pages. Its OCR/text cache is local and ignored by Git.
5. `scripts/validate.py` performs schema, reconciliation, total, balance-sheet, page-presence, classification, and verifier checks. It generates `output/flagged.csv`, `output/review.csv`, and the validated-hash inventory.
6. `scripts/build_csv.py` normalizes the JSON into summary, line-item, detail, progress, and supporting CSV outputs. `scripts/build_xlsx.py` assembles those outputs into `output/cashflow.xlsx`.
7. GitHub Actions runs fetching and validation. The current workflow commits generated source-repository outputs after JSON changes.

## Principal dependencies

- `output/file_list.csv` supplies filing identity, county, type, and source URL.
- `output/manifest.csv` connects filings to retained pages and page-selection metadata.
- `output/json/*.json` is the authoritative extracted record layer used by the builders.
- `trimmed/*.pdf` is the retained evidence population used by the existing verifier and page checker.
- `output/cashflow.xlsx` is a presentation artifact generated from the CSV outputs; it is not an independent source of truth.

## Baseline weaknesses

- The existing validator and workbook are downstream of the same extraction JSON. Internal agreement cannot independently prove extraction accuracy.
- Retained PDFs are curated subsets. A missing schedule in `trimmed/` prevents the existing page checker and verifier from assessing information absent from that subset.
- Blank reconciliation fields do not consistently distinguish not applicable, missing source, and not yet verified.
- Current duplicate checks establish exact-row uniqueness but do not yet enforce publication-specific inclusion rules across fund, combining, detail, and government-wide statements.
- Classification rules exist in application code and extraction instructions, but a versioned public classification dictionary has not yet been separated into this validation repository.
- The source repository has operational validation scripts but no standalone regression-test suite using deliberately valid and invalid financial examples.
