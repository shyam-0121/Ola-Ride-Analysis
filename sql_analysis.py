import pandas as pd
import sqlite3

# Load cleaned data
df = pd.read_csv('cleaned_bookings.csv')

# ════════════════════════════════════════════
# SETUP — Load CSV into SQLite Database
# ════════════════════════════════════════════
conn = sqlite3.connect('ola_bookings.db')
df.to_sql('bookings', conn, if_exists='replace', index=False)
print("✅ Database created: ola_bookings.db")
print("✅ Table created: bookings")
print("-" * 50)

# Helper function to run any query and print results
def run_query(title, query):
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print('=' * 50)
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

# ════════════════════════════════════════════
# QUERY 1 — Total bookings and revenue
# ════════════════════════════════════════════
run_query("Q1: OVERALL SUMMARY", """
    SELECT 
        COUNT(*)                        AS Total_Bookings,
        SUM(Booking_Value)              AS Total_Revenue,
        ROUND(AVG(Booking_Value), 2)    AS Avg_Booking_Value,
        ROUND(AVG(Ride_Distance), 2)    AS Avg_Distance_KM
    FROM bookings
""")

# ════════════════════════════════════════════
# QUERY 2 — Booking status breakdown
# ════════════════════════════════════════════
run_query("Q2: BOOKING STATUS BREAKDOWN", """
    SELECT 
        Booking_Status,
        COUNT(*)                                        AS Total,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) 
              FROM bookings), 2)                        AS Percentage
    FROM bookings
    GROUP BY Booking_Status
    ORDER BY Total DESC
""")

# ════════════════════════════════════════════
# QUERY 3 — Revenue by vehicle type
# ════════════════════════════════════════════
run_query("Q3: REVENUE BY VEHICLE TYPE", """
    SELECT 
        Vehicle_Type,
        COUNT(*)                        AS Total_Rides,
        SUM(Booking_Value)              AS Total_Revenue,
        ROUND(AVG(Booking_Value), 2)    AS Avg_Revenue,
        MAX(Booking_Value)              AS Max_Ride,
        MIN(Booking_Value)              AS Min_Ride
    FROM bookings
    WHERE Booking_Status = 'Success'
    GROUP BY Vehicle_Type
    ORDER BY Total_Revenue DESC
""")

# ════════════════════════════════════════════
# QUERY 4 — Payment method usage
# ════════════════════════════════════════════
run_query("Q4: PAYMENT METHOD USAGE", """
    SELECT 
        Payment_Method,
        COUNT(*)                        AS Total_Rides,
        SUM(Booking_Value)              AS Total_Revenue,
        ROUND(AVG(Booking_Value), 2)    AS Avg_Value
    FROM bookings
    WHERE Payment_Method != 'Not Applicable'
    GROUP BY Payment_Method
    ORDER BY Total_Rides DESC
""")

# ════════════════════════════════════════════
# QUERY 5 — Top 5 pickup locations
# ════════════════════════════════════════════
run_query("Q5: TOP 5 PICKUP LOCATIONS", """
    SELECT 
        Pickup_Location,
        COUNT(*)            AS Total_Pickups,
        SUM(Booking_Value)  AS Total_Revenue
    FROM bookings
    WHERE Booking_Status = 'Success'
    GROUP BY Pickup_Location
    ORDER BY Total_Pickups DESC
    LIMIT 5
""")

# ════════════════════════════════════════════
# QUERY 6 — Top 5 drop locations
# ════════════════════════════════════════════
run_query("Q6: TOP 5 DROP LOCATIONS", """
    SELECT 
        Drop_Location,
        COUNT(*)            AS Total_Drops,
        SUM(Booking_Value)  AS Total_Revenue
    FROM bookings
    WHERE Booking_Status = 'Success'
    GROUP BY Drop_Location
    ORDER BY Total_Drops DESC
    LIMIT 5
""")

# ════════════════════════════════════════════
# QUERY 7 — Cancellation analysis
# ════════════════════════════════════════════
run_query("Q7: CANCELLATION BY VEHICLE TYPE", """
    SELECT 
        Vehicle_Type,
        SUM(CASE WHEN Booking_Status = 'Canceled by Customer' THEN 1 ELSE 0 END) AS By_Customer,
        SUM(CASE WHEN Booking_Status = 'Canceled by Driver'   THEN 1 ELSE 0 END) AS By_Driver,
        SUM(CASE WHEN Booking_Status = 'Driver Not Found'     THEN 1 ELSE 0 END) AS Driver_Not_Found
    FROM bookings
    GROUP BY Vehicle_Type
    ORDER BY By_Customer DESC
""")

# ════════════════════════════════════════════
# QUERY 8 — Peak hours
# ════════════════════════════════════════════
run_query("Q8: TOP 5 PEAK HOURS", """
    SELECT 
        Hour,
        COUNT(*)            AS Total_Bookings,
        SUM(Booking_Value)  AS Total_Revenue
    FROM bookings
    GROUP BY Hour
    ORDER BY Total_Bookings DESC
    LIMIT 5
""")

# ════════════════════════════════════════════
# QUERY 9 — Ratings by vehicle type
# ════════════════════════════════════════════
run_query("Q9: AVERAGE RATINGS BY VEHICLE TYPE", """
    SELECT 
        Vehicle_Type,
        ROUND(AVG(Driver_Ratings), 2)   AS Avg_Driver_Rating,
        ROUND(AVG(Customer_Rating), 2)  AS Avg_Customer_Rating
    FROM bookings
    WHERE Booking_Status = 'Success'
    AND Driver_Ratings > 0
    GROUP BY Vehicle_Type
    ORDER BY Avg_Driver_Rating DESC
""")

# ════════════════════════════════════════════
# QUERY 10 — Daily revenue trend
# ════════════════════════════════════════════
run_query("Q10: DAILY REVENUE TREND", """
    SELECT 
        Day,
        COUNT(*)            AS Total_Rides,
        SUM(Booking_Value)  AS Daily_Revenue,
        ROUND(AVG(Booking_Value), 2) AS Avg_Value
    FROM bookings
    WHERE Booking_Status = 'Success'
    GROUP BY Day
    ORDER BY Day ASC
""")

conn.close()
print("\n✅ All queries done! Database connection closed.")