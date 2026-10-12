# ResumeLens: Formal Language-Based Resume Screening
## Project Documentation & Formal Specification

**Course Code:** 09772 
**Group Number:** Professor Group 5  
**Team Name:** JMapostles
**Team Members:**  
- Sarah Rodriguez Ardila A00411438
- Heidy Hernandez Huila A00411232
- Maria Camila Salamanca Cortes A00411234

---

## 2. Stage 1: Resume Information Extraction (Regular Expressions)

### **Objective**
Extract relevant textual information from raw résumé text using regular expressions (`re` module in Python). This stage detects candidate contact details, skills, experience, and educational background without evaluating equivalences or job profile matches.

### **Implemented Regular Expressions & Theoretical Pattern Analysis**

1. **Years of Professional Experience (`experience`)**
   * **Pattern:** `r'(\d+\+?\s+years?\s+of\s+experience[^\.\n]*\.)'`
   * **Recognized Language / Pattern:** Matches strings starting with one or more digits (`\d+`), an optional plus sign (`\+?`), whitespace (`\s+`), the keywords *year* or *years*, followed by *of experience* and any remaining character up to a period or newline (`[^\.\n]*\.`).
   * **Purpose:** Isolates explicit statements regarding candidate work experience duration and context.

2. **Technical Skills and Tools (`skills`)**
   * **Pattern:** `r'\b(JS|JavaScript|TypeScript|React\.js|React|Redux|NodeJS|Express\.js|Postgres|PostgreSQL|Git|REST APIs|Python|Pandas|NumPy|Scikit-learn|TensorFlow|SQL|AWS|Docker|Kubernetes|Terraform|Jenkins|Spark|Snowflake|Airflow|Kafka)\b'`
   * **Recognized Language / Pattern:** Defines a closed lexicon bounded by word boundaries (`\b`). Uses alternation (`|`) to match exact technical terms, languages, frameworks, and databases.

3. **Phone Number (`phone`)**
   * **Pattern:** `r'\+?\d{1,3}?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'`
   * **Recognized Language / Pattern:** Recognizes domestic and international phone formats. Allows optional country codes (`\+?`), optional parentheses for area codes, and flexible separators (hyphens, dots, or spaces).

4. **Email Address (`email`)**
   * **Pattern:** `r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'`
   * **Recognized Language / Pattern:** Identifies standard email addresses structured as `user@domain.extension`.

### **Data Output Structure**
Extracted strings are preserved in a structured Python dictionary/JSON to serve as input for Stage 2 (Normalization):

```python
extracted_data = {
    "contact": {
        "email": "mary.jane@example.com",
        "phone": "+1-555-0199"
    },
    "experience_raw": "2 years of experience developing predictive models.",
    "skills_raw": ["JS", "React.js", "NodeJS", "Postgres", "Git"]
}