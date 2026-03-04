import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def plot_cbc_trends(reports: list, output_dir: str):
    """
    Generates time-series plots for CBC parameters from a list of report dictionaries.
    Saves the plot to the output directory.
    """
    if not reports:
        print("No reports to plot.")
        return

    # Extract dates and data
    extracted_data = []
    
    for report in reports:
        date_str = report.get("report_date")
        if not date_str:
            continue
            
        try:
             # Try parsing logic similar to parser, assuming standardized YYYY-MM-DD
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
             continue
             
        row = report.get("cbc_report", {}).copy()
        row["date"] = date_obj
        extracted_data.append(row)

    if not extracted_data:
        print("No valid data points found for plotting.")
        return

    # Create DataFrame
    df = pd.DataFrame(extracted_data)
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

    if df.empty:
         print("DataFrame is empty.")
         return

    # Determine the number of parameters
    n_params = len(df.columns)
    if n_params == 0:
        print("No parameters to plot.")
        return

    # Create subplots with shared x-axis
    ncols = 3
    nrows = (n_params + ncols - 1) // ncols  # Ceiling division
    fig, axes = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows), sharex=True)
    
    if nrows * ncols == 1:
        axes_flat = [axes]
    else:
        axes_flat = axes.flatten()

    # Plot each CBC parameter
    for i, col in enumerate(df.columns):
        ax = axes_flat[i]
        ax.plot(df.index, df[col], marker='o', linestyle='-')
        ax.set_title(col)
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)

    # Hide unused subplots
    for j in range(i + 1, len(axes_flat)):
        axes_flat[j].axis('off')

    plt.tight_layout()
    output_path = os.path.join(output_dir, "cbc_trends.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Time series plot saved to {output_path}")
