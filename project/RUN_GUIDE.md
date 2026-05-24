# Run Guide: Python vs PySpark

Use this guide to decide when to use `--spark` and when not to use it.

Always run commands from this folder:

```powershell
cd A:\Spark_practice\project
```

## Basic Command Shape

Recommended simple command:

```powershell
python easy_run.py <solution_filename> --problem <problem_name> --testcase <case_file>
```

`easy_run.py` detects normal Python, PySpark, or SQL automatically.

Examples:

```powershell
python easy_run.py solution1.py --problem nth_highest_salary --testcase case1.json
python easy_run.py solution_join_spark_simple.py --testcase case_join.json
python easy_run.py solution_join.sql --problem Second_Highest_Sal --testcase case1.json
```

If the filename is unique, you can skip `--problem`:

```powershell
python easy_run.py solution_join_spark_simple.py --testcase case_join.json
```

If the filename appears in many folders, like `solution1.py`, add `--problem`.

The older direct command still works:

Normal Python:

```powershell
python run.py <problem_name> <solution_file> --testcase <case_file>
```

PySpark:

```powershell
python run.py --spark <problem_name> <solution_file> --testcase <case_file>
```

Run all testcases for a problem by removing `--testcase`:

```powershell
python run.py <problem_name> <solution_file>
python run.py --spark <problem_name> <solution_file>
```

## When To Use `--spark`

Use `--spark` only when the solution function looks like this:

```python
def solve(spark, inputs):
```

or when the file uses PySpark DataFrames, Spark SQL, `SparkSession`, or imports from `pyspark`.

Example PySpark solution:

```python
from pyspark.sql import functions as F

def solve(spark, inputs):
    employee = inputs["employee"]
    return employee.select(...)
```

Run it like this:

```powershell
python run.py --spark normalize_names problems\normalize_names\solutions\solution_join_spark_simple.py --testcase case_join.json
```

## When NOT To Use `--spark`

Do not use `--spark` when the solution function looks like this:

```python
def solve(params):
```

or:

```python
def solve(input_data):
```

or:

```python
def solve(nums, target):
```

These are normal Python solutions.

Example:

```python
def solve(params):
    data = params.get("data", [])
    return data
```

Run it like this:

```powershell
python run.py nth_highest_salary problems\nth_highest_salary\solutions\solution1.py --testcase case1.json
```

## Why The Error Happens

If you run a normal Python solution with `--spark`, the runner calls:

```python
solve(spark, inputs)
```

But your normal Python file may only accept:

```python
solve(params)
```

Then you see this error:

```text
solve() takes 1 positional argument but 2 were given
```

That means: remove `--spark`.

## Examples In This Project

Normal Python:

```powershell
python run.py nth_highest_salary problems\nth_highest_salary\solutions\solution1.py --testcase case1.json
python run.py second_highest_salary problems\second_highest_salary\solutions\solution1.py --testcase case1.json
python run.py search_suggestions problems\search_suggestions\solutions\solution1.py --testcase case1.json
python run.py set_zeroes problems\set_zeroes\solutions\solution1.py --testcase case1.json
```

PySpark:

```powershell
python run.py --spark normalize_names problems\normalize_names\solutions\solution_join_spark.py --testcase case_join.json
python run.py --spark normalize_names problems\normalize_names\solutions\solution_join_spark_simple.py --testcase case_join.json
```

## Keep Problem And Testcase Together

The problem name must match the folder under `problems`.

Good:

```powershell
python run.py nth_highest_salary problems\nth_highest_salary\solutions\solution1.py --testcase case1.json
```

Avoid mixing folders like this:

```powershell
python run.py nth_highest_salary problems\nth_highest_salary\solutions\solution1.py --testcase A:\Spark_practice\project\problems\Second_Highest_Sal\testCases\case1.json
```

Use the testcase from the same problem folder.

## Quick Rule

If the solution starts with:

```python
def solve(spark, inputs):
```

use `--spark`.

If the solution starts with:

```python
def solve(params):
```

do not use `--spark`.
