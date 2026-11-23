from .profile_prompt import SHARED_CLOSING_BLOCK

SUMMARY_SYSTEM_PROMPT = """You write a neutral executive summary for a human underwriter. You NEVER approve, reject, or score the application. You may recommend a review PATH only, from a fixed enum — never a decision."""

def build_summary_user_prompt(profile_json: str, risks_json: str, gaps_json: str) -> str:
    return f"""Summarize the applicant profile, risks, and gaps below in 3-5 sentences, neutral tone, no verdict language ("approve", "reject", "decline", "qualify", numeric score).
Then select exactly one recommendation from:
["Standard Review", "Additional Medical Review Recommended", "Additional Documents Required", "Senior Underwriter Review Recommended"]
and give a 1-2 sentence rationale referencing specific risks/gaps.

Profile: {profile_json}
Risks: {risks_json}
Gaps: {gaps_json}

{SHARED_CLOSING_BLOCK}"""
