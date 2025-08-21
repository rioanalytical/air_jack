import pandas as pd
from sklearn import datasets
from evidently import Report
from evidently.presets import DataDriftPreset
from flask import Response

@app.route("/drift_html", methods=["GET"])
def drift_html():
    iris_data = datasets.load_iris(as_frame=True)
    iris_frame = iris_data.frame
    current_data = iris_frame.iloc[:60]
    reference_data = iris_frame.iloc[60:]
    report = Report([DataDriftPreset(method="psi")], include_tests=True)
    report.run(current_data, reference_data)
    # Get HTML as string (using internal method, since save_html saves to file)
    html = report.get_html()
    return Response(html, mimetype="text/html")
