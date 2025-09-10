# 🚕 NYC Yellow Taxi Data with Apache Spark

This project demonstrates how to use Apache Spark for querying and analyzing the NYC Yellow Taxi trip dataset from January 2025. The data is stored in Parquet format, allowing for efficient columnar reads and large-scale data processing.

The project explores how Spark SQL can perform common analytical queries on millions of rows and compares Spark’s performance with Pandas on a single machine.

-----

##  Project Goals

  * Understand how Spark interacts with structured data.
  * Write SQL queries in Spark and inspect their execution plans.
  * Compare Spark’s performance with Pandas to highlight the benefits of distributed computation.

-----

##  Technologies

  * Python 3.10+
  * Java 8, 11, or 17 (JDK or JRE) — required for Spark
  * Apache Spark (PySpark)
  * Pandas
  * NYC Yellow Taxi dataset (January 2025, Parquet format)

-----

## Dataset

  * **File:** `yellow_tripdata_2025-01.parquet`
  * **Source:** NYC TLC Trip Records
  * **Key columns used:**
      * `tpep_pickup_datetime` – Trip start timestamp
      * `fare_amount` – Fare (USD)
      * `PULocationID` – Pickup location zone ID
      * `payment_type` – Encoded payment method (1=Credit card, 2=Cash, etc.)
      * `trip_distance` – Distance traveled in miles

-----

## How to Run

1.  **Install dependencies**
    ```bash
    pip install pyspark pandas pyarrow
    ```
2.  **Run the Spark app**
    ```bash
    python spark_app.py
    ```
    This will:
      * Load the Parquet dataset using Spark.
      * Run three analytical SQL queries.
      * Print both the results and the query execution plans to the console.

-----

## Queries Performed

### 1. Average Fare by Hour of Day

**Purpose:** Shows how Spark efficiently groups and aggregates timestamp data.

```sql
SELECT
    HOUR(tpep_pickup_datetime) AS pickup_hour,
    ROUND(AVG(fare_amount), 2) AS avg_fare
FROM trips
GROUP BY pickup_hour
ORDER BY pickup_hour;
```

### 2. Top 10 Pickup Zones by Trip Count

**Purpose:** Demonstrates grouping and sorting on a large dataset.

```sql
SELECT
    PULocationID,
    COUNT(*) AS trip_count
FROM trips
GROUP BY PULocationID
ORDER BY trip_count DESC
LIMIT 10;
```

### 3. Payment Type Distribution

**Purpose:** Shows Spark handling categorical columns and computing percentage shares using window functions.

```sql
SELECT
    payment_type,
    COUNT(*) AS trips,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percent_share
FROM trips
GROUP BY payment_type
ORDER BY trips DESC;
```

-----

## Performance Comparison: Pandas vs. Spark 

To highlight Spark’s scalability, we compared the time it takes to compute the average `fare_amount`.

**Pandas Code**

```python
import pandas as pd
import time

# Pandas timing
t0 = time.time()
pdf = pd.read_parquet("yellow_tripdata_2025-01.parquet")
avg_fare_pd = pdf["fare_amount"].mean()
t1 = time.time()
print(f"Pandas average fare: {avg_fare_pd:.2f} (time: {t1-t0:.2f}s)")
```

**Spark Code**

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("TaxiCompare").getOrCreate()
df = spark.read.parquet("yellow_tripdata_2025-01.parquet")
df.createOrReplaceTempView("trips")

# Spark timing
t2 = time.time()
avg_fare_spark = spark.sql("SELECT AVG(fare_amount) AS avg_fare FROM trips")
avg_fare_spark.show()
t3 = time.time()
print(f"Spark time: {t3-t2:.2f}s")
spark.stop()
```

**Expected Outcome:**

  * **Pandas** will attempt to load all data into memory, which can be slow and memory-intensive.
  * **Spark** will use lazy evaluation and optimized query plans, resulting in faster execution, even on a single large file.

-----

## Most Interesting Challenges

  * **Local Spark Configuration:** Ensuring the correct Java and Python environments are set up.
  * **Schema Handling:** Understanding Parquet column types and properly parsing timestamps.
  * **Query Plan Analysis:** Interpreting the output of Spark’s query optimizer to understand how it executes tasks.

-----

## How to Bundle and Run

  * Place `spark_app.py` and the `yellow_tripdata_2025-01.parquet` file in the same directory.
  * Run `python spark_app.py` from your terminal.
  * All queries and results will be printed to the console. No additional configuration is required, as Spark runs in local mode by default.

-----
