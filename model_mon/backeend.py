import pandas as pd
from sklearn import datasets
from evidently import Report
from evidently.presets import DataDriftPreset
from flask import request, jsonify

@app.route("/run_eval", methods=["POST"])
def run_eval():
    iris_data = datasets.load_iris(as_frame=True)
    iris_frame = iris_data.frame

    # Split current and reference data
    current_data = iris_frame.iloc[:60]
    reference_data = iris_frame.iloc[60:]
    
    # Run Evidently Data Drift preset with PSI
    report = Report([DataDriftPreset(method="psi")], include_tests=True)
    result = report.run(current_data, reference_data)
    # Return Evaluation as JSON
    return jsonify(result.as_dict())
