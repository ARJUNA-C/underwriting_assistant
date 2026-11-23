import logging
from models.schema import ApplicantProfile
from prompts.profile_prompt import PROFILE_SYSTEM_PROMPT, build_profile_user_prompt
from .llm_client import call_groq_json

logger = logging.getLogger(__name__)

async def extract_profile(extracted_text: str) -> ApplicantProfile:
    """
    Stage 2: Extracts 14-field applicant profile from document text.
    """
    user_prompt = build_profile_user_prompt(extracted_text)
    profile = await call_groq_json(
        system_prompt=PROFILE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        target_schema=ApplicantProfile
    )
    return profile
