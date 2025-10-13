from .matrix import Matrix

def mse(y_true: Matrix, y_pred: Matrix) -> float:
    n = y_true.rows
    return sum((y_true.data[i][0] - y_pred.data[i][0])**2 for i in range(n)) / n

def r2(y_true: Matrix, y_pred: Matrix) -> float:
    n = y_true.rows
    ybar = sum(r[0] for r in y_true.data) / n
    ss_tot = sum((r[0] - ybar)**2 for r in y_true.data)
    ss_res = sum((y_true.data[i][0] - y_pred.data[i][0])**2 for i in range(n))
    return 1.0 - (ss_res / ss_tot if ss_tot != 0 else 0.0)
