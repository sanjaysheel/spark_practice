from pyspark.sql.functions import col, dense_rank, desc, avg, sum, count, when, expr
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType

# Type of triangle:
from pyspark.sql import functions as F

def solve(spark, inputs):
    config = inputs["config"]
    n = config.first()[0]
    spark.range(1, n+1).show()
    df_result = spark.range(1, n+1).withColumnRenamed("id", "row_num").withColumn("stars", expr("concat_ws(' ', array_repeat('*', cast(row_num as INT)))"))
    return df_result
