import importlib

# __init__.py

__version__ = "1.0.0"
__author__ = "John Michael Garcia"

# Lazy import function
def lazy_import(module_name, function_name):
    """
    Dynamically import a function from a module only when it is called.
    """
    def wrapper(*args, **kwargs):
        module = importlib.import_module(module_name)
        function = getattr(module, function_name)
        return function(*args, **kwargs)
    return wrapper

# Core functions with proper lazy loading
parse_input = lazy_import('modules.parser', 'parse_lp_input')
solve_lp = lazy_import('modules.solver', 'solve_lp')
visualize_solution = lazy_import('modules.visualization', 'visualize_solution')
export_results = lazy_import('modules.export', 'export_results')

# Public API
__all__ = ["parse_input", "solve_lp", "visualize_solution", "export_results"]
