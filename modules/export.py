import pandas as pd
import json
import os
from reportlab.pdfgen import canvas

def ensure_directory(file_path):
    """Ensures the directory exists before writing a file."""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def export_to_csv(solution, file_path="output.csv"):
    """Exports the LP solver solution to a CSV file."""
    try:
        ensure_directory(file_path)
        rows = [{
            "Objective Value": solution.get("objective_value", "N/A"),
            **solution.get("variables", {}),
            **solution.get("dual_values", {}),
            **solution.get("slack_values", {})
        }]
        df = pd.DataFrame(rows)
        df.to_csv(file_path, index=False)
        print(f"Solution exported to CSV: {file_path}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

def export_to_json(solution, file_path="output.json"):
    """Exports the LP solver solution to a JSON file."""
    try:
        ensure_directory(file_path)
        with open(file_path, 'w') as json_file:
            json.dump(solution, json_file, indent=4)
        print(f"Solution exported to JSON: {file_path}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")

def export_to_pdf(solution, file_path="output.pdf"):
    """Exports the LP solver solution to a PDF file with proper formatting."""
    try:
        ensure_directory(file_path)
        c = canvas.Canvas(file_path)
        c.setTitle("Linear Programming Solution Report")

        y_position = 800  # Start position for writing
        line_spacing = 20  # Space between lines

        def write_line(text):
            """Helper function to handle line spacing and avoid overflow."""
            nonlocal y_position
            if y_position < 50:  # If too low, start a new page
                c.showPage()
                y_position = 800  # Reset position for new page
            c.drawString(100, y_position, text)
            y_position -= line_spacing  # Move to next line

        write_line("Linear Programming Solution Report")
        write_line(f"Objective Value: {solution.get('objective_value', 'N/A')}")

        write_line("Decision Variables:")
        for var, value in solution.get("variables", {}).items():
            write_line(f"  {var}: {value}")

        write_line("Constraint Dual Values:")
        for dual, value in solution.get("dual_values", {}).items():
            write_line(f"  {dual}: {value}")

        write_line("Constraint Slack Values:")
        for slack, value in solution.get("slack_values", {}).items():
            write_line(f"  {slack}: {value}")

        c.save()
        print(f"Solution exported to PDF: {file_path}")
    except Exception as e:
        print(f"Error exporting to PDF: {e}")

def export_solution(solution, file_path="output", formats=["csv", "json", "pdf"]):
    """Exports the LP solver solution to the specified formats (CSV, JSON, PDF)."""
    try:
        ensure_directory(file_path)

        if "csv" in formats:
            export_to_csv(solution, f"{file_path}.csv")
        if "json" in formats:
            export_to_json(solution, f"{file_path}.json")
        if "pdf" in formats:
            export_to_pdf(solution, f"{file_path}.pdf")

    except Exception as e:
        print(f"Error exporting solution: {e}")

# Example usage
if __name__ == "__main__":
    solution = {
        "status": "Optimal",
        "objective_value": 150.5,
        "variables": {"x1": 10, "x2": 20},
        "dual_values": {"c1": 0.5, "c2": 1.2},
        "slack_values": {"c1": 0, "c2": 3}
    }

    export_solution(solution)  # Exports to all formats
    export_solution(solution, "results/solution", ["json", "pdf"])  # Exports only JSON and PDF
