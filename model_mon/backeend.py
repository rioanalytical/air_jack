import dataiku
from flask import send_file
import os
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import pandas as pd

# Output path for HTML report
REPORT_PATH = "/tmp/evidently_report.html"

@app.route('/generate_report')
def generate_report():
    # Load datasets from Dataiku
    reference_df = dataiku.Dataset("reference_dataset").get_dataframe()
    current_df = dataiku.Dataset("current_dataset").get_dataframe()

    # Create a dashboard with Data Drift tab
    dashboard = Dashboard(tabs=[DataDriftTab()])
    dashboard.calculate(reference_df, current_df)

    # Save the dashboard to an HTML file
    dashboard.save(REPORT_PATH)

    # Return the HTML file for rendering
    return send_file(REPORT_PATH, mimetype='text/html')
