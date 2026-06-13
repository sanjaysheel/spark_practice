from pyspark.sql.functions import col, dense_rank, desc
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType



def solve(spark, inputs):
    products = inputs["products"]
    window_spec = Window.orderBy(col("price").desc())
    products = products.withColumn("rank", dense_rank().over(window_spec))
    result = products.filter(col("rank") == 3).select("product_id", "product_name", "price")
    return result