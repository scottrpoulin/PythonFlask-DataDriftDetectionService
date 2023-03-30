# Change detection on a weekly basis
# Drift over the span of configurable months.
# How does the last month compare to this X number of months average
from evidently.metric_preset import *
from evidently.report import Report
from datadriftdetectionservice.driftdetection import datasource
from datadriftdetectionservice.driftdetection import configuration


def data_drift_detection_previous(last_number_of_days):
    data_config, drift_config = configuration.read_configuration()
    tables = data_config.tables
    reports = drift_config.reports
    metrics = []
    for report in reports:
        parameters = report.report_config.parameters
        if report.report_type == "DataQualityPreset":
            columns = parameters.get('columns', [])
            if len(columns) > 0:
                metrics.append(DataQualityPreset(columns=columns))
            else:
                metrics.append(DataQualityPreset())
        elif report.report_type == "TargetDriftPreset":
            # TODO: Add support for other metrics
            # stattest = parameters['stattest']
            # cat_stattest = parameters['cat_stattest']
            # num_stattest = parameters['num_stattest']
            # per_column_stattest = parameters['per_column_stattest']
            # stattest_threshold = parameters['stattest_threshold']
            # cat_stattest_threshold = parameters['cat_stattest_threshold']
            # num_stattest_threshold = parameters['num_stattest_threshold']
            # per_column_stattest_threshold = parameters['per_column_stattest_threshold']
            columns = parameters.get('columns', [])
            if len(columns) > 0:
                metrics.append(TargetDriftPreset(columns=columns))
            else:
                metrics.append(TargetDriftPreset())
        elif report.report_type == "RegressionPerformancePreset":
            columns = parameters.get('columns', [])
            if len(columns) > 0:
                metrics.append(RegressionPreset(columns=columns))
            else:
                metrics.append(RegressionPreset())
        elif report.report_type == "ClassificationPerformancePreset":
            # TODO: Add support for columns and K metrics
            # columns = parameters['columns']
            # k = parameters['k']
            probas_threshold = parameters['probas_threshold']
            if probas_threshold is None:
                metrics.append(ClassificationPreset())
            else:
                metrics.append(ClassificationPreset(probas_threshold=probas_threshold))
        else:
            # TODO: Add support for other metrics
            # columns = parameters['columns']
            # stattest = parameters['stattest']
            # cat_stattest = parameters['cat_stattest']
            # num_stattest = parameters['num_stattest']
            # per_column_stattest = parameters['per_column_stattest']
            # stattest_threshold = parameters.get('stattest_threshold', None)
            # cat_stattest_threshold = parameters['cat_stattest_threshold']
            # num_stattest_threshold = parameters['num_stattest_threshold']
            # per_column_stattest_threshold = parameters['per_column_stattest_threshold']
            drift_share = parameters.get('drift_share', None)
            if drift_share is None:
                metrics.append(DataDriftPreset())
            else:
                metrics.append(DataDriftPreset(drift_share=drift_share))
    report = Report(metrics=metrics)
    for table in tables:
        reference_data, current_data = datasource.query_data(data_config, table, last_number_of_days, drift_config.sample_size)
        report.run(reference_data=reference_data, current_data=current_data)
        report.save_html('./datadriftdetectionservice/templates/results/'+table.table_name+'-past-'+str(last_number_of_days)+'-days.html')
    return

