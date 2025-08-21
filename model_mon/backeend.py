import pandas as pd
from flask import request, jsonify
from evidently.report import Report
from evidently.metrics import (
    ClassificationQualityMetric,
    PopulationStabilityIndex,
)
from evidently.metric_preset import DataDriftPreset
import dataiku

@app.route("/compute_metrics", methods=["POST"])
def compute_metrics():
    # Replace 'your_dataset_name' with your dataset name in Dataiku
    dataset = dataiku.Dataset("your_dataset_name")
    df = dataset.get_dataframe()
    
    # Assume your data has columns: 'y_true', 'y_pred', 'score'
    column_mapping = {
        "target": "y_true",
        "prediction": "y_pred"
    }
    
    # Evidently report for TPR (as part of Classification Quality)
    report = Report(metrics=[
        ClassificationQualityMetric(target="y_true", prediction="y_pred"),
        PopulationStabilityIndex(column_name="score"),
        DataDriftPreset(),
    ])
    
    # For PSI: need reference and current data; split accordingly
    df_ref = df.sample(frac=0.5, random_state=42)
    df_cur = df.drop(df_ref.index)
    
    report.run(
        reference_data=df_ref,
        current_data=df_cur,
        column_mapping=column_mapping
    )
    
    return jsonify(report.as_dict())
