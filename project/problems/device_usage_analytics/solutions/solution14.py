from pyspark.sql.functions import lit, regexp_replace,  concat_ws, col, dense_rank, desc, avg, sum, count, when, expr
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType, IntegerType

# Japan Population
from pyspark.sql import functions as F

def solve(spark, inputs):
    city = inputs["city"]
    city = city.groupBy("country_code").agg(sum("population").alias("Total_population")).filter(col("country_code") == "JPN").select("total_population")
    return city
    