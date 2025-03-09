import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_2d_feasible_region(lp_model, solution):
    """
    Plots the feasible region for a 2-variable LP problem.

    Args:
        lp_model (dict): The parsed LP problem containing constraints.
        solution (dict): The solution dictionary containing the optimal point.

    Returns:
        None
    """
    fig, ax = plt.subplots()
    
    # Extract constraints
    constraints = lp_model['constraints']
    x = np.linspace(0, 10, 400)
    
    # List to store feasible region boundaries
    y_limits = []

    for name, constraint in constraints.items():
        coeffs = constraint['coefficients']
        if 'x1' in coeffs and 'x2' in coeffs and coeffs['x2'] != 0:
            y = (constraint['rhs'] - coeffs['x1'] * x) / coeffs['x2']
            ax.plot(x, y, label=f"{name}: {coeffs['x1']}x1 + {coeffs['x2']}x2 {constraint['sense']} {constraint['rhs']}")
            y_limits.append(y)

    if y_limits:
        # Determine lower and upper bounds for shading
        y_min = np.maximum.reduce(y_limits)
        y_max = np.full_like(y_min, 10)  # Assume a reasonable upper limit
        ax.fill_between(x, y_min, y_max, alpha=0.3, color='gray')

    # Plot optimal solution if available
    if solution['status'] == 'Optimal':
        ax.plot(solution['variables']['x1'], solution['variables']['x2'], 'ro', label='Optimal Solution')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.legend()
    plt.title('2-Variable LP Feasible Region')
    plt.show()

def plot_multivariable_solution(lp_model, solution):
    """
    Visualizes multi-variable LP solutions using a table and heatmap.

    Args:
        lp_model (dict): The parsed LP problem containing constraints.
        solution (dict): The solution dictionary containing variable values.

    Returns:
        None
    """
    variables = solution['variables']
    
    # Create DataFrame for table visualization
    df = pd.DataFrame(list(variables.items()), columns=['Variable', 'Value'])
    print("Optimal Variable Values:")
    print(df)

    # Heatmap for variable sensitivity
    plt.figure(figsize=(8, 5))
    sns.heatmap(df.set_index('Variable').T, annot=True, cmap="coolwarm", linewidths=1)
    plt.title("Optimal Variable Values (Multi-Variable LP)")
    plt.show()

def visualize_solution(lp_model, solution):
    """
    Determines the appropriate visualization method based on the number of variables.

    Args:
        lp_model (dict): The parsed LP problem containing constraints.
        solution (dict): The solution dictionary containing results.

    Returns:
        None
    """
    if len(lp_model["variables"]) == 2:
        plot_2d_feasible_region(lp_model, solution)
    else:
        plot_multivariable_solution(lp_model, solution)
