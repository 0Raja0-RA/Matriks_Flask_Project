import os, tempfile
from core.matrix import Matrix
from core.io_csv import import_csv, export_csv

def test_csv_roundtrip():
    m = Matrix([[1.5, 2.0], [3.25, 4.75]])
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "m.csv")
        export_csv(m, p, include_header=True, header=["a","b"])
        m2 = import_csv(p, has_header=True)
        assert m == m2
