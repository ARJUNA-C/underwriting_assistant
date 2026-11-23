from .profile_prompt import SHARED_CLOSING_BLOCK

GAP_SYSTEM_PROMPT = """You check a proposal document for missing required information. You are one of two independent signals; a regex pass checks separately."""

def build_gap_user_prompt(required_fields: list[str], extracted_text: str) -> str:
    field_list_str = ", ".join(required_fields)
    return f"""For each of these required fields, state present (true/false) based ONLY on document text, plus why_it_matters if absent (null or empty if present):
Required fields: {field_list_str}

Document text: {extracted_text}

Output a JSON array of objects, each containing:
- field_name: string
- present: boolean (true if explicitly present, false if missing)
- why_it_matters: string (explanation of why missing field matters for underwriting, or null if present)

{SHARED_CLOSING_BLOCK}"""
