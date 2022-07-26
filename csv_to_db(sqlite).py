# creates / updates database tables with data from logged csv files (using apr_logger 'https://github.com/logical1862/OSMO_logger')

import sqlite3
import pandas as pd
import os

def to_dataframe(folder_path, file_list):
    # returns dictionary of dataframes from file list 
    df_group = {}
    for file in file_list:
        pool_name = file[:-4]

        # get path to csv for pandas to read, separated into file lists for multithreading
        file_path = f'{folder_path}\{file}'
        df = pd.read_csv(file_path)

        df_group[pool_name] = df
    return df_group

def df_to_database(df_dictionary, connection):
    # takes a dictionary of pandas dataframes, saves them to given sqlite database tables
    for pool_name in df_dictionary:
        df = df_dictionary[pool_name]

        try:
            df.to_sql(pool_name, connection, if_exists='replace')
            print(f'success {pool_name}')

        except:
            print(f'failed {pool_name}')

def main(database):
    # data files from apr_logger are saved here. updated daily
    user_path = os.environ['USERPROFILE']
    csv_folder_path = f"{user_path}\OSMO_apr_data\pool_info" 

    # initialize connection to database
    connection = sqlite3.connect(database)
    c = connection.cursor()

    files = os.listdir(csv_folder_path)

    # convert csv files to pandas dataframes
    df_dictionary = to_dataframe(csv_folder_path, files)
    
    # save to sqlite database
    df_to_database(df_dictionary, connection)



if __name__ == '__main__':
    database = 'pool_apr.db'
    main(database=database)
 