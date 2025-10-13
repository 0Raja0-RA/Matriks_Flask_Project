from __future__ import annotations
import csv
from typing import Iterable, Optional
from .matrix import Matrix

def import_csv(path: str, has_header: bool = True, sep: str = ",") -> Matrix:
    rows = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=sep)
        for i, row in enumerate(reader):
            if i == 0 and has_header:
                continue
            if not row:
                continue
            rows.append([float(x) for x in row])
    return Matrix(rows)

def export_csv(m: Matrix, path: str, include_header: bool = False, header: Optional[Iterable[str]] = None, sep: str = ",", floatfmt: str = ".6f") -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=sep)
        if include_header:
            if header is None:
                header = [f"c{j+1}" for j in range(m.cols)]
            writer.writerow(list(header))
        for row in m.data:
            writer.writerow([format(val, floatfmt) for val in row])

def load_xy_by_columns(path: str, x_cols: list[str], y_col: str, sep: str = ","):
    import csv
    from .matrix import Matrix
    rows = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=sep)
        for r in reader:
            rows.append(r)
    if not rows:
        raise ValueError("CSV kosong atau hanya header.")
    X, y = [], []
    for r in rows:
        X.append([float(r[c]) for c in x_cols])
        y.append([float(r[y_col])])
    return Matrix(X), Matrix(y)
