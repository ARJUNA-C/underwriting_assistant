import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

FIXTURES_DIR = os.path.dirname(__file__)

def create_digital_pdf(filepath: str):
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "HEALTH INSURANCE PROPOSAL FORM")
    
    c.setFont("Helvetica", 11)
    text_lines = [
        "Applicant Name: John Edward Doe",
        "Age: 42 years old",
        "Gender: Male",
        "Occupation: Software Engineer",
        "Annual Income: $120,000",
        "Sum Assured: $500,000",
        "Smoking Status: Smoker (5 cigarettes per day)",
        "Alcohol Use: Occasional social drinker",
        "Pre-Existing Conditions: Mild hypertension, diagnosed 2021",
        "Family Medical History: Father had Type 2 Diabetes at age 60",
        "Height: 178 cm",
        "Weight: 85 kg",
        "BMI: 26.8",
        "Policy Type: Comprehensive Health Term Plan",
    ]
    
    y = 710
    for line in text_lines:
        c.drawString(50, y, line)
        y -= 22
        
    c.save()

def create_disagreement_pdf(filepath: str):
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "HEALTH INSURANCE PROPOSAL FORM - DISAGREEMENT DEMO")
    
    c.setFont("Helvetica", 11)
    text_lines = [
        "Applicant Name: Jane Smith",
        "Age: 35 years old",
        "Gender: Female",
        "Occupation: Accountant",
        # Notice Income is listed in a non-standard ambiguous format or missing explicit label to cause disagreement
        "Financial Earnings: $85,000 per annum",
        "Sum Assured: $300,000",
        "Tobacco Habit: Non-smoker",
        "Alcohol: None",
        "Pre-Existing Conditions: None reported",
        "Family History: Mother had hypertension",
        "Height: 165 cm",
        "Weight: 60 kg",
        "BMI: 22.0",
        "Policy Type: Standard Term",
    ]
    
    y = 710
    for line in text_lines:
        c.drawString(50, y, line)
        y -= 22
        
    c.save()

def create_scanned_pdf(filepath: str):
    # Minimal text line to trigger OCR length < 50 threshold
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica", 8)
    c.drawString(50, 750, "SCAN")
    c.save()

if __name__ == "__main__":
    os.makedirs(FIXTURES_DIR, exist_ok=True)
    create_digital_pdf(os.path.join(FIXTURES_DIR, "sample_digital.pdf"))
    create_disagreement_pdf(os.path.join(FIXTURES_DIR, "sample_disagreement.pdf"))
    create_scanned_pdf(os.path.join(FIXTURES_DIR, "sample_scanned.pdf"))
    print("Fixtures created successfully!")
