"""Publication gates for independently verified financial facts."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Iterable, Mapping


class VerificationStatus(StrEnum):
    VERIFIED = "VERIFIED"
    UNDER_REVIEW = "UNDER_REVIEW"
    FAILED_VALIDATION = "FAILED_VALIDATION"
    INCOMPLETE_SOURCE = "INCOMPLETE_SOURCE"
    NOT_YET_VERIFIED = "NOT_YET_VERIFIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class VerificationDimension(StrEnum):
    EXTRACTION = "extraction"
    RECONCILIATION = "reconciliation"
    CLASSIFICATION = "classification"
    SOURCE_COMPLETENESS = "source_completeness"
    ENTITY_IDENTITY = "entity_identity"


REQUIRED_DIMENSIONS = tuple(VerificationDimension)
PASSING_STATUSES = {
    VerificationDimension.EXTRACTION: {VerificationStatus.VERIFIED},
    VerificationDimension.RECONCILIATION: {
        VerificationStatus.VERIFIED,
        VerificationStatus.NOT_APPLICABLE,
    },
    VerificationDimension.CLASSIFICATION: {VerificationStatus.VERIFIED},
    VerificationDimension.SOURCE_COMPLETENESS: {VerificationStatus.VERIFIED},
    VerificationDimension.ENTITY_IDENTITY: {VerificationStatus.VERIFIED},
}


@dataclass(frozen=True)
class PublicationCandidate:
    fact_id: str
    measure_definition_id: str
    entity_id: str
    reporting_period_end: str
    accounting_basis: str
    reporting_scope: str
    value_type: str
    amount: Decimal | None
    source_document_id: str | None
    source_page: int | None
    publication_role: str
    statuses: Mapping[VerificationDimension, VerificationStatus]
    transaction_scope: str = "external"


@dataclass(frozen=True)
class GateResult:
    eligible: bool
    reasons: tuple[str, ...]


def evaluate_publication(candidate: PublicationCandidate) -> GateResult:
    """Return whether one fact meets the minimum publication contract."""

    reasons: list[str] = []
    if candidate.amount is None:
        reasons.append("amount is missing; missing values cannot be published as zero")
    if not candidate.source_document_id:
        reasons.append("source document is missing")
    if candidate.source_page is None or candidate.source_page < 1:
        reasons.append("valid source page is missing")
    if not candidate.accounting_basis:
        reasons.append("accounting basis is missing")
    if not candidate.reporting_scope:
        reasons.append("reporting scope is missing")
    if not candidate.value_type:
        reasons.append("actual, estimated, or budget value type is missing")
    if candidate.publication_role not in {"primary", "detail"}:
        reasons.append(f"publication role {candidate.publication_role!r} is excluded")

    for dimension in REQUIRED_DIMENSIONS:
        status = candidate.statuses.get(dimension)
        if status is None:
            reasons.append(f"{dimension.value} status is missing")
        elif status not in PASSING_STATUSES[dimension]:
            reasons.append(f"{dimension.value} status is {status.value}")

    return GateResult(eligible=not reasons, reasons=tuple(reasons))


def evaluate_aggregate(candidates: Iterable[PublicationCandidate]) -> GateResult:
    """Check that facts can be combined without mixing incompatible measures."""

    facts = list(candidates)
    reasons: list[str] = []
    if not facts:
        return GateResult(False, ("aggregate has no facts",))

    for fact in facts:
        result = evaluate_publication(fact)
        reasons.extend(f"{fact.fact_id}: {reason}" for reason in result.reasons)

    duplicate_ids = sorted(
        fact_id for fact_id in {fact.fact_id for fact in facts} if sum(f.fact_id == fact_id for f in facts) > 1
    )
    if duplicate_ids:
        reasons.append("duplicate fact IDs: " + ", ".join(duplicate_ids))

    comparable_fields = {
        "measure definition": {fact.measure_definition_id for fact in facts},
        "reporting period": {fact.reporting_period_end for fact in facts},
        "accounting basis": {fact.accounting_basis for fact in facts},
        "reporting scope": {fact.reporting_scope for fact in facts},
        "value type": {fact.value_type for fact in facts},
    }
    for label, values in comparable_fields.items():
        if len(values) > 1:
            reasons.append(f"mixed {label}: " + ", ".join(sorted(values)))

    operating_measures = {"revenue", "receipts", "expense", "expenditure", "disbursements"}
    if facts[0].measure_definition_id in operating_measures:
        nonexternal = sorted(f.fact_id for f in facts if f.transaction_scope != "external")
        if nonexternal:
            reasons.append("operating aggregate includes nonexternal or unknown activity: " + ", ".join(nonexternal))

    return GateResult(eligible=not reasons, reasons=tuple(dict.fromkeys(reasons)))
