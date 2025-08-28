import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Gráfico de barras FP/FN
def plot_fp_fn_bars(m1, m2):
    labels = ["Custo FP", "Custo FN"]
    modelo_a = [m1[5], m1[6]]
    modelo_b = [m2[5], m2[6]]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(x - width/2, modelo_a, width, label='Modelo A', color="#f39c12")
    ax.bar(x + width/2, modelo_b, width, label='Modelo B', color="#27ae60")

    ax.set_ylabel('Custo (R$)')
    ax.set_title('Custo por Tipo de Erro')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    st.pyplot(fig)

# --- Radar de métricas
def plot_radar_metrics(m1, m2):
    categorias = ["Acurácia", "Precisão", "Recall", "Especificidade", "F1-Score"]

    valores_a = [m1[0], m1[1], m1[2], m1[3], m1[4]]
    valores_b = [m2[0], m2[1], m2[2], m2[3], m2[4]]
    valores_a += valores_a[:1]
    valores_b += valores_b[:1]

    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angulos, valores_a, color="#e67e22", linewidth=2, label="Modelo A")
    ax.fill(angulos, valores_a, color="#e67e22", alpha=0.25)
    ax.plot(angulos, valores_b, color="#2ecc71", linewidth=2, label="Modelo B")
    ax.fill(angulos, valores_b, color="#2ecc71", alpha=0.25)

    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.4)
    plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
    st.pyplot(fig)

# --- Heatmap de custo total
def plot_heatmap_custos(cm=None, cost_fp=None, cost_fn=None):
    custos_fixos = np.arange(500, 3001, 500)       
    custos_fraude = np.arange(500, 3001, 500)      

    total_cost = np.zeros((len(custos_fraude), len(custos_fixos)))

    for i, custo_fraude in enumerate(custos_fraude):
        for j, custo_fixo in enumerate(custos_fixos):
            if cm and cost_fp is not None and cost_fn is not None:
                custo_fp_total = cm.fp * cost_fp
                custo_fn_total = cm.fn * custo_fraude
                total_cost[i, j] = custo_fixo + custo_fp_total + custo_fn_total
            else:
                total_cost[i, j] = custo_fixo + (custo_fraude * 2)

    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.imshow(total_cost, cmap="YlOrBr", origin="lower")

    ax.set_xticks(np.arange(len(custos_fixos)))
    ax.set_xticklabels(custos_fixos)
    ax.set_yticks(np.arange(len(custos_fraude)))
    ax.set_yticklabels(custos_fraude)

    ax.set_xlabel("Custo Fixo por Mês (R$)")
    ax.set_ylabel("Custo por Fraude (R$)")
    ax.set_title("Projeção de Custo Total" if cm else "Simulação de Custo Total")

    fig.colorbar(cax, ax=ax, label="Custo Total (R$)")
    st.pyplot(fig)
