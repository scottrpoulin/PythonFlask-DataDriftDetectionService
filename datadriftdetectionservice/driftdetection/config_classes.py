class DatabaseConfig:
    def __init__(self, database_type="postgres", username="super_admin", password="SomeSecretPassword", host="localhost", port="5432", database="postgres", tables=None):
        self.database_type = database_type
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.tables = tables

    def __repr__(self):
        return f"DatabaseConfig(database_type={self.database_type}, username={self.username}, password={self.password}, host={self.host}, port={self.port}, database={self.database}, tables={self.tables})"

class Table:
    def __init__(self, table_name, date_column, target_column, numerical_columns, categorical_columns):
        self.table_name = table_name
        self.columns = [target_column] + numerical_columns + categorical_columns
        self.date_column = date_column
        self.target_column = target_column
        self.numerical_columns = numerical_columns
        self.categorical_columns = categorical_columns

    def __repr__(self):
        return f"Table(table_name={self.table_name}, columns={self.columns}, date_column={self.date_column}, target_column={self.target_column}, numerical_columns={self.numerical_columns}, categorical_columns={self.categorical_columns})"

class ReportConfig:
    def __init__(self, parameters=None):
        if parameters is None:
            parameters = {'drift_share': 0.75}
        self.parameters = parameters

    def __repr__(self):
        return f"ReportConfig(parameters={self.parameters})"

class Report:
    def __init__(self, report_type='DataDriftPreset', report_config=ReportConfig()):
        self.report_type = report_type
        self.report_config = report_config

    def __repr__(self):
        return f"Report(report_type={self.report_type}, report_config={self.report_config})"

class DriftConfig:
    def __init__(self, sample_size=None, reports=None):
        if reports is None:
            reports = [Report()]
        self.sample_size = sample_size
        self.reports = reports

    def __repr__(self):
        return f"DriftConfig(sample_size={self.sample_size}, reports={self.reports})"
