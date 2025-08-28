from src.metrics import ConfusionMatrix, summary, cost

CENARIO3 = ConfusionMatrix(vp=90, fn=10, fp=30, vn=8000)

def format_percent(x: float, digits: int = 2) -> str:
    return f"{x*100:.{digits}f}%"

def scenario3_report(cost_fp: float | None = None, cost_fn: float | None = None) -> str:
    cm = CENARIO3
    s = summary(cm)
    lines = [
        "Cenário 3 — Matriz de Confusão: VP=90, FN=10, FP=30, VN=8000",
        f"- Acurácia: {format_percent(s['accuracy'])}",
        f"- Precisão: {format_percent(s['precision'])}",
        f"- Recall: {format_percent(s['recall'])}",
        f"- Especificidade: {format_percent(s['specificity'])}",
        f"- F1-Score: {format_percent(s['f1'])}",
        f"- Prevalência: {format_percent(s['prevalence'], 3)}",
        f"- Acurácia Balanceada: {format_percent(s['balanced_accuracy'])}",
        f"- MCC: {s['mcc']:.3f}"
    ]
    if cost_fp is not None and cost_fn is not None:
        total_cost = cost(cm, cost_fp, cost_fn)
        lines.append(f"- Custo total (FP={cost_fp}, FN={cost_fn}): {total_cost:,.2f}")
    return "\n".join(lines)
