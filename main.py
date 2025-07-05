import json
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


with open("points.json") as f:
    points = json.load(f)

zy = 0

for i, (x, y) in enumerate(points):
    if x == 0:
        points.pop(i)
        zy = y
        break

degree = len(points)

equations = []

# leave as loop for conditional point selection
for x, y in points:
    equations.append(Equation([x**i for i in range(degree, 0, -1)], y - zy))

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

expression = ""

for i, coeff in enumerate(coeffs):
    if not coeff:
        continue
    term_str = (
        ("" if coeff > 0 else "-") if not expression else " + " if coeff > 0 else " - "
    )
    power = degree - i
    absv = abs(coeff)
    if absv != 1:
        term_str += str(absv)
    term_str += "x" + (f"^{power}" if power != 1 else "")
    expression += term_str

if zy:
    if not expression:
        expression = str(zy)
    else:
        expression += (" + " if zy > 0 else " - ") + str(abs(zy))

if not expression:
    expression = "0"

print("f(x) =", expression)
