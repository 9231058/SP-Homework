# In The Name of God
# =======================================
# [] File Name : p2-1.py
#
# [] Creation Date : 5-04-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================
from ortools.linear_solver import pywraplp


class Model:
    def __init__(self, name):
        self.name = name
        self.variables = []

        # Create the linear solver with the GLOP backend.
        self.solver = pywraplp.Solver("p4_2", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

        self.x1 = self.solver.NumVar(0, self.solver.infinity(), "x_1")
        self.y1 = self.solver.NumVar(0, self.solver.infinity(), "y_1")
        self.variables.extend([self.x1, self.y1])

        ct = self.solver.Constraint(100, 100, "first_year_demand")
        ct.SetCoefficient(self.x1, 1)
        ct.SetCoefficient(self.y1, -1)

        ct = self.solver.Constraint(0, 90, "storage")
        ct.SetCoefficient(self.y1, 1)

        self.objective = self.solver.Objective()
        self.objective.SetCoefficient(self.x1, 5)
        self.objective.SetCoefficient(self.y1, 1.5)

        self.objective.SetMinimization()

    def scenario(self, index, demand, price, probability):
        x2 = self.solver.NumVar(0, self.solver.infinity(), f"x_2_s{index}")

        self.variables.extend([x2])

        ct = self.solver.Constraint(
            demand, self.solver.infinity(), f"second_year_demand_s{index}"
        )
        ct.SetCoefficient(self.y1, 1)
        ct.SetCoefficient(x2, 1)

        self.objective.SetCoefficient(x2, price * probability)

    def solve(self):
        self.solver.Solve()

        print(f"{self.name:=^25}")
        print("Solution:")
        print("Objective value =", self.objective.Value())
        for v in self.variables:
            print(f"{v.name()}: {v.solution_value()}")

        return self.objective.Value()


if __name__ == "__main__":
    mda = Model("stochastic")
    mda.scenario(1, 100, 5, 1 / 3)
    mda.scenario(2, 150, 6, 1 / 3)
    mda.scenario(3, 180, 7.5, 1 / 3)

    print(mda.solver.ExportModelAsLpFormat(False))
    print()

    stochastic = mda.solve()
