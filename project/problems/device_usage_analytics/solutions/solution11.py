from pyspark.sql.functions import lit, regexp_replace,  concat_ws, col, dense_rank, desc, avg, sum, count, when, expr
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType, IntegerType

# The Blunder - salary calculation Error
from pyspark.sql import functions as F

def solve(spark, inputs):
    employees = inputs["employees"]
    employees = employees.agg(
        regexp_replace(sum("salary").cast(StringType()), "0+$", "").cast(IntegerType()).alias("error_amount")
    )
    
    return employees
    