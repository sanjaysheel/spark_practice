from pyspark.sql.functions import lit, array_repeat, concat_ws, col, dense_rank, desc, avg, sum, count, when, expr
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType

# Type of triangle:
from pyspark.sql import functions as F

def solve(spark, inputs):
    config = inputs["config"]
    n = config.first()[0]
    df_result = spark.range(1, n+1).withColumnRenamed("id", "row_num").withColumn("stars", concat_ws(" ", array_repeat(lit("*"), (lit(n) + 1 - col('row_num')).cast("int"))))
    return df_result
    