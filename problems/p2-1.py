# In The Name of God
# =======================================
# [] File Name : p2-1.py
#
# [] Creation Date : 16-02-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================
from ortools.linear_solver import pywraplp

class Scenario:
    def __init__(self, index, wheat_sell, probability):
        self.index = index
        self.wheat_sell = wheat_sell
        self.probability = probability

    def make(self, solver, objective, x1):
        y11 = solver.NumVar(0, solver.infinity(), f'y_11_s{self.index}')
        y12 = solver.NumVar(0, solver.infinity(), f'y_12_s{self.index}')

        ct = solver.Constraint(200, solver.infinity(), 'wheat_need')
        ct.SetCoefficient(x1, 2.5)
        ct.SetCoefficient(y11, 1)
        ct.SetCoefficient(y12, -1)

        objective.SetCoefficient(y11, -self.wheat_sell * 1.4 * self.probability)
        objective.SetCoefficient(y12, self.wheat_sell * self.probability)


def main():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver('p2_1',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    x1 = solver.NumVar(0, solver.infinity(), 'x_1')
    x2 = solver.NumVar(0, solver.infinity(), 'x_2')
    x3 = solver.NumVar(0, solver.infinity(), 'x_3')

    ct = solver.Constraint(0, 500, 'area')
    ct.SetCoefficient(x1, 1)
    ct.SetCoefficient(x2, 1)
    ct.SetCoefficient(x3, 1)

    y21 = solver.NumVar(0, solver.infinity(), f'y_21')
    y22 = solver.NumVar(0, solver.infinity(), f'y_22')
    y32 = solver.NumVar(0, 6000, f'y_32')
    y33 = solver.NumVar(0, solver.infinity(), f'y_33')

    ct = solver.Constraint(240, solver.infinity(), 'corn_need')
    ct.SetCoefficient(x2, 3)
    ct.SetCoefficient(y21, 1)
    ct.SetCoefficient(y22, -1)

    ct = solver.Constraint(0, solver.infinity(), 'beet_need')
    ct.SetCoefficient(x3, 20)
    ct.SetCoefficient(y32, -1)
    ct.SetCoefficient(y33, -1)

    objective = solver.Objective()
    objective.SetCoefficient(x1, -180)
    objective.SetCoefficient(x2, -280)
    objective.SetCoefficient(x2, -310)

    objective.SetCoefficient(y21, -170 * 1.4)
    objective.SetCoefficient(y22, 170)

    objective.SetCoefficient(y32, 41)
    objective.SetCoefficient(y33, 11)
    objective.SetMaximization()

    Scenario(1, 220, 0.5).make(solver, objective, x1)
    Scenario(2, 300, 0.5).make(solver, objective, x1)

    solver.Solve()

    print('Solution:')
    print('Objective value =', objective.Value())


if __name__ == '__main__':
    main()
