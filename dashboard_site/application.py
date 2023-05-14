import os
from flask import Flask, render_template, request, flash
import pandas as pd



import helpers


app = Flask(__name__)

app.secret_key='SECRET'
print(os.getcwd)

@app.route('/', methods=['GET', 'POST'])
def index():


    helpers.apr_database_check()
    name_list, conn = helpers.get_name_list()

    # get name of selected pool
    pool_plot_img_selection = request.form.get('pool_selection')

    # generate new plot
    selected_pool_df = pd.read_sql(
        f'SELECT * FROM {pool_plot_img_selection}',
        conn,
        index_col='index'
        )
    helpers.save_plot_image(selected_pool_df, pool_plot_img_selection)
    img_path = f"static/img_files/{pool_plot_img_selection}.png"

    flash(f'Selected: {pool_plot_img_selection}', 'pool_selection')

    return render_template('index.html', name_list=name_list, img_path=img_path)
