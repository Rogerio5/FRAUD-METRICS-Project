from src.visualize import plot_confusion_dashboard
from src.scenario3 import CENARIO3

plot_confusion_dashboard(
    cm=CENARIO3,
    layout="legend",
    cost_fp=10,
    cost_fn=5,
    save_path="output/dashboard.png"
)
