from pydantic import BaseModel, field_validator
from enum import Enum
from typing import Optional, Literal


class ApplicantProfile(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    annual_income: Optional[float] = None
    sum_assured: Optional[float] = None
    smoking_status: Optional[str] = None
    alcohol_use: Optional[str] = None
    pre_existing_conditions: Optional[list[str]] = None
    family_medical_history: Optional[list[str]] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    policy_type: Optional[str] = None


class Severity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class RiskCategory(str, Enum):
    MEDICAL = "Medical"
    LIFESTYLE = "Lifestyle"
    OCCUPATIONAL = "Occupational"


class RiskFactor(BaseModel):
    category: RiskCategory
    severity: Severity
    explanation: str
    why_it_matters: str
    source_evidence: str

    @field_validator("source_evidence")
    @classmethod
    def validate_source_evidence(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("source_evidence must be a non-empty string referencing the source document.")
        return v.strip()


class GapConfidence(str, Enum):
    HIGH = "high"
    DISPUTED = "disputed"


class GapItem(BaseModel):
    field_name: str
    why_it_matters: str
    confidence: GapConfidence
    regex_signal: bool  # True if present, False if missing
    llm_signal: bool    # True if present, False if missing


class Recommendation(str, Enum):
    STANDARD_REVIEW = "Standard Review"
    ADDITIONAL_MEDICAL_REVIEW = "Additional Medical Review Recommended"
    ADDITIONAL_DOCUMENTS_REQUIRED = "Additional Documents Required"
    SENIOR_UNDERWRITER_REVIEW = "Senior Underwriter Review Recommended"


class ExecutiveSummary(BaseModel):
    summary_text: str
    recommendation: Recommendation
    rationale: str


class SafetyCheckResult(BaseModel):
    passed: bool
    flagged_terms: list[str] = []


class ExtractionMeta(BaseModel):
    source: str  # "digital" | "ocr"
    page_count: int
    ocr_failed: bool = False


class PipelineResult(BaseModel):
    filename: str
    extraction_meta: ExtractionMeta
    profile: ApplicantProfile
    risks: list[RiskFactor]
    gaps: list[GapItem]
    summary: ExecutiveSummary
    safety_check: SafetyCheckResult


class StageUpdate(BaseModel):
    stage: Literal["extraction", "profile", "risks", "gaps", "summary", "safety_net"]
    status: Literal["running", "done", "failed", "skipped"]
    data: Optional[dict] = None
    error: Optional[str] = None
