from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Dict

# 📊 Classe principal
@dataclass(frozen=True)
class ConfusionMatrix:
    vp: int  # Verdadeiro Positivo
    fn: int  # Falso Negativo
    fp: int  # Falso Positivo
    vn: int  # Verdadeiro Negativo

    def totals(self) -> Tuple[int, int, int]:
        """
        Retorna (positivos, negativos, total de amostras).
        """
        positivos = self.vp + self.fn
        negativos = self.vn + self.fp
        total = positivos + negativos
        return positivos, negativos, total

    def to_dict(self) -> Dict[str, int]:
        """
        Exporta os valores da matriz como dicionário.
        """
        return {
            "VP": self.vp,
            "FN": self.fn,
            "FP": self.fp,
            "VN": self.vn
        }

# 🧮 Função auxiliar
def _safe_div(num: float, den: float) -> float:
    """
    Evita divisão por zero.
    """
    return num / den if den != 0 else 0.0

# 📈 Métricas principais
def accuracy(cm: ConfusionMatrix) -> float:
    """Acurácia: (VP + VN) / Total"""
    return _safe_div(cm.vp + cm.vn, cm.vp + cm.fn + cm.fp + cm.vn)

def precision(cm: ConfusionMatrix) -> float:
    """Precisão: VP / (VP + FP)"""
    return _safe_div(cm.vp, cm.vp + cm.fp)

def recall(cm: ConfusionMatrix) -> float:
    """Sensibilidade: VP / (VP + FN)"""
    return _safe_div(cm.vp, cm.vp + cm.fn)

def specificity(cm: ConfusionMatrix) -> float:
    """Especificidade: VN / (VN + FP)"""
    return _safe_div(cm.vn, cm.vn + cm.fp)

def f1(cm: ConfusionMatrix) -> float:
    """F1 Score: média harmônica entre precisão e recall"""
    p = precision(cm)
    r = recall(cm)
    return _safe_div(2 * p * r, p + r)

def prevalence(cm: ConfusionMatrix) -> float:
    """Prevalência: proporção de positivos no total"""
    positivos, _, total = cm.totals()
    return _safe_div(positivos, total)

def balanced_accuracy(cm: ConfusionMatrix) -> float:
    """Acurácia balanceada: média entre recall e especificidade"""
    return (recall(cm) + specificity(cm)) / 2

def mcc(cm: ConfusionMatrix) -> float:
    """Coeficiente de Correlação de Matthews"""
    num = (cm.vp * cm.vn) - (cm.fp * cm.fn)
    den = ((cm.vp + cm.fp) * (cm.vp + cm.fn) * (cm.vn + cm.fp) * (cm.vn + cm.fn)) ** 0.5
    return _safe_div(num, den)

# 💰 Custo operacional
def cost(cm: ConfusionMatrix, cost_fp: float, cost_fn: float) -> float:
    """
    Calcula o custo total com base nos pesos de FP e FN.
    """
    return cm.fp * cost_fp + cm.fn * cost_fn

# 📋 Resumo completo
def summary(cm: ConfusionMatrix) -> Dict[str, float]:
    """
    Retorna todas as métricas principais como dicionário.
    """
    return {
        "accuracy": accuracy(cm),
        "precision": precision(cm),
        "recall": recall(cm),
        "specificity": specificity(cm),
        "f1": f1(cm),
        "prevalence": prevalence(cm),
        "balanced_accuracy": balanced_accuracy(cm),
        "mcc": mcc(cm),
    }
