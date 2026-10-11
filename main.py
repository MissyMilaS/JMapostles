import streamlit as st
import pandas as pd

from src.extraction.regex_extractor import process_resume_to_short_cv

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

    if run_btn or resume_input:
        if not resume_input.strip():
            st.warning("Please enter valid resume text.")
        else:
            result = process_resume_to_short_cv(resume_input)

            st.success(f"Extraction successful for **{result['candidate_name']}**")

            tab_summary, tab_skills = st.tabs(["Extracted Summary", "Technical Skills"])

            with tab_summary:
                st.markdown(f"**Candidate:** {result['candidate_name']}")
                st.markdown(f"**Experience:** {result['experience']}")
                st.markdown("**Generated summary (Short CV):**")
                st.code(result["short_cv_text"], language="text")

            with tab_skills:
                st.markdown("**Identified technical skills:**")
                skills_list = result["raw_skills"]

                if skills_list:
                    st.code(" | ".join(skills_list), language="text")

                    skills_table = pd.DataFrame({"Skill": skills_list})
                    st.dataframe(
                        skills_table, use_container_width=True, hide_index=True
                    )
                else:
                    st.warning("No technical skills were identified by the `skills` " "regular expression.")
