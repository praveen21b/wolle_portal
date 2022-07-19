from flask import Flask,render_template
from portal import WebScraper
import pandas as pd
from db import save_data_db
import os,sys
from PortalException import PortalException
from portal_logs import logging
from save_csv import save_as_csv
app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def home():
    try:

        # creating dataframe
        df = WebScraper('schema.yaml').output()
        logging.info(f"Dataframe created")
        # saving to database
        save_data_db(data=df)
        logging.info(f"Database file created and all data saved.")
        save_as_csv(df)
        return render_template('home_render.html', tables=[df.to_html(classes='data', header="true")])
    
    except Exception as e:
        raise PortalException(e,sys)

if __name__ == '__main__':
    app.run(debug=True)