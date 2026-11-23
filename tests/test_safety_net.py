from models.schema import ExecutiveSummary, Recommendation
from pipeline.safety_net import safety_check

def test_safety_check_pass():
    summary = ExecutiveSummary(
        summary_text="Applicant presents mild hypertension and family history of diabetes. Full documentation provided.",
        recommendation=Recommendation.ADDITIONAL_MEDICAL_REVIEW,
        rationale="Medical review advised to assess hypertension severity."
    )
    result = safety_check(summary)
    assert result.passed is True
    assert len(result.flagged_terms) == 0

def test_safety_check_flagged_terms():
    summary = ExecutiveSummary(
        summary_text="We approve this policy application with standard rates and score 95.",
        recommendation=Recommendation.STANDARD_REVIEW,
        rationale="Application passed all underwriting criteria."
    )
    result = safety_check(summary)
    assert result.passed is False
    assert any(term.lower() in ["approve", "approved", "score", "passed", "pass"] for term in result.flagged_terms)
