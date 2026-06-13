from pyspark.sql.functions import lit, regexp_replace,  concat_ws, col, dense_rank, desc, avg, sum, count, when, expr
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType, IntegerType

# Count Citites with Population > 100000
from pyspark.sql import functions as F

def solve(spark, inputs):
    city = inputs["city"]
    city = city.filter(col("population") > 100000).select(count("*").alias("city_count"))
    return city
    