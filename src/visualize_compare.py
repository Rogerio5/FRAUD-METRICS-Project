# -*- coding: utf-8 -*-
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    roc_curve,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score
)

from src.metrics import summary, ConfusionMatrix

# 🔹 Gráfico de métricas + matriz de confusão
def plot_metrics_and_confusion(cm: ConfusionMatrix, save_path: str | None = None) -> None:
    s = summary(cm)
    keys = ["accuracy", "precision", "recall", "specificity", "f1", "balanced_accuracy"]
    vals = [s[k] for k in keys]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico de barras
    bars = axes[0].bar(keys, vals, color="#2a9d8f")
    axes[0].set_ylim(0, 1.0)
    axes[0].set_title("Métricas — Cenário")
    axes[0].set_ylabel("Valor (0–1)")
    for b, v in zip(bars, vals):
        axes[0].text(b.get_x() + b.get_width() / 2, v + 0.01, f"{v:.3f}", ha="center", va="bottom")

    # Matriz de confusão
    matrix = np.array([[cm.vp, cm.fn], [cm.fp, cm.vn]])
    labels = [["VP", "FN"], ["FP", "VN"]]
    axes[1].imshow(matrix, cmap="Blues")
    for (i, j), val in np.ndenumerate(matrix):
        axes[1].text(j, i, f"{labels[i][j]}\n{val}", ha="center", va="center")
    axes[1].set_title("Matriz de Confusão")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

# 🔹 Matriz de confusão proporcional
def plot_metrics_and_confusion_proportional(cm: ConfusionMatrix, save_path: str | None = None) -> None:
    matrix = np.array([[cm.vp, cm.fn], [cm.fp, cm.vn]])
    total = matrix.sum()
    fig, ax = plt.subplots(figsize=(5, 5))
    colors = [["#a7e9af", "#ffb3b3"], ["#ffb3b3", "#a7e9af"]]

    y_pos = 0
    for i in range(2):
        row_total = matrix[i, :].sum()
        row_height = row_total / total
        x_pos = 0
        for j in range(2):
            col_width = matrix[i, j] / row_total if row_total > 0 else 0
            ax.add_patch(plt.Rectangle((x_pos, y_pos), col_width, row_height, color=colors[i][j], alpha=0.8))
            ax.text(
                x_pos + col_width / 2,
                y_pos + row_height / 2,
                f"{matrix[i, j]}\n({matrix[i, j] / total * 100:.1f}%)",
                ha="center", va="center", fontsize=12, fontweight="bold"
            )
            x_pos += col_width
        y_pos += row_height

    ax.axis("off")
    if save_path:
        plt.savefig(save_path)
    plt.show()

# 🔹 Métricas com legenda + matriz com escala
def plot_metrics_confusion_with_legend(cm: ConfusionMatrix, save_path: str | None = None) -> None:
    s = summary(cm)
    keys = ["accuracy", "precision", "recall", "specificity", "f1", "balanced_accuracy"]
    vals = [s[k] for k in keys]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico de barras
    bars = axes[0].bar(keys, vals, color="#4a90e2")
    axes[0].set_ylim(0, 1.0)
    axes[0].set_title("Métricas com Legenda")
    axes[0].set_ylabel("Valor (0–1)")
    for b, v in zip(bars, vals):
        axes[0].text(b.get_x() + b.get_width() / 2, v + 0.01, f"{v:.3f}", ha="center")

    # Matriz com legenda de escala
    matrix = np.array([[cm.vp, cm.fn], [cm.fp, cm.vn]])
    labels = [["VP", "FN"], ["FP", "VN"]]
    cax = axes[1].imshow(matrix, cmap="Blues")
    for (i, j), val in np.ndenumerate(matrix):
        axes[1].text(j, i, f"{labels[i][j]}\n{val}", ha="center", va="center", color="black")
    axes[1].set_title("Matriz de Confusão")
    plt.colorbar(cax, ax=axes[1], fraction=0.046, pad=0.04, label="Quantidade")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

# 🔹 Curva ROC
def plot_roc_curve(y_true: list[int], y_scores: list[float]) -> None:
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    auc = roc_auc_score(y_true, y_scores)

    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}", color="#e76f51")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlabel("Taxa de Falsos Positivos")
    plt.ylabel("Taxa de Verdadeiros Positivos")
    plt.title("Curva ROC")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 🔹 Curva Precisão-Recall com AP
def plot_precision_recall_curve(y_true: list[int], y_scores: list[float], name: str = "Modelo") -> None:
    precision, recall, _ = precision_recall_curve(y_true, y_scores)
    avg_precision = average_precision_score(y_true, y_scores)

    plt.figure(figsize=(6, 6))
    plt.plot(recall, precision, label=f"{name} (AP={avg_precision:.2f})", color="#2a9d8f")
    plt.xlabel("Recall")
    plt.ylabel("Precisão")
    plt.title("Curva Precisão-Recall")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
