import pulp
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def solve_lp(lp_model, solver_name="default"):
    """
    Solves a linear programming problem using the PuLP library.

    Args:
        lp_model (dict): A dictionary containing the parsed LP problem.
        solver_name (str): A string that allows selection of the solver backend. Default is "default".

    Returns:
        dict: A dictionary containing the solver results.
    """
    try:
        # Validate lp_model structure
        required_keys = ["objective", "constraints"]
        for key in required_keys:
            if key not in lp_model:
                raise ValueError(f"lp_model is missing required key: '{key}'")

        # Define the LP problem
        prob = pulp.LpProblem("LP_Problem", pulp.LpMaximize if lp_model["objective"]["sense"] == "max" else pulp.LpMinimize)

        # Add decision variables
        variables = {}
        for var_name in set(lp_model["objective"]["coefficients"]).union(*[c["coefficients"].keys() for c in lp_model["constraints"].values()]):
            lower, upper = lp_model.get("bounds", {}).get(var_name, (0, None))
            variables[var_name] = pulp.LpVariable(var_name, lowBound=lower, upBound=upper if upper is not None else None)

        # Set the objective function
        prob += pulp.lpSum(coeff * variables[var] for var, coeff in lp_model["objective"]["coefficients"].items()), "Objective"

        # Add constraints
        for name, constraint in lp_model["constraints"].items():
            lhs = pulp.lpSum(coeff * variables[var] for var, coeff in constraint["coefficients"].items())
            if constraint["sense"] == "<=":
                prob += lhs <= constraint["rhs"], name
            elif constraint["sense"] == ">=":
                prob += lhs >= constraint["rhs"], name
            elif constraint["sense"] == "=":
                prob += lhs == constraint["rhs"], name
            else:
                raise ValueError(f"Unknown constraint sense: {constraint['sense']}")

        # Select and configure the solver
        solver_map = {
            "default": pulp.PULP_CBC_CMD(),
            "GLPK": pulp.GLPK_CMD(),
            "Gurobi": pulp.GUROBI_CMD(),
            "CPLEX": pulp.CPLEX_CMD(),
        }

        solver = solver_map.get(solver_name)
        if solver is None:
            raise ValueError(f"Unknown solver: {solver_name}")

        # Solve the problem
        start_time = time.time()
        prob.solve(solver)
        solver_time = time.time() - start_time

        # Retrieve results
        status = pulp.LpStatus[prob.status]
        objective_value = pulp.value(prob.objective) if prob.status == pulp.LpStatusOptimal else None
        variables_values = {var.name: var.varValue for var in prob.variables()}

        # Extract dual and slack values (only if available)
        dual_values = {}
        slack_values = {}
        if prob.status == pulp.LpStatusOptimal:
            for name, constraint in prob.constraints.items():
                try:
                    dual_values[name] = constraint.pi  # Shadow price (dual value)
                    slack_values[name] = constraint.slack  # Slack value
                except AttributeError:
                    pass  # Some solvers don't support duals/slack

        return {
            "status": status,
            "objective_value": objective_value,
            "variables": variables_values,
            "dual_values": dual_values,
            "slack_values": slack_values,
            "solver_time": solver_time
        }

    except Exception as e:
        logger.error(f"Error solving LP problem: {e}")
        return {"status": "Error", "message": str(e)}

# Example usage
if __name__ == "__main__":
    lp_model_example = {
        "objective": {
            "sense": "max",
            "coefficients": {"x1": 1, "x2": 2}
        },
        "constraints": {
            "c1": {"coefficients": {"x1": 1, "x2": 1}, "sense": "<=", "rhs": 5},
            "c2": {"coefficients": {"x1": 3, "x2": 2}, "sense": "<=", "rhs": 12}
        },
        "bounds": {
            "x1": (0, None),
            "x2": (0, None)
        }
    }

    result = solve_lp(lp_model_example)
    print(result)
