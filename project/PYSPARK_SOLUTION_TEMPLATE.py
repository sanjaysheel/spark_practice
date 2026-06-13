"""
CORRECT PYSPARK SOLUTION TEMPLATE

This shows the correct way to write PySpark solutions.
Copy this pattern for your own solutions.
"""

from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def solve(spark, inputs):
    """
    Main solution function for PySpark problems.
    
    Args:
        spark: SparkSession object
               - Use this to: spark.read.csv(), spark.sql(), spark.createDataFrame()
               - DO NOT use spark["something"] or spark[0] - this causes "not subscriptable" error
        
        inputs: Dictionary mapping table names to DataFrames
                - Example: {"employees": DataFrame, "departments": DataFrame}
                - Access tables with: inputs["table_name"]
                - DO NOT try to access like spark["table_name"]
    
    Returns:
        DataFrame or list of dicts (will be converted to DataFrame then to list)
    
    Example Problem: Join employees and departments tables
    """
    
    # ✅ CORRECT: Access input DataFrames from the inputs dict
    employees = inputs["employees"]  # ✅ Good: using inputs dict
    departments = inputs["departments"]  # ✅ Good: using inputs dict
    
    # ❌ WRONG (uncomment to see the error):
    # emp = spark["employees"]  # ❌ ERROR: 'SparkSession' object is not subscriptable
    # dept = spark[0]  # ❌ ERROR: 'SparkSession' object is not subscriptable
    
    # Perform your transformations
    result = (
        employees
        .join(departments, 
              employees.dept_id == departments.id, 
              how="left")
        .select(
            employees.id,
            employees.name,
            departments.dept_name
        )
    )
    
    return result


# Alternative: If you need to write parameters in reverse order
def solve_alt(inputs, spark):
    """
    Alternative signature: inputs first, spark second.
    The runner will try both signatures if the first one fails with TypeError.
    """
    employees = inputs["employees"]
    return employees.limit(10)


# ============================================================================
# COMMON PATTERNS
# ============================================================================

def example_filter(spark, inputs):
    """Example: Filter rows from a table"""
    df = inputs["my_table"]
    return df.filter(df.salary > 50000)


def example_aggregation(spark, inputs):
    """Example: Group and aggregate"""
    df = inputs["sales"]
    return (
        df.groupBy("department")
        .agg(F.sum("amount").alias("total_sales"))
    )


def example_join(spark, inputs):
    """Example: Join two tables"""
    employees = inputs["employees"]
    departments = inputs["departments"]
    return (
        employees.join(departments, "dept_id", how="left")
    )


def example_window_function(spark, inputs):
    """Example: Use window functions"""
    from pyspark.sql.window import Window
    
    df = inputs["employees"]
    
    window = Window.partitionBy("department").orderBy("salary")
    return (
        df.withColumn("rank", F.rank().over(window))
    )


# ============================================================================
# NOTES
# ============================================================================
# 
# 1. The runner will automatically:
#    - Convert input JSON/dicts to DataFrames
#    - Pass them via the inputs dict
#    - Convert your returned DataFrame back to dicts
#
# 2. If your function signature is solve(inputs, spark):
#    - The runner will try solve(spark, inputs) first
#    - If that fails with TypeError, it will try solve(inputs, spark)
#    - Make sure your code matches your signature!
#
# 3. Always access data from inputs, never from spark
#
# 4. To debug:
#    - Print available tables: print(list(inputs.keys()))
#    - Show a sample: inputs["table_name"].show()
#    - Check schema: inputs["table_name"].printSchema()
#
