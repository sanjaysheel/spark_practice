from pyspark.sql.functions import col, dense_rank, desc, avg, sum, count
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType

# Duplicate Email Records

def solve(spark, inputs):
    users = inputs["users"]
    df_result = users.groupBy("email").agg(count("email").cast(StringType()).alias("occurences_count")).orderBy(col("occurences_count").asc())
    return df_result

