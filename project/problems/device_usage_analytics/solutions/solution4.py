from pyspark.sql.functions import col, dense_rank, desc, avg, sum
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType



def solve(spark, inputs):
    sales = inputs["sales"]
    sales = sales.groupBy("category").agg(
        sum("amount").cast(StringType()).alias("total_sales"), 
        avg("amount").cast(DecimalType(10, 2)).cast(StringType()).alias("avg_amount")
    ).select(['category', 'total_sales', "avg_amount"])
    return sales

