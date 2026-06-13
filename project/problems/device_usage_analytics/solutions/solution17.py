from pyspark.sql.functions import abs, lit, regexp_replace,  concat_ws, col, dense_rank, desc, avg, sum, count, when, expr
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType, IntegerType

# Japan Population
from pyspark.sql import functions as F

def solve(spark, inputs):
    raw_data = inputs["raw_data"]
    raw_data = raw_data.dropna()
    raw_data.show()
    return raw_data
    