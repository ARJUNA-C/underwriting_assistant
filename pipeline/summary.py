import json
import logging
from models.schema import ExecutiveSummary, ApplicantProfile, RiskFactor, GapItem
from prompts.summary_prompt import SUMMARY_SYSTEM_PROMPT, build_summary_user_prompt
from .llm_client import call_groq_json

logger = logging.getLogger(__name__)

async def summarize(
    profile: ApplicantProfile,
    risks: list[RiskFactor],
    gaps: list[GapItem]
) -> ExecutiveSummary:
    """
    Stage 5: Generates neutral executive summary and selects Recommendation enum path.
    """
    profile_json = profile.model_dump_json(exclude_none=False)
    risks_json = json.dumps([r.model_dump() for r in risks])
    gaps_json = json.dumps([g.model_dump() for g in gaps])

    user_prompt = build_summary_user_prompt(profile_json, risks_json, gaps_json)

    summary = await call_groq_json(
        system_prompt=SUMMARY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        target_schema=ExecutiveSummary
    )
    return summary
