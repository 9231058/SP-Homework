# In The Name of God
# =======================================
# [] File Name : p7-3-1.py
#
# [] Creation Date : 26-04-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================

from ortools.linear_solver import pywraplp


class Model:
    def __init__(self, name, h1, h2, x1, x2):
        self.name = name
        self.variables = []

        # Create the linear solver with the GLOP backend.
        self.solver = pywraplp.Solver("p7_3", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

        x1 = self.solver.NumVar(x1, x1, "x_1")
        x2 = self.solver.NumVar(x2, x2, "x_2")
        self.variables.extend([x1, x2])

        ct = self.solver.Constraint(0, 7)
        ct.SetCoefficient(x1, 1)
        ct.SetCoefficient(x2, 1)

        y1 = self.solver.NumVar(0, self.solver.infinity(), "y_1")
        y2 = self.solver.NumVar(0, h2, "y_2")
        self.variables.extend([y1, y2])

        ct = self.solver.Constraint(h1, self.solver.infinity())
        ct.SetCoefficient(y1, 1)
        ct.SetCoefficient(y2, 2)

        ct = self.solver.Constraint(0, self.solver.infinity())
        ct.SetCoefficient(x1, 1)
        ct.SetCoefficient(y1, -1)

        ct = self.solver.Constraint(0, self.solver.infinity())
        ct.SetCoefficient(x2, 1)
        ct.SetCoefficient(y2, -1)

        self.objective = self.solver.Objective()
        self.objective.SetCoefficient(x1, 2)
        self.objective.SetCoefficient(x2, 1)

        self.objective.SetCoefficient(y1, -3)
        self.objective.SetCoefficient(y2, -4)

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
    evrs = 0

    for h1, h2 in [(3, 2), (5, 3), (7, 3)]:
        m = Model(f"({h1}, {h2})", h1, h2, 4, 3)
        optimal = m.solve()
        evrs += 1 / 3 * optimal
    print(evrs)
