# In The Name of God
# =======================================
# [] File Name : p2-1.py
#
# [] Creation Date : 16-02-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================
from ortools.linear_solver import pywraplp

class Model:
    def __init__(self, name):
        self.name = name
        self.variables = []

        # Create the linear solver with the GLOP backend.
        self.solver = pywraplp.Solver('p2_1',
                                 pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

        self.x1 = self.solver.NumVar(0, self.solver.infinity(), 'x_1')
        self.x2 = self.solver.NumVar(0, self.solver.infinity(), 'x_2')
        self.x3 = self.solver.NumVar(0, self.solver.infinity(), 'x_3')
        self.variables.extend([self.x1, self.x2, self.x3])

        ct = self.solver.Constraint(0, 500, 'area')
        ct.SetCoefficient(self.x1, 1)
        ct.SetCoefficient(self.x2, 1)
        ct.SetCoefficient(self.x3, 1)

        y21 = self.solver.NumVar(0, self.solver.infinity(), f'y_21')
        y22 = self.solver.NumVar(0, self.solver.infinity(), f'y_22')
        y32 = self.solver.NumVar(0, 6000, f'y_32')
        y33 = self.solver.NumVar(0, self.solver.infinity(), f'y_33')
        self.variables.extend([y21, y22, y32, y33])

        ct = self.solver.Constraint(240, self.solver.infinity(), 'corn_need')
        ct.SetCoefficient(self.x2, 3)
        ct.SetCoefficient(y21, 1)
        ct.SetCoefficient(y22, -1)

        ct = self.solver.Constraint(0, self.solver.infinity(), 'beet_need')
        ct.SetCoefficient(self.x3, 20)
        ct.SetCoefficient(y32, -1)
        ct.SetCoefficient(y33, -1)

        self.objective = self.solver.Objective()
        self.objective.SetCoefficient(self.x1, -180)
        self.objective.SetCoefficient(self.x2, -280)
        self.objective.SetCoefficient(self.x3, -310)

        self.objective.SetCoefficient(y21, -170 * 1.4)
        self.objective.SetCoefficient(y22, 170)

        self.objective.SetCoefficient(y32, 41)
        self.objective.SetCoefficient(y33, 11)
        self.objective.SetMaximization()

    def scenario(self, index, wheat_sell, probability):
        y11 = self.solver.NumVar(0, self.solver.infinity(), f'y_11_s{index}')
        y12 = self.solver.NumVar(0, self.solver.infinity(), f'y_12_s{index}')

        self.variables.extend([y11, y12])

        ct = self.solver.Constraint(200, self.solver.infinity(), 'wheat_need')
        ct.SetCoefficient(self.x1, 2.5)
        ct.SetCoefficient(y11, 1)
        ct.SetCoefficient(y12, -1)

        self.objective.SetCoefficient(y11, -wheat_sell * 1.4 * probability)
        self.objective.SetCoefficient(y12, wheat_sell * probability)


    def solve(self):
        self.solver.Solve()

        print(f'{self.name:=^25}')
        print('Solution:')
        print('Objective value =', self.objective.Value())
        for v in self.variables:
            print(f'{v.name()}: {v.solution_value()}')


if __name__ == '__main__':
    mda = Model('stochastic')
    mda.scenario(1, 220, 0.5)
    mda.scenario(2, 300, 0.5)
    mda.solve()

    mdw = Model('worst')
    mdw.scenario(1, 220, 1)
    mdw.solve()

    mdb = Model('best')
    mdb.scenario(1, 300, 1)
    mdb.solve()
