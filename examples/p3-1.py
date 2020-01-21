# In The Name of God
# =======================================
# [] File Name : p3-1.py
#
# [] Creation Date : 21-01-2020
#
# [] Created By : Parham Alvani <parham.alvani@gmail.com>
# =======================================
from ortools.linear_solver import pywraplp


def main():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver('p3_1',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    a = 150
    r = 5
    q = 25
    c = 10

    x = solver.NumVar(0, a, 'x')
    y1 = solver.NumVar(0, 50, 'y_1')
    y2 = solver.NumVar(0, 100, 'y_2')
    y3 = solver.NumVar(0, 150, 'y_3')
    z1 = solver.NumVar(0, solver.infinity(), 'z_1')
    z2 = solver.NumVar(0, solver.infinity(), 'z_2')
    z3 = solver.NumVar(0, solver.infinity(), 'z_3')

    print('Number of variables =', solver.NumVariables())

    ct = solver.Constraint(0, 0, 'state_1')
    ct.SetCoefficient(x, -1)
    ct.SetCoefficient(y1, 1)
    ct.SetCoefficient(z1, 1)

    ct = solver.Constraint(0, 0, 'state_2')
    ct.SetCoefficient(x, -1)
    ct.SetCoefficient(y2, 1)
    ct.SetCoefficient(z2, 1)

    ct = solver.Constraint(0, 0, 'state_3')
    ct.SetCoefficient(x, -1)
    ct.SetCoefficient(y3, 1)
    ct.SetCoefficient(z3, 1)

    print('Number of constraints =', solver.NumConstraints())

    objective = solver.Objective()
    objective.SetCoefficient(x, -c)
    objective.SetCoefficient(y1, 1/3 * q)
    objective.SetCoefficient(y2, 1/3 * q)
    objective.SetCoefficient(y3, 1/3 * q)
    objective.SetCoefficient(z1, 1/3 * r)
    objective.SetCoefficient(z2, 1/3 * r)
    objective.SetCoefficient(z3, 1/3 * r)
    objective.SetMaximization()

    solver.Solve()

    print('Solution:')
    print('Objective value =', objective.Value())
    for v in [x, y1, y2, y3, z1, z2, z3]:
        print(f'{v.name()} = {v.solution_value()}')


if __name__ == '__main__':
    main()
