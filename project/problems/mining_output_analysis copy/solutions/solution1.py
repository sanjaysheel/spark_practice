from pyspark.sql.functions import col, sum
from pyspark.sql.types import DecimalType


def solve(spark, inputs):
    mc_extraction = inputs["mc_extraction"]
    mc_mines = inputs["mc_mines"]

    df_result = mc_extraction.join(mc_mines, how="inner", on=mc_extraction["mine_id"] == mc_mines["id"]) 
    df_result = df_result.groupBy("location", "mineral").agg(sum("quantity").cast("int").alias("total_quantity"))


    return df_result.select(['location', "mineral", "total_quantity"])