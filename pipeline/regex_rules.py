import re
from typing import Dict

REQUIRED_FIELDS = [
    "full_name",
    "age",
    "gender",
    "occupation",
    "annual_income",
    "sum_assured",
    "smoking_status",
    "alcohol_use",
    "pre_existing_conditions",
    "family_medical_history",
    "height_cm",
    "weight_kg",
    "bmi",
    "policy_type",
]

REGEX_PATTERNS: Dict[str, list[str]] = {
    "full_name": [
        r"(?:name|applicant|proposer|insured)\s*[:\-]\s*[A-Za-z]+",
        r"\b(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Za-z]+",
    ],
    "age": [
        r"\b(?:age|years?\s*old|dob|date\s*of\s*birth)\b",
        r"\b\d{1,2}\s*(?:years?\s*old|yrs)\b",
    ],
    "gender": [
        r"\b(?:gender|sex)\s*[:\-]\s*(?:male|female|other)\b",
        r"\b(?:male|female)\b",
    ],
    "occupation": [
        r"\b(?:occupation|profession|job\s*title|employment)\b",
    ],
    "annual_income": [
        r"\b(?:annual\s*income|salary|earnings|annual\s*pay)\b",
        r"\b(?:income)\s*[:\-]\s*\$?\d+",
    ],
    "sum_assured": [
        r"\b(?:sum\s*assured|coverage\s*amount|sum\s*insured|policy\s*amount)\b",
    ],
    "smoking_status": [
        r"\b(?:smok(?:er|ing)|tobacco|cigarettes?|nicotine)\b",
    ],
    "alcohol_use": [
        r"\b(?:alcohol|drink(?:er|ing)?|liquor|wine|beer)\b",
    ],
    "pre_existing_conditions": [
        r"\b(?:pre[\-\s]*existing|medical\s*conditions?|past\s*illness|chronic)\b",
    ],
    "family_medical_history": [
        r"\b(?:family\s*history|family\s*medical|hereditary)\b",
    ],
    "height_cm": [
        r"\b(?:height|ht\.?)\b",
        r"\b\d{2,3}\s*cm\b",
    ],
    "weight_kg": [
        r"\b(?:weight|wt\.?)\b",
        r"\b\d{2,3}\s*kg\b",
    ],
    "bmi": [
        r"\b(?:bmi|body\s*mass\s*index)\b",
    ],
    "policy_type": [
        r"\b(?:policy\s*type|plan\s*type|product|coverage\s*plan)\b",
    ],
}

FIELD_WHY_IT_MATTERS: Dict[str, str] = {
    "full_name": "Applicant identity verification is essential for legal underwriting binding.",
    "age": "Age determines mortal/morbidity risk brackets and rate tables.",
    "gender": "Gender influences actuarial risk calculations and premium rates.",
    "occupation": "Occupational hazards affect injury and disability risk assessment.",
    "annual_income": "Income verification ensures anti-selection and financial underwriting suitability.",
    "sum_assured": "Sum assured sets exposure limit and determines underwriting authority requirements.",
    "smoking_status": "Tobacco use significantly increases cardiovascular and pulmonary risk.",
    "alcohol_use": "Excessive alcohol consumption impacts hepatic and metabolic health parameters.",
    "pre_existing_conditions": "Prior illnesses dictate exclusions, loadings, or specialized medical reviews.",
    "family_medical_history": "Family history highlights genetic predispositions to critical illnesses.",
    "height_cm": "Height is required alongside weight to calculate BMI and assess obesity risk.",
    "weight_kg": "Weight is required alongside height to evaluate physical risk parameters.",
    "bmi": "Body Mass Index (BMI) correlates with cardiovascular and metabolic risk factors.",
    "policy_type": "Policy type specifies coverage scope, riders, and benefit limits.",
}

def check_field_regex(text: str, field_name: str) -> bool:
    """Returns True if regex detects presence of field in text, False if missing."""
    patterns = REGEX_PATTERNS.get(field_name, [])
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def check_all_fields_regex(text: str) -> Dict[str, bool]:
    """Returns dict of {field_name: bool_present} for all 14 required fields."""
    return {field: check_field_regex(text, field) for field in REQUIRED_FIELDS}
