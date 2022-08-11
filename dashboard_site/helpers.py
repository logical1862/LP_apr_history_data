# functions for site

import wget
import os
import sqlite3
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from datetime import datetime


def save_plot_image(df:pd.DataFrame, file_name:str):
    
    sns.set_style('darkgrid')
    plt.figure(figsize=(15, 10))
    
    plot = sns.lineplot(data=df)
    
    plot.set_xticks(range(len(df.day)))
    plot.set_xticklabels(df['day'])

    plt.xlabel('Date of Record')
    plt.ylabel('Pool Reward Annual Percentage Rate') 
    plt.xticks(rotation=45)
    
    # test_plot_folder = 'static\\function_test_sample_files\\'

    plot_folder = 'static/plot_imgs/'

    #remove excess whitespace around image and save
    plt.savefig('{}{}'.format(plot_folder, file_name), bbox_inches='tight')



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







if __name__ == '__main__':

    csv_path = R'dashboard_site/static/function_test_sample_files/AKT_OSMO.csv'
    file_name = csv_path[49:-3]
    df = pd.read_csv(csv_path)
    
    save_plot_image(df, file_name)