# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Optional, List

from src.visualize_compare import (
    plot_metrics_confusion_with_legend,
    plot_metrics_and_confusion,
    plot_metrics_and_confusion_proportional,
    plot_roc_curve,
    plot_precision_recall_curve
)
from src.metrics import ConfusionMatrix, cost
from src.utils import validate_costs


def calcular_metricas(cm: ConfusionMatrix) -> dict:
    vp, fn, fp, vn = cm.vp, cm.fn, cm.fp, cm.vn
    total = vp + fn + fp + vn

    acuracia = (vp + vn) / total if total > 0 else 0
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0
    recall = vp / (vp + fn) if (vp + fn) > 0 else 0
    f1 = 2 * (precisao * recall) / (precisao + recall) if (precisao + recall) > 0 else 0

    return {
        "acuracia": acuracia,
        "precisao": precisao,
        "recall": recall,
        "f1": f1
    }


def plot_confusion_dashboard(
    cm: ConfusionMatrix,
    layout: str = "legend",
    cost_fp: Optional[float] = None,
    cost_fn: Optional[float] = None,
    save_path: Optional[str] = None,
    y_true: Optional[List[int]] = None,
    y_scores: Optional[List[float]] = None
) -> None:
    """
    Gera visualizações da matriz de confusão e métricas do modelo com diferentes layouts.
    """

    if cost_fp is not None and cost_fn is not None:
        validate_costs(cost_fp, cost_fn)
        total_cost = cost(cm, cost_fp, cost_fn)
        print(f"Custo total (FP={cost_fp}, FN={cost_fn}): R$ {total_cost:,.2f}")

    if layout == "legend":
        plot_metrics_confusion_with_legend(cm, save_path)

    elif layout == "basic":
        plot_metrics_and_confusion(cm, save_path)

    elif layout == "proportional":
        plot_metrics_and_confusion_proportional(cm, save_path)

    elif layout == "roc":
        if y_true and y_scores:
            plot_roc_curve(y_true, y_scores)
        else:
            print("⚠️ y_true e y_scores são necessários para curva ROC.")

    elif layout == "pr_curve":
        if y_true and y_scores:
            plot_precision_recall_curve(y_true, y_scores)
        else:
            print("⚠️ y_true e y_scores são necessários para curva Precision-Recall.")

    elif layout == "dashboard":
        m = calcular_metricas(cm)
        matriz = np.array([[cm.vp, cm.fn], [cm.fp, cm.vn]])

        plt.figure(figsize=(10, 6))

        ax = plt.subplot(121)
        sns.heatmap(
            matriz,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["Positivo", "Negativo"],
            yticklabels=["Positivo", "Negativo"]
        )
        plt.title("🔍 Matriz de Confusão")
        plt.xlabel("Previsto")
        plt.ylabel("Real")

        ax2 = plt.subplot(122)
        ax2.axis("off")
        texto = f"""
        ✅ Métricas do Modelo

        Acurácia:  {m['acuracia']:.2%}
        Precisão:  {m['precisao']:.2%}
        Recall:    {m['recall']:.2%}
        F1-Score:  {m['f1']:.2%}

        Custo FP:  R$ {cost_fp if cost_fp else 0:.2f}
        Custo FN:  R$ {cost_fn if cost_fn else 0:.2f}
        """
        ax2.text(
            0, 0.5, texto,
            fontsize=12,
            va="center",
            fontfamily="monospace",
            bbox=dict(facecolor="#f4f4f4", edgecolor="#ccc", boxstyle="round,pad=1")
        )

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300)
            print(f"📊 Painel com matriz e métricas salvo em: {save_path}")
        plt.close()

    else:
        raise ValueError(f"❌ Layout '{layout}' não reconhecido.")


def plot_comparativo_dashboard(
    cm1: ConfusionMatrix,
    cm2: ConfusionMatrix,
    nome1: str = "Modelo A",
    nome2: str = "Modelo B",
    cost_fp: Optional[float] = None,
    cost_fn: Optional[float] = None,
    save_path: Optional[str] = None
) -> None:
    """
    Gera um painel comparativo entre dois modelos com matriz de confusão e métricas.
    """

    m1 = calcular_metricas(cm1)
    m2 = calcular_metricas(cm2)

    matriz1 = np.array([[cm1.vp, cm1.fn], [cm1.fp, cm1.vn]])
    matriz2 = np.array([[cm2.vp, cm2.fn], [cm2.fp, cm2.vn]])

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    sns.heatmap(matriz1, annot=True, fmt="d", cmap="Blues", ax=axes[0, 0])
    axes[0, 0].set_title(f"Matriz - {nome1}")
    axes[0, 0].set_xlabel("Previsto")
    axes[0, 0].set_ylabel("Real")

    sns.heatmap(matriz2, annot=True, fmt="d", cmap="Greens", ax=axes[0, 1])
    axes[0, 1].set_title(f"Matriz - {nome2}")
    axes[0, 1].set_xlabel("Previsto")
    axes[0, 1].set_ylabel("Real")

    texto1 = f"""
    {nome1}
    Acurácia: {m1['acuracia']:.2%}
    Precisão: {m1['precisao']:.2%}
    Recall:   {m1['recall']:.2%}
    F1-Score: {m1['f1']:.2%}
    Custo FP: R$ {cm1.fp * cost_fp:.2f}
    Custo FN: R$ {cm1.fn * cost_fn:.2f}
    """
    axes[1, 0].axis("off")
    axes[1, 0].text(0, 0.5, texto1, fontsize=11, va="center", fontfamily="monospace")

    texto2 = f"""
    {nome2}
    Acurácia: {m2['acuracia']:.2%}
    Precisão: {m2['precisao']:.2%}
    Recall:   {m2['recall']:.2%}
    F1-Score: {m2['f1']:.2%}
    Custo FP: R$ {cm2.fp * cost_fp:.2f}
    Custo FN: R$ {cm2.fn * cost_fn:.2f}
    """
    axes[1, 1].axis("off")
    axes[1, 1].text(0, 0.5, texto2, fontsize=11, va="center", fontfamily="monospace")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"📊 Painel comparativo salvo em: {save_path}")
    plt.close()
