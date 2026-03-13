from pathlib import Path
import pandas as pd

# gets the project root directory
BASE_DIR = Path(__file__).resolve().parents[3]

# file paths
file_path = BASE_DIR/"data"/"cancer_incidence.xlsx"
output_path = BASE_DIR/"data"/"skin_melanoma.xlsx"

# reads the Excel sheet containing the melanoma dataset
df = pd.read_excel(file_path, sheet_name="Table S1a.1", header=5)

# keeps only the required columns for the analysis
df = df[
    [
        "Data type",
        "Cancer group/site",
        "Year",
        "Sex",
        "Age group (years)",
        "Count",
        "Age-specific rate\n(per 100,000)"
    ]
]

# filters rows to keep only melanoma cases
df = df[df["Cancer group/site"] == "Melanoma of the skin"]

# filters rows to keep only age groups 15–19 and 20–24
df = df[df["Age group (years)"].isin(["15–19", "20–24"])]

# estimates population using the rate formula
df["population"] = df["Count"] / df["Age-specific rate\n(per 100,000)"] * 100000

# groups rows by year and sex and combines the two age bands
result = (
    df.groupby(["Data type", "Cancer group/site", "Year", "Sex"], as_index=False)
    .agg({"Count": "sum", "population": "sum"})
)

# assigns the merged age category
result["Age group (years)"] = "15–24"

# recalculates the age-specific rate for the combined population
result["Age-specific rate\n(per 100,000)"] = (result["Count"] / result["population"] * 100000).round(2)

# removes the temporary population column
result = result.drop(columns=["population"])

# saves the processed dataset
result.to_excel(output_path, index=False)

print(result.head())

# Data source reference
# The melanoma incidence data used in this script originates
# from the Australian Institute of Health and Welfare (AIHW)
# "Cancer Data in Australia" dataset.

# Dataset title:
# Cancer Incidence from 1982 to 2017 in Australia

# Accessed from:
# https://www.aihw.gov.au/getmedia/e8779760-1b3c-4c2e-a6c2-b0a8d764c66b/AIHW-CAN-122-CDiA-2021-Book-1a-Cancer-incidence-age-standardised-rates-5-year-age-groups.xlsx.aspx