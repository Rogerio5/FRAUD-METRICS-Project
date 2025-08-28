# -*- coding: utf-8 -*-
import os
from datetime import datetime

from src.scenario3 import scenario3_report
from src.scenario_company import y_true_company, y_scores_company
from src.visualize import plot_confusion_dashboard
from src.visualize_company import visualize_company
from src.simulacao import simular_custos
from src.metrics import ConfusionMatrix

def gerar_dashboard_cenario3():
    cm = ConfusionMatrix(vp=90, fn=10, fp=30, vn=8000)
    plot_confusion_dashboard(
        cm=cm,
        layout="dashboard",
        cost_fp=10,
        cost_fn=5,
        save_path="output/dashboard.png"
    )
    print("✅ Dashboard do Cenário 3 gerado.")

def gerar_curva_empresa():
    visualize_company(
        y_true=y_true_company,
        y_scores=y_scores_company,
        name="DetectorFraudeCorp",
        save_path="output/curva_precision_recall_empresa.png"
    )
    print("✅ Curva Precisão-Recall da empresa gerada.")

def gerar_simulacao_custos():
    cm = ConfusionMatrix(vp=90, fn=10, fp=30, vn=8000)
    print("\n💸 Simulando custos com matriz de confusão...")
    resultado = simular_custos(cm)
    print("\n🔍 Top 5 cenários mais econômicos:\n")
    print(resultado)
    return resultado

def gerar_relatorio_html(resultado_simulacao: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    html_path = f"output/relatorio_{timestamp}.html"

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Métricas</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 40px;
                background-color: #fdfdfd;
                color: #333;
            }}
            h1 {{
                color: #2a9d8f;
                border-bottom: 2px solid #ccc;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #264653;
                margin-top: 40px;
            }}
            .metricas {{
                background: #f4f4f4;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.05);
            }}
            pre {{
                background: #eee;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            img {{
                max-width: 100%;
                height: auto;
                border: 1px solid #ddd;
                border-radius: 6px;
                box-shadow: 0 0 8px rgba(0,0,0,0.1);
            }}
            footer {{
                margin-top: 60px;
                font-size: 0.9em;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>📊 Relatório de Métricas</h1>

        <div class="metricas">
            <h2>🔍 Cenário 3</h2>
            <pre>{scenario3_report(cost_fp=10, cost_fn=5)}</pre>
        </div>

        <h2>🖼️ Dashboard de Métricas</h2>
        <img src="dashboard.png" alt="Dashboard de Métricas">

        <h2>📈 Curva Precisão-Recall</h2>
        <img src="curva_precision_recall_empresa.png" alt="Curva Precisão-Recall">

        <h2>💸 Simulação de Custos</h2>
        <pre>{resultado_simulacao}</pre>
        <img src="simulacao_custos.png" alt="Heatmap de Simulação de Custos">

        <footer>
            Relatório gerado automaticamente por DetectorFraudeCorp &mdash; {os.path.basename(__file__)}
        </footer>
    </body>
    </html>
    """
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n📝 Relatório HTML salvo em: {html_path}")

def main():
    os.makedirs("output", exist_ok=True)

    print("\n📊 Gerando relatório do Cenário 3...")
    print(scenario3_report(cost_fp=10, cost_fn=5))

    gerar_dashboard_cenario3()
    gerar_curva_empresa()
    resultado_simulacao = gerar_simulacao_custos()
    gerar_relatorio_html(resultado_simulacao)

    print("\n✅ Tudo executado com sucesso!")

if __name__ == "__main__":
    main()
