# In The Name of God
# =======================================
# [] File Name : 11scenario.py
#
# [] Creation Date : 17-05-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================

from ortools.linear_solver import pywraplp

scenarios = [0.5, 0.4, 0.3, 0.2, 0.1, 0, -0.05, -0.1, -0.15, -0.2, -0.25]
# area represents a total farm area
area = 500
wheat_cost = 150
wheat_buy_price = 238
wheat_sell_price = 170

corn_cost = 230
corn_buy_price = 210
corn_sell_price = 150


class WheatSubProblem:
    base = 2.5
    require = 200

    def __init__(self):
        self.variables = []
        self.points = []
        self.solver = pywraplp.Solver(
            "wheat_sub_problem", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )
        self.x1 = self.solver.NumVar(0, area, "x_1")
        self.variables.append(self.x1)

        self.objective = self.solver.Objective()
        self.objective.SetMinimization()

        n = len(scenarios)  # probability of each scenario is 1/n
        for i, s in enumerate(scenarios):
            y1 = self.solver.NumVar(0, self.solver.infinity(), f"y_1_1_{i}")
            y2 = self.solver.NumVar(0, self.solver.infinity(), f"y_1_2_{i}")
            ct = self.solver.Constraint(self.require, self.solver.infinity())
            ct.SetCoefficient(self.x1, self.base + self.base * s)
            ct.SetCoefficient(y1, 1)
            ct.SetCoefficient(y2, -1)

            self.objective.SetCoefficient(y1, 1 / n * wheat_buy_price)
            self.objective.SetCoefficient(y2, -1 / n * wheat_sell_price)

    def solve(self, pi_1, pi_4):
        self.objective.SetCoefficient(self.x1, pi_4 + wheat_cost)
        self.solver.Solve()

        return self.objective.Value() + pi_1


class CornSubProblem:
    base = 3
    require = 240

    def __init__(self):
        self.variables = []
        self.points = []
        self.solver = pywraplp.Solver(
            "wheat_sub_problem", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )
        self.x2 = self.solver.NumVar(0, area, "x_2")
        self.variables.append(self.x2)

        self.objective = self.solver.Objective()
        self.objective.SetMinimization()

        n = len(scenarios)  # probability of each scenario is 1/n
        for i, s in enumerate(scenarios):
            y1 = self.solver.NumVar(0, self.solver.infinity(), f"y_2_1_{i}")
            y2 = self.solver.NumVar(0, self.solver.infinity(), f"y_2_2_{i}")
            ct = self.solver.Constraint(self.require, self.solver.infinity())
            ct.SetCoefficient(self.x2, self.base + self.base * s)
            ct.SetCoefficient(y1, 1)
            ct.SetCoefficient(y2, -1)

            self.objective.SetCoefficient(y1, 1 / n * corn_buy_price)
            self.objective.SetCoefficient(y2, -1 / n * corn_sell_price)

    def solve(self, pi_2, pi_4):
        self.objective.SetCoefficient(self.x2, pi_4 + corn_cost)
        self.solver.Solve()

        return self.objective.Value() + pi_2


class MasterProblem:
    def __init__(self, subproblem):
        self.solver = pywraplp.Solver(
            "p2_5_master_problem", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )
        self.cts = []
        self.etas = []

        ct = self.solver.Constraint(1, 1)
        for i in range(len(subproblem.points)):
            eta = self.solver.NumVar(0, self.solver.infinity(), f"eta_{i}")
            self.etas.append(eta)
            ct.SetCoefficient(eta, 1)
        self.cts.append(ct)

        ct = self.solver.Constraint(0, 630)
        for eta, point in zip(self.etas, subproblem.points):
            ct.SetCoefficient(eta, 1 / 7 * point[0])
            ct.SetCoefficient(eta, 1 * point[1])
        self.cts.append(ct)

        ct = self.solver.Constraint(0, 600)
        for eta, point in zip(self.etas, subproblem.points):
            ct.SetCoefficient(eta, 1 / 2 * point[0] + 5 / 6 * point[1])
        self.cts.append(ct)

        self.objective = self.solver.Objective()
        self.objective.SetMaximization()

        for eta, point in zip(self.etas, subproblem.points):
            self.objective.SetCoefficient(eta, 10 * point[0] + 9 * point[1])

    def solve(self):
        self.solver.Solve()

        return self.objective.Value()


if __name__ == "__main__":
    sp = SubProblemI()

    sp.points.append((0, 0))

    while True:
        mp = MasterProblem(sp)
        mp.solve()
        pi_1 = mp.cts[0].DualValue()
        pi_2 = mp.cts[1].DualValue()
        pi_3 = mp.cts[2].DualValue()
        if sp.solve(pi_1, pi_2, pi_3) == 0:
            break
        sp.points.append((sp.x1.solution_value(), sp.x2.solution_value()))

    print(sp.points)
    print(mp.objective.Value())
