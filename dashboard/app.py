import json
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

# Localiza automaticamente a raiz do projeto ServerRest-Compass
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho completo do relatório gerado pelo Pytest
REPORT_PATH = BASE_DIR / "reports" / "test_results.json"


# ============================================================
# CONFIGURAÇÃO DO DASHBOARD
# ============================================================

st.set_page_config(
    page_title="ServeRest | E2E Test Dashboard",
    page_icon="🧪",
    layout="wide"
)


# ============================================================
# VALIDAÇÃO DO RELATÓRIO
# ============================================================

if not REPORT_PATH.exists():
    st.warning(
        "⚠️ Relatório de testes não encontrado.\n\n"
        "Execute primeiro:\n\n"
        "pytest tests -v --json-report "
        "--json-report-file=reports/test_results.json"
    )
    st.stop()


@st.cache_data
def carregar_resultados():
    with open(REPORT_PATH, encoding="utf-8") as arquivo:
        report = json.load(arquivo)

    registros = []

    for test in report.get("tests", []):
        nodeid = test.get("nodeid", "")
        outcome = test.get("outcome", "unknown")

        partes = nodeid.split("::")
        caminho = partes[0] if partes else ""
        nome_teste = partes[-1] if partes else nodeid

        path_parts = caminho.replace("\\", "/").split("/")

        modulo = (
            path_parts[1]
            if len(path_parts) > 1
            else "outros"
        )

        setup = test.get("setup", {}).get("duration", 0)
        call = test.get("call", {}).get("duration", 0)
        teardown = test.get("teardown", {}).get("duration", 0)

        duracao = setup + call + teardown

        registros.append(
            {
                "teste": nome_teste,
                "nodeid": nodeid,
                "modulo": modulo,
                "status": outcome,
                "duracao": duracao,
            }
        )

    return pd.DataFrame(registros), report


df, report = carregar_resultados()

total = len(df)

passed = (df["status"] == "passed").sum()
failed = (df["status"] == "failed").sum()
skipped = (df["status"] == "skipped").sum()

taxa_sucesso = (
    passed / total * 100
    if total > 0
    else 0
)

duracao_total = df["duracao"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total de testes", total)
col2.metric("Passed", passed)
col3.metric("Failed", failed)
col4.metric("Skipped", skipped)
col5.metric("Taxa de sucesso", f"{taxa_sucesso:.1f}%")

status_modulo = (
    df.groupby(["modulo", "status"])
    .size()
    .reset_index(name="quantidade")
)

fig = px.bar(
    status_modulo,
    x="modulo",
    y="quantidade",
    color="status",
    barmode="group",
    title="Resultado dos testes por módulo"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

mais_lentos = (
    df.sort_values("duracao", ascending=False)
    .head(10)
)

fig_lentos = px.bar(
    mais_lentos,
    x="duracao",
    y="teste",
    orientation="h",
    title="Top 10 testes mais lentos"
)

fig_lentos.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig_lentos,
    use_container_width=True
)

st.subheader("Detalhamento da execução")

st.dataframe(
    df[
        [
            "modulo",
            "teste",
            "status",
            "duracao"
        ]
    ],
    use_container_width=True,
    hide_index=True
)