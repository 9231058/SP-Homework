# In The Name of God
# =======================================
# [] File Name : p20-2.py
#
# [] Creation Date : 23-04-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================


from ortools.linear_solver import pywraplp

demands = [
    [(200, 0.2), (220, 0.05), (250, 0.35), (270, 0.2), (300, 0.2)],
    [(50, 0.3), (150, 0.7), (150, 0), (150, 0), (150, 0)],
    [(140, 0.1), (160, 0.2), (180, 0.4), (200, 0.2), (220, 0.1)],
    [(10, 0.2), (50, 0.2), (80, 0.3), (100, 0.2), (340, 0.1)],
    [(580, 0.1), (600, 0.8), (620, 0.1), (620, 0), (620, 0)],
]


class Model:
    airplanes = 4
    ways = 5
    available_airplanes = [10, 19, 25, 15]
    prices = [13, 13, 7, 7, 1]
    capacity = [
        [16, 15, 28, 23, 81],
        [0, 10, 14, 15, 57],
        [0, 5, 0, 7, 29],
        [9, 11, 22, 17, 55],
    ]
    operational_costs = [
        [18, 21, 18, 16, 10],
        [1000, 15, 16, 14, 9],
        [1000, 10, 1000, 9, 6],
        [17, 16, 17, 15, 10],
    ]

    def __init__(self):
        self.variables = []
        self.x = {}

        # Create the linear solver with the GLOP backend.
        self.solver = pywraplp.Solver("p21_2", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

        for i in range(self.airplanes):
            for j in range(self.ways):
                self.x[(i, j)] = self.solver.NumVar(
                    0, self.solver.infinity(), f"x_({i},{j})"
                )

        for i in range(self.airplanes):
            ct = self.solver.Constraint(
                0, self.available_airplanes[i], f"available_airplanes_{i}"
            )
            for j in range(self.ways):
                ct.SetCoefficient(self.x[(i, j)], 1)

        self.variables.extend(self.x.values())

        self.objective = self.solver.Objective()

        self.objective.SetMaximization()

        for i in range(self.airplanes):
            for j in range(self.ways):
                self.objective.SetCoefficient(
                    self.x[(i, j)], -1 * self.operational_costs[i][j]
                )

    def scenario(self, index, demands, probability):
        if probability == 0:
            return

        y = {}

        for i in range(self.airplanes):
            for j in range(self.ways):
                y[(i, j)] = self.solver.NumVar(
                    0, self.solver.infinity(), f"y_({i},{j})_s_{index}"
                )

        self.variables.extend(y.values())

        for i in range(self.airplanes):
            for j in range(self.ways):
                ct = self.solver.Constraint(
                    0, self.solver.infinity(), f"capacity_constraint_({i}, {j})_{index}"
                )
                ct.SetCoefficient(y[(i, j)], 1)
                ct.SetCoefficient(self.x[(i, j)], self.capacity[i][j])

        for j in range(self.ways):
            ct = self.solver.Constraint(0, demands[j], f"demand_way_{j}_{index}")
            for i in range(self.airplanes):
                ct.SetCoefficient(y[(i, j)], 1)

        for i in range(self.airplanes):
            for j in range(self.ways):
                self.objective.SetCoefficient(y[(i, j)], self.prices[j] * probability)

    def solve(self):
        self.solver.Solve()

        print("Solution:")
        print("Objective value =", self.objective.Value())
        for v in self.variables:
            print(f"{v.name()}: {v.solution_value()}")

        return self.objective.Value()


if __name__ == "__main__":
    mda = Model()

    for i1, (d1, p1) in enumerate(demands[0]):
        for i2, (d2, p2) in enumerate(demands[1]):
            for i3, (d3, p3) in enumerate(demands[2]):
                for i4, (d4, p4) in enumerate(demands[3]):
                    for i5, (d5, p5) in enumerate(demands[4]):
                        mda.scenario(
                            (i1, i2, i3, i4, i5),
                            [d1, d2, d3, d4, d5],
                            p1 * p2 * p3 * p4 * p5,
                        )

    print(mda.solver.ExportModelAsLpFormat(False))
    print()

    print(mda.solve())
