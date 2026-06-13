from pyspark.sql.functions import col
from pyspark.sql.types import DecimalType


def solve(spark, inputs):
    rp_employees = inputs["rp_employees"].alias("p")
    rp_payroll = inputs["rp_payroll"].alias("a")

    df_result = rp_employees.join(rp_payroll, how="inner", on="employee_id")
    df_result = df_result.withColumn("pay", (col("hours_worked").cast("double") * col("hourly_rate").cast("double")).cast(DecimalType(10, 2)).cast("string"))

    return df_result.select(['employee_id', "name", "pay", "position"])