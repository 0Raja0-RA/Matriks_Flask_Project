from .matrix import Matrix

def add_intercept(X: Matrix) -> Matrix:
    # tambahkan kolom 1 di depan: [1, x1, x2, ...]
    return Matrix([[1.0] + row for row in X.to_list()])
