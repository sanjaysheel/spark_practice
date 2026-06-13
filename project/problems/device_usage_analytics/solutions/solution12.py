from pyspark.sql.functions import lit, regexp_replace,  concat_ws, col, dense_rank, desc, avg, sum, count, when, expr
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType, IntegerType

# Sum Population for california
from pyspark.sql import functions as F

def solve(spark, inputs):
    city = inputs["city"]
    city = city.groupBy("district").agg(sum("population").cast(IntegerType()).alias("total_population")).filter(col("district") == "California").select("total_population")
    return city
    