import logging
from pydantic import BaseModel
from models.schema import RiskFactor, ApplicantProfile
from prompts.risk_prompt import RISK_SYSTEM_PROMPT, build_risk_user_prompt
from .llm_client import call_groq_json

logger = logging.getLogger(__name__)

class RiskAnalysisWrapper(BaseModel):
    risks: list[RiskFactor]

async def analyze_risks(extracted_text: str, profile: ApplicantProfile) -> list[RiskFactor]:
    """
    Stage 3: Identifies Medical, Lifestyle, Occupational risks from text & profile.
    Returns list of RiskFactor.
    """
    profile_json = profile.model_dump_json(exclude_none=False)
    user_prompt = build_risk_user_prompt(profile_json, extracted_text)

    wrapper = await call_groq_json(
        system_prompt=RISK_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        target_schema=RiskAnalysisWrapper
    )
    return wrapper.risks
