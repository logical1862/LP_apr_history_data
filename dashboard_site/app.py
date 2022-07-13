from flask import Flask, render_template, request
import sqlite3

import helpers
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

   # create cursor connection to database, get list of table names
    with sqlite3.connect('../pool_apr.db') as conn:
       cur = conn.cursor()
       cur.execute("""
SELECT name FROM sqlite_schema
WHERE type='table'
ORDER BY name;
                """)
       name_list = cur.fetchall()

    # first plot img shown on site load

    # TODO dynamically set first img to first pool name in list, file path should be '\static\plot_imgs\{< first pool >}'

    initial_img_path = R"\static\function_test_sample_files\AKT_ATOM.png"

    # post should happen when submit button is clicked to view different pool plots
    if request.method == 'POST':
       pool_plot_img_selection = request.form.get('pool_selection')

      # TODO set path to selected pool in '\static\plot_imgs\'

       img_path = "\\static\\function_test_sample_files\\{}.png".format(pool_plot_img_selection)
       return render_template('index.html', name_list=name_list, img_path=img_path)
   # page first load
    return render_template('index.html', name_list=name_list, img_path=initial_img_path)
