from __future__ import annotations
from typing import List, Tuple
from .matrix import Matrix

_EPS = 1e-12

def transpose(A: Matrix) -> Matrix:
    r, c = A.shape()
    return Matrix([[A.data[i][j] for i in range(r)] for j in range(c)])

def matmul(A: Matrix, B: Matrix) -> Matrix:
    if A.cols != B.rows:
        raise ValueError("Dimensi tidak cocok untuk perkalian.")
    out = [[0.0] * B.cols for _ in range(A.rows)]
    # triple loop klasik
    for i in range(A.rows):
        Ai = A.data[i]
        for k in range(A.cols):
            aik = Ai[k]
            Bk = B.data[k]
            for j in range(B.cols):
                out[i][j] += aik * Bk[j]
    return Matrix(out)

def _partial_pivot(M: List[List[float]], col: int, start_row: int) -> int:
    # pilih baris dengan nilai absolut terbesar di kolom 'col' mulai dari start_row
    pivot = start_row
    max_val = abs(M[start_row][col])
    for r in range(start_row + 1, len(M)):
        v = abs(M[r][col])
        if v > max_val:
            max_val = v
            pivot = r
    return pivot

def determinant(A: Matrix) -> float:
    if not A.is_square():
        raise ValueError("Determinant hanya untuk matriks bujur sangkar.")
    # salin agar tidak merusak A
    M = [row[:] for row in A.data]
    n = A.rows
    det = 1.0
    sign = 1
    for col in range(n):
        pivot = _partial_pivot(M, col, col)
        if abs(M[pivot][col]) < _EPS:
            return 0.0
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            sign *= -1
        pivot_val = M[col][col]
        det *= pivot_val
        # eliminasi ke bawah
        for r in range(col + 1, n):
            factor = M[r][col] / pivot_val
            if factor != 0.0:
                for k in range(col, n):
                    M[r][k] -= factor * M[col][k]
    return sign * det

def inverse(A: Matrix) -> Matrix:
    if not A.is_square():
        raise ValueError("Inverse hanya untuk matriks bujur sangkar.")
    n = A.rows
    # bentuk [A | I]
    M = [A.data[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    # Gauss-Jordan dengan partial pivot
    for col in range(n):
        pivot = _partial_pivot(M, col, col)
        if abs(M[pivot][col]) < _EPS:
            raise ValueError("Matriks singular (det ~ 0), tidak punya inverse.")
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        # normalisasi baris pivot
        pv = M[col][col]
        inv_pv = 1.0 / pv
        for j in range(2*n):
            M[col][j] *= inv_pv
        # nol-kan kolom lain
        for r in range(n):
            if r == col:
                continue
            factor = M[r][col]
            if factor != 0.0:
                for j in range(2*n):
                    M[r][j] -= factor * M[col][j]
    # ambil sisi kanan jadi inverse
    inv = [row[n:] for row in M]
    return Matrix(inv)

def solve_normal_equation(X: Matrix, y: Matrix) -> Matrix:
    """
    Untuk regresi linear sederhana/umum:
      beta = (X^T X)^(-1) X^T y
    Return: beta (k x 1)
    """
    Xt = transpose(X)
    XtX = matmul(Xt, X)
    XtX_inv = inverse(XtX)
    Xty = matmul(Xt, y)
    return matmul(XtX_inv, Xty)

def predict(X: Matrix, beta: Matrix) -> Matrix:
    return matmul(X, beta)
