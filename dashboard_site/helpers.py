# functions for site



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
    # TODO set correct folder path
    test_plot_folder = 'dashboard_site\\static\\function_test_sample_files\\'

    # plot_folder = 
    plt.savefig('{}{}'.format(test_plot_folder, file_name))
    # plt.show()


if __name__ == '__main__':

    path = R'dashboard_site\static\function_test_sample_files\AKT_ATOM.csv'
    file_name = path[49:-3]
    df = pd.read_csv(path)
    
    save_plot_image(df, file_name)