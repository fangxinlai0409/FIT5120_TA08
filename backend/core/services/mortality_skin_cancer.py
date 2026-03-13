from pathlib import Path
import pandas as pd

# resolves project root directory
BASE_DIR = Path(__file__).resolve().parents[3]

# paths to input and output datasets
file_path = BASE_DIR/"data"/"mortality_melanoma.xlsx"
output_path = BASE_DIR/"data"/"mortality_melanoma_10yr.xlsx"

# reads the Excel sheet containing melanoma mortality
df = pd.read_excel(file_path, sheet_name="Table S2a.1", header=5)

# keeps only the required columns
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

# keeps only data from 1982 onward
df = df[df["Year"] >= 1982]

# filters rows to keep only melanoma deaths
df = df[df["Cancer group/site"] == "Melanoma of the skin"]

# extracts the starting age from each age band
df["age_start"] = df["Age group (years)"].str.extract(r"(\d+)").astype(float)

# keeps only age groups 15 years and older
df = df[df["age_start"] >= 15]

# reconstructs population from the epidemiological rate formula
df["population"] = df["Count"] / df["Age-specific rate\n(per 100,000)"] * 100000

# computes the new 10-year age bands starting at 15
df["age_bin_start"] = ((df["age_start"] - 15) // 10) * 10 + 15

df["Age group (years)"] = (
    df["age_bin_start"].astype(int).astype(str)
    + "–"
    + (df["age_bin_start"] + 9).astype(int).astype(str)
)

# aggregates rows by year, sex and new age group
result = df.groupby(
    ["Year", "Sex", "Age group (years)"],
    as_index=False
).agg(
    {
        "Count": "sum",
        "population": "sum"
    }
)

# recomputes the mortality rate for the combined population
result["Age-specific rate(per 100,000)"] = (
    (result["Count"] / result["population"] * 100000).round(2)
)

# removes the temporary population column
result = result.drop(columns=["population"])

# saves the processed dataset into the shared data folder
result.to_excel(output_path, index=False)


# Data source reference
# The melanoma mortality data used in this script originates
# from the Australian Institute of Health and Welfare (AIHW)
# "Cancer Data in Australia" dataset.

# Dataset title:
# Cancer Mortality from 1982 to 2017 in Australia

# Accessed from:
# https://www.aihw.gov.au/getmedia/9f5cdd1c-87f7-4f05-9a4f-8c5141a3e17e/AIHW-CAN-122-CDiA-2021-Book-2a-Cancer-mortality-age-standardised-rates-5-year-age-groups.xlsx.aspx