from __future__ import annotations
from typing import Iterable
from ..matrix import Matrix

def print_matrix(m: Matrix | Iterable[Iterable[float]], floatfmt: str = ".4f") -> None:
    """
    Pretty print matriks ke stdout. Untuk Flask nanti, pakai tabel HTML, bukan ini.
    """
    if isinstance(m, Matrix):
        rows = m.data
    else:
        rows = [list(r) for r in m]
    # hitung lebar kolom
    cols = max(len(r) for r in rows)
    col_widths = [0] * cols
    tmp = []
    for r in rows:
        line = [format(v, floatfmt) for v in r]
        tmp.append(line)
        for j, s in enumerate(line):
            col_widths[j] = max(col_widths[j], len(s))
    for line in tmp:
        cells = [s.rjust(col_widths[j]) for j, s in enumerate(line)]
        print("[ " + "  ".join(cells) + " ]")
