from pyspark.sql.functions import col
from pyspark.sql.types import DecimalType


def solve(spark, inputs):
    confirmations = inputs["confirmations"]
    signups = inputs["signups"]

    result = confirmations.join(signups, on="user_id", how="inner")
    confirmation_count = result.groupBy("user_id").count().filter(col("count") > 1).select("user_id")
    confirmation_count.show()
    return confirmation_count