# Regular Expressions Explanation for ResumeLens

Below is a detailed, step-by-step breakdown of each regular expression used in the information extraction stage of the **ResumeLens** project.

---

## 1. Work Experience (`experience`)

```regex
(\d+\+?\s+years?\s+of\s+experience[^\.\n]*\.)
```

This regular expression is designed to capture full sentences or fragments indicating a candidate's years of experience in their résumé (e.g., `"3 years of experience developing web applications."`).

### **Step-by-Step Breakdown:**

* `(` ... `)`: **Primary Capturing Group**. Groups the entire matching phrase or sentence for extraction.
* `\d+`: Matches one or more numerical digits ($0-9$). Represents the number of years (e.g., `3`, `10`).
* `\+?`: Matches the literal `+` symbol optionally ($0$ or $1$ time). Useful for patterns like `"5+ years"`.
* `\s+`: Matches one or more whitespace characters (spaces, tabs, newlines).
* `years?`: Matches the word `"year"` or `"years"`. The `s?` makes the letter 's' optional to support both singular and plural forms (e.g., `"1 year"` or `"3 years"`).
* `\s+of\s+experience`: Matches the literal text `" of experience"`, enforcing single/multiple space separators.
* `[^\.\n]*`: **Negated Character Class**. Matches any character that is **NOT** a period (`.`) or a newline (`\n`), repeated $0$ or more times. This consumes the rest of the sentence describing the candidate's responsibilities/skills until it reaches a period or end-of-line.
* `\.`: Escapes the dot character to match a literal period (`.`), marking the end of the sentence.

---

## 2. Technical Skills (`skills`)

```regex
\b(JS|JavaScript|TypeScript|React\.js|React|Redux|NodeJS|Express\.js|Postgres|PostgreSQL|Git|REST APIs|Python|Pandas|NumPy|Scikit-learn|TensorFlow|SQL|AWS|Docker|Kubernetes|Terraform|Jenkins|Spark|Snowflake|Airflow|Kafka)\b
```

This regular expression extracts specific keywords corresponding to programming languages, libraries, frameworks, and technical tools.

### **Step-by-Step Breakdown:**

* `\b`: **Word Boundary**. Ensures that the match is an isolated word and not part of a larger word (e.g., prevents matching `"JS"` inside `"JSON"`).
* `(` ... `)`: **Alternation Group**. Contains options separated by the `|` (logical OR) operator.
* `JS | JavaScript | TypeScript | ...`: Each term separated by `|` represents an independent keyword option to match.
* `React\.js` / `Express\.js`: The period (`.`) is escaped with a backslash `\.` to match a literal dot rather than acting as a wildcard character (which matches any character).
* `\b`: Trailing word boundary to ensure the match ends cleanly at a word edge.

---

## 3. Phone Number (`phone`)

```regex
\+?\d{1,3}?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}
```

This regular expression identifies telephone numbers across various international and local formats (e.g., `+1-123-456-7890`, `(601) 456 7890`, `3101234567`).

### **Step-by-Step Breakdown:**

* `\+?`: Optionally matches a leading `+` sign for international country codes.
* `\d{1,3}?`: Matches between 1 and 3 digits for the country code. The trailing `?` makes it non-greedy (lazy) so it doesn't consume extra digits belonging to the local number.
* `[-.\s]?`: Matches an optional delimiter (hyphen `-`, dot `.`, or space `\s`).
* `\(?`: Matches an optional opening parenthesis `(`.
* `\d{2,4}`: Matches between 2 and 4 digits (area code or local prefix).
* `\)?`: Matches an optional closing parenthesis `)`.
* `[-.\s]?`: Matches an optional delimiter (hyphen, dot, or space).
* `\d{3,4}`: Matches the first block of the local subscriber number (3 to 4 digits).
* `[-.\s]?`: Matches an optional final delimiter.
* `\d{3,4}`: Matches the second block of the local subscriber number (3 to 4 digits).

---

## 4. Email Address (`email`)

```regex
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

This regular expression extracts standard email addresses (e.g., `user.name+tag@domain.co`).

### **Step-by-Step Breakdown:**

* `[a-zA-Z0-9._%+-]+`: **Local Part / Username**.
  * `a-zA-Z`: Uppercase and lowercase ASCII letters.
  * `0-9`: Digits 0 through 9.
  * `._%+-`: Allowed special characters in email usernames.
  * `+`: Requires one or more of these characters.
* `@`: Literal `@` symbol separating the local username from the domain.
* `[a-zA-Z0-9.-]+`: **Domain Name**.
  * Allows letters, numbers, hyphens, and dots (for subdomains like `sub.domain`).
  * `+`: Requires one or more valid domain characters.
* `\.`: Escaped literal period separating the domain name from the top-level domain (TLD).
* `[a-zA-Z]{2,}`: **Top-Level Domain (TLD)** (e.g., `com`, `org`, `edu`, `co`).
  * Accepts uppercase and lowercase letters.
  * `{2,}`: Mandates a minimum length of 2 characters with no upper limit.