# In The Name of God
# =======================================
# [] File Name : p20-2.py
#
# [] Creation Date : 23-04-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================


from ortools.linear_solver import pywraplp


class Model:
    def __init__(self):
        self.variables = []

        # Create the linear solver with the GLOP backend.
        self.solver = pywraplp.Solver("p20_2", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

        self.x1 = self.solver.NumVar(0, 12, "x_1")
        self.x2 = self.solver.NumVar(0, 24, "x_2")
        self.x3 = self.solver.NumVar(0, 140, "x_3")
        self.variables.extend([self.x1, self.x2, self.x3])

        self.objective = self.solver.Objective()

        self.objective.SetMaximization()

    def scenario(self, index, p, probability):
        self.objective.SetCoefficient(
            self.x1, (3 * p - (1 - p) * 1.5 * 3) * probability
        )
        self.objective.SetCoefficient(
            self.x2, (2 * p - (1 - p) * 1.5 * 2) * probability
        )
        self.objective.SetCoefficient(
            self.x3, (1 * p - (1 - p) * 1.5 * 1) * probability
        )

    def solve(self):
        self.solver.Solve()

        print("Solution:")
        print("Objective value =", self.objective.Value())
        for v in self.variables:
            print(f"{v.name()}: {v.solution_value()}")

        return self.objective.Value()


if __name__ == "__main__":
    mda = Model()
    mda.scenario(1, 100, 0.5)
    mda.scenario(2, 90, 0.25)
    mda.scenario(3, 80, 0.25)

    print(mda.solver.ExportModelAsLpFormat(False))
    print()

    print(mda.solve())
