from .profile_prompt import SHARED_CLOSING_BLOCK

RISK_SYSTEM_PROMPT = """You identify underwriting-relevant risk factors from a proposal document. You are advisory only — never output approve/reject/score language."""

def build_risk_user_prompt(profile_json: str, extracted_text: str) -> str:
    return f"""Given the applicant profile and document text below, list risk factors across three categories: Medical, Lifestyle, Occupational.

For each risk factor provide:
- category: "Medical" | "Lifestyle" | "Occupational"
- severity: "Low" | "Medium" | "High"
- explanation: what the risk is
- why_it_matters: underwriting relevance, described neutrally (no verdict)
- source_evidence: verbatim/near-verbatim quote from the text

Applicant profile: {profile_json}
Document text: {extracted_text}

{SHARED_CLOSING_BLOCK}"""
