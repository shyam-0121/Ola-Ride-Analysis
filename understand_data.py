import pandas as pd

# Load the data
df = pd.read_excel('bookings.xlsx')

# 1. How many rows and columns?
print("Shape:", df.shape)

# 2. What are the column names?
print("\nColumns:", df.columns.tolist())

# 3. What data types are there?
print("\nData Types:")
print(df.dtypes)

# 4. See first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# 5. Basic statistics
print("\nBasic Stats:")
print(df.describe())