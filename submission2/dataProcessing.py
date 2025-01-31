import pandas as pd

contractData = pd.read_csv("data/input/CPSC_Contract_Info_2015_01.csv", encoding='latin1', skiprows=1, names=[
        "contractid", "planid", "org_type", "plan_type", "partd", "snp", "eghp", "org_name",
        "org_marketing_name", "plan_name", "parent_org", "contract_date"
    ], dtype={
        "contractid": str,
        "planid": float,
        "org_type": str,
        "plan_type": str,
        "partd": str,
        "snp": str,
        "eghp": str,
        "org_name": str,
        "org_marketing_name": str,
        "plan_name": str,
        "parent_org": str,
        "contract_date": str
    })


enrollmentData = pd.read_csv("data/input/CPSC_Enrollment_Info_2015_01.csv", skiprows=1, names=[
        "contractid", "planid", "ssa", "fips", "state", "county", "enrollment"
    ], dtype={
        "contractid": str,
        "planid": float,
        "ssa": float,
        "fips": float,
        "state": str,
        "county": str,
        "enrollment": float
    }, na_values="*")

contractData['idCount'] = contractData.groupby(['contractid', 'planid']).cumcount() + 1
contractData = contractData[contractData["idCount"] == 1].drop(columns=['idCount'])

# merge:
mergedData = contractData.merge(enrollmentData, on=["contractid", "planid"], how="left")
mergedData['year'] = 2015

# do more cleaning with FIPS codes, etc.
mergedData['fips'] = mergedData.groupby(['state', 'county',])['fips'].ffill().bfill()

for char in ['plan_type', 'partd', 'snp', 'eghp', 'plan_name']:
    mergedData[char] = mergedData.groupby(['contractid', 'planid'])[char].ffill().bfill()

for char in ['org_type', 'org_name', 'org_marketing_name', 'parent_org']:
    mergedData[char] = mergedData.groupby(['contractid'])[char].ffill().bfill()

mergedData.rename(columns={"enrollment": "avg_enrollment"}, inplace=True)

compMergedData = pd.DataFrame()
compMergedData = pd.concat([compMergedData, mergedData], ignore_index=True)

compMergedData.to_csv("data/output/compTotalData.csv")