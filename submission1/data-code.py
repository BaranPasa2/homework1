import pandas as pd
import os
from tabulate import tabulate

# Load the datasets
enrollment_dataFrame = pd.read_csv("data/input/CPSC_Enrollment_Info_2015_01.csv")
serviceArea_dataFrame = pd.read_csv("data/input/MA_Cnty_SA_2015_01.csv")
contract_dataFrame = pd.read_csv("data/input/CPSC_Contract_Info_2015_01.csv", encoding='latin1')

# Standardize column names
enrollment_dataFrame.columns = enrollment_dataFrame.columns.str.strip().str.replace(" ", "_")
contract_dataFrame.columns = contract_dataFrame.columns.str.strip().str.replace(" ", "_")
serviceArea_dataFrame.columns = contract_dataFrame.columns.str.strip().str.replace(" ", "_")


# Perform an inner merge on Contract Number/Contract ID and Plan ID
combined_dataFrame = enrollment_dataFrame.merge(
    contract_dataFrame, serviceArea_dataFrame,
    left_on=["Contract_Number", "Plan_ID"],
    right_on=["Contract_ID", "Plan_ID"],
    how="inner"
    )

# Dropping redundant columns
combined_dataFrame.drop(columns=["Contract_ID"], inplace=True)

# Saving the result
combined_dataFrame.to_csv("Merged_Enrollment_Data_2015.csv", index=False)

# 1. Count of plans by type
plan_count_by_type = combined_dataFrame['Plan_Type'].value_counts().reset_index()
plan_count_by_type.columns = ['Plan_Type', 'Count']

# 2. Excluding SNP, EGHP, and "800-series" plans
excludedPlans_dataFrame = combined_dataFrame[
    (combined_dataFrame['SNP_Plan'] == 'No') &
    (combined_dataFrame['EGHP'] == 'No') &
    (~combined_dataFrame['Plan_ID'].astype(str).str.startswith("800"))
]

filtered_plan_count_by_type = excludedPlans_dataFrame['Plan_Type'].value_counts().reset_index()
filtered_plan_count_by_type.columns = ['Plan_Type', 'Count']

# 3. Average enrollment by type
excludedPlans_dataFrame['Enrollment'] = pd.to_numeric(excludedPlans_dataFrame['Enrollment'], errors='coerce')
avg_enrollment_type = excludedPlans_dataFrame.groupby('Plan_Type')['Enrollment'].mean().reset_index()
avg_enrollment_type.columns = ['Plan_Type', 'Average_Enrollment']

# Save results directly to the "output" folder
output_folder = "data/output"

# The following lines are commented out so that files are not repeatedly createed/added to the Output folder.

plan_count_by_type.to_csv(os.path.join(output_folder, "Plan_Count_by_Type_Original.csv"), index=False)
filtered_plan_count_by_type.to_csv(os.path.join(output_folder, "Plan_Count_by_Type_Filtered.csv"), index=False)
avg_enrollment_type.to_csv(os.path.join(output_folder, "Average_Enrollment_by_Type.csv"), index=False)

print(f"Results saved to the '{output_folder}' folder.")

print("\nPlan Count by Type (Original):")
print(tabulate(plan_count_by_type, headers='keys', tablefmt='pretty'))

print("\nPlan Count by Type (Filtered):")
print(tabulate(filtered_plan_count_by_type, headers='keys', tablefmt='pretty'))

print("\nAverage Enrollment by Type:")
print(tabulate(avg_enrollment_type, headers='keys', tablefmt='pretty'))

print(f"\nResults saved to the '{output_folder}' folder.")