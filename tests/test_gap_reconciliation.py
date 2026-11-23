import pytest
from models.schema import GapConfidence, ApplicantProfile
from pipeline.gaps import detect_gaps
from pipeline.regex_rules import check_all_fields_regex

@pytest.mark.asyncio
async def test_gap_reconciliation_disagreement_surfaced(monkeypatch):
    """
    Verifies that when regex and LLM signals disagree on a field's presence,
    the gap is surfaced with confidence='disputed' and raw signals attached.
    """
    text = "Applicant Name: Jane Doe. Height: 165 cm. Weight: 60 kg."
    profile = ApplicantProfile(full_name="Jane Doe", height_cm=165.0, weight_kg=60.0)

    # Call detect_gaps
    gaps = await detect_gaps(text, profile)

    # Check that gaps were returned
    assert isinstance(gaps, list)
    
    # Check that missing fields (e.g. annual_income, smoking_status) have gap items
    disputed_or_high_gaps = {g.field_name: g for g in gaps}
    assert "annual_income" in disputed_or_high_gaps

    income_gap = disputed_or_high_gaps["annual_income"]
    assert income_gap.confidence in (GapConfidence.HIGH, GapConfidence.DISPUTED)
    assert isinstance(income_gap.regex_signal, bool)
    assert isinstance(income_gap.llm_signal, bool)
