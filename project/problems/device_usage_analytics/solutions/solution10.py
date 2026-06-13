from pyspark.sql.functions import lit, concat_ws, col, dense_rank, desc, avg, sum, count, when, expr
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType

# Type of triangle:
from pyspark.sql import functions as F

def solve(spark, inputs):
    city = inputs["city"]
    country = inputs["country"]
    df_result = city.join(country, how="inner", on=city["country_code"] == country["code"]).groupBy("continent").agg(sum("population").alias("total_population")).select("total_population")
    return df_result
    