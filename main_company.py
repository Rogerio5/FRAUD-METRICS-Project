from src.visualize_company import visualize_company
from src.scenario_company import y_true_company, y_scores_company

visualize_company(
    y_true=y_true_company,
    y_scores=y_scores_company,
    name="DetectorFraudeCorp",
    save_path="output/curva_precision_recall_empresa.png"
)
