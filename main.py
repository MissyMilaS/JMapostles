
import streamlit as st
import pandas as pd
from textx.exceptions import TextXSemanticError, TextXSyntaxError

from src.dsl.specification import generate_candidate_profile
from src.pipeline import process_resume_pipeline

from src.classification.profile_automata import PROFILE_PATTERNS
from src.pipeline import process_resume_pipeline


# =========================================================
# CONFIGURACIÓN
# =========================================================

GREEN = "#4E8252"
DARK_GREEN = "#365C3A"
DARK = "#26352A"
MUTED = "#6F7D72"
BORDER = "#E1E8E1"
LIGHT_GREEN = "#F1F6F1"
WHITE = "#FFFFFF"

PROFILE_LABELS = {
    "FULL_STACK": "Full Stack Developer",
    "ML_ENGINEER": "Machine Learning Engineer",
    "DEVOPS_ENGINEER": "DevOps Engineer",
    "DATA_ENGINEER": "Data Engineer",
}

st.set_page_config(
    page_title="ResumeLens",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# ESTILOS VISUALES
# =========================================================

st.markdown(
    f"""
    <style>
    /* Fondo y tipografía general */
    .stApp {{
        background-color: #FBFCFB;
        color: {DARK};
    }}

    [data-testid="stHeader"] {{
        background-color: #FBFCFB;
    }}

    .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }}

    /* Barra lateral */
    [data-testid="stSidebar"] {{
        background-color: {LIGHT_GREEN};
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {{
        color: {DARK};
    }}

    .brand {{
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: {DARK};
        margin-bottom: 0;
    }}

    .brand span {{
        color: {GREEN};
    }}

    .sidebar-caption {{
        font-size: 0.8rem;
        color: {MUTED};
        line-height: 1.5;
    }}

    /* Encabezado principal */
    .eyebrow {{
        color: {GREEN};
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 1.8px;
        margin-bottom: 0.6rem;
    }}

    .hero-title {{
        color: {DARK};
        font-size: clamp(2rem, 4vw, 3rem);
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.15;
        margin-bottom: 0.7rem;
    }}

    .hero-title span {{
        color: {GREEN};
    }}

    .hero-description {{
        color: {MUTED};
        font-size: 1rem;
        line-height: 1.7;
        max-width: 780px;
    }}

    /* Títulos y textos */
    h2, h3 {{
        color: {DARK};
    }}

    [data-testid="stMarkdownContainer"] p {{
        color: {DARK};
    }}

    .section-description {{
        color: {MUTED};
        font-size: 0.9rem;
        line-height: 1.6;
    }}

    /* Campos de entrada: tema claro */
    .stTextArea textarea,
    .stTextInput input {{
        background-color: {WHITE} !important;
        color: {DARK} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 10px !important;
    }}

    .stTextArea textarea::placeholder {{
        color: #8A968C !important;
    }}

    div[data-baseweb="select"] > div {{
        background-color: {WHITE} !important;
        color: {DARK} !important;
        border-color: {BORDER} !important;
        border-radius: 10px !important;
    }}

    /* Área de carga */
    [data-testid="stFileUploader"] section {{
        background-color: {WHITE} !important;
        border: 1px dashed #B9CDBA !important;
        border-radius: 10px !important;
    }}

    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] section * {{
        color: {DARK} !important;
    }}

    /* Botones */
    .stFormSubmitButton button,
    .stButton button {{
        border-radius: 9px !important;
        font-weight: 650 !important;
        min-height: 2.7rem;
    }}

    .stFormSubmitButton button[kind="primary"],
    .stButton button[kind="primary"] {{
        background-color: {GREEN} !important;
        border: 1px solid {GREEN} !important;
        color: #FFFFFF !important;
    }}

    .stFormSubmitButton button[kind="primary"]:hover,
    .stButton button[kind="primary"]:hover {{
        background-color: {DARK_GREEN} !important;
        border-color: {DARK_GREEN} !important;
        color: #FFFFFF !important;
    }}

    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        border-bottom: 1px solid {BORDER};
    }}

    if run_btn:
        if not resume_input.strip():
            st.warning("Please enter valid resume text.")
        else:
            result = process_resume_pipeline(resume_input)
    .stTabs [data-baseweb="tab"] {{
        color: {MUTED};
        font-weight: 600;
    }}

    .stTabs [aria-selected="true"] {{
        color: {GREEN} !important;
    }}

    /* Tablas */
    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
        overflow: hidden;
    }}

    /* Mensajes y pie de página */
    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}

    .footer {{
        margin-top: 2.5rem;
        padding-top: 1.2rem;
        border-top: 1px solid {BORDER};
        color: {MUTED};
        font-size: 0.8rem;
        line-height: 1.7;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# BARRA LATERAL
# =========================================================

with st.sidebar:
    st.markdown(
        '<p class="brand">Resume<span>Lens</span></p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="sidebar-caption">'
        "Formal Language-Based Resume Screening"
        "</p>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### Workflow")

    stages = [
        ("01", "Extraction", "Find resume information."),
        ("02", "Normalization", "Standardize qualifications."),
        ("03", "Classification", "Recognize profile patterns."),
        ("04", "Validation", "Grammar validation pending."),
    ]

    for number, title, description in stages:
        if number == "04":
            circle_background = "#E1E9E1"
            circle_color = MUTED
        else:
            circle_background = GREEN
            circle_color = WHITE

        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:flex-start;
                gap:12px;
                margin:20px 0;
            ">
                <div style="
                    min-width:34px;
                    height:34px;
                    border-radius:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:{circle_background};
                    color:{circle_color};
                    font-weight:750;
                    font-size:0.8rem;
                ">{number}</div>
                <div>
                    <div style="
                        font-weight:700;
                        color:{DARK};
                        margin:2px 0 5px;
                    ">{title}</div>
                    <div style="
                        font-size:0.78rem;
                        color:{MUTED};
                        line-height:1.5;
                    ">{description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        '<p class="sidebar-caption">'
        "Powered by Python and Streamlit."
        "</p>",
        unsafe_allow_html=True,
    )


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    """
    <div class="eyebrow">INTELLIGENT RESUME ANALYSIS</div>
    <div class="hero-title">
        Understand every <span>resume.</span>
    </div>
    <div class="hero-description">
        Extract information, normalize qualifications, and recognize
        formal professional-profile patterns through a structured pipeline.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# =========================================================
# FORMULARIO
# IMPORTANTE: el botón debe permanecer dentro de st.form()
# =========================================================

with st.container(border=True):
    with st.form("resume_form"):
        left, right = st.columns([1.45, 1], gap="large")

        with left:
            st.markdown("### Upload resume")

            st.markdown(
                '<p class="section-description">'
                "Upload a TXT file or paste the resume content below."
                "</p>",
                unsafe_allow_html=True,
            )

            uploaded_file = st.file_uploader(
                "Upload a .txt file",
                type=["txt"],
                help="Only plain-text TXT files are supported.",
            )

            resume_input = st.text_area(
                "RResume content",
                height=220,
                placeholder=(
                    "Paste the resume text here...\n\n"
                    "Example: Python, JavaScript, React, Node.js..."
                ),
                help=(
                    "The content will be processed by the "
                    "extraction, normalization, and classification stages."
                ),
            )

            tab_summary, tab_skills, tab_stage4 = st.tabs(
                ["Extracted Summary", "Technical Skills", "Stage 4 DSL & Report"]
            )

            with tab_summary:
                st.markdown(f"**Candidate:** {result['candidate_name']}")
                st.markdown(f"**Experience:** {result['experience']}")
                st.markdown("**Generated summary (Short CV):**")
                st.code(
                    f"{result['candidate_name']} | {result['experience']} | "
                    f"Technical Skills: {', '.join(result['extracted_skills']) or 'None identified'}.",
                    language="text",
                )
                st.markdown("**Profile classification:**")
                st.json(result["profile_results"])

            with tab_skills:
                st.markdown("**Identified technical skills:**")
                skills_list = result["extracted_skills"]
        with right:
            st.markdown("### Target profile")

            st.markdown(
                '<p class="section-description">'
                "Select the professional profile whose qualification "
                "pattern you want to evaluate."
                "</p>",
                unsafe_allow_html=True,
            )

            selected_profile = st.selectbox(
                "Professional profile",
                options=list(PROFILE_PATTERNS),
                format_func=lambda profile: PROFILE_LABELS[profile],
            )

            st.write("")

            st.info(
                "The selected profile determines the qualification "
                "sequence used for pattern recognition."
            )

            st.write("")

            submitted = st.form_submit_button(
                "Analyze resume  →",
                type="primary",
                use_container_width=True,
            )


# =========================================================
# PROCESAMIENTO
# =========================================================

if submitted:
    text_to_process = resume_input.strip()

    # Si se adjunta un TXT válido con contenido, se usa ese texto.
    if uploaded_file is not None:
        try:
            file_text = uploaded_file.getvalue().decode("utf-8-sig").strip()

            if file_text:
                text_to_process = file_text
            else:
                st.warning(
                    "The uploaded TXT file is empty. "
                    "Please provide resume content."
                )
                st.stop()

        except UnicodeDecodeError:
            st.error(
                "The TXT file could not be decoded as UTF-8. "
                "Please save it using UTF-8 encoding and try again."
            )
            st.stop()

    if not text_to_process:
        st.warning(
            "Enter resume text or upload a TXT file before processing."
        )
    else:
        try:
            with st.spinner("Analyzing resume..."):
                result = process_resume_pipeline(
                    text_to_process,
                    profile=selected_profile,
                )

            st.session_state["resume_result"] = result
            st.session_state["resume_profile"] = selected_profile

            st.success("Resume analysis completed successfully.")

        except Exception:
            st.error(
                "The resume could not be processed. "
                "Check the terminal for the technical error details."
            )
            st.exception(__import__("sys").exc_info()[1])


# =========================================================
# RESULTADOS
# =========================================================

if "resume_result" in st.session_state:
    result = st.session_state["resume_result"]
    result_profile = st.session_state["resume_profile"]

    st.write("")
    st.markdown("## Analysis results")

    st.markdown(
        '<p class="section-description">'
        "Review the information returned by each stage of the pipeline."
        "</p>",
        unsafe_allow_html=True,
    )

    # -------------------- RESUMEN --------------------

    metric1, metric2, metric3 = st.columns(3, gap="medium")

    with metric1:
        with st.container(border=True):
            st.caption("Candidate")
            st.markdown(f"**{result['candidate_name']}**")

    with metric2:
        with st.container(border=True):
            st.caption("Extracted qualifications")
            st.markdown(f"## {len(result['extracted_skills'])}")

    with metric3:
        with st.container(border=True):
            st.caption("Normalized qualifications")
            st.markdown(f"## {len(result['normalized_skills'])}")

    st.write("")

    # -------------------- PESTAÑAS --------------------

    extraction_tab, normalization_tab, classification_tab = st.tabs(
        [
            "01 · Extraction",
            "02 · Normalization",
            "03 · Profile recognition",
        ]
    )

    # =====================================================
    # ETAPA 1: EXTRACCIÓN
    # =====================================================

    with extraction_tab:
        st.subheader("Extracted information")

        info_left, info_right = st.columns(2, gap="large")

        with info_left:
            st.markdown("**Candidate**")
            st.write(result["candidate_name"])

            st.markdown("**Experience**")
            st.write(result["experience"])

        with info_right:
            contact_info = result["contact_info"]

            st.markdown("**Email**")
            st.write(contact_info["email"])

            st.markdown("**Phone**")
            st.write(contact_info["phone"])

        st.divider()
        st.markdown("#### Extracted qualifications")

        if result["extracted_skills"]:
            st.dataframe(
                [
                    {
                        "No.": index,
                        "Qualification": skill,
                    }
                    for index, skill in enumerate(
                        result["extracted_skills"],
                        start=1,
                    )
                else:
                    st.warning("No technical skills were identified by the `skills` " "regular expression.")

            with tab_stage4:
                try:
                    artifacts = generate_candidate_profile(result, "data/processed")
                except (TextXSemanticError, TextXSyntaxError) as error:
                    st.error(f"Stage 4 rejected the candidate profile: {error}")
                else:
                    st.success("The candidate profile passed DSL validation.")
                    st.download_button(
                        "Download Resume specification",
                        data=artifacts["dsl"],
                        file_name=artifacts["specification_path"].name,
                        mime="text/plain",
                    )
                    html_report = artifacts["html_path"].read_text(encoding="utf-8")
                    st.download_button(
                        "Download HTML visualization",
                        data=html_report,
                        file_name=artifacts["html_path"].name,
                        mime="text/html",
                    )
                    st.components.v1.html(html_report, height=700, scrolling=True)
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No supported qualifications were extracted.")

    # =====================================================
    # ETAPA 2: NORMALIZACIÓN
    # =====================================================

    with normalization_tab:
        st.subheader("Canonical qualifications")

        st.markdown(
            '<p class="section-description">'
            "Qualifications are standardized and ordered for "
            f"{PROFILE_LABELS[result_profile]}."
            "</p>",
            unsafe_allow_html=True,
        )

        if result["normalized_skills"]:
            st.dataframe(
                [
                    {
                        "Position": index,
                        "Canonical qualification": skill,
                    }
                    for index, skill in enumerate(
                        result["normalized_skills"],
                        start=1,
                    )
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("There are no known qualifications to normalize.")

    # =====================================================
    # ETAPA 3: CLASIFICACIÓN
    # =====================================================

    with classification_tab:
        st.subheader("Qualification pattern recognition")

        selected_result = result["classification"]

        if selected_result == "ACCEPTED":
            st.success(
                f"{PROFILE_LABELS[result_profile]} pattern: "
                f"{selected_result}"
            )
        else:
            st.warning(
                f"{PROFILE_LABELS[result_profile]} pattern: "
                f"{selected_result}"
            )

        st.markdown("#### Results for all supported profiles")

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
            "A result indicates whether the qualification sequence "
            "matches a formal pattern. It is not a candidate ranking "
            "or a hiring decision."
        )
