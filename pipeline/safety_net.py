import re
import logging
from models.schema import ExecutiveSummary, SafetyCheckResult

logger = logging.getLogger(__name__)

# Blocklist regex patterns for verdict/decision/scoring terms
BLOCKED_PATTERNS = [
    r"\bapprove[ds]?\b",
    r"\breject(?:ed|s)?\b",
    r"\bdecline[ds]?\b",
    r"\bqualif(?:y|ied|ies)\b",
    r"\bscore[s]?\b",
    r"\bpass(?:ed|es)?\b",
    r"\bfail(?:ed|es)?\b",
]

def safety_check(summary: ExecutiveSummary) -> SafetyCheckResult:
    """
    Stage 6: Checks executive summary and recommendation rationale against verdict word blocklist.
    Returns SafetyCheckResult.
    """
    text_to_check = f"{summary.summary_text} {summary.rationale}"
    flagged_terms = []

    for pattern in BLOCKED_PATTERNS:
        matches = re.findall(pattern, text_to_check, re.IGNORECASE)
        if matches:
            flagged_terms.extend(matches)

    # Unique flagged terms
    unique_flagged = list(set(flagged_terms))
    passed = len(unique_flagged) == 0

    if not passed:
        logger.warning(f"Safety check flagged prohibited verdict terms: {unique_flagged}")

    return SafetyCheckResult(passed=passed, flagged_terms=unique_flagged)
