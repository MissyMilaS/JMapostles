## Configuración de los Escenarios (Etapa 1: Extracción de Información - Expresiones Regulares)

| Nombre | Clase | Escenario |
|--------|------|----------|
| setUp1 | InformationExtractorTest | Texto de CV válido en formato plano estructurado con emails, teléfonos de formato internacional y URLs de perfiles (GitHub/LinkedIn) |
| setUp2 | InformationExtractorTest | Texto de CV con múltiples menciones y variaciones de lenguajes de programación (ej. JS, Javascript, TypeScript, Python) |
| setUp3 | InformationExtractorTest | Texto de CV con menciones de frameworks/librerías frontend y backend en diversos estilos (ej. React.js, ReactJS, NodeJS, Spring Boot, Vue.js) |
| setUp4 | InformationExtractorTest | Texto de CV con motores de bases de datos relacionales y NoSQL (ej. Postgres, PostgreSQL, MySQL, MongoDB) |
| setUp5 | InformationExtractorTest | Texto de CV con librerías y frameworks de Machine Learning e Inteligencia Artificial (ej. Scikit-learn, sklearn, TensorFlow, PyTorch, Pandas, NumPy) |
| setUp6 | InformationExtractorTest | Texto de CV con herramientas de control de versiones, repositorios y DevOps (ej. Git, GitHub, Docker, Kubernetes) |
| setUp7 | InformationExtractorTest | Texto de CV con grados académicos (Bachelor, B.S., Master) y años de experiencia expresados en texto/números |
| setUp8 | InformationExtractorTest | Cadena de texto vacía (`""`) |
| setUp9 | InformationExtractorTest | Texto plano narrativo/ruidoso con palabras comunes sin presencia de habilidades técnicas ni datos de contacto |
| setUp10 | InformationExtractorTest | Texto con calificaciones técnicas pegadas a signos de puntuación o delimitadores (ej. `"JS, React.js; NodeJS/Postgres"`) |

---

## Diseño de Casos de Prueba - InformationExtractor (Etapa 1: Expresiones Regulares)

**Objetivo de la Prueba:** Validar el correcto funcionamiento de los métodos de extracción mediante expresiones regulares (módulo `re` de Python) para capturar la información técnica y de contacto desde el texto plano del currículum.

| Clase | Método | Escenario | Valores de Entrada | Resultado esperado |
|------|--------|----------|-------------------|-------------------|
| InformationExtractorTest | extract_contact_info | setUp1 | `"Contact: wednesday@addams.com \| +1-555-0199 \| github.com/wednesday \| linkedin.com/in/wednesday"` | `{"emails": ["wednesday@addams.com"], "phones": ["+1-555-0199"], "urls": ["github.com/wednesday", "linkedin.com/in/wednesday"]}` |
| InformationExtractorTest | extract_contact_info | setUp8 | `""` | `{"emails": [], "phones": [], "urls": []}` |
| InformationExtractorTest | extract_contact_info | setUp9 | `"Enthusiastic software engineer with strong teamwork abilities."` | `{"emails": [], "phones": [], "urls": []}` |
| InformationExtractorTest | extract_programming_languages | setUp2 | `"Proficient in JS, Javascript, TypeScript, and Python 3.9."` | `["JS", "Javascript", "TypeScript", "Python"]` |
| InformationExtractorTest | extract_programming_languages | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_programming_languages | setUp9 | `"Responsible for daily customer support and project tracking."` | `[]` |
| InformationExtractorTest | extract_frameworks | setUp3 | `"Experience in React.js, ReactJS, NodeJS, Spring Boot and Vue.js."` | `["React.js", "ReactJS", "NodeJS", "Spring Boot", "Vue.js"]` |
| InformationExtractorTest | extract_frameworks | setUp10 | `"Skills: React.js/NodeJS."` | `["React.js", "NodeJS"]` |
| InformationExtractorTest | extract_frameworks | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_databases | setUp4 | `"Worked with Postgres, PostgreSQL, MySQL, and MongoDB databases."` | `["Postgres", "PostgreSQL", "MySQL", "MongoDB"]` |
| InformationExtractorTest | extract_databases | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_databases | setUp9 | `"Managed project schedules and internal communication."` | `[]` |
| InformationExtractorTest | extract_ml_libraries | setUp5 | `"Hands-on with Scikit-learn, sklearn, TensorFlow, PyTorch, Pandas and NumPy."` | `["Scikit-learn", "sklearn", "TensorFlow", "PyTorch", "Pandas", "NumPy"]` |
| InformationExtractorTest | extract_ml_libraries | setUp10 | `"Models developed using Scikit-learn/TensorFlow."` | `["Scikit-learn", "TensorFlow"]` |
| InformationExtractorTest | extract_ml_libraries | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_tools | setUp6 | `"Version control using Git, remote repositories on GitHub, and Docker containers."` | `["Git", "GitHub", "Docker"]` |
| InformationExtractorTest | extract_tools | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_tools | setUp9 | `"Facilitated team sync meetings twice a week."` | `[]` |
| InformationExtractorTest | extract_experience_and_education | setUp7 | `"B.S. in Computer Science. 3 years of experience developing web applications."` | `{"degree": "B.S. in Computer Science", "years_experience": 3}` |
| InformationExtractorTest | extract_experience_and_education | setUp8 | `""` | `{"degree": null, "years_experience": 0}` |
| InformationExtractorTest | extract_all_qualifications | setUp1 | `"Technical Skills: JS, React.js, NodeJS, Postgres, Git."` | `["JS", "React.js", "NodeJS", "Postgres", "Git"]` |
| InformationExtractorTest | extract_all_qualifications | setUp5 | `"Technical Skills: Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git."` | `["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "SQL", "Git"]` |
| InformationExtractorTest | extract_all_qualifications | setUp8 | `""` | `[]` |
| InformationExtractorTest | extract_all_qualifications | setUp9 | `"Good communication, leadership, and proactive problem solving."` | `[]` |
___
## Configuración de los Escenarios (Etapa 2: Normalización y Ordenamiento Canónico - FST)

| Nombre | Clase | Escenario |
|--------|------|----------|
| setUp11 | QualificationNormalizerTest | Lista de calificaciones extraídas con variaciones de nombres de lenguajes de programación (ej. JS, Javascript -> JAVASCRIPT) |
| setUp12 | QualificationNormalizerTest | Lista de calificaciones con variaciones sintácticas de frameworks frontend y backend (ej. React.js, ReactJS -> REACT; NodeJS, Node.js -> NODE_JS) |
| setUp13 | QualificationNormalizerTest | Lista de calificaciones con diferentes formas de nombrar motores de bases de datos (ej. Postgres, PostgreSQL -> POSTGRESQL) |
| setUp14 | QualificationNormalizerTest | Lista de calificaciones con variantes de librerías de Machine Learning (ej. sklearn, scikit learn, Scikit-learn -> SCIKIT_LEARN; Tensor Flow, TensorFlow -> TENSORFLOW) |
| setUp15 | QualificationNormalizerTest | Lista de calificaciones con variaciones de nombres de herramientas de control de versiones y entornos (ej. Git, github -> GIT) |
| setUp16 | QualificationNormalizerTest | Lista de calificaciones con combinaciones mixtas de variaciones válidas de un perfil Full Stack |
| setUp17 | QualificationNormalizerTest | Lista de calificaciones con combinaciones mixtas de variaciones válidas de un perfil Machine Learning Engineer |
| setUp18 | QualificationNormalizerTest | Cadena o lista de entrada vacía (`[]`) recibida desde la etapa de extracción |
| setUp19 | QualificationNormalizerTest | Lista de calificaciones conteniendo símbolos desconocidos o no pertenecientes al alfabeto de entrada $\Sigma$ del transductor |
| setUp20 | QualificationNormalizerTest | Lista de calificaciones desordenadas orientadas al perfil Full Stack Developer (requiere ordenamiento: Frontend -> Backend -> Database -> Version Control) |
| setUp21 | QualificationNormalizerTest | Lista de calificaciones desordenadas orientadas al perfil Machine Learning Engineer (requiere ordenamiento: Language -> Data processing -> ML Framework -> Database -> Version Control) |
| setUp22 | QualificationNormalizerTest | Lista de calificaciones ya ordenada previamente según el orden canónico del perfil objetivo |

---

## Diseño de Casos de Prueba - QualificationNormalizer (Etapa 2: Transductores de Estado Finito)

**Objetivo de la Prueba:** Validar la correcta transformación de variantes textuales a tokens canónicos únicos mediante transductores de estado finito (`pyformlang`) y el posterior ordenamiento de la secuencia según la estructura del perfil seleccionado[cite: 2].

| Clase | Método | Escenario | Valores de Entrada | Resultado esperado |
|------|--------|----------|-------------------|-------------------|
| QualificationNormalizerTest | normalize_qualification | setUp11 | `"JS"` | `"JAVASCRIPT"` |
| QualificationNormalizerTest | normalize_qualification | setUp11 | `"Javascript"` | `"JAVASCRIPT"` |
| QualificationNormalizerTest | normalize_qualification | setUp12 | `"React.js"` | `"REACT"` |
| QualificationNormalizerTest | normalize_qualification | setUp12 | `"ReactJS"` | `"REACT"` |
| QualificationNormalizerTest | normalize_qualification | setUp12 | `"NodeJS"` | `"NODE_JS"` |
| QualificationNormalizerTest | normalize_qualification | setUp12 | `"Node.js"` | `"NODE_JS"` |
| QualificationNormalizerTest | normalize_qualification | setUp13 | `"Postgres"` | `"POSTGRESQL"` |
| QualificationNormalizerTest | normalize_qualification | setUp13 | `"PostgreSQL"` | `"POSTGRESQL"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"sklearn"` | `"SCIKIT_LEARN"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"scikit learn"` | `"SCIKIT_LEARN"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"Scikit-learn"` | `"SCIKIT_LEARN"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"Tensor Flow"` | `"TENSORFLOW"` |
| QualificationNormalizerTest | normalize_qualification | setUp14 | `"TensorFlow"` | `"TENSORFLOW"` |
| QualificationNormalizerTest | normalize_qualification | setUp15 | `"Git"` | `"GIT"` |
| QualificationNormalizerTest | normalize_qualification | setUp19 | `"UnknownTech"` | `UNKNOWN` (O se descarta según regla de diseño) |
| QualificationNormalizerTest | normalize_sequence | setUp16 | `["JS", "React.js", "NodeJS", "Postgres", "Git"]` | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | normalize_sequence | setUp17 | `["Python", "pandas", "sklearn", "TensorFlow", "Postgres", "Git"]` | `["PYTHON", "PANDAS", "SCIKIT_LEARN", "TENSORFLOW", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | normalize_sequence | setUp18 | `[]` | `[]` |
| QualificationNormalizerTest | sort_canonical | setUp20 | `["Git", "NodeJS", "JS", "Postgres", "React.js"]`, `profile="FULL_STACK"` | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | sort_canonical | setUp21 | `["Git", "TensorFlow", "Python", "Pandas", "Postgres"]`, `profile="ML_ENGINEER"` | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | sort_canonical | setUp22 | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]`, `profile="FULL_STACK"` | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` |
| QualificationNormalizerTest | sort_canonical | setUp18 | `[]`, `profile="FULL_STACK"` | `[]` |
___
## Configuración de los Escenarios (Etapa 3: Reconocimiento de Patrones - Autómatas Finitos)

| Nombre | Clase | Escenario |
|--------|------|----------|
| setUp23 | ProfilePatternRecognizerTest | Secuencia canónica ordenada válida para el perfil Full Stack Developer (ej. JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT)[cite: 2] |
| setUp24 | ProfilePatternRecognizerTest | Secuencia canónica ordenada válida para el perfil Machine Learning Engineer (ej. PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, GIT)[cite: 2] |
| setUp25 | ProfilePatternRecognizerTest | Secuencia canónica ordenada válida para el Perfil Adicional 1 - Software Engineering (ej. DevOps / Cloud Engineer: PYTHON, DOCKER, KUBERNETES, AWS, GIT) |
| setUp26 | ProfilePatternRecognizerTest | Secuencia canónica ordenada válida para el Perfil Adicional 2 - AI/Data (ej. Data Engineer: PYTHON, SPARK, AIRFLOW, POSTGRESQL, GIT) |
| setUp27 | ProfilePatternRecognizerTest | Secuencia incompleta para Full Stack Developer a la que le falta el token de Backend o Base de Datos[cite: 2] |
| setUp28 | ProfilePatternRecognizerTest | Secuencia incompleta para Machine Learning Engineer a la que le falta la librería de ML/Data[cite: 2] |
| setUp29 | ProfilePatternRecognizerTest | Secuencia con símbolos fuera del alfabeto $\Sigma$ del autómata de un perfil específico (ej. tokens de ML evaluados en el autómata de Full Stack)[cite: 2] |
| setUp30 | ProfilePatternRecognizerTest | Secuencia que viola el orden canónico estricto requerido por el autómata del perfil |
| setUp31 | ProfilePatternRecognizerTest | Lista de calificaciones canónicas vacía (`[]`)[cite: 2] |
| setUp32 | ProfilePatternRecognizerTest | Evaluación multipromocional: secuencia de candidato válida para ML Engineer probada simultáneamente en los 4 autómatas[cite: 2] |

---

## Diseño de Casos de Prueba - ProfilePatternRecognizer (Etapa 3: Autómatas Finitos)

**Objetivo de la Prueba:** Validar la clasificación de secuencias canónicas mediante autómatas finitos (DFA/NFA en `pyformlang`), verificando que se determine de manera precisa el estado de aceptación (`ACCEPTED`) o rechazo (`REJECTED`) para cada uno de los 4 perfiles profesionales[cite: 2].

| Clase | Método | Escenario | Valores de Entrada | Resultado esperado |
|------|--------|----------|-------------------|-------------------|
| ProfilePatternRecognizerTest | evaluate_full_stack | setUp23 | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]`[cite: 2] | `ACCEPTED`[cite: 2] |
| ProfilePatternRecognizerTest | evaluate_full_stack | setUp27 | `["JAVASCRIPT", "REACT", "GIT"]`[cite: 2] | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_full_stack | setUp29 | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]`[cite: 2] | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_full_stack | setUp31 | `[]`[cite: 2] | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_ml_engineer | setUp24 | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]`[cite: 2] | `ACCEPTED`[cite: 2] |
| ProfilePatternRecognizerTest | evaluate_ml_engineer | setUp28 | `["PYTHON", "POSTGRESQL", "GIT"]`[cite: 2] | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_ml_engineer | setUp29 | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]`[cite: 2] | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_ml_engineer | setUp31 | `[]`[cite: 2] | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_devops_engineer | setUp25 | `["PYTHON", "DOCKER", "KUBERNETES", "AWS", "GIT"]` | `ACCEPTED` |
| ProfilePatternRecognizerTest | evaluate_devops_engineer | setUp23 | `["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_data_engineer | setUp26 | `["PYTHON", "SPARK", "AIRFLOW", "POSTGRESQL", "GIT"]` | `ACCEPTED` |
| ProfilePatternRecognizerTest | evaluate_data_engineer | setUp24 | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]` | `REJECTED` |
| ProfilePatternRecognizerTest | evaluate_all_profiles | setUp32 | `["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]`[cite: 2] | `{"FULL_STACK": "REJECTED", "ML_ENGINEER": "ACCEPTED", "DEVOPS_ENGINEER": "REJECTED", "DATA_ENGINEER": "REJECTED"}`[cite: 2] |
| ProfilePatternRecognizerTest | evaluate_all_profiles | setUp30 | `["REACT", "JAVASCRIPT", "NODE_JS", "POSTGRESQL", "GIT"]` | `{"FULL_STACK": "REJECTED", "ML_ENGINEER": "REJECTED", "DEVOPS_ENGINEER": "REJECTED", "DATA_ENGINEER": "REJECTED"}` |
___
## Configuración de los Escenarios (Etapa 4: Lenguaje de Perfil y DSL - Gramáticas Libres de Contexto con textX)

| Nombre | Clase | Escenario |
|--------|------|----------|
| setUp33 | ProfileDSLParserTest | Archivo de especificación DSL válido que contiene datos personales, experiencia laboral múltiple, habilidades técnicas normalizadas y clasificaciones de perfil aceptadas (ej. FULL_STACK: ACCEPTED, ML_ENGINEER: REJECTED)[cite: 2] |
| setUp34 | ProfileDSLParserTest | Archivo DSL válido para un candidato con múltiples registros de educación, múltiples empleos y varias clasificaciones aceptadas simultáneamente[cite: 2] |
| setUp35 | ProfileDSLParserTest | Archivo DSL inválido por omisión de secciones obligatorias (ej. falta bloque de información de contacto o falta bloque de clasificación de perfil)[cite: 2] |
| setUp36 | ProfileDSLParserTest | Archivo DSL inválido por errores sintácticos/léxicos (ej. comillas sin cerrar, delimitadores incorrectos o palabras clave mal escritas no reconocidas por la gramática textX)[cite: 2] |
| setUp37 | ProfileDSLParserTest | Archivo DSL inválido con tipos de datos inconsistentes (ej. años de experiencia expresados con texto en lugar de un entero numérico requerido)[cite: 2] |
| setUp38 | ProfileDSLParserTest | Generación exitosa de documento de visualización HTML a partir del modelo DSL parseado y validado en `textX`[cite: 2] |
| setUp39 | ProfileDSLParserTest | Generación exitosa de documento de visualización Markdown a partir del modelo DSL parseado y validado en `textX`[cite: 2] |
| setUp40 | ProfileDSLParserTest | Intento de generación de visualización (HTML/Markdown) a partir de una estructura AST/modelo no validado o corrupto |

---

## Diseño de Casos de Prueba - ProfileDSLParser & Renderer (Etapa 4: Context-Free Grammars con textX)

**Objetivo de la Prueba:** Validar el parsing sintáctico y léxico del lenguaje de dominio específico (DSL) mediante gramáticas libres de contexto en `textX`, la correcta detección de errores en especificaciones inválidas y la generación fiel de archivos de visualización en HTML/Markdown[cite: 2].

| Clase | Método | Escenario | Valores de Entrada | Resultado esperado |
|------|--------|----------|-------------------|-------------------|
| ProfileDSLParserTest | parse_dsl_string | setUp33 | Cadena DSL bien estructurada con candidato "Wednesday Addams", 3 años exp., habilidades normalizadas y clasificación `FULL_STACK: ACCEPTED`[cite: 2] | Objeto modelo `CandidateProfile` instanciado correctamente sin errores |
| ProfileDSLParserTest | parse_dsl_string | setUp34 | Cadena DSL completa con 2 experiencias laborales, B.S. en CS, e ítems normalizados con clasificaciones múltiples válidas[cite: 2] | Objeto modelo `CandidateProfile` con listas de `experience` y `evaluations` correctamente pobladas[cite: 2] |
| ProfileDSLParserTest | parse_dsl_string | setUp35 | Cadena DSL donde falta la sección obligatoria `evaluations`[cite: 2] | Lanza `TextXSyntaxError` indicando elemento obligatorio faltante[cite: 2] |
| ProfileDSLParserTest | parse_dsl_string | setUp36 | Cadena DSL con clave errónea `"CandidateProfile_BadSyntax { ... }"` | Lanza `TextXSyntaxError` por regla no reconocida |
| ProfileDSLParserTest | parse_dsl_string | setUp37 | Cadena DSL con `experience_years = "tres"` (se esperaba valor entero) | Lanza `TextXSemanticError` o `TextXSyntaxError` por tipo de dato inválido |
| ProfileDSLParserTest | generate_html_visualization | setUp38 | Objeto modelo `CandidateProfile` procesado válidamente desde `setUp33`[cite: 2] | Genera archivo `wednesday_addams_profile.html` válido que contiene las etiquetas HTML de resumen y estado `ACCEPTED`[cite: 2] |
| ProfileDSLParserTest | generate_markdown_visualization | setUp39 | Objeto modelo `CandidateProfile` procesado válidamente desde `setUp34`[cite: 2] | Genera archivo `mary_jane_profile.md` estructurado con tablas/listas Markdown del candidato[cite: 2] |
| ProfileDSLParserTest | generate_html_visualization | setUp40 | `None` o modelo DSL no parseado | Lanza excepción `ValueError` o `AttributeError` impidiendo la generación de salida |