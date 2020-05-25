import math

from ortools.linear_solver import pywraplp

BIG_M = 100 * 100 * 100

scenarios = [0.2, 0, -0.2]

EPSILON = 0.01

AREA = 500

WHEAT_COST = 150
WHEAT_PRODUCE = 2.5
WHEAT_REQUIREMENT = 200
WHEAT_BUY_PRICE = 238
WHEAT_SELL_PRICE = 170

CORN_COST = 230
CORN_PRODUCE = 3
CORN_REQUIREMENT = 240
CORN_BUY_PRICE = 210
CORN_SELL_PRICE = 150

BEET_COST = 260
BEET_PRODUCE = 20
BEET_MAX_DEMAND = 6000
BEET_SELL_PRICE_LOW = 10
BEET_SELL_PRICE_HIGH = 36


class MasterProblem:
    def __init__(self):
        self.solver = pywraplp.Solver(
            "benders_master_porblem", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )

        self.x_1 = self.solver.NumVar(0, self.solver.infinity(), "x_1")
        self.x_2 = self.solver.NumVar(0, self.solver.infinity(), "x_2")
        self.x_3 = self.solver.NumVar(0, self.solver.infinity(), "x_3")

        self.phi = self.solver.NumVar(
            -100 * 100 * 100, self.solver.infinity(), "phi"
        )

        area_constraint = self.solver.Constraint(0, AREA, "area_constraint")
        area_constraint.SetCoefficient(self.x_1, 1)
        area_constraint.SetCoefficient(self.x_2, 1)
        area_constraint.SetCoefficient(self.x_3, 1)

        self.objective = self.solver.Objective()
        self.objective.SetCoefficient(self.x_1, WHEAT_COST)
        self.objective.SetCoefficient(self.x_2, CORN_COST)
        self.objective.SetCoefficient(self.x_3, BEET_COST)
        self.objective.SetCoefficient(self.phi, 1)
        self.objective.SetMinimization()

    def add_cut(self, constant, pi_1, pi_2, pi_3):
        """
        add_cut adds new cuts to master problem based
        on given dual values and constant.
        these parameters come from the sub problem
        optimal solution in each benders iteration.
        """
        cut = self.solver.Constraint(constant, self.solver.infinity(), "cut")
        cut.SetCoefficient(self.x_1, -pi_1)
        cut.SetCoefficient(self.x_2, -pi_2)
        cut.SetCoefficient(self.x_3, -pi_3)
        cut.SetCoefficient(self.phi, 1)

    def solve(self):
        self.solver.Solve()

        return (
            self.objective.Value(),
            self.x_1.solution_value(),
            self.x_2.solution_value(),
            self.x_3.solution_value(),
        )


class SubProblem:
    def __init__(self):
        self.solver = pywraplp.Solver(
            "benders_sub_porblem", pywraplp.Solver.CLP_LINEAR_PROGRAMMING
        )

        self.x_1 = self.solver.NumVar(0, self.solver.infinity(), "x_1")
        self.x_2 = self.solver.NumVar(0, self.solver.infinity(), "x_2")
        self.x_3 = self.solver.NumVar(0, self.solver.infinity(), "x_3")

        self.objective = self.solver.Objective()
        self.objective.SetMinimization()

        for index, scenario in enumerate(scenarios):
            self._wheat_variables_constraint(index, scenario)
            self._corn_variables_constraint(index, scenario)
            self._beet_variables_constraints(index, scenario)

    def solve(self, x_1, x_2, x_3):
        x_hat_1 = self.solver.Constraint(x_1, x_1, "x_hat_1")
        x_hat_1.SetCoefficient(self.x_1, 1)

        x_hat_2 = self.solver.Constraint(x_2, x_2, "x_hat_2")
        x_hat_2.SetCoefficient(self.x_2, 1)

        x_hat_3 = self.solver.Constraint(x_3, x_3, "x_hat_3")
        x_hat_3.SetCoefficient(self.x_3, 1)

        self.solver.Solve()

        return (
            1 / len(scenarios) * self.objective.Value(),
            x_hat_1.DualValue(),
            x_hat_2.DualValue(),
            x_hat_3.DualValue(),
        )

    def _wheat_variables_constraint(self, index, scenario):
        y_11 = self.solver.NumVar(0, self.solver.infinity(), f"y_11_{index}")
        y_12 = self.solver.NumVar(0, self.solver.infinity(), f"y_12_{index}")
        v_1 = self.solver.NumVar(0, self.solver.infinity(), f"v_1_{index}")
        wheat_produce_constraint = self.solver.Constraint(
            WHEAT_REQUIREMENT,
            self.solver.infinity(),
            "wheat_produce_constraint",
        )
        wheat_produce_constraint.SetCoefficient(
            self.x_1, WHEAT_PRODUCE * scenario
        )
        wheat_produce_constraint.SetCoefficient(y_11, 1)
        wheat_produce_constraint.SetCoefficient(y_12, -1)
        wheat_produce_constraint.SetCoefficient(v_1, 1)

        self.objective.SetCoefficient(y_11, WHEAT_BUY_PRICE)
        self.objective.SetCoefficient(y_12, -WHEAT_SELL_PRICE)
        self.objective.SetCoefficient(v_1, BIG_M)

    def _corn_variables_constraint(self, index, scenario):
        y_21 = self.solver.NumVar(0, self.solver.infinity(), f"y_21_{index}")
        y_22 = self.solver.NumVar(0, self.solver.infinity(), f"y_22_{index}")
        v_2 = self.solver.NumVar(0, self.solver.infinity(), f"v_2_{index}")
        corn_produce_constraint = self.solver.Constraint(
            CORN_REQUIREMENT,
            self.solver.infinity(),
            "corn_produce_constraint",
        )
        corn_produce_constraint.SetCoefficient(
            self.x_2, CORN_PRODUCE * scenario
        )
        corn_produce_constraint.SetCoefficient(y_21, 1)
        corn_produce_constraint.SetCoefficient(y_22, -1)
        corn_produce_constraint.SetCoefficient(v_2, 1)

        self.objective.SetCoefficient(y_21, CORN_BUY_PRICE)
        self.objective.SetCoefficient(y_22, -CORN_SELL_PRICE)
        self.objective.SetCoefficient(v_2, BIG_M)

    def _beet_variables_constraints(self, index, scenario):
        y_32 = self.solver.NumVar(0, BEET_MAX_DEMAND, f"y_32_{index}")
        y_33 = self.solver.NumVar(0, self.solver.infinity(), f"y_33_{index}")
        v_3 = self.solver.NumVar(0, self.solver.infinity(), f"v_3_{index}")
        beet_produce_constraint = self.solver.Constraint(
            0, self.solver.infinity(), "beet_produce_constraint",
        )
        beet_produce_constraint.SetCoefficient(
            self.x_3, BEET_PRODUCE * scenario
        )
        beet_produce_constraint.SetCoefficient(y_32, -1)
        beet_produce_constraint.SetCoefficient(y_33, -1)
        beet_produce_constraint.SetCoefficient(v_3, 1)

        self.objective.SetCoefficient(y_32, -BEET_SELL_PRICE_HIGH)
        self.objective.SetCoefficient(y_33, -BEET_SELL_PRICE_LOW)
        self.objective.SetCoefficient(v_3, BIG_M)


def main():
    master_problem = MasterProblem()
    iterations = 0

    while True:
        print()
        print(f"> {iterations}")
        iterations += 1

        z_lb, x_1, x_2, x_3 = master_problem.solve()
        print(f"x_1: {x_1}, x_2: {x_2}, x_3: {x_3}", f"z_lb: {z_lb}")

        z_star, pi_1, pi_2, pi_3 = SubProblem().solve(x_1, x_2, x_3)
        z_ub = z_star + WHEAT_COST * x_1 + CORN_COST * x_2 + BEET_COST * x_3
        print(f"pi_1: {pi_1}, pi_2: {pi_2}, pi_3: {pi_3}", f"z_ub: {z_ub}")

        if math.isclose(z_lb, z_ub, abs_tol=EPSILON):
            print()
            print(f"x_1: {x_1}, x_2: {x_2}, x_3: {x_3}")
            print(f"Z: {z_lb}")
            break

        master_problem.add_cut(
            z_star - pi_1 * x_1 - pi_2 * x_2 - pi_3 * x_3, x_1, x_2, x_3
        )


if __name__ == "__main__":
    main()
