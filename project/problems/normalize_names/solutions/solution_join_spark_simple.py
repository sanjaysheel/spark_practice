from pyspark.sql import functions as F


def solve(spark, inputs):
    """Simple PySpark solution for LeetCode-style Person/Address input."""
    person = inputs["person"].alias("p")
    address = inputs["address"].alias("a")

    return (
        person.join(address, F.col("p.personId") == F.col("a.personId"), "left")
        .select(
            F.col("p.firstName").alias("firstName"),
            F.col("p.lastName").alias("lastName"),
            F.coalesce(F.col("a.city"), F.lit("Null")).alias("city"),
            F.coalesce(F.col("a.state"), F.lit("Null")).alias("state"),
        )
    )
