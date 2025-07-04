from copy import deepcopy
from typing import Self


class Equation:
    def __init__(self, lhs: list[float], rhs: float):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        deg = len(self.lhs)
        return (
            " + ".join(f"{self.lhs[i]}a_{deg - i}" for i in range(deg))
            + " = "
            + str(self.rhs)
        )

    def __mul__(self, other: float):
        return Equation(
            [p for e in self.lhs if (p := e * other) != 0], self.rhs * other
        )

    def __sub__(self, other: Self):
        slen = len(self.lhs)
        olen = len(other.lhs)
        return Equation(
            [
                res
                for i in range(max(slen, olen))
                if (
                    res := (self.lhs[i] if i < slen else 0)
                    - (other.lhs[i] if i < olen else 0)
                )
                != 0
            ],
            self.rhs - other.rhs,
        )


points = [
    (4, 20),
    (6, 9),
    (69, 420),
    (420, 69),
    (42069, 69420),
    (69420, 42069),
]

degree = len(points)

equations = []

# leave as loop for conditional point selection
for x, y in points:
    equations.append(Equation([x**i for i in range(degree, 0, -1)], y))

old_collapsed = deepcopy(equations)
new_collapsed = []

while len(old_collapsed) > 1:
    for i in range(len(old_collapsed) - 1):
        eqn_l, eqn_r = old_collapsed[i], old_collapsed[i + 1]
        factor = eqn_r.lhs[0] / eqn_l.lhs[0]
        eqn_mul = eqn_l * factor
        eqn_new = eqn_r - eqn_mul
        # correct for floating point errors
        if len(eqn_new.lhs) == len(eqn_r.lhs):
            eqn_new.lhs = eqn_new.lhs[1:]
        new_collapsed.append(eqn_new)
    old_collapsed = deepcopy(new_collapsed)
    equations.extend(new_collapsed)
    new_collapsed.clear()

root_eqn = old_collapsed[0]
coeffs = [root_eqn.rhs / root_eqn.lhs[0]]

i = len(equations) - 1
last_len = 1

while i > 0:
    if len(equations[i].lhs) <= last_len:
        i -= 1
        continue
    eqn = equations[i]
    lhs = eqn.lhs
    rhs = eqn.rhs
    n = len(lhs)
    for j in range(len(coeffs)):
        cidx = n - (j + 1)
        rhs -= lhs[cidx] * coeffs[j]
    new_coeff = rhs / lhs[0]
    coeffs.append(new_coeff)
    last_len = n

coeffs.reverse()

print(
    "f(x) = "
    + "".join(
        f"{" + " if i>0 and coeff>0 else " - " if i>0 and coeff<0 else "-" if coeff<0 else ""}{abs(coeff)}x{f"^{degree - i}" if degree - i > 1 else ""}"
        for i, coeff in enumerate(coeffs)
    )
)
