from pyspark.sql.functions import col, sum
from pyspark.sql.types import DecimalType

def solve(spark, inputs):
    so_planet = inputs["so_planet"]
    so_star = inputs["so_star"]

    df_result = so_planet.alias("p").join(
        so_star.alias("s"), 
        col("p.star_id") == col("s.id"), 
        how="inner"
    ).select([
        col("s.name").alias("star_name"),
        col("s.color").alias("star_color"),
        col("s.type").alias("star_type"),
        col("p.name").alias("planet_name"),
        col("p.type").alias("planet_type"),
        col("s.distance").alias("distance_star_earth"),
        col("p.distance").alias("distance_planet_star")
    ])
    return df_result