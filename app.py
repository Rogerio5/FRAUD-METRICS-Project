# 📦 Imports principais
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# 📚 Imports internos
from src.metrics import ConfusionMatrix
from src.scenario3 import scenario3_report
from src.scenario_company import y_true_company, y_scores_company
from src.visualize import plot_confusion_dashboard
from src.visualize_company import visualize_company
from src.simulacao import simular_custos
from src.db import criar_tabela, salvar_simulacao, consultar_simulacoes_filtradas

# 🔹 Importa função com especificidade já incluída
from src.visualize import calcular_metricas  

# 🔓 Autenticação desativada temporariamente
# from src.auth import login, verificar_autenticacao
# login()
# verificar_autenticacao()

# 🗃️ Inicializa banco de dados
criar_tabela()

# 🎨 Configurações visuais
st.set_page_config(page_title="DetectorFraudeCorp - Relatórios", page_icon="🛡️", layout="wide")
st.markdown("""
    <style>
        .responsive-img {
            width: 100%;
            height: auto;
            max-width: 900px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .stDownloadButton button {
            background-color: #2a9d8f;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# 📁 Pasta de saída
os.makedirs("output", exist_ok=True)

# 📂 Sidebar: filtros e parâmetros
st.sidebar.header("📂 Filtros")
modelo_selecionado = st.sidebar.selectbox("🧠 Modelo de risco", ["DetectorFraudeCorp", "Modelo B", "Modelo C"])
data_selecionada = st.sidebar.date_input("📅 Data da avaliação", value=datetime.today())

st.sidebar.header("💰 Custos por Erro")
cost_fp = st.sidebar.number_input("💸 Custo por Falso Positivo (FP)", min_value=0.0, value=10.0, step=1.0)
cost_fn = st.sidebar.number_input("💸 Custo por Falso Negativo (FN)", min_value=0.0, value=5.0, step=1.0)

st.sidebar.header("🚨 Alerta de Custo Total")
limite_alerta = st.sidebar.number_input("🔔 Limite de custo total (R$)", min_value=0.0, value=1000.0, step=50.0)

# 📊 Matriz de confusão simulada
cm_cenario3 = ConfusionMatrix(vp=90, fn=10, fp=30, vn=8000)

# 🔍 Funções de cada aba
def aba_resumo():
    st.subheader("📋 Relatório do Cenário 3")
    relatorio = scenario3_report(cost_fp=cost_fp, cost_fn=cost_fn)
    st.code(relatorio, language="text")

def aba_dashboard():
    st.subheader("📊 Dashboard de Métricas")
    dashboard_path = "output/dashboard.png"

    # Calcula métricas, incluindo especificidade
    m = calcular_metricas(cm_cenario3)

    plot_confusion_dashboard(
        cm=cm_cenario3,
        layout="dashboard",
        cost_fp=cost_fp,
        cost_fn=cost_fn,
        save_path=dashboard_path
    )

    st.image(dashboard_path, caption="📊 Matriz de confusão e métricas", use_container_width=True)

    # Exibe métricas detalhadas
    st.markdown(f"""
    **Acurácia:** {m['acuracia']:.2%}  
    **Precisão:** {m['precisao']:.2%}  
    **Recall (Sensibilidade):** {m['recall']:.2%}  
    **Especificidade:** {m['especificidade']:.2%}  
    **F1-Score:** {m['f1']:.2%}  
    """)

def aba_curva():
    st.subheader("📈 Curva Precisão-Recall")
    curva_path = "output/curva_precision_recall_empresa.png"
    visualize_company(
        y_true=y_true_company,
        y_scores=y_scores_company,
        name=modelo_selecionado,
        save_path=curva_path
    )
    st.image(curva_path, caption="📈 Desempenho do modelo", use_column_width=True)

def aba_simulacao():
    st.subheader("💸 Simulação de Custos Operacionais")
    resultado = simular_custos(cm_cenario3)
    st.code(resultado, language="text")

    custo_total = cm_cenario3.fp * cost_fp + cm_cenario3.fn * cost_fn
    if custo_total > limite_alerta:
        st.warning(f"🚨 Custo total estimado: R$ {custo_total:.2f} > limite de R$ {limite_alerta:.2f}")
        sugestao = "Reduzir Falsos Positivos (FP)" if cm_cenario3.fp * cost_fp > cm_cenario3.fn * cost_fn else "Reduzir Falsos Negativos (FN)"
        st.markdown(f"🔧 **Sugestão**: {sugestao}")

    if st.button("💾 Salvar simulação"):
        salvar_simulacao(modelo_selecionado, cm_cenario3, cost_fp, cost_fn)
        st.success("✅ Simulação salva com sucesso!")

def aba_exportar():
    st.subheader("📝 Exportar Relatório HTML")
    relatorio = scenario3_report(cost_fp=cost_fp, cost_fn=cost_fn)
    resultado = simular_custos(cm_cenario3)

    if st.button("📝 Gerar HTML"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        html_path = f"output/relatorio_{timestamp}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="pt-br"><head><meta charset="UTF-8"><title>Relatório</title></head><body>
<h1>📊 Relatório de Métricas</h1>
<h2>🔍 Cenário 3</h2>
<pre>{relatorio}</pre>
<h2>💸 Simulação de Custos</h2>
<pre>{resultado}</pre>
<footer>Relatório gerado por DetectorFraudeCorp</footer></body></html>""")
        st.success(f"✅ Relatório gerado: {html_path}")

def aba_historico():
    st.subheader("📚 Histórico de Simulações")
    filtro_modelo = st.selectbox("🔎 Modelo", ["Todos", "DetectorFraudeCorp", "Modelo B", "Modelo C"])
    filtro_data = st.date_input("📅 Data específica (opcional)")

    modelo_param = None if filtro_modelo == "Todos" else filtro_modelo
    data_param = filtro_data.strftime("%Y-%m-%d") if filtro_data else None

    registros = consultar_simulacoes_filtradas(modelo=modelo_param, data=data_param)

    if registros:
        df = pd.DataFrame(registros, columns=[
            "ID", "Modelo", "Data", "Custo FP", "Custo FN", "Custo Total", "VP", "VN", "FP", "FN"
        ])
        st.dataframe(df.style.format({
            "Custo FP": "{:.2f}", "Custo FN": "{:.2f}", "Custo Total": "{:.2f}"
        }))
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar CSV", data=csv, file_name="simulacoes.csv", mime="text/csv")
    else:
        st.info("📭 Nenhuma simulação encontrada com os filtros selecionados.")

def aba_heatmap_personalizado():
    st.subheader("🧮 Simulação Visual com Fórmula")
    formula = st.selectbox("📐 Fórmula", ["FP + FN", "FP * peso + FN", "FP + FN * peso"])
    peso = st.slider("⚖️ Peso", 0.5, 5.0, 1.0, step=0.5)
    fp_max = st.slider("📊 Máximo FP", 0, 175, 150, step=25)
    fn_max = st.slider("📊 Máximo FN", 0, 175, 150, step=25)

    fp_values = list(range(0, fp_max + 25, 25))
    fn_values = list(range(0, fn_max + 25, 25))

    data = []
    for fn in fn_values:
        for fp in fp_values:
            if formula == "FP + FN":
                custo = fp + fn
            elif formula == "FP * peso + FN":
                custo = fp * peso + fn
            elif formula == "FP + FN * peso":
                custo = fp + fn * peso
            data.append({
                "FP": fp,
                "FN": fn,
                "Custo Total": round(custo, 2)
            })

    df = pd.DataFrame(data)

    fig = px.density_heatmap(
        df, x="FP", y="FN", z="Custo Total",
        color_continuous_scale="YlOrBr",
        hover_data=["Custo Total"]
    )
    fig.update_layout(
        title=f"📊 Simulação de Custo Total — Fórmula: {formula}",
        xaxis_title="Falsos Positivos (FP)",
        yaxis_title="Falsos Negativos (FN)",
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # 📥 Exportação dos dados simulados
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Exportar dados como CSV",
        data=csv,
        file_name="heatmap_simulacao.csv",
        mime="text/csv"
    )

# 🧭 Navegação entre abas
aba = st.sidebar.radio(
    "📌 Selecione uma aba",
    ["Resumo", "Dashboard", "Curva", "Simulação", "Exportar", "Histórico", "Heatmap"]
)

if aba == "Resumo":
    aba_resumo()
elif aba == "Dashboard":
    aba_dashboard()
elif aba == "Curva":
    aba_curva()
elif aba == "Simulação":
    aba_simulacao()
elif aba == "Exportar":
    aba_exportar()
elif aba == "Histórico":
    aba_historico()
elif aba == "Heatmap":
    aba_heatmap_personalizado()
