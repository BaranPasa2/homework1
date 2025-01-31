import pandas as pd

# import the dataset that we created
compTotalData = pd.read_csv("data/output/compTotalData.csv")

#create the tables:

typePlans = compTotalData.pivot_table(index='plan_type', columns='year', values='planid', aggfunc='count')

compTotalDataFin = compTotalData[(compTotalData['snp'] == "No") & (compTotalData['eghp'] == "No") & ((compTotalData['planid'] < 800) | (compTotalData['planid'] >= 900))]
typePlans = compTotalDataFin.pivot_table(index='plan_type', columns='year', values='avg_enrollment', aggfunc='count')

enrollmentType = compTotalDataFin.pivot_table(index='plan_type', columns='year', values='avg_enrollment', aggfunc='mean')
