from core.matrix import Matrix
from core.linalg import transpose, matmul, determinant, inverse

def test_transpose():
    A = Matrix([[1,2,3],[4,5,6]])
    AT = transpose(A)
    assert AT.shape() == (3,2)
    assert AT == Matrix([[1,4],[2,5],[3,6]])

def test_det_and_inverse():
    A = Matrix([[4,7],[2,6]])
    detA = determinant(A)
    assert abs(detA - 10.0) < 1e-9
    invA = inverse(A)
    # A * A^{-1} ≈ I
    I = matmul(A, invA)
    assert I == Matrix([[1,0],[0,1]])
