# basic-linear-programming-application

**Access Webpage here:**
  - https://jaygarciaaa.github.io/basic-linear-programming-application/
  
Problem Set 3 from Optimization Techniques Course

## Problem Set 3 - Basic Linear Programming Application

Create a Basic Linear Programming Application in Python. 

## 1. Python Environment & Libraries

1. **Python Version**
  * A stable Python 3.x environment (3.7 or higher recommended).

2. **LP Solver Library**
  * Must install or include a solver interface such as **PuLP, Pyomo** to an external site., or another LP solver library (e.g., **Gurobi** to an external site. / **CPLEX** if you have a license).


3. **Plotting/Visualization (if graphical output is required)**
  * A plotting library, e.g. **matplotlib, plotly**, or **seaborn**.
  * Optional for advanced visualization: networkx for network-based flows, or **geoplot** for spatial data.

4. **Data Handling**
  * **NumPy** for numerical operations, arrays, or matrix manipulations.
  * **Pandas** if you plan to read or store data in tabular form (CSV, Excel, etc.).

## 2. Problem Specification & Data Input (20 points)

1. **Problem Definition Module**
  * A mechanism to define the **objective function** (e.g., cost minimization, profit maximization).
  * A structure to define **decision variables** (variable names, types, bounds).


2. **Constraints Representation**
  * Ability to parse or directly input constraints (inequalities, equalities)

## 3. Solver Integration (15 points)

1. **Choice of Solver**
  * Specify which solvers are supported (e.g., built-in CBC solver in PuLP, or external solvers like Gurobi, GLPK CPLEX).
  * Provide an interface to select the solver or adjust solver parameters.

2. **Execution Flow**
* Automatic model building from the specified problem.
  * One-click or single-function call to run the solver.
  * Capture solver status (Optimal, Infeasible, Unbounded, etc.).

3. **Robust Error Handling**
  * If the solver fails, or the problem is infeasible, provide a clear error message or fallback.

## 4. Output & Reporting (15 points)

1. **Solution Extraction**
  * Once solved, retrieve the **optimal objective value and variable values**.
  * Provide a structured format for this data (dictionary, table, or direct printing).

2. **Statistical Summaries**
  * Summaries like total cost/profit, slack values for constraints, or shadow prices (dual values) if relevant.

3. **Visualization (for 2-variable or small-scale problems)**
  * Plot constraints, feasible region, and the solution point(s).
  * Label intersections or highlight feasible polygons.
  * For multi-dimensional problems, consider textual/graph-based representation or no direct plot (since it’s hard to visualize high dimensions).

4. **Export Options**
  * Export solution results to CSV, JSON, or database.
  * Possibly generate a PDF or HTML report with the solution.

## 5. Usability, Documentation, Presentation (50 points)
1. **User Interface**
  * If the application is CLI-based, provide clear usage instructions.
  * If it’s notebook-based (Jupyter), include well-organized cells with instructions.
  * Optional: A simple GUI using a library like Tkinter or a web-based dashboard (e.g., Streamlit).

2. **Modularity**
  * Keep the code organized: separate modules for problem definition, solver invocation, result processing, and visualization.

3. **Tutorials/Examples**
  * Provide at least one or two example problems (small LPs) to demonstrate usage.
  * Step-by-step instructions, especially for novices.

4. **Extensibility**
  * Clear instructions on how to add new constraints, additional data fields, or new solution methods.

## Example: Minimal Requirements in One List
1. **Python 3.x**
2. **PuLP** or **Pyomo** for modeling.
3. **NumPy** / **Pandas** for data manipulation (optional).
4. **matplotlib** for plotting 2D feasible regions or solution graphics (if needed).
5. A **main script or notebook** that:
  * Reads problem data (coefficients).
  * Constructs an LP model (objective, variables, constraints).
  * Calls the solver, checks feasibility/optimality.
  * Outputs the solution in a user-friendly format.
  * (Optionally) Visualizes results if problem dimension is small enough.
