"""Spark SQL runner for .sql solution files."""

from typing import Any, Dict, List

from spark_judge.loader import load_testcases
from spark_judge.parser import parse_solution
from spark_judge.validator import validate_sql
from spark_judge.pyspark_runner import SparkSession, create_spark_session


def _to_spark_df(spark, rows):
    return spark.createDataFrame(rows or [])


def _from_spark_df(df):
    return [row.asDict() for row in df.collect()]


def _normalize_nulls(value: Any) -> Any:
    if isinstance(value, str) and value.lower() == "null":
        return None
    if isinstance(value, list):
        return [_normalize_nulls(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize_nulls(item) for key, item in value.items()}
    return value


def run_solution_sql(solution_path: str, testcases: List[Dict]) -> List[Dict]:
    sql = parse_solution(solution_path).strip().rstrip(";")
    if not sql:
        raise RuntimeError("SQL solution file is empty")
    if not validate_sql(sql):
        raise RuntimeError("SQL solution contains a disallowed statement")
    if SparkSession is None:
        raise RuntimeError("PySpark is not installed or failed to import")

    spark = create_spark_session("local_sql_judge")
    results = []

    try:
        for case in testcases:
            inp = case.get("input")
            expected = _normalize_nulls(case.get("expected"))

            try:
                if not isinstance(inp, dict):
                    raise TypeError("SQL test input must be a dict of table_name -> rows")

                for table_name, rows in inp.items():
                    if isinstance(rows, list):
                        _to_spark_df(spark, rows).createOrReplaceTempView(table_name)

                actual = _from_spark_df(spark.sql(sql))
                actual = _normalize_nulls(actual)
                passed = actual == expected
            except Exception as exc:
                error_msg = str(exc)
                # Check for common subscript error and provide helpful message
                if "'SparkSession' object is not subscriptable" in error_msg:
                    error_msg = (
                        "'SparkSession' object is not subscriptable. "
                        "Your SQL solution may have a Python syntax error. "
                        "Ensure your .sql file contains only SQL (no Python code), "
                        "or use the Python runner for Python+PySpark solutions."
                    )
                actual = f"<error: {error_msg}>"
                passed = False

            results.append(
                {
                    "input": inp,
                    "expected": expected,
                    "actual": actual,
                    "passed": passed,
                }
            )
    finally:
        from spark_judge.pyspark_runner import keep_spark_ui_alive_if_requested

        keep_spark_ui_alive_if_requested()
        spark.stop()

    return results
