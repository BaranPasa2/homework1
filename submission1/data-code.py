import pandas as pd
import os
from tabulate import tabulate

# Load the datasets
enrollment_file_path = "data/input/CPSC_Enrollment_Info_2015_01.csv"  # Update with your file path
contract_file_path = "data/input/CPSC_Contract_Info_2015_01.csv"  # Update with your file path

enrollment_df = pd.read_csv(enrollment_file_path)
contract_df = pd.read_csv(contract_file_path, encoding='latin1')

# Standardize column names
enrollment_df.columns = enrollment_df.columns.str.strip().str.replace(" ", "_")
contract_df.columns = contract_df.columns.str.strip().str.replace(" ", "_")

# Perform an inner merge on Contract Number/Contract ID and Plan ID
merged_df = enrollment_df.merge(
    contract_df,
    left_on=["Contract_Number", "Plan_ID"],
    right_on=["Contract_ID", "Plan_ID"],
    how="inner"
)

# Drop redundant columns after merging
merged_df.drop(columns=["Contract_ID"], inplace=True)

# Save the result
merged_df.to_csv("Merged_Enrollment_Data_2015.csv", index=False)

# 1. Count of plans by type
plan_count_by_type = merged_df['Plan_Type'].value_counts().reset_index()
plan_count_by_type.columns = ['Plan_Type', 'Count']

# 2. Exclude SNP, EGHP, and "800-series" plans
filtered_df = merged_df[
    (merged_df['SNP_Plan'] == 'No') &
    (merged_df['EGHP'] == 'No') &
    (~merged_df['Plan_ID'].astype(str).str.startswith("800"))
]

filtered_plan_count_by_type = filtered_df['Plan_Type'].value_counts().reset_index()
filtered_plan_count_by_type.columns = ['Plan_Type', 'Count']

# 3. Average enrollment by type
filtered_df['Enrollment'] = pd.to_numeric(filtered_df['Enrollment'], errors='coerce')
avg_enrollment_by_type = filtered_df.groupby('Plan_Type')['Enrollment'].mean().reset_index()
avg_enrollment_by_type.columns = ['Plan_Type', 'Average_Enrollment']

# Save results directly to the "output" folder
output_folder = "data/output"
plan_count_by_type.to_csv(os.path.join(output_folder, "Plan_Count_by_Type_Original.csv"), index=False)
filtered_plan_count_by_type.to_csv(os.path.join(output_folder, "Plan_Count_by_Type_Filtered.csv"), index=False)
avg_enrollment_by_type.to_csv(os.path.join(output_folder, "Average_Enrollment_by_Type.csv"), index=False)

print(f"Results saved to the '{output_folder}' folder.")

print("\nPlan Count by Type (Original):")
print(tabulate(plan_count_by_type, headers='keys', tablefmt='pretty'))

print("\nPlan Count by Type (Filtered):")
print(tabulate(filtered_plan_count_by_type, headers='keys', tablefmt='pretty'))

print("\nAverage Enrollment by Type:")
print(tabulate(avg_enrollment_by_type, headers='keys', tablefmt='pretty'))

print(f"\nResults saved to the '{output_folder}' folder.")