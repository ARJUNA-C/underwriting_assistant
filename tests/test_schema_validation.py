import pytest
from pydantic import ValidationError
from models.schema import (
    ApplicantProfile,
    RiskFactor,
    RiskCategory,
    Severity,
    GapItem,
    GapConfidence,
    ExecutiveSummary,
    Recommendation,
    SafetyCheckResult,
    PipelineResult,
    ExtractionMeta,
)

def test_applicant_profile_defaults():
    profile = ApplicantProfile(full_name="John Doe", age=30)
    assert profile.full_name == "John Doe"
    assert profile.age == 30
    assert profile.annual_income is None
    assert profile.pre_existing_conditions is None

def test_risk_factor_evidence_validation():
    # Non-empty source_evidence should pass
    rf = RiskFactor(
        category=RiskCategory.MEDICAL,
        severity=Severity.HIGH,
        explanation="Hypertension",
        why_it_matters="Elevated cardiovascular risk",
        source_evidence="Mild hypertension diagnosed 2021"
    )
    assert rf.source_evidence == "Mild hypertension diagnosed 2021"

    # Empty or whitespace source_evidence should raise ValidationError
    with pytest.raises(ValidationError):
        RiskFactor(
            category=RiskCategory.MEDICAL,
            severity=Severity.HIGH,
            explanation="Hypertension",
            why_it_matters="Elevated cardiovascular risk",
            source_evidence="   "
        )

def test_gap_item_creation():
    gap = GapItem(
        field_name="annual_income",
        why_it_matters="Financial underwriting requirement",
        confidence=GapConfidence.DISPUTED,
        regex_signal=False,
        llm_signal=True
    )
    assert gap.confidence == GapConfidence.DISPUTED
    assert gap.regex_signal is False
    assert gap.llm_signal is True

def test_executive_summary_recommendation_enum():
    summary = ExecutiveSummary(
        summary_text="Applicant is 42 with mild hypertension.",
        recommendation=Recommendation.ADDITIONAL_MEDICAL_REVIEW,
        rationale="Hypertension requires elevated medical scrutiny."
    )
    assert summary.recommendation == Recommendation.ADDITIONAL_MEDICAL_REVIEW
