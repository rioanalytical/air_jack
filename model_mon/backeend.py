@app.route("/drift_html", methods=["GET"])
def drift_html():
    iris_data = datasets.load_iris(as_frame=True)
    iris_frame = iris_data.frame
    current_data = iris_frame.iloc[:60]
    reference_data = iris_frame.iloc[60:]
    report = Report([DataDriftPreset(method="psi")], include_tests=True)
    report.run(current_data, reference_data)
    report.save_html("temp_report.html")
    with open("temp_report.html", "r") as f:
        html = f.read()
    return Response(html, mimetype="text/html")
