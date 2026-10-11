import streamlit as st
import pandas as pd
from textx.exceptions import TextXSemanticError, TextXSyntaxError

from src.dsl.specification import generate_candidate_profile
from src.pipeline import process_resume_pipeline

st.set_page_config(page_title="ResumeLens - Extraction", layout="wide")

st.title("ResumeLens: Formal Language-Based Resume Screening")
st.subheader("Resume Information Extraction")
st.divider()

# Two-column layout
col_left, col_right = st.columns([1, 1], gap="large")

# User input (left column)
with col_left:
    st.markdown("### Resume Input Text")

    resume_input = st.text_area(label="Resume content:",value="",height=220,help="Candidate text to process using regular expressions.")

    run_btn = st.button("Run Extraction", type="primary", use_container_width=True)

# Processing and results (right column)
with col_right:
    st.markdown("### Extracted Information")

    if run_btn:
        if not resume_input.strip():
            st.warning("Please enter valid resume text.")
        else:
            result = process_resume_pipeline(resume_input)

            st.success(f"Extraction successful for **{result['candidate_name']}**")

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

                if skills_list:
                    st.code(" | ".join(skills_list), language="text")

                    skills_table = pd.DataFrame({"Skill": skills_list})
                    st.dataframe(
                        skills_table, use_container_width=True, hide_index=True
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
