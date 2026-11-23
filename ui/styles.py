CUSTOM_CSS = """
<style>
/* Modern Inter Font & Minimal Global Layout */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1e293b;
}

/* Minimal Header */
.main-header {
    padding: 0.5rem 0 1.2rem 0;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
}

.main-header h1 {
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0;
    color: #0f172a;
    letter-spacing: -0.02em;
}

.main-header p {
    margin-top: 0.25rem;
    color: #64748b;
    font-size: 0.88rem;
}

/* Section Header */
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0f172a;
    margin: 1.2rem 0 0.8rem 0;
}

/* Minimal Staged Stepper Bar */
.stepper-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #f8fafc;
    border: 1px solid #f1f5f9;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 1.5rem;
    overflow-x: auto;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    font-weight: 500;
    color: #64748b;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
}

.step-item.running {
    background: #eff6ff;
    color: #2563eb;
    font-weight: 600;
}

.step-item.done {
    color: #059669;
}

.step-item.failed {
    color: #dc2626;
}

.step-icon {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    background: #cbd5e1;
    color: white;
}

.step-item.running .step-icon { background: #2563eb; }
.step-item.done .step-icon { background: #10b981; }
.step-item.failed .step-icon { background: #ef4444; }

/* Minimal Risk Cards */
.risk-card {
    background: #ffffff;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #cbd5e1;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.8rem;
}

.risk-card.High { border-left-color: #ef4444; }
.risk-card.Medium { border-left-color: #f59e0b; }
.risk-card.Low { border-left-color: #10b981; }

.badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
}

.badge-high { background: #fef2f2; color: #991b1b; }
.badge-medium { background: #fffbeb; color: #92400e; }
.badge-low { background: #ecfdf5; color: #065f46; }
.badge-disputed { background: #f3e8ff; color: #6b21a8; }
.badge-missing { background: #ffedd5; color: #9a3412; }

/* Minimal Recommendation Banner */
.recommendation-card {
    background: #0f172a;
    color: #f8fafc;
    padding: 1.1rem 1.3rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
}

.recommendation-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #38bdf8;
}

/* Quote Box */
.evidence-quote {
    background: #f8fafc;
    border-left: 3px solid #94a3b8;
    padding: 0.5rem 0.8rem;
    font-size: 0.85rem;
    color: #334155;
    margin-top: 0.4rem;
    border-radius: 0 4px 4px 0;
}
</style>
"""
