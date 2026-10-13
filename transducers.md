```mermaid
flowchart LR
    %% JAVASCRIPT
    js_q0((q0)) -->|"j / ε"| js_q1((q1))
    js_q1 -->|"s / ε"| js_q2((q2))
    js_q2 -->|"ε / JAVASCRIPT"| qf(((qf)))
    js_q2 -->|"a / ε"| js_q3((q3))
    js_q3 -->|"v / ε"| js_q4((q4))
    js_q4 -->|"a / ε"| js_q5((q5))
    js_q5 -->|"s / ε"| js_q6((q6))
    js_q6 -->|"c / ε"| js_q7((q7))
    js_q7 -->|"r / ε"| js_q8((q8))
    js_q8 -->|"i / ε"| js_q9((q9))
    js_q9 -->|"p / ε"| js_q10((q10))
    js_q10 -->|"t / ε"| js_q11((q11))
    js_q11 -->|"ε / JAVASCRIPT"| qf

    %% TYPESCRIPT
    ts_q0((q0)) -->|"t / ε"| ts_q1((q1))
    ts_q1 -->|"s / ε"| ts_q2((q2))
    ts_q2 -->|"ε / TYPESCRIPT"| qf
    ts_q1 -->|"y / ε"| ts_q3((q3))
    ts_q3 -->|"p / ε"| ts_q4((q4))
    ts_q4 -->|"e / ε"| ts_q5((q5))
    ts_q5 -->|"s / ε"| ts_q6((q6))
    ts_q6 -->|"c / ε"| ts_q7((q7))
    ts_q7 -->|"r / ε"| ts_q8((q8))
    ts_q8 -->|"i / ε"| ts_q9((q9))
    ts_q9 -->|"p / ε"| ts_q10((q10))
    ts_q10 -->|"t / ε"| ts_q11((q11))
    ts_q11 -->|"ε / TYPESCRIPT"| qf

    %% REACT
    react_q0((q0)) -->|"r / ε"| react_q1((q1))
    react_q1 -->|"e / ε"| react_q2((q2))
    react_q2 -->|"a / ε"| react_q3((q3))
    react_q3 -->|"c / ε"| react_q4((q4))
    react_q4 -->|"t / ε"| react_q5((q5))
    react_q5 -->|"ε / REACT"| qf
    react_q5 -->|"."| react_q6((q6))
    react_q6 -->|"j / ε"| react_q7((q7))
    react_q7 -->|"s / ε"| react_q8((q8))
    react_q8 -->|"ε / REACT"| qf
    react_q5 -->|"j / ε"| react_q9((q9))
    react_q9 -->|"s / ε"| react_q10((q10))
    react_q10 -->|"ε / REACT"| qf

    %% NODE_JS
    node_q0((q0)) -->|"n / ε"| node_q1((q1))
    node_q1 -->|"o / ε"| node_q2((q2))
    node_q2 -->|"d / ε"| node_q3((q3))
    node_q3 -->|"e / ε"| node_q4((q4))
    node_q4 -->|"ε / NODE_JS"| qf
    node_q4 -->|"j / ε"| node_q5((q5))
    node_q5 -->|"s / ε"| node_q6((q6))
    node_q6 -->|"ε / NODE_JS"| qf
    node_q4 -->|"."| node_q7((q7))
    node_q7 -->|"j / ε"| node_q8((q8))
    node_q8 -->|"s / ε"| qf
    node_q4 -->|"␠ / ε"| node_q9((q9))
    node_q9 -->|"j / ε"| node_q10((q10))
    node_q10 -->|"s / ε"| qf
    node_q4 -->|"_"| node_q11((q11))
    node_q11 -->|"j / ε"| node_q12((q12))
    node_q12 -->|"s / ε"| qf

    %% POSTGRESQL
    pg_q0((q0)) -->|"p / ε"| pg_q1((q1))
    pg_q1 -->|"o / ε"| pg_q2((q2))
    pg_q2 -->|"s / ε"| pg_q3((q3))
    pg_q3 -->|"t / ε"| pg_q4((q4))
    pg_q4 -->|"g / ε"| pg_q5((q5))
    pg_q5 -->|"r / ε"| pg_q6((q6))
    pg_q6 -->|"e / ε"| pg_q7((q7))
    pg_q7 -->|"s / ε"| pg_q8((q8))
    pg_q8 -->|"ε / POSTGRESQL"| qf
    pg_q8 -->|"q / ε"| pg_q9((q9))
    pg_q9 -->|"l / ε"| pg_q10((q10))
    pg_q10 -->|"ε / POSTGRESQL"| qf

    %% SCIKIT_LEARN
    skl_q0((q0)) -->|"s / ε"| skl_q1((q1))
    skl_q1 -->|"k / ε"| skl_q2((q2))
    skl_q2 -->|"l / ε"| skl_q3((q3))
    skl_q3 -->|"e / ε"| skl_q4((q4))
    skl_q4 -->|"a / ε"| skl_q5((q5))
    skl_q5 -->|"r / ε"| skl_q6((q6))
    skl_q6 -->|"n / ε"| skl_q7((q7))
    skl_q7 -->|"ε / SCIKIT_LEARN"| qf
    skl_q1 -->|"c / ε"| skl_q8((q8))
    skl_q8 -->|"i / ε"| skl_q9((q9))
    skl_q9 -->|"k / ε"| skl_q10((q10))
    skl_q10 -->|"_"| skl_q11((q11))
    skl_q10 -->|"-"| skl_q12((q12))
    skl_q10 -->|"␠ / ε"| skl_q13((q13))
    skl_q11 -->|"l / ε"| skl_q14((q14))
    skl_q12 -->|"l / ε"| skl_q14
    skl_q13 -->|"l / ε"| skl_q14
    skl_q14 -->|"e / ε"| skl_q15((q15))
    skl_q15 -->|"a / ε"| skl_q16((q16))
    skl_q16 -->|"r / ε"| skl_q17((q17))
    skl_q17 -->|"n / ε"| skl_q18((q18))
    skl_q18 -->|"ε / SCIKIT_LEARN"| qf

    %% TENSORFLOW
    tf_q0((q0)) -->|"t / ε"| tf_q1((q1))
    tf_q1 -->|"e / ε"| tf_q2((q2))
    tf_q2 -->|"n / ε"| tf_q3((q3))
    tf_q3 -->|"s / ε"| tf_q4((q4))
    tf_q4 -->|"o / ε"| tf_q5((q5))
    tf_q5 -->|"r / ε"| tf_q6((q6))
    tf_q6 -->|"f / ε"| tf_q7((q7))
    tf_q6 -->|"␠ / ε"| tf_q8((q8))
    tf_q8 -->|"f / ε"| tf_q7
    tf_q7 -->|"l / ε"| tf_q9((q9))
    tf_q9 -->|"o / ε"| tf_q10((q10))
    tf_q10 -->|"w / ε"| tf_q11((q11))
    tf_q11 -->|"ε / TENSORFLOW"| qf

    %% PYTORCH
    pt_q0((q0)) -->|"p / ε"| pt_q1((q1))
    pt_q1 -->|"y / ε"| pt_q2((q2))
    pt_q2 -->|"t / ε"| pt_q3((q3))
    pt_q2 -->|"␠ / ε"| pt_q4((q4))
    pt_q4 -->|"t / ε"| pt_q3
    pt_q3 -->|"o / ε"| pt_q5((q5))
    pt_q5 -->|"r / ε"| pt_q6((q6))
    pt_q6 -->|"c / ε"| pt_q7((q7))
    pt_q7 -->|"h / ε"| pt_q8((q8))
    pt_q8 -->|"ε / PYTORCH"| qf

    %% GITHUB_ACTIONS
    gh_q0((q0)) -->|"g / ε"| gh_q1((q1))
    gh_q1 -->|"i / ε"| gh_q2((q2))
    gh_q2 -->|"t / ε"| gh_q3((q3))
    gh_q3 -->|"h / ε"| gh_q4((q4))
    gh_q4 -->|"u / ε"| gh_q5((q5))
    gh_q5 -->|"b / ε"| gh_q6((q6))
    gh_q6 -->|"_"| gh_q7((q7))
    gh_q6 -->|"␠ / ε"| gh_q8((q8))
    gh_q7 -->|"a / ε"| gh_q9((q9))
    gh_q8 -->|"a / ε"| gh_q9
    gh_q9 -->|"c / ε"| gh_q10((q10))
    gh_q10 -->|"t / ε"| gh_q11((q11))
    gh_q11 -->|"i / ε"| gh_q12((q12))
    gh_q12 -->|"o / ε"| gh_q13((q13))
    gh_q13 -->|"n / ε"| gh_q14((q14))
    gh_q14 -->|"s / ε"| gh_q15((q15))
    gh_q15 -->|"ε / GITHUB_ACTIONS"| qf
