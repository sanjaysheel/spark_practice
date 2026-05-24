"""Keep a small Spark session alive so Spark UI is always available in Docker."""

import os
import time

from pyspark.sql import SparkSession


def main():
    master_url = os.environ.get("SPARK_MASTER_URL", "local[*]")
    spark = (
        SparkSession.builder
        .master(master_url)
        .appName("spark_practice_ui")
        .config("spark.ui.bindAddress", "0.0.0.0")
        .config("spark.driver.bindAddress", "0.0.0.0")
        .getOrCreate()
    )

    print("Spark UI server is running.")
    print("Open: http://localhost:4040")
    print(f"Spark version: {spark.version}")

    # Run a tiny action so the UI has an application and at least one job.
    spark.range(1).count()

    try:
        while True:
            time.sleep(3600)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
