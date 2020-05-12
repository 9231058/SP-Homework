# In The Name of God
# =======================================
# [] File Name : p2-5-1.py
#
# [] Creation Date : 12-05-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================
from ortools.linear_solver import pywraplp


def main():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver("p2-5-1", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    x1 = solver.NumVar(0, solver.infinity(), "x_1")
    x2 = solver.NumVar(0, solver.infinity(), "x_2")

    eta0 = solver.NumVar(0, solver.infinity(), "eta_0")
    eta1 = solver.NumVar(0, solver.infinity(), "eta_1")
    eta2 = solver.NumVar(0, solver.infinity(), "eta_2")
    eta3 = solver.NumVar(0, solver.infinity(), "eta_3")

    print("Number of variables =", solver.NumVariables())

    ct = solver.Constraint(0, 630, "c1")
    ct.SetCoefficient(x1, 0.7)
    ct.SetCoefficient(x2, 1)

    ct = solver.Constraint(0, 600, "c2")
    ct.SetCoefficient(x1, 0.5)
    ct.SetCoefficient(x2, 5 / 6)

    ct = solver.Constraint(0, 0, "x_1")
    ct.SetCoefficient(x1, 1)
    ct.SetCoefficient(eta0, 0)
    ct.SetCoefficient(eta1, -708)
    ct.SetCoefficient(eta2, -474.55)
    ct.SetCoefficient(eta3, 0)

    ct = solver.Constraint(0, 0, "x_2")
    ct.SetCoefficient(x2, 1)
    ct.SetCoefficient(eta0, 0)
    ct.SetCoefficient(eta1, 0)
    ct.SetCoefficient(eta2, -350.18)
    ct.SetCoefficient(eta3, 540)

    ct = solver.Constraint(0, 1, "eta")
    ct.SetCoefficient(eta0, 1)
    ct.SetCoefficient(eta1, 1)
    ct.SetCoefficient(eta2, 1)
    ct.SetCoefficient(eta3, 1)

    print("Number of constraints =", solver.NumConstraints())

    objective = solver.Objective()
    objective.SetCoefficient(x1, 10)
    objective.SetCoefficient(x2, 9)
    objective.SetMaximization()

    solver.Solve()

    print("Solution:")
    print("Objective value =", objective.Value())
    for v in [x1, x2]:
        print(f"{v.name()} = {v.solution_value()}")


if __name__ == "__main__":
    main()
