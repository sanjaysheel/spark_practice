from pyspark.sql import functions as F
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import IntegerType


def solve(spark, inputs):

    employee_df = inputs["employee"]

    distinct_salary_df = (
        employee_df
        .select("salary")
        .distinct()
        .orderBy(F.col("salary").desc())
    )

    salary_rows = distinct_salary_df.limit(2).collect()

    second_highest_salary = (
        salary_rows[1]["salary"]
        if len(salary_rows) > 1
        else None
    )

    schema = StructType([
        StructField(
            "SecondHighestSalary",
            IntegerType(),
            True
        )
    ])

    df = spark.createDataFrame(
        [(second_highest_salary,)],
        schema
    )
    return df