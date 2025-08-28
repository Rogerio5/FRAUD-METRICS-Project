def validate_costs(cost_fp: float, cost_fn: float) -> None:
    if cost_fp < 0 or cost_fn < 0:
        raise ValueError("Os custos FP e FN devem ser positivos.")

