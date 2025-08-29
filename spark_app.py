from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("NYC Taxi Spark Project") \
    .getOrCreate()

df = spark.read.parquet("yellow_tripdata_2025-01.parquet")
df.createOrReplaceTempView("trips")

# Query 1
print("=== Average Fare by Hour ===")
q1 = spark.sql("""
SELECT HOUR(tpep_pickup_datetime) AS pickup_hour,
       ROUND(AVG(fare_amount), 2) AS avg_fare
FROM trips
GROUP BY pickup_hour
ORDER BY pickup_hour
""")
q1.show(24)
q1.explain(True)

# Query 2
print("=== Top 10 Pickup Zones ===")
q2 = spark.sql("""
SELECT PULocationID,
       COUNT(*) AS trip_count
FROM trips
GROUP BY PULocationID
ORDER BY trip_count DESC
LIMIT 10
""")
q2.show()
q2.explain(True)

# Query 3
print("=== Payment Type Distribution ===")
q3 = spark.sql("""
SELECT payment_type,
       COUNT(*) AS trips,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percent_share
FROM trips
GROUP BY payment_type
ORDER BY trips DESC
""")
q3.show()
q3.explain(True)

spark.stop()

