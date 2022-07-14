# functions for site



from matplotlib.transforms import Bbox
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def save_plot_image(df:pd.DataFrame, file_name:str):

    # TODO automagically run script once per day to update plot images
    
    sns.set_style('darkgrid')
    plt.figure(figsize=(15, 10))
    
    plot = sns.lineplot(data=df)
    
    plot.set_xticks(range(len(df.day)))
    plot.set_xticklabels(df['day'])

    plt.xlabel('Date of Record')
    plt.ylabel('Pool Reward Annual Percentage Rate') 
    plt.xticks(rotation=45)
    
    # test_plot_folder = 'static\\function_test_sample_files\\'

    plot_folder = 'static\\plot_imgs\\'

    #remove excess whitespace around image and save
    plt.savefig('{}{}'.format(plot_folder, file_name), bbox_inches='tight')
    # plt.show()


if __name__ == '__main__':

    csv_path = R'dashboard_site\static\function_test_sample_files\AKT_OSMO.csv'
    file_name = csv_path[49:-3]
    df = pd.read_csv(csv_path)
    
    save_plot_image(df, file_name)