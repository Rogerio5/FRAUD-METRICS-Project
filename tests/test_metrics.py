from src.metrics import ConfusionMatrix, accuracy, precision, recall, specificity, f1

def test_scenario3_values():
    cm = ConfusionMatrix(90, 10, 30, 8000)
    assert round(accuracy(cm), 4) == round(8090/8130, 4)
    assert precision(cm) == 0.75
    assert recall(cm) == 0.90
    assert round(specificity(cm), 4) == round(8000/8030, 4)
    assert round(f1(cm), 4) == 0.8182
