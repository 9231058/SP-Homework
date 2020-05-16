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

beet_cost = 260
beet_sell_price_low = 10
beet_sell_price_high = 36


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

        return (
            self.objective.Value() + pi_1,
            [x.solution_value() for x in self.variables],
        )


class CornSubProblem:
    base = 3
    require = 240

    def __init__(self):
        self.variables = []
        self.points = []
        self.solver = pywraplp.Solver(
            "corn_sub_problem", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
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

        return (
            self.objective.Value() + pi_2,
            [x.solution_value() for x in self.variables],
        )


class BeetSubProblem:
    base = 20
    bound = 6000

    def __init__(self):
        self.variables = []
        self.points = []
        self.solver = pywraplp.Solver(
            "beet_sub_problem", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )
        self.x3 = self.solver.NumVar(0, area, "x_3")
        self.variables.append(self.x3)

        self.objective = self.solver.Objective()
        self.objective.SetMinimization()

        n = len(scenarios)  # probability of each scenario is 1/n
        for i, s in enumerate(scenarios):
            y2 = self.solver.NumVar(0, self.bound, f"y_3_2_{i}")
            y3 = self.solver.NumVar(0, self.solver.infinity(), f"y_3_3_{i}")
            ct = self.solver.Constraint(-self.solver.infinity(), 0)
            ct.SetCoefficient(self.x3, -self.base - self.base * s)
            ct.SetCoefficient(y2, 1)
            ct.SetCoefficient(y3, 1)

            self.objective.SetCoefficient(y2, 1 / n * beet_sell_price_high)
            self.objective.SetCoefficient(y3, 1 / n * beet_sell_price_low)

    def solve(self, pi_3, pi_4):
        self.objective.SetCoefficient(self.x3, pi_4 + beet_cost)
        self.solver.Solve()

        return (
            self.objective.Value() + pi_3,
            [x.solution_value() for x in self.variables],
        )


class MasterProblem:
    def __init__(self, wsp, csp, bsp):
        self.solver = pywraplp.Solver(
            "master_problem", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )
        self.cts = []
        self.etas = []

        self.objective = self.solver.Objective()
        self.objective.SetMaximization()

        area_ct = self.solver.Constraint(0, area)

        ct = self.solver.Constraint(1, 1)
        for i, point in enumerate(wsp.points):
            eta = self.solver.NumVar(0, self.solver.infinity(), f"eta_1_{i}")
            x1 = point[0]
            area_ct.SetCoefficient(eta, x1)
            self.objective.SetCoefficient(eta, -150 * x1)
            ct.SetCoefficient(eta, 1)
        self.cts.append(ct)

        ct = self.solver.Constraint(1, 1)
        for i, point in enumerate(csp.points):
            eta = self.solver.NumVar(0, self.solver.infinity(), f"eta_2_{i}")
            x2 = point[0]
            area_ct.SetCoefficient(eta, x2)
            self.objective.SetCoefficient(eta, -230 * x2)
            ct.SetCoefficient(eta, 1)
        self.cts.append(ct)

        ct = self.solver.Constraint(1, 1)
        for i, point in enumerate(bsp.points):
            eta = self.solver.NumVar(0, self.solver.infinity(), f"eta_3_{i}")
            x3 = point[0]
            area_ct.SetCoefficient(eta, x3)
            self.objective.SetCoefficient(eta, -260 * x3)
            ct.SetCoefficient(eta, 1)
        self.cts.append(ct)

    def solve(self):
        self.solver.Solve()

        return self.objective.Value()


if __name__ == "__main__":
    wsp = WheatSubProblem()
    csp = CornSubProblem()
    bsp = BeetSubProblem()

    # register initial points

    while True:
        mp = MasterProblem(wsp, csp, bsp)
        mp.solve()
        pi_1 = mp.cts[0].DualValue()
        pi_2 = mp.cts[1].DualValue()
        pi_3 = mp.cts[2].DualValue()
        pi_4 = mp.cts[4].DualValue()

        if sp.solve(pi_1, pi_2, pi_3) == 0:
            break
        sp.points.append((sp.x1.solution_value(), sp.x2.solution_value()))

    print(sp.points)
    print(mp.objective.Value())
