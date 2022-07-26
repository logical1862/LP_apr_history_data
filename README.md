# LP_apr_history_data
 visualization of historical data for Osmosis crypto liquidity pool apr data
 
 still under development
 
 planned AWS services: Lambda, S3, Elastic Beanstalk, CloudWatch Events
 
 lambda function scheduled to run once daily:
  (taken from my OSMO_logger repo, configured for s3 and lambda)
  -makes request to API for pool data, reads APR data from response as Pandas Dataframe, converts to csv, saves to s3 bucket
  
  Flask App:
  reads data from s3 bucket. data passed to helpers.save_plot_image() to plot line graph figure, save figure as .png in static directory, then rerenders page with selected pool (selected from html page)
 
 
 
 major issues:
  configuration for AWS S3 bucket for database
  change db from sqlite3 to better alternative
  intital render of page renders outdated static plot img
