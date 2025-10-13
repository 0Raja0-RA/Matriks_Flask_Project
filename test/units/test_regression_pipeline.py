from core.matrix import Matrix
from core.features import add_intercept
from core.linalg import solve_normal_equation, predict
from core.metrics import r2, mse

def test_zoo_visitors_pipeline_simple():
    # data mini sintetis: kalau tiket makin murah, pengunjung naik
    X = Matrix([[50],[45],[40],[35],[30]])      # ticket_price
    y = Matrix([[1200],[1500],[1700],[1900],[2100]])  # visitors

    X_i = add_intercept(X)
    beta = solve_normal_equation(X_i, y)  # [a,b]
    yhat = predict(X_i, beta)

    assert beta.rows == 2 and beta.cols == 1
    assert beta.data[1][0] < 0          # slope negatif (harga naik → pengunjung turun)
    assert r2(y, yhat) > 0.9            # fit cukup baik untuk data linear
    assert mse(y, yhat) < 2e4           # MSE kecil (ambang longgar)
