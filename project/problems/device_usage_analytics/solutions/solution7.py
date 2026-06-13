from pyspark.sql.functions import col, dense_rank, desc, avg, sum, count, when
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType

# Type of triangle:
from pyspark.sql import functions as F

def solve(spark, inputs):
    triangles = inputs["triangles"]
    
    # Apply the conditional logic using F.when().otherwise()
    df_result = triangles.withColumn(
        "triangle_type",
        F.when(
            (F.col("a") + F.col("b") <= F.col("c")) | 
            (F.col("a") + F.col("c") <= F.col("b")) | 
            (F.col("b") + F.col("c") <= F.col("a")), 
            "Not A Triangle"
        )
        .when((F.col("a") == F.col("b")) & (F.col("b") == F.col("c")), "Equilateral")
        .when((F.col("a") == F.col("b")) | (F.col("b") == F.col("c")) | (F.col("a") == F.col("c")), "Isosceles")
        .otherwise("Scalene")
    )
    
    return df_result
