import streamlit as st

from src.classification.profile_automata import PROFILE_PATTERNS
from src.pipeline import process_resume_pipeline

PROFILE_LABELS = {
    "FULL_STACK": "Full Stack Developer",
    "ML_ENGINEER": "Machine Learning Engineer",
    "DEVOPS_ENGINEER": "DevOps Engineer",
    "DATA_ENGINEER": "Data Engineer",
}

GREEN = "#4E8252"

st.set_page_config(
    page_title="ResumeLens",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- ESTILOS --------------------
st.markdown(
    """
    <style>
    :root {
        --rl-green: #4E8252;
        --rl-dark: #24352A;
        --rl-muted: #718078;
        --rl-border: #E1E9E2;
        --rl-light: #F5F8F5;
    }

    .stApp {
        background: #FBFCFB;
        color: var(--rl-dark);
    }

    [data-testid="stSidebar"] {
        background: #F1F6F1;
        border-right: 1px solid var(--rl-border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    .brand {
        color: var(--rl-dark);
        font-size: 1.65rem;
        font-weight: 750;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    .brand span {
        color: var(--rl-green);
    }

    .eyebrow {
        color: var(--rl-green);
        font-size: .78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .hero-title {
        font-size: 2.6rem;
        line-height: 1.15;
        font-weight: 750;
        letter-spacing: -1.5px;
        color: var(--rl-dark);
        margin-bottom: .35rem;
    }

    .hero-title span {
        color: var(--rl-green);
    }

    .muted {
        color: var(--rl-muted);
        line-height: 1.65;
    }

    .section-heading {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--rl-dark);
        margin-bottom: .2rem;
    }

    .panel {
        background: white;
        border: 1px solid var(--rl-border);
        border-radius: 15px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .metric-label {
        font-size: .82rem;
        color: var(--rl-muted);
        margin-bottom: .4rem;
    }

    .metric-value {
        font-size: 1.45rem;
        font-weight: 750;
        color: var(--rl-dark);
    }

    .stage-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: #E5EFE6;
        color: var(--rl-green);
        font-weight: 750;
        margin-right: .55rem;
    }

    .status {
        border-radius: 10px;
        padding: .85rem 1rem;
        font-weight: 650;
        margin: .7rem 0;
    }

    .status-ok {
        color: #315F37;
        background: #EDF6EE;
        border: 1px solid #D0E5D2;
    }

    .status-no {
        color: #984646;
        background: #FFF1F0;
        border: 1px solid #F1D4D1;
    }

    .small-note {
        font-size: .82rem;
        color: var(--rl-muted);
        line-height: 1.5;
    }

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"] {
        background: var(--rl-green);
        border: 1px solid var(--rl-green);
        color: white;
        border-radius: 9px;
        min-height: 2.8rem;
        font-weight: 650;
    }

    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button[kind="primary"]:hover {
        background: #3E6942;
        border-color: #3E6942;
        color: white;
    }

    div[data-baseweb="select"] > div,
    .stTextArea textarea {
        border-radius: 9px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--rl-border);
        border-radius: 10px;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 1px solid var(--rl-border);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--rl-muted);
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        color: var(--rl-green) !important;
    }

    .footer {
        color: var(--rl-muted);
        font-size: .78rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--rl-border);
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- BARRA LATERAL --------------------
with st.sidebar:
    st.markdown(
        '<p class="brand">Resume<span>Lens</span></p>',
        unsafe_allow_html=True,
    )
    st.caption("Formal Language-Based Resume Screening")
    st.divider()

    st.markdown("### Workflow")

    stages = [
        ("01", "Extract", "Find résumé information using regex."),
        ("02", "Normalize", "Standardize qualifications."),
        ("03", "Classify", "Recognize formal profile patterns."),
        ("04", "Validate", "Grammar validation — coming soon."),
    ]

    for number, title, description in stages:
        st.markdown(
            f"""
            <div style="display:flex; gap:12px; margin:18px 0;">
                <div style="
                    min-width:32px;height:32px;border-radius:50%;
                    display:flex;align-items:center;justify-content:center;
                    background:{'#4E8252' if number != '04' else '#E6ECE6'};
                    color:{'white' if number != '04' else '#718078'};
                    font-weight:700;font-size:.8rem;">
                    {number}
                </div>
                <div>
                    <div style="font-weight:700;color:#24352A">{title}</div>
                    <div style="font-size:.78rem;color:#718078;
                                line-height:1.5">{description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.caption("Built with Python and Streamlit")

# -------------------- ENCABEZADO --------------------
st.markdown(
    """
    <div class="eyebrow">INTELLIGENT RESUME ANALYSIS</div>
    <div class="hero-title">Understand every <span>résumé.</span></div>
    <p class="muted">
        Extract information, normalize qualifications, and recognize
        formal professional-profile patterns.
    </p>
    """,
    unsafe_allow_html=True,
)

st.write("")

# -------------------- FORMULARIO --------------------
with st.container(border=True):
    left, right = st.columns([1.5, 1], gap="large")

    with st.form("resume_form"):
        with left:
            st.markdown("### Upload résumé")
            st.caption(
                "Paste the résumé text or upload a plain-text file."
            )

            uploaded_file = st.file_uploader(
                "Upload a .txt file",
                type=["txt"],
                help="Only plain-text .txt files are supported.",
            )

            resume_input = st.text_area(
                "Résumé content",
                height=220,
                placeholder=(
                    "Paste the résumé text here...\n\n"
                    "Example: Python, JavaScript, React, Node.js..."
                ),
                help="The text is processed by the existing pipeline.",
            )

        with right:
            st.markdown("### Target profile")
            st.caption(
                "Choose the profile whose formal qualification pattern "
                "you want to evaluate."
            )

            selected_profile = st.selectbox(
                "Professional profile",
                options=list(PROFILE_PATTERNS),
                format_func=lambda profile: PROFILE_LABELS[profile],
            )

            st.markdown(
                """
                <div style="
                    background:#F1F6F1;border:1px solid #E1E9E2;
                    padding:14px;border-radius:10px;margin:10px 0 20px;">
                    <div style="font-weight:650;color:#315F37">
                        Profile-based analysis
                    </div>
                    <div style="font-size:.83rem;color:#718078;
                                line-height:1.5;margin-top:5px">
                        The selected profile determines the qualification
                        sequence used for pattern recognition.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            submitted = st.form_submit_button(
                "Analyze résumé  →",
                type="primary",
                use_container_width=True,
            )

# -------------------- PROCESAMIENTO --------------------
if submitted:
    text_to_process = resume_input.strip()

    if uploaded_file is not None:
        try:
            file_text = uploaded_file.getvalue().decode("utf-8-sig").strip()
            if file_text:
                text_to_process = file_text
        except UnicodeDecodeError:
            st.error("The TXT file must use UTF-8 text encoding.")
            st.stop()

    if not text_to_process:
        st.warning("Paste résumé text or upload a TXT file before processing.")
    else:
        try:
            with st.spinner("Analyzing résumé..."):
                result = process_resume_pipeline(
                    text_to_process,
                    profile=selected_profile,
                )
            st.session_state["resume_result"] = result
            st.session_state["resume_profile"] = selected_profile
            st.success("Résumé analysis completed.")
        except Exception as error:
            st.error("The résumé could not be processed.")
            st.exception(error)

# -------------------- RESULTADOS --------------------
if "resume_result" in st.session_state:
    result = st.session_state["resume_result"]
    result_profile = st.session_state["resume_profile"]

    st.write("")
    st.markdown(
        """
        <div class="section-heading">Analysis results</div>
        <p class="muted">
            Explore the information returned by each stage of the pipeline.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Summary metrics
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            f"""
            <div class="panel">
                <div class="metric-label">Candidate</div>
                <div class="metric-value" style="font-size:1.15rem">
                    {result['candidate_name']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            f"""
            <div class="panel">
                <div class="metric-label">Extracted qualifications</div>
                <div class="metric-value">
                    {len(result['extracted_skills'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            f"""
            <div class="panel">
                <div class="metric-label">Normalized qualifications</div>
                <div class="metric-value">
                    {len(result['normalized_skills'])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    extraction_tab, normalization_tab, classification_tab = st.tabs(
        [
            "01  Extraction",
            "02  Normalization",
            "03  Profile recognition",
        ]
    )

    with extraction_tab:
        st.markdown("### Extracted information")

        info_left, info_right = st.columns(2)

        with info_left:
            st.markdown("**Candidate**")
            st.write(result["candidate_name"])
            st.markdown("**Experience**")
            st.write(result["experience"])

        with info_right:
            contact = result["contact_info"]
            st.markdown("**Email**")
            st.write(contact["email"])
            st.markdown("**Phone**")
            st.write(contact["phone"])

        st.markdown("#### Extracted qualifications")

        if result["extracted_skills"]:
            st.dataframe(
                [
                    {"#": index, "Qualification": skill}
                    for index, skill in enumerate(
                        result["extracted_skills"], start=1
                    )
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No supported qualifications were extracted.")

    with normalization_tab:
        st.markdown("### Canonical qualifications")
        st.caption(
            "Qualification variants are normalized and ordered for "
            f"{PROFILE_LABELS[result_profile]}."
        )

        if result["normalized_skills"]:
            st.dataframe(
                [
                    {
                        "Position": index,
                        "Canonical qualification": skill,
                    }
                    for index, skill in enumerate(
                        result["normalized_skills"], start=1
                    )
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("There are no known qualifications to normalize.")

    with classification_tab:
        st.markdown("### Qualification pattern recognition")

        selected_result = result["classification"]

        if selected_result == "ACCEPTED":
            st.markdown(
                f"""
                <div class="status status-ok">
                    ✓ &nbsp; {PROFILE_LABELS[result_profile]}:
                    {selected_result}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="status status-no">
                    ! &nbsp; {PROFILE_LABELS[result_profile]}:
                    {selected_result}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("#### All supported profiles")

        st.dataframe(
            [
                {
                    "Professional profile": PROFILE_LABELS[profile],
                    "Pattern result": profile_result,
                }
                for profile, profile_result
                in result["profile_results"].items()
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "These results indicate whether the qualification sequence "
            "matches a formal pattern. They are not candidate rankings "
            "or hiring decisions."
        )

st.markdown(
    """
    <div class="footer">
        ResumeLens · Formal Language-Based Resume Screening<br>
        Analysis is based on the implemented extraction, normalization,
        and classification pipeline.
    </div>
    """,
    unsafe_allow_html=True,
)
