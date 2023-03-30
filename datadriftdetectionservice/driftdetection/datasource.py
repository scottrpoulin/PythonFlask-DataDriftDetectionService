import sqlalchemy
from sqlalchemy import text
import pandas as pd
from datadriftdetectionservice.driftdetection.config_classes import DatabaseConfig, Table
# Connection to PostgreSQL
from sqlalchemy.exc import SQLAlchemyError


def postgres(user, pwd, host, port, database):
    db_connect_str = f"postgresql://{user}:{pwd}@{host}:{port}/{database}"
    try:
        engine = sqlalchemy.create_engine(db_connect_str)
        engine = engine.connect()
    except SQLAlchemyError as err:
        print(f"Could not connect to {host} {database} database - {err}")
        exit(5000)

    return engine


def query_data(database_config: DatabaseConfig, table:Table, interval, sample_size=None):
    if database_config.database_type == 'postgres':
        engine = postgres(database_config.username, database_config.password, database_config.host, database_config.port, database_config.database)
        reference_data, current_data = None, None
        if engine is not None:
            columns = table.columns
            columns_str = ""
            for i in range(len(columns)):
                if i < len(columns)-1:
                    columns_str += columns[i] + ","
                else:
                    columns_str += columns[i]
            ref_sqlstr = """SELECT """+columns_str+""" FROM """+str(table.table_name)+""" WHERE """+str(table.date_column)+"""::date > (current_date - interval '"""+str(interval*2)+"""' day)::date AND """+table.date_column+"""::date < (current_date - interval '"""+str(interval)+"""' day)::date"""
            cur_sqlstr = """SELECT """+columns_str+""" FROM """+str(table.table_name)+""" WHERE """+str(table.date_column)+"""::date > (current_date - interval '"""+str(interval)+"""' day)::date"""
            if sample_size is not None:
                ref_sqlstr += """ LIMIT """+str(sample_size)
                cur_sqlstr += """ LIMIT """+str(sample_size)
            ref_sqlstr = text(ref_sqlstr)
            cur_sqlstr = text(cur_sqlstr)
            reference_data = pd.read_sql_query(sql=ref_sqlstr, con=engine)
            current_data = pd.read_sql_query(sql=cur_sqlstr, con=engine)
            engine.close()
        return reference_data, current_data
    else:
        print("No Database Provided")
        return
