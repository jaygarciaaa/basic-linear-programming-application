import re

def parse_lp_input(user_input):
    """
    Parses a Linear Programming (LP) problem from user input using regex.
    
    Extracts:
    - Objective function (max/min)
    - Constraints (inequalities & equalities)
    - Decision variables
    
    Returns:
    A structured dictionary:
    {
        "objective": {"type": "max", "coefficients": {"xA": 2, "xB": 4}},
        "constraints": [
            {"coefficients": {"xA": 2, "xB": 3}, "sign": "<=", "rhs": 10},
            {"coefficients": {"xA": 1, "xB": 5}, "sign": "=", "rhs": 6}
        ],
        "variables": {"xA", "xB"}
    }
    """

    lp_model = {
        "objective": {"type": "", "coefficients": {}},
        "constraints": [],
        "variables": set()
    }

    # Normalize input (remove spaces, standardize inequalities)
    user_input = user_input.replace('<=', '≤').replace('>=', '≥').replace(' ', '')

    # Extract Objective Function (Supports "Maximize: 2xA + 3xB" format)
    objective_match = re.search(r'(Maximize|Minimize)[:\s]+([\+\-]?\d*[a-zA-Z]\w*(?:[\+\-]\d*[a-zA-Z]\w*)*)', user_input, re.IGNORECASE)
    if objective_match:
        lp_model["objective"]["type"] = objective_match.group(1).lower()
        objective_terms = re.findall(r'([\+\-]?\d*\.?\d*)([a-zA-Z]\w*)', objective_match.group(2))
        for coef, var in objective_terms:
            coef = float(coef) if coef not in ["", "+", "-"] else float(f"{coef}1")
            lp_model["objective"]["coefficients"][var] = coef
            lp_model["variables"].add(var)
    else:
        raise ValueError("Objective function not found or incorrectly formatted.")

    # Extract Constraints (Supports multiple constraints)
    constraints = re.findall(r'([\+\-]?\d*[a-zA-Z]\w*(?:[\+\-]\d*[a-zA-Z]\w*)*)\s*([≤≥=])\s*(-?\d+\.?\d*)', user_input)
    if not constraints:
        raise ValueError("No valid constraints found.")

    for lhs, sign, rhs in constraints:
        constraint_dict = {"coefficients": {}, "sign": sign, "rhs": float(rhs)}
        terms = re.findall(r'([\+\-]?\d*\.?\d*)([a-zA-Z]\w*)', lhs)
        for coef, var in terms:
            coef = float(coef) if coef not in ["", "+", "-"] else float(f"{coef}1")
            constraint_dict["coefficients"][var] = coef
            lp_model["variables"].add(var)
        lp_model["constraints"].append(constraint_dict)

    return lp_model
