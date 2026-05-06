import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('cleaned_bookings.csv')
success = df[df['Booking_Status'] == 'Success']

# Global style
sns.set_theme(style='whitegrid')
plt.rcParams['figure.dpi'] = 120

# ════════════════════════════════════════════
# CHART 1 — Booking Status (Bar Chart)
# ════════════════════════════════════════════
plt.figure(figsize=(8, 5))
status_counts = df['Booking_Status'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#e67e22', '#3498db']
plt.bar(status_counts.index, status_counts.values, color=colors)
plt.title('Booking Status Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Status')
plt.ylabel('Count')
for i, v in enumerate(status_counts.values):
    plt.text(i, v + 200, f'{v:,}', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('chart1_booking_status.png')
plt.show()
print("✅ Chart 1 saved")

# ════════════════════════════════════════════
# CHART 2 — Vehicle Type Popularity (Horizontal Bar)
# ════════════════════════════════════════════
plt.figure(figsize=(8, 5))
veh_counts = df['Vehicle_Type'].value_counts()
sns.barplot(x=veh_counts.values, y=veh_counts.index, palette='Blues_r')
plt.title('Vehicle Type Popularity', fontsize=14, fontweight='bold')
plt.xlabel('Number of Bookings')
plt.ylabel('Vehicle Type')
plt.tight_layout()
plt.savefig('chart2_vehicle_type.png')
plt.show()
print("✅ Chart 2 saved")

# ════════════════════════════════════════════
# CHART 3 — Revenue by Vehicle Type (Bar)
# ════════════════════════════════════════════
plt.figure(figsize=(8, 5))
rev_by_veh = success.groupby('Vehicle_Type')['Booking_Value'].sum().sort_values(ascending=False)
sns.barplot(x=rev_by_veh.values, y=rev_by_veh.index, palette='Greens_r')
plt.title('Total Revenue by Vehicle Type', fontsize=14, fontweight='bold')
plt.xlabel('Total Revenue (₹)')
plt.ylabel('Vehicle Type')
for i, v in enumerate(rev_by_veh.values):
    plt.text(v + 10000, i, f'₹{v:,.0f}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('chart3_revenue_by_vehicle.png')
plt.show()
print("✅ Chart 3 saved")

# ════════════════════════════════════════════
# CHART 4 — Payment Method (Pie Chart)
# ════════════════════════════════════════════
plt.figure(figsize=(7, 7))
pm = success['Payment_Method'].value_counts()
plt.pie(pm.values, labels=pm.index, autopct='%1.1f%%',
        colors=['#3498db','#2ecc71','#e74c3c','#f39c12'],
        startangle=140, wedgeprops={'edgecolor':'white','linewidth':2})
plt.title('Payment Method Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart4_payment_method.png')
plt.show()
print("✅ Chart 4 saved")

# ════════════════════════════════════════════
# CHART 5 — Bookings by Hour (Line Chart)
# ════════════════════════════════════════════
plt.figure(figsize=(12, 5))
hourly = df.groupby('Hour')['Booking_ID'].count()
plt.plot(hourly.index, hourly.values, color='#2980b9', linewidth=2.5, marker='o', markersize=5)
plt.fill_between(hourly.index, hourly.values, alpha=0.2, color='#2980b9')
plt.title('Bookings by Hour of Day', fontsize=14, fontweight='bold')
plt.xlabel('Hour (0 = Midnight, 12 = Noon)')
plt.ylabel('Number of Bookings')
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig('chart5_hourly_bookings.png')
plt.show()
print("✅ Chart 5 saved")

# ════════════════════════════════════════════
# CHART 6 — Daily Revenue Trend (Line Chart)
# ════════════════════════════════════════════
plt.figure(figsize=(12, 5))
daily_rev = success.groupby('Day')['Booking_Value'].sum()
plt.plot(daily_rev.index, daily_rev.values, color='#27ae60', linewidth=2.5, marker='o', markersize=5)
plt.fill_between(daily_rev.index, daily_rev.values, alpha=0.2, color='#27ae60')
plt.title('Daily Revenue Trend — July 2024', fontsize=14, fontweight='bold')
plt.xlabel('Day of Month')
plt.ylabel('Total Revenue (₹)')
plt.tight_layout()
plt.savefig('chart6_daily_revenue.png')
plt.show()
print("✅ Chart 6 saved")

# ════════════════════════════════════════════
# CHART 7 — Cancellations by Vehicle Type
# ════════════════════════════════════════════
plt.figure(figsize=(9, 5))
cancelled = df[df['Booking_Status'].str.contains('Canceled')]
cancel_veh = cancelled.groupby(['Vehicle_Type','Booking_Status'])['Booking_ID'].count().unstack()
cancel_veh.plot(kind='bar', figsize=(9,5), color=['#e74c3c','#e67e22'])
plt.title('Cancellations by Vehicle Type', fontsize=14, fontweight='bold')
plt.xlabel('Vehicle Type')
plt.ylabel('Cancellations')
plt.xticks(rotation=30)
plt.legend(title='Canceled By')
plt.tight_layout()
plt.savefig('chart7_cancellations.png')
plt.show()
print("✅ Chart 7 saved")

# ════════════════════════════════════════════
# CHART 8 — Driver vs Customer Ratings
# ════════════════════════════════════════════
plt.figure(figsize=(8, 5))
rated = success[success['Driver_Ratings'] > 0]
plt.hist(rated['Driver_Ratings'], bins=20, alpha=0.6, color='#3498db', label='Driver Rating')
plt.hist(rated['Customer_Rating'], bins=20, alpha=0.6, color='#e74c3c', label='Customer Rating')
plt.title('Driver vs Customer Ratings Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig('chart8_ratings.png')
plt.show()
print("✅ Chart 8 saved")

print("\n✅ ALL 8 CHARTS SAVED IN YOUR FOLDER!")