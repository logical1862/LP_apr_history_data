from flask import Flask, render_template, request, flash
from datetime import datetime
import sqlite3
import pandas as pd
import wget
import os

import helpers


def update_apr_db():
   """Removes current pool_apr.db and replaces with the most current database from S3"""
   
   os.remove('pool_apr.db')

   database_s3_url = 'https://osmosystemdata.s3.amazonaws.com/poolAPRdatabase/pool_apr.db'

   database_local_path = 'pool_apr.db'

   try:
      wget.download(database_s3_url, out=database_local_path)

   except Exception as e:
      pass


def apr_db_needs_update():

   # both times are in UNIX timestamp format

   time_of_last_update = os.path.getctime('pool_apr.db')

   time_now = datetime.now().timestamp()

   # function returns seconds since creation, 86400 seconds in a day
   if (time_now - time_of_last_update) > 86400:
      return True

   return False



def apr_database_check():
   if apr_db_needs_update():
      update_apr_db()

   else:
      pass

def get_name_list():
    # create cursor connection to database, get list of table names
      conn = sqlite3.connect('pool_apr.db')
      cur = conn.cursor()
      cur.execute("""
   SELECT name FROM sqlite_schema
   WHERE type='table'
   ORDER BY name;
                  """)
      name_list = cur.fetchall()
      return name_list, conn


app = Flask(__name__)

app.secret_key='SECRET'

@app.route('/', methods=['GET', 'POST'])
def index():


   apr_database_check()


   if request.method == 'GET':
      # create cursor connection to database, get list of table names
      name_list, conn = get_name_list()



      # first plot img shown on site load

      # TODO dynamically set first img to first pool name in list, file path should be '\static\plot_imgs\{< first pool >}'

      initial_img_path = R"/static/function_test_sample_files/AKT_ATOM.png"

      return render_template('index.html', name_list=name_list, img_path=initial_img_path)



    # post should happen when submit button is clicked to view different pool plots
   if request.method == 'POST':
      name_list, conn = get_name_list()

      # get name of selected pool
      pool_plot_img_selection = request.form.get('pool_selection')

      # create dataframe by reading pool_apr.db,with name of pool pass to helpers.save_plot_image(overwriting if it exists)
      # before calling on that image to return index template with selected pool as new plot image

      selected_pool_df = pd.read_sql(f'SELECT * FROM {pool_plot_img_selection}', conn, index_col='index')

      helpers.save_plot_image(selected_pool_df, pool_plot_img_selection)


      # TODO set path to selected pool in '\static\plot_imgs\'

      img_path = "/static/plot_imgs/{}.png".format(pool_plot_img_selection)

      flash(f'Selected: {pool_plot_img_selection}', 'pool_selection')
      return render_template('index.html', name_list=name_list, img_path=img_path)
   # page first load

