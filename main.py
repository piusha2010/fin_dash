import pandas as pd
import os
import matplotlib.pyplot as plt

os.makedirs("output", exist_ok=True) # Create output dir if doesn't exist

### 1.Load data

df = pd.read_csv("data.csv") # Load data
print(df.head()) # Print first 5 rows


### 2. Understand data
print("\n--- INFO ---")
print(df.info()) # Basis info

print("\n--- DESCRIBE ---")
print(df.describe()) # Basic stats

print("\n--- COLUMNS ---")
print(df.columns)# Column names

### 3. Clean data
print("\n--- MISSING VALUES ---")
print(df.isnull().sum()) # Check for missing values
df = df.dropna() # Drop rows with mising values

### 4. Analyze data
expenses  = ['Rent', 'Loan_Repayment', 'Insurance', 'Groceries', 'Transport', 'Eating_Out',
       'Entertainment', 'Utilities', 'Healthcare', 'Education', 'Miscellaneous']

print("\n--- AVERAGE EXPENSES ---")
print(df[expenses].mean().sort_values(ascending=False)) # Average expenses

# Savings Summary
print("\n--- SAVINGS STATS ---")
print("Average disposable income: ", df['Disposable_Income'].mean())
print("Average Desired Savings: ", df['Desired_Savings'].mean())

# City-wise Disposable Income
print("\n--- DISPOSABLE INCOME BY CITY TIER ---")
print(df.groupby('City_Tier')['Disposable_Income'].mean()) # Average disposable income by city tier

# % of income spent per category
for expense in expenses:
    df[f'{expense}_pct'] = (df[expense] / df['Income']) * 100 # Percentage of income spent on each category

print("\n--- % OF INCOME SPENT PER CATEGORY ---")
for expense in expenses:
    print(f"{expense.title()}: {df[f'{expense}_pct'].mean():.2f}")


# Top 3 Expenses
avg_expenses = df[expenses].mean().sort_values(ascending=False)
print("\n--- TOP 3 SPENDING CATEGORIES ---")
print(avg_expenses.head()) # Top 3 spending categories
      
# Potential Savings Summary
savings_col = [col for col in df.columns if 'Savings' in col]
avg_savings = df[savings_col].mean().sort_values(ascending=False)

print("\n --- Avg potential savings per category ---")
print(avg_savings)


### 5. Visualize data

# Bar Chart – Average Spend per Category
avg_expenses.plot(kind = 'bar', figsize=(10,6), color='red')
plt.title("Avg spend per category")
plt.xlabel("Expense Category")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("output/avg_spend_bar.png")
plt.clf()

# Pie Chart – Share of Total Spend
(df[expenses].mean() / df[expenses].mean().sum()).plot(kind='pie', figsize=(10,6), autopct='%1.1f%%')
plt.title("Share of monthly spend")
plt.ylabel("") # Remove y-label
plt.tight_layout()
plt.savefig("output/spend_pie.png")
plt.clf()

# Bar Chart – Potential Savings
avg_savings.plot(kind='bar', figsize=(10,6), color='green')
plt.title("Avg potential savings per category")
plt.ylabel("Amount")
plt.xlabel("Savings Category")
plt.tight_layout()
plt.savefig("output/savings_bar.png")
plt.clf()

df.to_csv("output/cleaned_data.csv", index=False) # Save cleaned data
print("Cleaned data saved to output/cleaned_data.csv")

report = f"""
PERSONAL FINANCE REPORT
========================

Avg Income: ₹{df['Income'].mean():.2f}
Avg Disposable Income: ₹{df['Disposable_Income'].mean():.2f}
Avg Desired Savings: ₹{df['Desired_Savings'].mean():.2f}

Top 3 Spending Categories: {avg_expenses.head(3)}
"""

with open("output/report.txt", "w", encoding = "utf-8") as f:
    f.write(report) # Save report to report.txt

print("Report saved to output/report.txt")