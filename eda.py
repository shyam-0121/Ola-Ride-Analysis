import pandas as pd

# Load the CLEANED data (not the original!)
df = pd.read_csv('cleaned_bookings.csv')

# ════════════════════════════════════════════
# 1. BOOKING STATUS — How many success vs cancel?
# ════════════════════════════════════════════
print("=" * 50)
print("1. BOOKING STATUS BREAKDOWN")
print("=" * 50)
print(df['Booking_Status'].value_counts())
print("\nIn percentages:")
print(df['Booking_Status'].value_counts(normalize=True).mul(100).round(2))

# ════════════════════════════════════════════
# 2. VEHICLE TYPE — Which is most popular?
# ════════════════════════════════════════════
print("\n" + "=" * 50)
print("2. VEHICLE TYPE POPULARITY")
print("=" * 50)
print(df['Vehicle_Type'].value_counts())

# ════════════════════════════════════════════
# 3. REVENUE — Total, Average, Max, Min
# ════════════════════════════════════════════
print("\n" + "=" * 50)
print("3. REVENUE ANALYSIS (Successful rides only)")
print("=" * 50)
success = df[df['Booking_Status'] == 'Success']

print(f"Total Revenue:    ₹{success['Booking_Value'].sum():,.0f}")
print(f"Average per Ride: ₹{success['Booking_Value'].mean():,.2f}")
print(f"Max Single Ride:  ₹{success['Booking_Value'].max():,.0f}")
print(f"Min Single Ride:  ₹{success['Booking_Value'].min():,.0f}")

# ════════════════════════════════════════════
# 4. REVENUE BY VEHICLE TYPE
# ════════════════════════════════════════════
print("\n" + "=" * 50)
print("4. REVENUE BY VEHICLE TYPE")
print("=" * 50)
rev_by_vehicle = success.groupby('Vehicle_Type')['Booking_Value'].sum().sort_values(ascending=False)
print(rev_by_vehicle)

# ════════════════════════════════════════════
# 5. PAYMENT METHOD — How do people pay?
# ════════════════════════════════════════════
print("\n" + "=" * 50)
print("5. PAYMENT METHOD")
print("=" * 50)
print(df[df['Payment_Method'] != 'Not Applicable']['Payment_Method'].value_counts())

# ════════════════════════════════════════════
# 6. PEAK HOURS — When do most rides happen?
# ════════════════════════════════════════════
print("\n" + "=" * 50)
print("6. PEAK HOURS (Top 5)")
print("=" * 50)
print(df.groupby('Hour')['Booking_ID'].count().sort_values(ascending=False).head(5))

# ════════════════════════════════════════════
# 7. CANCELLATION — Who cancels more?
# ════════════════════════════════════════════
print("\n" + "=" * 50)
print("7. CANCELLATION ANALYSIS")
print("=" * 50)
canceled_customer = (df['Booking_Status'] == 'Canceled by Customer').sum()
canceled_driver   = (df['Booking_Status'] == 'Canceled by Driver').sum()
driver_not_found  = (df['Booking_Status'] == 'Driver Not Found').sum()

print(f"Canceled by Customer: {canceled_customer:,}")
print(f"Canceled by Driver:   {canceled_driver:,}")
print(f"Driver Not Found:     {driver_not_found:,}")

# ════════════════════════════════════════════
# 8. RATINGS — How good is the service?
# ════════════════════════════════════════════
print("\n" + "=" * 50)
print("8. RATINGS (Successful rides only)")
print("=" * 50)
rated = success[success['Driver_Ratings'] > 0]
print(f"Avg Driver Rating:   {rated['Driver_Ratings'].mean():.2f} / 5")
print(f"Avg Customer Rating: {rated['Customer_Rating'].mean():.2f} / 5")

# ════════════════════════════════════════════
# 9. RIDE DISTANCE — How far do people travel?
# ════════════════════════════════════════════
print("\n" + "=" * 50)
print("9. RIDE DISTANCE")
print("=" * 50)
print(f"Average Distance: {success['Ride_Distance'].mean():.2f} km")
print(f"Max Distance:     {success['Ride_Distance'].max()} km")
print(f"Min Distance:     {success['Ride_Distance'].min()} km")

# ════════════════════════════════════════════
# 10. TIME PERIOD — Morning vs Night?
# ════════════════════════════════════════════
print("\n" + "=" * 50)
print("10. BOOKINGS BY TIME PERIOD")
print("=" * 50)
print(df.groupby('Time_Period')['Booking_ID'].count().sort_values(ascending=False))