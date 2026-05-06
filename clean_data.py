import pandas as pd

# Load the data
df = pd.read_excel('bookings.xlsx')

print("Shape BEFORE cleaning:", df.shape)

# ── STEP 1: Check nulls ──────────────────────────────
print("\nNull values in each column:")
print(df.isnull().sum())

# ── STEP 2: Drop useless column ─────────────────────
# 'Vehicle Images' is 100% empty — no use keeping it
df.drop(columns=['Vehicle Images'], inplace=True)
print("\n✅ Dropped 'Vehicle Images' column")

# ── STEP 3: Fill nulls with logical values ───────────
# NOTE: We do NOT delete rows! Nulls exist because
# cancelled rides have no payment, rating etc. — that's valid

df['Payment_Method']            = df['Payment_Method'].fillna('Not Applicable')
df['Driver_Ratings']            = df['Driver_Ratings'].fillna(0)
df['Customer_Rating']           = df['Customer_Rating'].fillna(0)
df['V_TAT']                     = df['V_TAT'].fillna(0)
df['C_TAT']                     = df['C_TAT'].fillna(0)
df['Incomplete_Rides']          = df['Incomplete_Rides'].fillna('No')
df['Incomplete_Rides_Reason']   = df['Incomplete_Rides_Reason'].fillna('Not Applicable')
df['Canceled_Rides_by_Customer']= df['Canceled_Rides_by_Customer'].fillna('No')
df['Canceled_Rides_by_Driver']  = df['Canceled_Rides_by_Driver'].fillna('No')
print("✅ Filled all nulls with logical values")

# ── STEP 4: Fix data types ───────────────────────────
df['Date'] = pd.to_datetime(df['Date'])
print("✅ Fixed Date column type")

# ── STEP 5: Add useful new columns ──────────────────
df['Day']       = df['Date'].dt.day
df['DayOfWeek'] = df['Date'].dt.day_name()
df['Hour']      = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.hour
print("✅ Added Day, DayOfWeek, Hour columns")

# ── STEP 6: Add Time Period label ────────────────────
def get_time_period(hour):
    if pd.isna(hour):    return 'Unknown'
    if 5  <= hour < 12:  return 'Morning'
    if 12 <= hour < 17:  return 'Afternoon'
    if 17 <= hour < 21:  return 'Evening'
    return 'Night'

df['Time_Period'] = df['Hour'].apply(get_time_period)
print("✅ Added Time_Period column (Morning/Afternoon/Evening/Night)")

# ── STEP 7: Verify zero nulls ────────────────────────
print("\nNull values AFTER cleaning:")
print(df.isnull().sum())

print("\nShape AFTER cleaning:", df.shape)

# ── STEP 8: Save cleaned data ────────────────────────
df.to_csv('cleaned_bookings.csv', index=False)
print("\n✅ Saved cleaned data as cleaned_bookings.csv")