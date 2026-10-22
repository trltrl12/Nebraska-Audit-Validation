PRAGMA foreign_keys = ON;

CREATE TABLE source_document (
    document_id TEXT PRIMARY KEY,
    content_sha256 TEXT NOT NULL UNIQUE CHECK (length(content_sha256) = 64),
    filename TEXT NOT NULL,
    source_url TEXT,
    entity_id TEXT NOT NULL,
    reporting_period_start TEXT,
    reporting_period_end TEXT NOT NULL,
    accounting_basis TEXT NOT NULL,
    filing_type TEXT NOT NULL,
    page_count INTEGER CHECK (page_count IS NULL OR page_count > 0),
    retained_page_count INTEGER CHECK (retained_page_count IS NULL OR retained_page_count >= 0),
    source_completeness_status TEXT NOT NULL CHECK (source_completeness_status IN (
        'VERIFIED', 'UNDER_REVIEW', 'FAILED_VALIDATION', 'INCOMPLETE_SOURCE',
        'NOT_YET_VERIFIED', 'NOT_APPLICABLE'
    )),
    created_at TEXT NOT NULL
);

CREATE TABLE source_observation (
    observation_id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES source_document(document_id),
    original_label TEXT NOT NULL,
    original_amount TEXT,
    original_text TEXT,
    statement_name TEXT NOT NULL,
    fund_name TEXT,
    source_page INTEGER NOT NULL CHECK (source_page > 0),
    source_column TEXT,
    reporting_scope TEXT NOT NULL,
    value_type TEXT NOT NULL CHECK (value_type IN (
        'AUDITED_ACTUAL', 'UNAUDITED_ACTUAL', 'ESTIMATED_ACTUAL', 'BUDGET'
    )),
    extraction_method TEXT NOT NULL,
    extraction_timestamp TEXT NOT NULL,
    UNIQUE (document_id, statement_name, fund_name, source_page, source_column, original_label, original_amount)
);

CREATE TABLE classification_rule (
    rule_id TEXT NOT NULL,
    rule_version TEXT NOT NULL,
    category TEXT NOT NULL,
    definition TEXT NOT NULL,
    applicable_basis TEXT,
    applicable_scope TEXT,
    effective_from TEXT NOT NULL,
    retired_at TEXT,
    PRIMARY KEY (rule_id, rule_version)
);

CREATE TABLE standardized_fact (
    fact_id TEXT PRIMARY KEY,
    observation_id TEXT NOT NULL REFERENCES source_observation(observation_id),
    measure_definition_id TEXT NOT NULL,
    standardized_category TEXT NOT NULL,
    amount TEXT NOT NULL,
    accounting_basis TEXT NOT NULL,
    reporting_scope TEXT NOT NULL,
    transaction_scope TEXT NOT NULL CHECK (transaction_scope IN (
        'EXTERNAL', 'INTERFUND', 'INTRA_ENTITY', 'UNKNOWN'
    )),
    publication_role TEXT NOT NULL CHECK (publication_role IN (
        'PRIMARY', 'DETAIL', 'ELIMINATION', 'EXCLUDED'
    )),
    classification_rule_id TEXT NOT NULL,
    classification_rule_version TEXT NOT NULL,
    classification_support TEXT NOT NULL CHECK (classification_support IN (
        'DIRECT_LABEL', 'SOURCE_NOTE', 'DOCUMENTED_RULE', 'HUMAN_DECISION'
    )),
    created_at TEXT NOT NULL,
    FOREIGN KEY (classification_rule_id, classification_rule_version)
        REFERENCES classification_rule(rule_id, rule_version)
);

CREATE TABLE verification_assessment (
    assessment_id TEXT PRIMARY KEY,
    fact_id TEXT NOT NULL REFERENCES standardized_fact(fact_id),
    dimension TEXT NOT NULL CHECK (dimension IN (
        'extraction', 'reconciliation', 'classification', 'source_completeness', 'entity_identity'
    )),
    status TEXT NOT NULL CHECK (status IN (
        'VERIFIED', 'UNDER_REVIEW', 'FAILED_VALIDATION', 'INCOMPLETE_SOURCE',
        'NOT_YET_VERIFIED', 'NOT_APPLICABLE'
    )),
    reason TEXT NOT NULL,
    method TEXT NOT NULL,
    rule_version TEXT NOT NULL,
    evidence_reference TEXT,
    assessed_at TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    CHECK (status != 'NOT_APPLICABLE' OR dimension = 'reconciliation'),
    UNIQUE (fact_id, dimension, rule_version, assessed_at)
);

CREATE TABLE human_decision (
    decision_id TEXT PRIMARY KEY,
    fact_id TEXT REFERENCES standardized_fact(fact_id),
    question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('OPEN', 'DECIDED', 'SUPERSEDED')),
    decision TEXT,
    rationale TEXT,
    evidence_reference TEXT,
    decided_by TEXT,
    decided_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE correction_log (
    correction_id TEXT PRIMARY KEY,
    fact_id TEXT NOT NULL REFERENCES standardized_fact(fact_id),
    original_observation_id TEXT NOT NULL REFERENCES source_observation(observation_id),
    prior_value TEXT,
    corrected_value TEXT,
    affected_metric TEXT NOT NULL,
    reason TEXT NOT NULL,
    evidence_reference TEXT NOT NULL,
    code_or_rule_change TEXT,
    validation_result TEXT NOT NULL,
    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL
);

CREATE INDEX idx_observation_document ON source_observation(document_id);
CREATE INDEX idx_fact_observation ON standardized_fact(observation_id);
CREATE INDEX idx_assessment_fact_dimension ON verification_assessment(fact_id, dimension);
