import sqlite3
import pandas as pd
import PortalException
from portal_logs import logging
import os, sys

def save_data_db(data:pd.DataFrame) -> None:

    try:
        # database connection
        logging.info(f"Connecting to the database")
        conn = sqlite3.connect('wolle_portal.db')

        #create_sql = 'CREATE TABLE IF NOT EXISTS portal(brand_name text, price text, \
                        #needle_size text, compose text,delivery_time text'

        #cursor = conn.cursor()
        # table creation
        #cursor.execute(create_sql)
        logging.info(f"Creating or replacing table in the databse")
        data.to_sql(name = 'portal', con=conn, if_exists='replace', index=False)
        conn.commit()
        logging.info('The data is saved into the Database')
        # view saved data in the db using sql studio or https://inloop.github.io/sqlite-viewer/
    
    except Exception as e:
        raise PortalException(e,sys) from e