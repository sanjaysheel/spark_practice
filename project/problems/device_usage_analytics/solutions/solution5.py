from pyspark.sql.functions import col, dense_rank, desc, avg, sum
from pyspark.sql.window import Window
from pyspark.sql.types import DecimalType, StringType

# employees not in the departments table

def solve(spark, inputs):
    departments = inputs["departments"]
    employees = inputs["employees"]
    # df_result = employees.join(departments, how='left_anti', on='department_id')
    df_result = employees.join(departments, how='left', on='department_id')
    # 3. Filter for rows where the department name from the RIGHT table is null
    # df_result.show()
    df_result = df_result.where(col("department_name").isNull())
    return df_result.select(['employee_id', 'name', 'department_id'])

