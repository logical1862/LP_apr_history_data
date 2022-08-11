from flask import Flask, render_template, request, flash
import pandas as pd



import helpers


app = Flask(__name__)

app.secret_key='SECRET'

@app.route('/', methods=['GET', 'POST'])
def index():


   helpers.apr_database_check()


   if request.method == 'GET':
      # create cursor connection to database, get list of table names
      name_list, conn = helpers.get_name_list()



      # first plot img shown on site load

      # TODO dynamically set first img to first pool name in list, file path should be '\static\plot_imgs\{< first pool >}'

      initial_img_path = R"/static/function_test_sample_files/AKT_ATOM.png"

      return render_template('index.html', name_list=name_list, img_path=initial_img_path)



    # post should happen when submit button is clicked to view different pool plots
   if request.method == 'POST':
      name_list, conn = helpers.get_name_list()

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

