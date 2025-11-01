
import numpy as np
def linear_regression(x, y):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1: raise ValueError("x dan y harus 1D")
    if len(x) != len(y): raise ValueError("panjang x dan y harus sama")
    n = len(x)
    if n < 2: raise ValueError("minimal 2 titik")
    sx, sy = x.sum(), y.sum()
    sxx, sxy = (x*x).sum(), (x*y).sum()
    denom = n*sxx - sx*sx
    if denom == 0: return 0.0, float(y.mean())
    m = (n*sxy - sx*sy)/denom
    c = (sy - m*sx)/n
    return float(m), float(c)
