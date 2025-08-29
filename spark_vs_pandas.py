import time
import pandas as pd

# --- Pandas ---
t0 = time.time()
pdf = pd.read_parquet("yellow_tripdata_2025-01.parquet", engine="pyarrow")
avg_fare_pd = pdf["fare_amount"].mean()
t1 = time.time()
print(f"Pandas average fare: {avg_fare_pd:.2f} (time: {t1 - t0:.2f}s)")

# --- Spark ---
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("TaxiCompare").getOrCreate()

df = spark.read.parquet("yellow_tripdata_2025-01.parquet")
df.createOrReplaceTempView("trips")

t2 = time.time()
avg_fare_spark = spark.sql("SELECT AVG(fare_amount) AS avg_fare FROM trips")
avg_fare_spark.show()
t3 = time.time()
print(f"Spark average fare time: {t3 - t2:.2f}s")

spark.stop()
