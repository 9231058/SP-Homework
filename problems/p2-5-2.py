# In The Name of God
# =======================================
# [] File Name : p2-5-2.py
#
# [] Creation Date : 12-05-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================

from ortools.linear_solver import pywraplp


class SubProblemI:
    def __init__(self):
        self.points = []
        self.solver = pywraplp.Solver(
            "p2_5_sub_problem", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )
        self.x1 = self.solver.NumVar(0, self.solver.infinity(), "x_1")
        self.x2 = self.solver.NumVar(0, self.solver.infinity(), "x_2")

        ct = self.solver.Constraint(0, 708)
        ct.SetCoefficient(self.x1, 1)
        ct.SetCoefficient(self.x2, 2 / 3)

        ct = self.solver.Constraint(0, 135)
        ct.SetCoefficient(self.x1, 1 / 10)
        ct.SetCoefficient(self.x2, 1 / 4)

        self.objective = self.solver.Objective()
        self.objective.SetMinimization()

    def solve(self, pi_1, pi_2, pi_3):
        self.objective.SetCoefficient(self.x1, 7 / 10 * pi_2 + 1 / 2 * pi_3 - 10)
        self.objective.SetCoefficient(self.x2, pi_2 + 5 / 6 * pi_3 - 9)
        self.solver.Solve()

        return self.objective.Value() + pi_1


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
