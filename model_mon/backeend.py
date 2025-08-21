import dataiku
from flask import send_file
import os
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd

# Optional: set a temp file path
REPORT_PATH = "/tmp/evidently_report.html"

@app.route('/generate_report')
def generate_report():
    # Load datasets (adjust names as needed)
    ref_dataset = dataiku.Dataset("reference_dataset").get_dataframe()
    cur_dataset = dataiku.Dataset("current_dataset").get_dataframe()

    # Create the report
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref_dataset, current_data=cur_dataset)

    # Save report to HTML
    report.save_html(REPORT_PATH)
    return send_file(REPORT_PATH, mimetype='text/html')
