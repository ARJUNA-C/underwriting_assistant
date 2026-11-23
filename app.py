import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Set page config as the very first Streamlit call
st.set_page_config(
    page_title="AI Health Underwriting Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from ui.styles import CUSTOM_CSS
from ui.components import (
    render_header,
    render_profile_card,
    render_risk_cards,
    render_gap_cards,
    render_summary_card,
    render_download_button,
)
from models.schema import PipelineResult
from pipeline.orchestrator import run_pipeline_streaming

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Session state initialization
if "stage_status" not in st.session_state:
    st.session_state["stage_status"] = {
        "extraction": "pending",
        "profile": "pending",
        "risks": "pending",
        "gaps": "pending",
        "summary": "pending",
        "safety_net": "pending",
    }

if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None

if "uploaded_filename" not in st.session_state:
    st.session_state["uploaded_filename"] = None

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Document Ingest")
    uploaded_file = st.file_uploader("Upload Proposal Form (PDF)", type=["pdf"])
    st.caption("ℹ️ **Advisory Only**: Provides risk assessment & missing field signals. Does NOT approve, reject, or score applications.")

# Header
render_header()

async def execute_pipeline_async(pdf_bytes: bytes, filename: str):
    stage_status = {k: "pending" for k in st.session_state["stage_status"]}
    st.session_state["stage_status"] = stage_status
    pipeline_res = None

    async for update in run_pipeline_streaming(pdf_bytes, filename):
        stage_status[update.stage] = update.status
        st.session_state["stage_status"] = stage_status

        if update.data and "pipeline_result" in update.data:
            pipeline_res = PipelineResult.model_validate(update.data["pipeline_result"])

    if pipeline_res:
        st.session_state["pipeline_result"] = pipeline_res

def run_pipeline_sync(pdf_bytes: bytes, filename: str):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, execute_pipeline_async(pdf_bytes, filename))
            future.result()
    else:
        asyncio.run(execute_pipeline_async(pdf_bytes, filename))

if uploaded_file is not None:
    filename = uploaded_file.name
    
    # If a new file is uploaded, run analysis
    if st.session_state["uploaded_filename"] != filename or st.session_state["pipeline_result"] is None:
        if not os.getenv("GROQ_API_KEY"):
            st.error("Please enter a valid GROQ_API_KEY in the sidebar or environment to run the AI analysis pipeline.")
        else:
            pdf_bytes = uploaded_file.read()
            st.session_state["uploaded_filename"] = filename
            
            with st.spinner("Processing PDF through staged underwriting pipeline..."):
                try:
                    run_pipeline_sync(pdf_bytes, filename)
                    st.success("Pipeline execution completed successfully!")
                except Exception as e:
                    st.error(f"Error running underwriting pipeline: {e}")

# Render Results Dashboard if available
result: PipelineResult = st.session_state.get("pipeline_result")
if result:
    st.markdown("---")
    
    # Top Bar Download & Extraction Meta
    meta_col1, meta_col2 = st.columns([3, 1])
    with meta_col1:
        st.caption(
            f"📄 **Document**: {result.filename} | "
            f"**Pages**: {result.extraction_meta.page_count} | "
            f"**Extraction Source**: {result.extraction_meta.source.upper()} "
            f"{'(OCR fallback triggered)' if result.extraction_meta.source == 'ocr' else ''}"
        )
    with meta_col2:
        render_download_button(result)

    # Executive Summary & Recommendation
    render_summary_card(result.summary, result.safety_check)

    # Tabs for Profile, Risks, Gaps
    tab_profile, tab_risks, tab_gaps = st.tabs(["👤 Profile Data", "⚠️ Risk Factors", "🔍 Missing Info & Gaps"])
    
    with tab_profile:
        render_profile_card(result.profile)
        
    with tab_risks:
        render_risk_cards(result.risks)
        
    with tab_gaps:
        render_gap_cards(result.gaps)

else:
    if uploaded_file is None:
        st.info("👈 Upload a proposal PDF form in the sidebar to begin automated underwriting analysis.")
