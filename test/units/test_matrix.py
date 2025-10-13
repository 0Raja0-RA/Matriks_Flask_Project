from core.matrix import Matrix

def test_construct_and_shape():
    m = Matrix([[1,2],[3,4]])
    assert m.shape() == (2,2)
    assert m.is_square()

def test_equality_with_tolerance():
    m1 = Matrix([[1.000000001]])
    m2 = Matrix([[1.0]])
    assert m1 == m2
