from pyspark.sql.functions import col
from pyspark.sql.types import DecimalType


def solve(spark, inputs):
    ark_artifacts = inputs["ark_artifacts"]

    df_result = ark_artifacts.withColumn("Material", col("Material").upper())
    return df_result