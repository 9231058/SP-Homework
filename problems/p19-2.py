# In The Name of God
# =======================================
# [] File Name : p19-2.py
#
# [] Creation Date : 19-04-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================

from ortools.linear_solver import pywraplp


class Model:
    def __init__(self):
        self.variables = []

        # Create the linear solver with the GLOP backend.
        self.solver = pywraplp.Solver("p19_2", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

        self.x1 = self.solver.NumVar(0, self.solver.infinity(), "x_1")
        self.x2 = self.solver.NumVar(0, self.solver.infinity(), "x_2")
        self.x3 = self.solver.NumVar(0, self.solver.infinity(), "x_3")
        self.variables.extend([self.x1, self.x2, self.x3])

        ct = self.solver.Constraint(0, 200, "airplane_capacity_constraint")
        ct.SetCoefficient(self.x1, 2)
        ct.SetCoefficient(self.x2, 1.5)
        ct.SetCoefficient(self.x3, 1)

        self.objective = self.solver.Objective()

        self.objective.SetMaximization()

    def scenario(self, index, th1, th2, th3, probability):
        y1 = self.solver.NumVar(0, th1, f"y_1_s{index}")
        y2 = self.solver.NumVar(0, th2, f"y_2_s{index}")
        y3 = self.solver.NumVar(0, th3, f"y_3_s{index}")

        self.variables.extend([y1, y2, y3])

        ct = self.solver.Constraint(
            0, self.solver.infinity(), f"seat_constraint_s{index}"
        )
        ct.SetCoefficient(self.x1, 1)
        ct.SetCoefficient(y1, -1)

        ct = self.solver.Constraint(
            0, self.solver.infinity(), f"seat_constraint_s{index}"
        )
        ct.SetCoefficient(self.x2, 1)
        ct.SetCoefficient(y2, -1)

        ct = self.solver.Constraint(
            0, self.solver.infinity(), f"seat_constraint_s{index}"
        )
        ct.SetCoefficient(self.x3, 1)
        ct.SetCoefficient(y3, -1)

        self.objective.SetCoefficient(y1, 3 * probability)
        self.objective.SetCoefficient(y2, 2 * probability)
        self.objective.SetCoefficient(y3, 1 * probability)

    def solve(self):
        self.solver.Solve()

        print("Solution:")
        print("Objective value =", self.objective.Value())
        for v in self.variables:
            print(f"{v.name()}: {v.solution_value()}")

        return self.objective.Value()


if __name__ == "__main__":
    mda = Model()
    mda.scenario(1, 20, 50, 200, 1 / 3)
    mda.scenario(2, 10, 25, 175, 1 / 3)
    mda.scenario(3, 5, 10, 150, 1 / 3)

    print(mda.solver.ExportModelAsLpFormat(False))
    print()

    mda.solve()
