SHARED_CLOSING_BLOCK = """
Respond with valid JSON only, matching the given schema exactly.
Do not infer, assume, or fill in values not explicitly present in the source text.
If a field is not present in the text, set it to null (profile) or omit the item (risks/gaps).
Every risk MUST include source_evidence: a verbatim quote or close paraphrase pointing to the exact text that supports it. Never fabricate evidence.
"""

PROFILE_SYSTEM_PROMPT = """You are extracting structured applicant data from a health insurance proposal form for underwriter review. You do not make decisions — extraction only."""

def build_profile_user_prompt(extracted_text: str) -> str:
    return f"""Extract the following 14 fields from the document text below.
Use null for any field not explicitly stated. Do not infer age from DOB or vice versa unless both would be derived from the same explicit statement.

Fields: full_name, age, gender, occupation, annual_income, sum_assured, smoking_status, alcohol_use, pre_existing_conditions, family_medical_history, height_cm, weight_kg, bmi, policy_type

Document text:
{extracted_text}

{SHARED_CLOSING_BLOCK}"""
