import pandas as pd
import os

contact_info2015 = pd.read_csv('data/input/CPSC_Contract_Info_2015_01.csv', encoding='latin1')
year = 2015

#print(contact_info2015.info())

contract_info = pd.read_csv('data/input/CPSC_Contract_Info_2015_01.csv', encoding='latin1', skiprows=1,
                                names = [    
                                    "Contract ID", "Plan ID", "organization Type", "Plan Type",
                                    "Offers Part D",  "SNP Plan", "EGHP", "Organization Name", 
                                    "Organization Marketing Name", "plan Name", "Parent Organization",
                                    "Contract Effective Date"], dtype={
                                        "Contract ID": object, "Plan ID": float, "organization Type": object, 
                                        "Plan Type": object, "Offers Part D": object,  "SNP Plan": object, "EGHP": object, "Organization Name": object, 
                                        "Organization Marketing Name": object, "Plan Name": object, "Parent Organization": object,
                                        "Contract Effective Date": object
                                    })
contract_info['id_count'] = contract_info.groupby(['Contract ID', "Plan ID"]).cumcount() + 1
contract_info = contract_info[contract_info['id_count'] == 1].drop(columns=['id_count'])

enrollment_info= pd.read_csv('data/input/CPSC_Enrollment_Info_2015_01.csv', encoding='latin1', skiprows=1,
                             names = [
                                 "Contract Number", "Plan ID", "SSA State County Code", "FIPS State County Code",
                                 "State", "County", "Enrollment"
                             ], dtype = {
                                  "Contract Number": object, "Plan ID": int, "SSA State County Code": int, "FIPS State County Code": float,
                                 "State": object, "County": object, "Enrollment": object
                             }, na_values=['*'])

enrollment_info.rename(columns={"Contract Number": "Contract ID"}, inplace=True)

# Do not need to specify year because they are all for the year 2015

plan_data = contract_info.merge(enrollment_info, on=["Contract ID", "Plan ID"], how="left")

