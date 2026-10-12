{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOwZHR1A+cWywr0EA3HBHjm",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/MissyMilaS/JMapostles/blob/docs/automatons.md\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 15,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 2082
        },
        "id": "1JpotZErxmBw",
        "outputId": "f867ea3b-04bd-4530-a61a-9294863d4e72"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "--- PROBANDO CONSTRUCCIÓN DE AUTÓMATAS ---\n",
            " [OK] FST JavaScript construido exitosamente.\n",
            " [OK] DFA Machine Learning -> Aceptada: True\n",
            " [OK] DFA Full Stack -> Aceptada: True\n",
            "\n",
            "=== RENDERIZANDO DIAGRAMAS COMO IMÁGENES EN COLAB ===\n",
            "\n",
            "Gráfico: 1_javascript\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "<img src=\"https://mermaid.ink/img/CmZsb3djaGFydCBMUgogICAgcTAoKHEwKSkgLS0gImogLyDOtSIgLS0+IHExKChxMSkpCiAgICBxMSAtLSAicyAvIM61IiAtLT4gcTIoKHEyKSkKICAgIHEyIC0tICLOtSAvIEpBVkFTQ1JJUFQiIC0tPiBxZigoKHFmKSkpCiAgICBxMiAtLSAiYSAvIM61IiAtLT4gcTMoKHEzKSkKICAgIHEzIC0tICJ2IC8gzrUiIC0tPiBxNCgocTQpKQogICAgcTQgLS0gImEgLyDOtSIgLS0+IHE1KChxNSkpCiAgICBxNSAtLSAicyAvIM61IiAtLT4gcTYoKHE2KSkKICAgIHE2IC0tICJjIC8gzrUiIC0tPiBxNygocTcpKQogICAgcTcgLS0gInIgLyDOtSIgLS0+IHE4KChxOCkpCiAgICBxOCAtLSAiaSAvIM61IiAtLT4gcTkoKHE5KSkKICAgIHE5IC0tICJwIC8gzrUiIC0tPiBxMTAoKHExMCkpCiAgICBxMTAgLS0gInQgLyDOtSIgLS0+IHExMSgocTExKSkKICAgIHExMSAtLSAizrUgLyBKQVZBU0NSSVBUIiAtLT4gcWYK\"/>"
            ],
            "text/plain": [
              "<IPython.core.display.Image object>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Gráfico: 2_typescript\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "<img src=\"https://mermaid.ink/img/CmZsb3djaGFydCBMUgogICAgcTAoKHEwKSkgLS0gInQgLyDOtSIgLS0+IHExKChxMSkpCiAgICBxMSAtLSAicyAvIM61IiAtLT4gcTIoKHEyKSkKICAgIHEyIC0tICLOtSAvIFRZUEVTQ1JJUFQiIC0tPiBxZigoKHFmKSkpCiAgICBxMSAtLSAieSAvIM61IiAtLT4gcTMoKHEzKSkKICAgIHEzIC0tICJwIC8gzrUiIC0tPiBxNCgocTQpKQogICAgcTQgLS0gImUgLyDOtSIgLS0+IHE1KChxNSkpCiAgICBxNSAtLSAicyAvIM61IiAtLT4gcTYoKHE2KSkKICAgIHE2IC0tICJjIC8gzrUiIC0tPiBxNygocTcpKQogICAgcTcgLS0gInIgLyDOtSIgLS0+IHE4KChxOCkpCiAgICBxOCAtLSAiaSAvIM61IiAtLT4gcTkoKHE5KSkKICAgIHE5IC0tICJwIC8gzrUiIC0tPiBxMTAoKHExMCkpCiAgICBxMTAgLS0gInQgLyDOtSIgLS0+IHExMSgocTExKSkKICAgIHExMSAtLSAizrUgLyBUWVBFU0NSSVBUIiAtLT4gcWYK\"/>"
            ],
            "text/plain": [
              "<IPython.core.display.Image object>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Gráfico: 3_react\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "<img src=\"https://mermaid.ink/img/CmZsb3djaGFydCBMUgogICAgcTAoKHEwKSkgLS0gInIgLyDOtSIgLS0+IHExKChxMSkpCiAgICBxMSAtLSAiZSAvIM61IiAtLT4gcTIoKHEyKSkKICAgIHEyIC0tICJhIC8gzrUiIC0tPiBxMygocTMpKQogICAgcTMgLS0gImMgLyDOtSIgLS0+IHE0KChxNCkpCiAgICBxNCAtLSAidCAvIM61IiAtLT4gcTUoKHE1KSkKICAgIHE1IC0tICLOtSAvIFJFQUNUIiAtLT4gcWYoKChxZikpKQogICAgcTUgLS0gIi4iIC0tPiBxNigocTYpKQogICAgcTYgLS0gImogLyDOtSIgLS0+IHE3KChxNykpCiAgICBxNyAtLSAicyAvIM61IiAtLT4gcTgoKHE4KSkKICAgIHE4IC0tICLOtSAvIFJFQUNUIiAtLT4gcWYKICAgIHE1IC0tICJqIC8gzrUiIC0tPiBxOSgocTkpKQogICAgcTkgLS0gInMgLyDOtSIgLS0+IHExMCgocTEwKSkKICAgIHExMCAtLSAizrUgLyBSRUFDVCIgLS0+IHFmCg==\"/>"
            ],
            "text/plain": [
              "<IPython.core.display.Image object>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Gráfico: 4_nodejs\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "<img src=\"https://mermaid.ink/img/CmZsb3djaGFydCBMUgogICAgcTAoKHEwKSkgLS0gIm4gLyDOtSIgLS0+IHExKChxMSkpCiAgICBxMSAtLSAibyAvIM61IiAtLT4gcTIoKHEyKSkKICAgIHEyIC0tICJkIC8gzrUiIC0tPiBxMygocTMpKQogICAgcTMgLS0gImUgLyDOtSIgLS0+IHE0KChxNCkpCiAgICBxNCAtLSAizrUgLyBOT0RFX0pTIiAtLT4gcWYoKChxZikpKQogICAgcTQgLS0gImogLyDOtSIgLS0+IHE1KChxNSkpCiAgICBxNSAtLSAicyAvIM61IiAtLT4gcTYoKHE2KSkKICAgIHE2IC0tICLOtSAvIE5PREVfSlMiIC0tPiBxZgogICAgcTQgLS0gIi4iIC0tPiBxNygocTcpKQogICAgcTcgLS0gImogLyDOtSIgLS0+IHE4KChxOCkpCiAgICBxOCAtLSAicyAvIM61IiAtLT4gcWYKICAgIHE0IC0tICLikKAgLyDOtSIgLS0+IHE5KChxOSkpCiAgICBxOSAtLSAiaiAvIM61IiAtLT4gcTEwKChxMTApKQogICAgcTEwIC0tICJzIC8gzrUiIC0tPiBxZgogICAgcTQgLS0gIl8iIC0tPiBxMTEoKHExMSkpCiAgICBxMTEgLS0gImogLyDOtSIgLS0+IHExMigocTEyKSkKICAgIHExMiAtLSAicyAvIM61IiAtLT4gcWYK\"/>"
            ],
            "text/plain": [
              "<IPython.core.display.Image object>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Gráfico: 5_postgresql\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "<img src=\"https://mermaid.ink/img/CmZsb3djaGFydCBMUgogICAgcTAoKHEwKSkgLS0gInAgLyDOtSIgLS0+IHExKChxMSkpCiAgICBxMSAtLSAibyAvIM61IiAtLT4gcTIoKHEyKSkKICAgIHEyIC0tICJzIC8gzrUiIC0tPiBxMygocTMpKQogICAgcTMgLS0gInQgLyDOtSIgLS0+IHE0KChxNCkpCiAgICBxNCAtLSAiZyAvIM61IiAtLT4gcTUoKHE1KSkKICAgIHE1IC0tICJyIC8gzrUiIC0tPiBxNigocTYpKQogICAgcTYgLS0gImUgLyDOtSIgLS0+IHE3KChxNykpCiAgICBxNyAtLSAicyAvIM61IiAtLT4gcTgoKHE4KSkKICAgIHE4IC0tICLOtSAvIFBPU1RHUkVTUUwiIC0tPiBxZigoKHFmKSkpCiAgICBxOCAtLSAicSAvIM61IiAtLT4gcTkoKHE5KSkKICAgIHE5IC0tICJsIC8gzrUiIC0tPiBxMTAoKHExMCkpCiAgICBxMTAgLS0gIs61IC8gUE9TVEdSRVNRTCIgLS0+IHFmCg==\"/>"
            ],
            "text/plain": [
              "<IPython.core.display.Image object>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Gráfico: 6_scikit_learn\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "<img src=\"https://mermaid.ink/img/CmZsb3djaGFydCBMUgogICAgcTAoKHEwKSkgLS0gInMgLyDOtSIgLS0+IHExKChxMSkpCiAgICBxMSAtLSAiayAvIM61IiAtLT4gcTIoKHEyKSkKICAgIHEyIC0tICJsIC8gzrUiIC0tPiBxMygocTMpKQogICAgcTMgLS0gImUgLyDOtSIgLS0+IHE0KChxNCkpCiAgICBxNCAtLSAiYSAvIM61IiAtLT4gcTUoKHE1KSkKICAgIHE1IC0tICJyIC8gzrUiIC0tPiBxNigocTYpKQogICAgcTYgLS0gIm4gLyDOtSIgLS0+IHE3KChxNykpCiAgICBxNyAtLSAizrUgLyBTQ0lLSVRfTEVBUk4iIC0tPiBxZigoKHFmKSkpCiAgICBxMSAtLSAiYyAvIM61IiAtLT4gcTgoKHE4KSkKICAgIHE4IC0tICJpIC8gzrUiIC0tPiBxOSgocTkpKQogICAgcTkgLS0gImsgLyDOtSIgLS0+IHExMCgocTEwKSkKICAgIHExMCAtLSAiXyIgLS0+IHExMSgocTExKSkKICAgIHExMCAtLSAiLSIgLS0+IHExMigocTEyKSkKICAgIHExMCAtLSAi4pCgIC8gzrUiIC0tPiBxMTMoKHExMykpCiAgICBxMTEgLS0gImwgLyDOtSIgLS0+IHExNCgocTE0KSkKICAgIHExMiAtLSAibCAvIM61IiAtLT4gcTE0CiAgICBxMTMgLS0gImwgLyDOtSIgLS0+IHExNAogICAgcTE0IC0tICJlIC8gzrUiIC0tPiBxMTUoKHExNSkpCiAgICBxMTUgLS0gImEgLyDOtSIgLS0+IHExNigocTE2KSkKICAgIHExNiAtLSAiciAvIM61IiAtLT4gcTE3KChxMTcpKQogICAgcTE3IC0tICJuIC8gzrUiIC0tPiBxMTgoKHExOCkpCiAgICBxMTggLS0gIs61IC8gU0NJS0lUX0xFQVJOIiAtLT4gcWYK\"/>"
            ],
            "text/plain": [
              "<IPython.core.display.Image object>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Gráfico: 7_tensorflow\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "<img src=\"https://mermaid.ink/img/CmZsb3djaGFydCBMUgogICAgcTAoKHEwKSkgLS0gInQgLyDOtSIgLS0+IHExKChxMSkpCiAgICBxMSAtLSAiZSAvIM61IiAtLT4gcTIoKHEyKSkKICAgIHEyIC0tICJuIC8gzrUiIC0tPiBxMygocTMpKQogICAgcTMgLS0gInMgLyDOtSIgLS0+IHE0KChxNCkpCiAgICBxNCAtLSAibyAvIM61IiAtLT4gcTUoKHE1KSkKICAgIHE1IC0tICJyIC8gzrUiIC0tPiBxNigocTYpKQogICAgcTYgLS0gImYgLyDOtSIgLS0+IHE3KChxNykpCiAgICBxNiAtLSAi4pCgIC8gzrUiIC0tPiBxOCgocTgpKQogICAgcTggLS0gImYgLyDOtSIgLS0+IHE3CiAgICBxNyAtLSAibCAvIM61IiAtLT4gcTkoKHE5KSkKICAgIHE5IC0tICJvIC8gzrUiIC0tPiBxMTAoKHExMCkpCiAgICBxMTAgLS0gIncgLyDOtSIgLS0+IHExMSgocTExKSkKICAgIHExMSAtLSAizrUgLyBURU5TT1JGTE9XIiAtLT4gcWYoKChxZikpKQo=\"/>"
            ],
            "text/plain": [
              "<IPython.core.display.Image object>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Gráfico: 8_pytorch\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "<img src=\"https://mermaid.ink/img/CmZsb3djaGFydCBMUgogICAgcTAoKHEwKSkgLS0gInAgLyDOtSIgLS0+IHExKChxMSkpCiAgICBxMSAtLSAieSAvIM61IiAtLT4gcTIoKHEyKSkKICAgIHEyIC0tICJ0IC8gzrUiIC0tPiBxMygocTMpKQogICAgcTIgLS0gIuKQoCAvIM61IiAtLT4gcTQoKHE0KSkKICAgIHE0IC0tICJ0IC8gzrUiIC0tPiBxMwogICAgcTMgLS0gIm8gLyDOtSIgLS0+IHE1KChxNSkpCiAgICBxNSAtLSAiciAvIM61IiAtLT4gcTYoKHE2KSkKICAgIHE2IC0tICJjIC8gzrUiIC0tPiBxNygocTcpKQogICAgcTcgLS0gImggLyDOtSIgLS0+IHE4KChxOCkpCiAgICBxOCAtLSAizrUgLyBQWVRPUkNIIiAtLT4gcWYoKChxZikpKQo=\"/>"
            ],
            "text/plain": [
              "<IPython.core.display.Image object>"
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Gráfico: 9_github_actions\n"
          ]
        },
        {
          "output_type": "display_data",
          "data": {
            "text/html": [
              "<img src=\"https://mermaid.ink/img/CmZsb3djaGFydCBMUgogICAgcTAoKHEwKSkgLS0gImcgLyDOtSIgLS0+IHExKChxMSkpCiAgICBxMSAtLSAiaSAvIM61IiAtLT4gcTIoKHEyKSkKICAgIHEyIC0tICJ0IC8gzrUiIC0tPiBxMygocTMpKQogICAgcTMgLS0gImggLyDOtSIgLS0+IHE0KChxNCkpCiAgICBxNCAtLSAidSAvIM61IiAtLT4gcTUoKHE1KSkKICAgIHE1IC0tICJiIC8gzrUiIC0tPiBxNigocTYpKQogICAgcTYgLS0gIl8iIC0tPiBxNygocTcpKQogICAgcTYgLS0gIuKQoCAvIM61IiAtLT4gcTgoKHE4KSkKICAgIHE3IC0tICJhIC8gzrUiIC0tPiBxOSgocTkpKQogICAgcTggLS0gImEgLyDOtSIgLS0+IHE5CiAgICBxOSAtLSAiYyAvIM61IiAtLT4gcTEwKChxMTApKQogICAgcTEwIC0tICJ0IC8gzrUiIC0tPiBxMTEoKHExMSkpCiAgICBxMTEgLS0gImkgLyDOtSIgLS0+IHExMigocTEyKSkKICAgIHExMiAtLSAibyAvIM61IiAtLT4gcTEzKChxMTMpKQogICAgcTEzIC0tICJuIC8gzrUiIC0tPiBxMTQoKHExNCkpCiAgICBxMTQgLS0gInMgLyDOtSIgLS0+IHExNSgocTE1KSkKICAgIHExNSAtLSAizrUgLyBHSVRIVUJfQUNUSU9OUyIgLS0+IHFmKCgocWYpKSkK\"/>"
            ],
            "text/plain": [
              "<IPython.core.display.Image object>"
            ]
          },
          "metadata": {}
        }
      ],
      "source": [
        "!pip install pyformlang -q\n",
        "\n",
        "\"\"\"\n",
        "ResumeLens: Core Automata & FST Builders for Visualization\n",
        "\"\"\"\n",
        "\n",
        "from typing import Tuple\n",
        "from pyformlang.fst import FST\n",
        "from pyformlang.finite_automaton import DeterministicFiniteAutomaton\n",
        "from IPython.display import display, Image\n",
        "import base64\n",
        "\n",
        "\n",
        "# ============================================================================\n",
        "# 1. FST: JAVASCRIPT NORMALIZATION\n",
        "# ============================================================================\n",
        "\n",
        "def build_javascript_fst() -> FST:\n",
        "    \"\"\"Construye y retorna el FST para normalizar variantes de JavaScript.\"\"\"\n",
        "    fst = FST()\n",
        "    fst.add_start_state(\"q0\")\n",
        "    fst.add_final_state(\"qf\")\n",
        "\n",
        "    # Transiciones para \"JS\"\n",
        "    fst.add_transition(\"q0\", \"j\", \"q1\", [])\n",
        "    fst.add_transition(\"q1\", \"s\", \"q2\", [])\n",
        "    fst.add_transition(\"q2\", \"epsilon\", \"qf\", [\"JAVASCRIPT\"])\n",
        "\n",
        "    # Transiciones para \"JavaScript\" / \"Javascript\"\n",
        "    transitions = [\n",
        "        (\"q0\", \"j\", \"q1\"), (\"q1\", \"a\", \"q3\"), (\"q3\", \"v\", \"q4\"),\n",
        "        (\"q4\", \"a\", \"q5\"), (\"q5\", \"s\", \"q6\"), (\"q6\", \"c\", \"q7\"),\n",
        "        (\"q7\", \"r\", \"q8\"), (\"q8\", \"i\", \"q9\"), (\"q9\", \"p\", \"q10\"),\n",
        "        (\"q10\", \"t\", \"q11\")\n",
        "    ]\n",
        "    for u, symbol, v in transitions:\n",
        "        fst.add_transition(u, symbol, v, [])\n",
        "    fst.add_transition(\"q11\", \"epsilon\", \"qf\", [\"JAVASCRIPT\"])\n",
        "\n",
        "    return fst\n",
        "\n",
        "\n",
        "# ============================================================================\n",
        "# 2. DFA: MACHINE LEARNING ENGINEER\n",
        "# ============================================================================\n",
        "\n",
        "def build_ml_engineer_dfa() -> DeterministicFiniteAutomaton:\n",
        "    \"\"\"Construye y retorna el DFA para el perfil de Machine Learning.\"\"\"\n",
        "    dfa = DeterministicFiniteAutomaton()\n",
        "    dfa.add_start_state(0)\n",
        "    dfa.add_final_state(5)\n",
        "\n",
        "    delta = {\n",
        "        (0, \"PYTHON\"): 1,\n",
        "        (1, \"PANDAS\"): 2, (1, \"NUMPY\"): 2,\n",
        "        (2, \"PANDAS\"): 2, (2, \"NUMPY\"): 2,\n",
        "        (2, \"SCIKIT_LEARN\"): 3, (2, \"TENSORFLOW\"): 3, (2, \"PYTORCH\"): 3,\n",
        "        (3, \"SCIKIT_LEARN\"): 3, (3, \"TENSORFLOW\"): 3, (3, \"PYTORCH\"): 3,\n",
        "    }\n",
        "\n",
        "    for db in [\"SQL\", \"POSTGRESQL\", \"MYSQL\", \"MONGODB\", \"NOSQL\"]:\n",
        "        delta[(3, db)] = 4\n",
        "        delta[(4, db)] = 4\n",
        "\n",
        "    delta[(4, \"GIT\")] = 5\n",
        "    delta[(5, \"GIT\")] = 5\n",
        "\n",
        "    for (state, symbol), next_state in delta.items():\n",
        "        dfa.add_transition(state, symbol, next_state)\n",
        "\n",
        "    return dfa\n",
        "\n",
        "\n",
        "# ============================================================================\n",
        "# 3. DFA: FULL STACK DEVELOPER\n",
        "# ============================================================================\n",
        "\n",
        "def build_full_stack_dfa() -> DeterministicFiniteAutomaton:\n",
        "    \"\"\"Construye y retorna el DFA para el perfil Full Stack.\"\"\"\n",
        "    dfa = DeterministicFiniteAutomaton()\n",
        "    dfa.add_start_state(0)\n",
        "    dfa.add_final_state(5)\n",
        "\n",
        "    delta = {\n",
        "        (0, \"JAVASCRIPT\"): 1, (0, \"TYPESCRIPT\"): 1,\n",
        "        (1, \"JAVASCRIPT\"): 1, (1, \"TYPESCRIPT\"): 1,\n",
        "        (1, \"REACT\"): 2, (1, \"ANGULAR\"): 2, (1, \"VUE\"): 2,\n",
        "        (2, \"REACT\"): 2, (2, \"ANGULAR\"): 2, (2, \"VUE\"): 2,\n",
        "        (2, \"NODE_JS\"): 3, (2, \"DJANGO\"): 3, (2, \"SPRING_BOOT\"): 3,\n",
        "        (3, \"NODE_JS\"): 3, (3, \"DJANGO\"): 3, (3, \"SPRING_BOOT\"): 3,\n",
        "    }\n",
        "\n",
        "    for db in [\"SQL\", \"POSTGRESQL\", \"MYSQL\", \"MONGODB\", \"NOSQL\"]:\n",
        "        delta[(3, db)] = 4\n",
        "        delta[(4, db)] = 4\n",
        "\n",
        "    delta[(4, \"REST_API\")] = 4\n",
        "    delta[(4, \"GIT\")] = 5\n",
        "    delta[(5, \"GIT\")] = 5\n",
        "\n",
        "    for (state, symbol), next_state in delta.items():\n",
        "        dfa.add_transition(state, symbol, next_state)\n",
        "\n",
        "    return dfa\n",
        "\n",
        "\n",
        "# ============================================================================\n",
        "# 4. DIAGRAMAS MERMAID (9 DIAGRAMAS SOLICITADOS)\n",
        "# ============================================================================\n",
        "\n",
        "MERMAID_DIAGRAMS = {\n",
        "    \"1_javascript\": \"\"\"\n",
        "flowchart LR\n",
        "    q0((q0)) -- \"j / ε\" --> q1((q1))\n",
        "    q1 -- \"s / ε\" --> q2((q2))\n",
        "    q2 -- \"ε / JAVASCRIPT\" --> qf(((qf)))\n",
        "    q2 -- \"a / ε\" --> q3((q3))\n",
        "    q3 -- \"v / ε\" --> q4((q4))\n",
        "    q4 -- \"a / ε\" --> q5((q5))\n",
        "    q5 -- \"s / ε\" --> q6((q6))\n",
        "    q6 -- \"c / ε\" --> q7((q7))\n",
        "    q7 -- \"r / ε\" --> q8((q8))\n",
        "    q8 -- \"i / ε\" --> q9((q9))\n",
        "    q9 -- \"p / ε\" --> q10((q10))\n",
        "    q10 -- \"t / ε\" --> q11((q11))\n",
        "    q11 -- \"ε / JAVASCRIPT\" --> qf\n",
        "\"\"\",\n",
        "    \"2_typescript\": \"\"\"\n",
        "flowchart LR\n",
        "    q0((q0)) -- \"t / ε\" --> q1((q1))\n",
        "    q1 -- \"s / ε\" --> q2((q2))\n",
        "    q2 -- \"ε / TYPESCRIPT\" --> qf(((qf)))\n",
        "    q1 -- \"y / ε\" --> q3((q3))\n",
        "    q3 -- \"p / ε\" --> q4((q4))\n",
        "    q4 -- \"e / ε\" --> q5((q5))\n",
        "    q5 -- \"s / ε\" --> q6((q6))\n",
        "    q6 -- \"c / ε\" --> q7((q7))\n",
        "    q7 -- \"r / ε\" --> q8((q8))\n",
        "    q8 -- \"i / ε\" --> q9((q9))\n",
        "    q9 -- \"p / ε\" --> q10((q10))\n",
        "    q10 -- \"t / ε\" --> q11((q11))\n",
        "    q11 -- \"ε / TYPESCRIPT\" --> qf\n",
        "\"\"\",\n",
        "    \"3_react\": \"\"\"\n",
        "flowchart LR\n",
        "    q0((q0)) -- \"r / ε\" --> q1((q1))\n",
        "    q1 -- \"e / ε\" --> q2((q2))\n",
        "    q2 -- \"a / ε\" --> q3((q3))\n",
        "    q3 -- \"c / ε\" --> q4((q4))\n",
        "    q4 -- \"t / ε\" --> q5((q5))\n",
        "    q5 -- \"ε / REACT\" --> qf(((qf)))\n",
        "    q5 -- \".\" --> q6((q6))\n",
        "    q6 -- \"j / ε\" --> q7((q7))\n",
        "    q7 -- \"s / ε\" --> q8((q8))\n",
        "    q8 -- \"ε / REACT\" --> qf\n",
        "    q5 -- \"j / ε\" --> q9((q9))\n",
        "    q9 -- \"s / ε\" --> q10((q10))\n",
        "    q10 -- \"ε / REACT\" --> qf\n",
        "\"\"\",\n",
        "    \"4_nodejs\": \"\"\"\n",
        "flowchart LR\n",
        "    q0((q0)) -- \"n / ε\" --> q1((q1))\n",
        "    q1 -- \"o / ε\" --> q2((q2))\n",
        "    q2 -- \"d / ε\" --> q3((q3))\n",
        "    q3 -- \"e / ε\" --> q4((q4))\n",
        "    q4 -- \"ε / NODE_JS\" --> qf(((qf)))\n",
        "    q4 -- \"j / ε\" --> q5((q5))\n",
        "    q5 -- \"s / ε\" --> q6((q6))\n",
        "    q6 -- \"ε / NODE_JS\" --> qf\n",
        "    q4 -- \".\" --> q7((q7))\n",
        "    q7 -- \"j / ε\" --> q8((q8))\n",
        "    q8 -- \"s / ε\" --> qf\n",
        "    q4 -- \"␠ / ε\" --> q9((q9))\n",
        "    q9 -- \"j / ε\" --> q10((q10))\n",
        "    q10 -- \"s / ε\" --> qf\n",
        "    q4 -- \"_\" --> q11((q11))\n",
        "    q11 -- \"j / ε\" --> q12((q12))\n",
        "    q12 -- \"s / ε\" --> qf\n",
        "\"\"\",\n",
        "    \"5_postgresql\": \"\"\"\n",
        "flowchart LR\n",
        "    q0((q0)) -- \"p / ε\" --> q1((q1))\n",
        "    q1 -- \"o / ε\" --> q2((q2))\n",
        "    q2 -- \"s / ε\" --> q3((q3))\n",
        "    q3 -- \"t / ε\" --> q4((q4))\n",
        "    q4 -- \"g / ε\" --> q5((q5))\n",
        "    q5 -- \"r / ε\" --> q6((q6))\n",
        "    q6 -- \"e / ε\" --> q7((q7))\n",
        "    q7 -- \"s / ε\" --> q8((q8))\n",
        "    q8 -- \"ε / POSTGRESQL\" --> qf(((qf)))\n",
        "    q8 -- \"q / ε\" --> q9((q9))\n",
        "    q9 -- \"l / ε\" --> q10((q10))\n",
        "    q10 -- \"ε / POSTGRESQL\" --> qf\n",
        "\"\"\",\n",
        "    \"6_scikit_learn\": \"\"\"\n",
        "flowchart LR\n",
        "    q0((q0)) -- \"s / ε\" --> q1((q1))\n",
        "    q1 -- \"k / ε\" --> q2((q2))\n",
        "    q2 -- \"l / ε\" --> q3((q3))\n",
        "    q3 -- \"e / ε\" --> q4((q4))\n",
        "    q4 -- \"a / ε\" --> q5((q5))\n",
        "    q5 -- \"r / ε\" --> q6((q6))\n",
        "    q6 -- \"n / ε\" --> q7((q7))\n",
        "    q7 -- \"ε / SCIKIT_LEARN\" --> qf(((qf)))\n",
        "    q1 -- \"c / ε\" --> q8((q8))\n",
        "    q8 -- \"i / ε\" --> q9((q9))\n",
        "    q9 -- \"k / ε\" --> q10((q10))\n",
        "    q10 -- \"_\" --> q11((q11))\n",
        "    q10 -- \"-\" --> q12((q12))\n",
        "    q10 -- \"␠ / ε\" --> q13((q13))\n",
        "    q11 -- \"l / ε\" --> q14((q14))\n",
        "    q12 -- \"l / ε\" --> q14\n",
        "    q13 -- \"l / ε\" --> q14\n",
        "    q14 -- \"e / ε\" --> q15((q15))\n",
        "    q15 -- \"a / ε\" --> q16((q16))\n",
        "    q16 -- \"r / ε\" --> q17((q17))\n",
        "    q17 -- \"n / ε\" --> q18((q18))\n",
        "    q18 -- \"ε / SCIKIT_LEARN\" --> qf\n",
        "\"\"\",\n",
        "    \"7_tensorflow\": \"\"\"\n",
        "flowchart LR\n",
        "    q0((q0)) -- \"t / ε\" --> q1((q1))\n",
        "    q1 -- \"e / ε\" --> q2((q2))\n",
        "    q2 -- \"n / ε\" --> q3((q3))\n",
        "    q3 -- \"s / ε\" --> q4((q4))\n",
        "    q4 -- \"o / ε\" --> q5((q5))\n",
        "    q5 -- \"r / ε\" --> q6((q6))\n",
        "    q6 -- \"f / ε\" --> q7((q7))\n",
        "    q6 -- \"␠ / ε\" --> q8((q8))\n",
        "    q8 -- \"f / ε\" --> q7\n",
        "    q7 -- \"l / ε\" --> q9((q9))\n",
        "    q9 -- \"o / ε\" --> q10((q10))\n",
        "    q10 -- \"w / ε\" --> q11((q11))\n",
        "    q11 -- \"ε / TENSORFLOW\" --> qf(((qf)))\n",
        "\"\"\",\n",
        "    \"8_pytorch\": \"\"\"\n",
        "flowchart LR\n",
        "    q0((q0)) -- \"p / ε\" --> q1((q1))\n",
        "    q1 -- \"y / ε\" --> q2((q2))\n",
        "    q2 -- \"t / ε\" --> q3((q3))\n",
        "    q2 -- \"␠ / ε\" --> q4((q4))\n",
        "    q4 -- \"t / ε\" --> q3\n",
        "    q3 -- \"o / ε\" --> q5((q5))\n",
        "    q5 -- \"r / ε\" --> q6((q6))\n",
        "    q6 -- \"c / ε\" --> q7((q7))\n",
        "    q7 -- \"h / ε\" --> q8((q8))\n",
        "    q8 -- \"ε / PYTORCH\" --> qf(((qf)))\n",
        "\"\"\",\n",
        "    \"9_github_actions\": \"\"\"\n",
        "flowchart LR\n",
        "    q0((q0)) -- \"g / ε\" --> q1((q1))\n",
        "    q1 -- \"i / ε\" --> q2((q2))\n",
        "    q2 -- \"t / ε\" --> q3((q3))\n",
        "    q3 -- \"h / ε\" --> q4((q4))\n",
        "    q4 -- \"u / ε\" --> q5((q5))\n",
        "    q5 -- \"b / ε\" --> q6((q6))\n",
        "    q6 -- \"_\" --> q7((q7))\n",
        "    q6 -- \"␠ / ε\" --> q8((q8))\n",
        "    q7 -- \"a / ε\" --> q9((q9))\n",
        "    q8 -- \"a / ε\" --> q9\n",
        "    q9 -- \"c / ε\" --> q10((q10))\n",
        "    q10 -- \"t / ε\" --> q11((q11))\n",
        "    q11 -- \"i / ε\" --> q12((q12))\n",
        "    q12 -- \"o / ε\" --> q13((q13))\n",
        "    q13 -- \"n / ε\" --> q14((q14))\n",
        "    q14 -- \"s / ε\" --> q15((q15))\n",
        "    q15 -- \"ε / GITHUB_ACTIONS\" --> qf(((qf)))\n",
        "\"\"\"\n",
        "}\n",
        "\n",
        "\n",
        "# ============================================================================\n",
        "# RENDERIZADO COMO IMAGEN ESTÁTICA\n",
        "# ============================================================================\n",
        "\n",
        "def render_mermaid_as_image(mermaid_code: str):\n",
        "    \"\"\"Genera un link de imagen usando mermaid.ink y lo visualiza.\"\"\"\n",
        "    # Codificar la definición del diagrama en base64 para construir la URL del servicio\n",
        "    encoded_bytes = base64.b64encode(mermaid_code.encode(\"utf-8\"))\n",
        "    encoded_str = encoded_bytes.decode(\"utf-8\")\n",
        "    image_url = f\"https://mermaid.ink/img/{encoded_str}\"\n",
        "    display(Image(url=image_url))\n",
        "\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    print(\"--- PROBANDO CONSTRUCCIÓN DE AUTÓMATAS ---\")\n",
        "\n",
        "    fst = build_javascript_fst()\n",
        "    print(\" [OK] FST JavaScript construido exitosamente.\")\n",
        "\n",
        "    ml_dfa = build_ml_engineer_dfa()\n",
        "    test_ml = [\"PYTHON\", \"NUMPY\", \"TENSORFLOW\", \"POSTGRESQL\", \"GIT\"]\n",
        "    print(f\" [OK] DFA Machine Learning -> Aceptada: {ml_dfa.accepts(test_ml)}\")\n",
        "\n",
        "    fs_dfa = build_full_stack_dfa()\n",
        "    test_fs = [\"TYPESCRIPT\", \"REACT\", \"NODE_JS\", \"MYSQL\", \"REST_API\", \"GIT\"]\n",
        "    print(f\" [OK] DFA Full Stack -> Aceptada: {fs_dfa.accepts(test_fs)}\")\n",
        "\n",
        "    print(\"\\n=== RENDERIZANDO DIAGRAMAS COMO IMÁGENES EN COLAB ===\")\n",
        "    for name, code in sorted(MERMAID_DIAGRAMS.items()):\n",
        "        print(f\"\\nGráfico: {name}\")\n",
        "        render_mermaid_as_image(code)"
      ]
    }
  ]
}