from __future__ import annotations
from typing import List, Iterable
from math import isclose

Number = float

class Matrix:
    """
    Representasi matriks sederhana berbasis list of lists.
    - Menjamin semua baris punya jumlah kolom sama.
    - Data disimpan sebagai float untuk konsistensi operasi linalg.
    """

    def __init__(self, data: Iterable[Iterable[Number]]):
        rows = [list(map(float, row)) for row in data]
        if not rows:
            raise ValueError("Matrix tidak boleh kosong.")
        cols = len(rows[0])
        if cols == 0:
            raise ValueError("Matrix harus memiliki setidaknya 1 kolom.")
        for r in rows:
            if len(r) != cols:
                raise ValueError("Semua baris harus memiliki jumlah kolom yang sama.")
        self.data: List[List[float]] = rows
        self.rows: int = len(rows)
        self.cols: int = cols

    def copy(self) -> "Matrix":
        return Matrix([row[:] for row in self.data])

    def shape(self) -> tuple[int, int]:
        return (self.rows, self.cols)

    def is_square(self) -> bool:
        return self.rows == self.cols

    def to_list(self) -> List[List[float]]:
        return [row[:] for row in self.data]

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        if len(value) != self.cols:
            raise ValueError("Panjang baris tidak cocok.")
        self.data[idx] = list(map(float, value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix) or self.shape() != other.shape():
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if not isclose(self.data[i][j], other.data[i][j], rel_tol=1e-9, abs_tol=1e-8):
                    return False
        return True


    def __repr__(self) -> str:
        return f"Matrix({self.data!r})"

    def __str__(self) -> str:
        return "\n".join(str(row) for row in self.data)
