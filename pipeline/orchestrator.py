import logging
from typing import AsyncIterator
from models.schema import (
    StageUpdate,
    PipelineResult,
    ExtractionMeta,
    ApplicantProfile,
    RiskFactor,
    GapItem,
    ExecutiveSummary,
    SafetyCheckResult,
    Recommendation,
)
from .ingest import extract_text, ExtractionError
from .profile import extract_profile
from .risks import analyze_risks
from .gaps import detect_gaps
from .summary import summarize
from .safety_net import safety_check

logger = logging.getLogger(__name__)

async def run_pipeline_streaming(pdf_bytes: bytes, filename: str) -> AsyncIterator[StageUpdate]:
    """
    Orchestrates the 6-stage underwriting analysis pipeline asynchronously.
    Yields StageUpdate events progressive updates for UI rendering.
    """
    # Initialize container variables for degraded state continuation
    extracted_text = ""
    extraction_meta = ExtractionMeta(source="digital", page_count=1, ocr_failed=False)
    profile = ApplicantProfile()
    risks: list[RiskFactor] = []
    gaps: list[GapItem] = []
    summary = ExecutiveSummary(
        summary_text="Analysis incomplete due to pipeline stage failure.",
        recommendation=Recommendation.SENIOR_UNDERWRITER_REVIEW,
        rationale="Automated summary could not be generated.",
    )
    safety_res = SafetyCheckResult(passed=True, flagged_terms=[])

    # STAGE 1: Extraction
    yield StageUpdate(stage="extraction", status="running")
    try:
        extracted_text, extraction_meta = extract_text(pdf_bytes)
        yield StageUpdate(
            stage="extraction",
            status="done",
            data=extraction_meta.model_dump()
        )
    except Exception as e:
        logger.error(f"Stage 1 Extraction failed: {e}")
        yield StageUpdate(stage="extraction", status="failed", error=str(e))
        # Hard fail if PDF cannot be read at all
        return

    # STAGE 2: Profile Extraction
    yield StageUpdate(stage="profile", status="running")
    try:
        profile = await extract_profile(extracted_text)
        yield StageUpdate(
            stage="profile",
            status="done",
            data=profile.model_dump()
        )
    except Exception as e:
        logger.error(f"Stage 2 Profile extraction failed: {e}")
        yield StageUpdate(stage="profile", status="failed", error=str(e))

    # STAGE 3: Risk Analysis
    yield StageUpdate(stage="risks", status="running")
    try:
        risks = await analyze_risks(extracted_text, profile)
        yield StageUpdate(
            stage="risks",
            status="done",
            data={"risks": [r.model_dump() for r in risks]}
        )
    except Exception as e:
        logger.error(f"Stage 3 Risk analysis failed: {e}")
        yield StageUpdate(stage="risks", status="failed", error=str(e))

    # STAGE 4: Gap Detection (Regex + LLM Reconciliation)
    yield StageUpdate(stage="gaps", status="running")
    try:
        gaps = await detect_gaps(extracted_text, profile)
        yield StageUpdate(
            stage="gaps",
            status="done",
            data={"gaps": [g.model_dump() for g in gaps]}
        )
    except Exception as e:
        logger.error(f"Stage 4 Gap detection failed: {e}")
        yield StageUpdate(stage="gaps", status="failed", error=str(e))

    # STAGE 5: Executive Summary & Recommendation
    yield StageUpdate(stage="summary", status="running")
    try:
        summary = await summarize(profile, risks, gaps)
        yield StageUpdate(
            stage="summary",
            status="done",
            data=summary.model_dump()
        )
    except Exception as e:
        logger.error(f"Stage 5 Summary failed: {e}")
        yield StageUpdate(stage="summary", status="failed", error=str(e))

    # STAGE 6: Post-generation Safety Net
    yield StageUpdate(stage="safety_net", status="running")
    try:
        safety_res = safety_check(summary)
        yield StageUpdate(
            stage="safety_net",
            status="done",
            data=safety_res.model_dump()
        )
    except Exception as e:
        logger.error(f"Stage 6 Safety Net failed: {e}")
        yield StageUpdate(stage="safety_net", status="failed", error=str(e))

    # Emit complete result as data on final update or final object
    final_pipeline_result = PipelineResult(
        filename=filename,
        extraction_meta=extraction_meta,
        profile=profile,
        risks=risks,
        gaps=gaps,
        summary=summary,
        safety_check=safety_res,
    )
    yield StageUpdate(
        stage="safety_net",
        status="done",
        data={"pipeline_result": final_pipeline_result.model_dump()}
    )


async def run_pipeline(pdf_bytes: bytes, filename: str) -> PipelineResult:
    """
    Non-streaming entry point that runs pipeline to completion and returns PipelineResult.
    """
    final_result = None
    async for update in run_pipeline_streaming(pdf_bytes, filename):
        if update.data and "pipeline_result" in update.data:
            final_result = PipelineResult.model_validate(update.data["pipeline_result"])

    if final_result is None:
        raise RuntimeError("Pipeline execution failed to produce a final PipelineResult.")

    return final_result
