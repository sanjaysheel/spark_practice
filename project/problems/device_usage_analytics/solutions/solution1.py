from pyspark.sql.functions import col
from pyspark.sql.types import DecimalType


def solve(spark, inputs):
    da_viewership = inputs["da_viewership"]

    da_viewership = da_viewership.filter(col("device_type").isin("laptop", "tablet")).alias("device_type_filter")
    return da_viewership