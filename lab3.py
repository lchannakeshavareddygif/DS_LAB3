import pandas as pd
import numpy as np
from scipy import stats
file_path = r"C:\Users\Keshava\Downloads\Inc_Exp_Data - Inc_Exp_Data.csv"
df = pd.read_csv(file_path)
num_cols = ["Mthly_HH_Income","Mthly_HH_Expense","Emi_or_Rent_Amt",
            "Annual_HH_Income","No_of_Fly_Members","No_of_Earning_Members"]
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
income_mean = df["Mthly_HH_Income"].mean()
income_median = df["Mthly_HH_Income"].median()
income_mode = df["Mthly_HH_Income"].mode().tolist()

expense_mean = df["Mthly_HH_Expense"].mean()
expense_median = df["Mthly_HH_Expense"].median()
income_range = df["Mthly_HH_Income"].max() - df["Mthly_HH_Income"].min()

df["Income_to_Expense_Ratio"] = df["Mthly_HH_Income"] / df["Mthly_HH_Expense"]
highest_ratio_row = df.loc[df["Income_to_Expense_Ratio"].idxmax()]
avg_family = df["No_of_Fly_Members"].mean()
std_family = df["No_of_Fly_Members"].std(ddof=0)
df["Dependency_Ratio"] = (df["No_of_Fly_Members"] - df["No_of_Earning_Members"]) / df["No_of_Fly_Members"]
highest_dependency_row = df.loc[df["Dependency_Ratio"].idxmax()]

df["Emi_percent_of_Income"] = df["Emi_or_Rent_Amt"] / df["Mthly_HH_Income"]
avg_emi_pct = df["Emi_percent_of_Income"].mean() * 100
emi_over_40 = df[df["Emi_percent_of_Income"] > 0.40]

df["Disposable_Income"] = df["Mthly_HH_Income"] - df["Mthly_HH_Expense"] - df["Emi_or_Rent_Amt"]
lowest_disposable_row = df.loc[df["Disposable_Income"].idxmin()]


df["Annual_from_Monthly"] = df["Mthly_HH_Income"] * 12
df["Annual_Consistent"] = np.isclose(df["Annual_HH_Income"], df["Annual_from_Monthly"], rtol=0.01)
annual_inconsistent = df[~df["Annual_Consistent"]]

qualification_group = pd.DataFrame()
if "Highest_Qualified_Member" in df.columns:
    qualification_group = df.groupby("Highest_Qualified_Member")["Mthly_HH_Income"].agg(["mean","median"])


z_scores = np.abs(stats.zscore(df["Mthly_HH_Income"].dropna()))
outliers_df = df.loc[z_scores > 3]

corr_income_expense = df["Mthly_HH_Income"].corr(df["Mthly_HH_Expense"])
corr_earningmembers_income = df["No_of_Earning_Members"].corr(df["Mthly_HH_Income"])


print("=== 1. Income & Expenditure ===")
print(f"Mean Income: {income_mean:.2f}")
print(f"Median Income: {income_median:.2f}")
print(f"Mode Income: {income_mode}")
print(f"Mean Expense: {expense_mean:.2f}")
print(f"Median Expense: {expense_median:.2f}")
print(f"Income Range: {income_range:.2f}")
print("Highest Income-to-Expense Ratio Household:")
print(highest_ratio_row)

print("\n=== 2. Family Structure ===")
print(f"Average Family Members: {avg_family:.2f}")
print(f"Std Dev Family Members: {std_family:.2f}")
print("Highest Dependency Ratio Household:")
print(highest_dependency_row)

print("\n=== 3. Housing & EMI ===")
print(f"Average EMI % of Income: {avg_emi_pct:.2f}%")
print("Households with EMI > 40% of Income:")
print(emi_over_40)
print("Lowest Disposable Income Household:")
print(lowest_disposable_row)

print("\n=== 4. Annual Income & Qualification ===")
print(f"Annual Income Consistent: {df['Annual_Consistent'].sum()} households")
print(f"Annual Income Inconsistent: {len(annual_inconsistent)} households")
print("Annual Income Inconsistencies:")
print(annual_inconsistent)
if not qualification_group.empty:
    print("\nAverage Income by Qualification:")
    print(qualification_group)

print("\n=== 5. Outliers & Correlation ===")
print("Outliers in Monthly Income:")
print(outliers_df)
print(f"Correlation (Income vs Expense): {corr_income_expense:.2f}")
print(f"Correlation (No_of_Earning_Members vs Income): {corr_earningmembers_income:.2f}")

