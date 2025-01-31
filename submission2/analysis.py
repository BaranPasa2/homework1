import pandas as pd

# import the dataset that we created
compTotalData = pd.read_csv("data/output/compTotalData.csv")

#create the tables:

typePlans = compTotalData.pivot_table(index='plan_type', columns='year', values='planid', aggfunc='count')
