import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

if __name__ == '__main__':
    data = pd.read_csv('./soup-data.csv')
    user = 'super_admin'
    pwd = 'SomeSecretPassword'
    host = 'localhost'
    port = '5432'
    database = 'postgres'

    db_connect_str = f"postgresql://{user}:{pwd}@{host}:{port}/{database}"
    engine = None
    try:
        engine = sqlalchemy.create_engine(db_connect_str)
        engine.connect()
    except SQLAlchemyError as err:
        print(f"Could not connect to {host} {database} database - {err}")
        #         logger.error(f"Could not connect to {host} {database} database - {err}")
        #         logger.error(f"Error {err}")
        exit(5000)

    data.to_sql('soup_shop', con=engine, if_exists='replace', index=False)


