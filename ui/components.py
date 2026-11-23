import streamlit as st
import json
from models.schema import (
    ApplicantProfile,
    RiskFactor,
    GapItem,
    ExecutiveSummary,
    SafetyCheckResult,
    PipelineResult,
    GapConfidence,
)

def render_header():
    st.markdown(
        """
        <div class="main-header">
            <h1>🛡️ AI Health Underwriting Assistant</h1>
            <p>First-pass advisory analysis • Traceable evidence • Zero automated decision-making</p>
        </div>
        """,
        unsafe_allow_html=True,
    )



def _format_currency(val) -> str:
    if val is None:
        return "Not Stated"
    try:
        return f"${float(val):,.2f}"
    except (ValueError, TypeError):
        return str(val)

def _format_number(val, suffix="", fmt=None) -> str:
    if val is None:
        return "Not Stated"
    try:
        num = float(val)
        if fmt:
            return f"{num:{fmt}} {suffix}".strip()
        return f"{num:g} {suffix}".strip()
    except (ValueError, TypeError):
        return f"{val} {suffix}".strip()

def render_profile_card(profile: ApplicantProfile):
    st.markdown('<div class="section-title">👤 Applicant Profile</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Full Name", profile.full_name or "Not Stated")
        st.metric("Age", _format_number(profile.age, "yrs"))
        st.metric("Gender", profile.gender or "Not Stated")
        st.metric("Occupation", profile.occupation or "Not Stated")
    
    with col2:
        st.metric("Annual Income", _format_currency(profile.annual_income))
        st.metric("Sum Assured", _format_currency(profile.sum_assured))
        st.metric("Smoking Status", profile.smoking_status or "Not Stated")
        st.metric("Alcohol Use", profile.alcohol_use or "Not Stated")
        
    with col3:
        st.metric("Height", _format_number(profile.height_cm, "cm"))
        st.metric("Weight", _format_number(profile.weight_kg, "kg"))
        st.metric("BMI", _format_number(profile.bmi, fmt=".1f"))
        st.metric("Policy Type", profile.policy_type or "Not Stated")

    with col4:
        st.markdown("**Pre-Existing Conditions**")
        if profile.pre_existing_conditions:
            for cond in profile.pre_existing_conditions:
                st.markdown(f"- {cond}")
        else:
            st.caption("None reported / Not stated")
            
        st.markdown("**Family History**")
        if profile.family_medical_history:
            for item in profile.family_medical_history:
                st.markdown(f"- {item}")
        else:
            st.caption("None reported / Not stated")

def render_risk_cards(risks: list[RiskFactor]):
    st.markdown('<div class="section-title">⚠️ Identified Risk Factors</div>', unsafe_allow_html=True)

    if not risks:
        st.info("No significant risk factors identified in document text.")
        return

    for i, risk in enumerate(risks):
        sev_str = risk.severity.value if hasattr(risk.severity, "value") else str(risk.severity)
        cat_str = risk.category.value if hasattr(risk.category, "value") else str(risk.category)
        badge_cls = f"badge-{sev_str.lower()}"
        with st.container():
            st.markdown(
                f"""
                <div class="risk-card {sev_str}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong>[{cat_str}] {risk.explanation}</strong>
                        <span class="badge {badge_cls}">Severity: {sev_str}</span>
                    </div>
                    <p style="margin: 0.3rem 0; font-size: 0.92rem; color: #475569;">
                        <strong>Why it matters:</strong> {risk.why_it_matters}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Enforce evidence grounding visibility on expand
            with st.expander(f"📍 View Source Citation & Evidence (Risk #{i+1})"):
                if risk.source_evidence:
                    st.markdown(f'<div class="evidence-quote">"{risk.source_evidence}"</div>', unsafe_allow_html=True)
                else:
                    st.warning("No ground truth evidence cited for this item.")

def render_gap_cards(gaps: list[GapItem]):
    st.markdown('<div class="section-title">🔍 Missing Information & Signal Disagreements</div>', unsafe_allow_html=True)

    if not gaps:
        st.success("All 14 required underwriting fields are present in the proposal text.")
        return

    # Separate disputed gaps from agreed missing gaps
    disputed_gaps = []
    agreed_gaps = []
    for g in gaps:
        conf_val = g.confidence.value if hasattr(g.confidence, "value") else str(g.confidence)
        if conf_val == GapConfidence.DISPUTED.value:
            disputed_gaps.append(g)
        else:
            agreed_gaps.append(g)

    if disputed_gaps:
        st.warning(f"⚠️ **{len(disputed_gaps)} Signal Disagreement(s) Surfaced** — Regex parser and AI model disagree on presence/absence:")
        for gap in disputed_gaps:
            with st.container():
                st.markdown(
                    f"""
                    <div style="background: #faf5ff; border: 1px solid #e9d5ff; padding: 1rem; border-radius: 10px; margin-bottom: 0.8rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #6b21a8;">Field: {gap.field_name}</strong>
                            <span class="badge badge-disputed">Disputed Signal</span>
                        </div>
                        <p style="margin: 0.4rem 0 0.2rem 0; font-size: 0.9rem; color: #581c87;">
                            <strong>Deterministic Regex Signal:</strong> {'Present' if gap.regex_signal else 'Absent'} | 
                            <strong>AI LLM Signal:</strong> {'Present' if gap.llm_signal else 'Absent'}
                        </p>
                        <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem; color: #475569;">
                            {gap.why_it_matters}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    if agreed_gaps:
        st.markdown(f"**Missing Required Fields ({len(agreed_gaps)}):**")
        for gap in agreed_gaps:
            st.markdown(
                f"""
                <div style="background: #fff7ed; border: 1px solid #ffedd5; padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                    <span class="badge badge-missing">Missing Field</span> <strong>{gap.field_name}</strong>: {gap.why_it_matters}
                </div>
                """,
                unsafe_allow_html=True
            )

def render_summary_card(summary: ExecutiveSummary, safety_check: SafetyCheckResult):
    st.markdown('<div class="section-title">📋 Executive Assessment & Recommended Path</div>', unsafe_allow_html=True)

    rec_str = summary.recommendation.value if hasattr(summary.recommendation, "value") else str(summary.recommendation)

    # Recommendation Container
    st.markdown(
        f"""
        <div class="recommendation-card">
            <div class="recommendation-title">Recommended Review Path: {rec_str}</div>
            <p style="margin-top: 0.5rem; color: #e2e8f0; font-size: 0.95rem;">
                <strong>Rationale:</strong> {summary.rationale}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Executive Summary Text
    st.markdown("**Executive Summary**")
    st.info(summary.summary_text)

    # Safety Net Status
    if safety_check.passed:
        st.caption("✅ Safety Net Check Passed: Zero automated decision/verdict terms emitted.")
    else:
        st.error(f"🚨 Safety Net Warning: Summary contains prohibited verdict terms: {', '.join(safety_check.flagged_terms)}")


def render_download_button(result: PipelineResult):
    json_str = result.model_dump_json(indent=2)
    st.download_button(
        label="📥 Download Structured Underwriting Report (JSON)",
        data=json_str,
        file_name=f"underwriting_report_{result.filename}.json",
        mime="application/json",
        use_container_width=True,
    )
