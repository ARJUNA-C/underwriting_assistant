import logging
import asyncio
from pydantic import BaseModel
from typing import Optional
from models.schema import GapItem, GapConfidence, ApplicantProfile
from prompts.gap_prompt import GAP_SYSTEM_PROMPT, build_gap_user_prompt
from .llm_client import call_groq_json, LLMError
from .regex_rules import REQUIRED_FIELDS, FIELD_WHY_IT_MATTERS, check_all_fields_regex

logger = logging.getLogger(__name__)

class RawLLMGapSignal(BaseModel):
    field_name: str
    present: bool
    why_it_matters: Optional[str] = None

class LLMGapResponse(BaseModel):
    gaps: list[RawLLMGapSignal]

async def detect_gaps(extracted_text: str, profile: ApplicantProfile) -> list[GapItem]:
    """
    Stage 4: Missing-info detection. Runs regex signal & LLM signal, reconciles results.
    - Both present -> No gap item.
    - Both absent -> GapItem (confidence='high').
    - Disagree -> GapItem (confidence='disputed').
    """
    # 1. Regex signal (deterministic)
    regex_signals = check_all_fields_regex(extracted_text)

    # 2. LLM signal
    llm_signals: dict[str, bool] = {}
    llm_why: dict[str, str] = {}

    try:
        user_prompt = build_gap_user_prompt(REQUIRED_FIELDS, extracted_text)
        response = await call_groq_json(
            system_prompt=GAP_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            target_schema=LLMGapResponse
        )
        for item in response.gaps:
            llm_signals[item.field_name] = item.present
            if item.why_it_matters:
                llm_why[item.field_name] = item.why_it_matters
    except Exception as e:
        logger.warning(f"LLM gap detection call failed, defaulting LLM signals to Profile presence: {e}")
        # Fallback for LLM signal using profile values if LLM call fails
        profile_dict = profile.model_dump()
        for field in REQUIRED_FIELDS:
            llm_signals[field] = profile_dict.get(field) is not None

    # 3. Reconciliation
    reconciled_gaps: list[GapItem] = []

    for field in REQUIRED_FIELDS:
        reg_present = regex_signals.get(field, False)
        # Default LLM signal to True if field is in profile, else fallback to reg_present
        profile_has_val = getattr(profile, field, None) is not None
        llm_present = llm_signals.get(field, profile_has_val)

        if reg_present and llm_present:
            # Both agree present -> Not a gap
            continue
        elif not reg_present and not llm_present:
            # Both agree absent -> High confidence gap
            why = llm_why.get(field) or FIELD_WHY_IT_MATTERS.get(field, "Field is missing from application.")
            reconciled_gaps.append(
                GapItem(
                    field_name=field,
                    why_it_matters=why,
                    confidence=GapConfidence.HIGH,
                    regex_signal=False,
                    llm_signal=False,
                )
            )
        else:
            # Disagreement (one signals present, one signals absent) -> Surface disputed gap
            why = (
                f"Disagreement detected between deterministic parser (regex={'present' if reg_present else 'absent'}) "
                f"and AI model (LLM={'present' if llm_present else 'absent'}). Manual verification needed. "
                + (FIELD_WHY_IT_MATTERS.get(field, ""))
            )
            reconciled_gaps.append(
                GapItem(
                    field_name=field,
                    why_it_matters=why,
                    confidence=GapConfidence.DISPUTED,
                    regex_signal=reg_present,
                    llm_signal=llm_present,
                )
            )

    return reconciled_gaps
