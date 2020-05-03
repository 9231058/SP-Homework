# In The Name of God
# =======================================
# [] File Name : p7-3-2.py
#
# [] Creation Date : 26-04-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================

from ortools.linear_solver import pywraplp


class Model:
    def __init__(self, name, h1, h2):
        self.name = name
        self.variables = []

        # Create the linear solver with the GLOP backend.
        self.solver = pywraplp.Solver("p7_3", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

        x1 = self.solver.NumVar(0, self.solver.infinity(), "x_1")
        x2 = self.solver.NumVar(0, self.solver.infinity(), "x_2")
        self.variables.extend([x1, x2])

        ct = self.solver.Constraint(0, 7)
        ct.SetCoefficient(x1, 1)
        ct.SetCoefficient(x2, 1)

        y1s = self.solver.NumVar(0, self.solver.infinity(), "y_1_s")
        y2s = self.solver.NumVar(0, h2, "y_2_s")
        self.variables.extend([y1s, y2s])

        ct = self.solver.Constraint(h1, self.solver.infinity())
        ct.SetCoefficient(y1s, 1)
        ct.SetCoefficient(y2s, 2)

        ct = self.solver.Constraint(0, self.solver.infinity())
        ct.SetCoefficient(x1, 1)
        ct.SetCoefficient(y1s, -1)

        ct = self.solver.Constraint(0, self.solver.infinity())
        ct.SetCoefficient(x2, 1)
        ct.SetCoefficient(y2s, -1)

        y1r = self.solver.NumVar(0, self.solver.infinity(), "y_1_r")
        y2r = self.solver.NumVar(0, 3, "y_2_r")
        self.variables.extend([y1r, y2r])

        ct = self.solver.Constraint(7, self.solver.infinity())
        ct.SetCoefficient(y1r, 1)
        ct.SetCoefficient(y2r, 2)

        ct = self.solver.Constraint(0, self.solver.infinity())
        ct.SetCoefficient(x1, 1)
        ct.SetCoefficient(y1r, -1)

        ct = self.solver.Constraint(0, self.solver.infinity())
        ct.SetCoefficient(x2, 1)
        ct.SetCoefficient(y2r, -1)

        self.objective = self.solver.Objective()
        self.objective.SetCoefficient(x1, 2)
        self.objective.SetCoefficient(x2, 1)

        self.objective.SetCoefficient(y1r, -3 * (1 / 3))
        self.objective.SetCoefficient(y2r, -4 * (1 / 3))

        self.objective.SetMinimization()

    def solve(self):
        self.solver.Solve()

        print(f"{self.name:=^25}")
        print("Solution:")
        print("Objective value =", self.objective.Value())
        for v in self.variables:
            print(f"{v.name()}: {v.solution_value()}")

        return self.objective.Value()


if __name__ == "__main__":
    m = Model("pair", 3, 2)
    print(m.solve())

    spev = 0.0
    for ps, (h1, h2) in [(1 / 3, (5, 3)), (1 / 3, (3, 2))]:
        m = Model(f"(r, ({h1}, {h2}))", h1, h2)
        spev += ps * m.solve()

    spev *= 1 / (1 - 1 / 3)
    print(f"SPEV = {spev}")
