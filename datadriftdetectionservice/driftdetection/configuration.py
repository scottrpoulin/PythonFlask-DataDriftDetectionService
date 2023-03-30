import yaml
import os
from datadriftdetectionservice.driftdetection.config_classes import *


def read_configuration():
    database_config = DatabaseConfig()
    drift_config = DriftConfig()
    config_file = os.environ.get("CONFIG_PATH", "datadriftconfig.yaml")
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
        if config[0] is not None:
            database_configuration_data = config[0]['database_config']
            database_type = database_configuration_data['database_type']
            username = database_configuration_data['username']
            password = database_configuration_data['pwd']
            host = database_configuration_data['host']
            port = database_configuration_data['port']
            database = database_configuration_data['database']
            tables = []
            for table_data in database_configuration_data['tables']:
                table = Table(table_data['table_name'],
                              table_data['date_column'],
                              table_data['target_column'],
                              table_data['numerical_columns'],
                              table_data['categorical_columns'])
                tables.append(table)
            database_config = DatabaseConfig(database_type, username, password, host, port, database, tables=tables)
        if config[1] is not None:
            drift_config_data = config[1]['drift_config']
            sample_size = drift_config_data.get('sample_size', None)
            reports_data = drift_config_data['reports']
            reports = []
            for report_data in reports_data:
                report_type = report_data['report_type']
                if report_data.get('parameters') is None:
                    parameters = {}
                else:
                    parameters = report_data['parameters']
                report_config = ReportConfig(parameters)
                reports.append(Report(report_type, report_config))
            drift_config = DriftConfig(sample_size, reports)
        f.close()
    return database_config, drift_config


if __name__ == '__main__':
    read_configuration()
