# How To Run Solutions

Run every command from the project folder:

```powershell
cd A:\Spark_practice\project
```

## Easiest Way

Use `easy_run.py`.

It automatically detects:

- normal Python solution
- PySpark solution
- SQL solution

Command format:

```powershell
python easy_run.py <solution_file_name> --problem <problem_name> --testcase <case_file>
```

If the solution filename is unique, `--problem` can be skipped.

If the solution filename is common, like `solution1.py`, use `--problem`.

## Run A Normal Python Solution

Use this for files like:

```python
def solve(params):
```

Example:

```powershell
python easy_run.py solution1.py --problem nth_highest_salary --testcase case1.json
```

Run all testcases:

```powershell
python easy_run.py solution1.py --problem nth_highest_salary
```

## Run A PySpark Solution

Use this for files like:

```python
def solve(spark, inputs):
```

Example:

```powershell
python easy_run.py solution_join_spark_simple.py --testcase case_join.json
```

Run all testcases:

```powershell
python easy_run.py solution_join_spark_simple.py
```

Note: only run all testcases if all testcases belong to that solution type.

## Run A SQL Solution

SQL solution files are inside `sql_solutions`.

Example:

```powershell
python easy_run.py solution_join.sql --problem Second_Highest_Sal --testcase case1.json
```

Run all SQL testcases:

```powershell
python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

## Same Testcases

Python, PySpark, and SQL use the same testcase folder for the problem.

Example:

```text
problems/Second_Highest_Sal/
  solutions/
  sql_solutions/
  testCases/
```

Both commands use the same `testCases` folder:

```powershell
python easy_run.py solution1.py --problem Second_Highest_Sal
python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

## Quick Examples

Normal Python:

```powershell
python easy_run.py solution1.py --problem nth_highest_salary --testcase case1.json
```

PySpark:

```powershell
python easy_run.py solution_join_spark_simple.py --testcase case_join.json
```

SQL:

```powershell
python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

## Old Direct Commands Still Work

Normal Python:

```powershell
python run.py nth_highest_salary problems\nth_highest_salary\solutions\solution1.py --testcase case1.json
```

PySpark:

```powershell
python run.py --spark normalize_names problems\normalize_names\solutions\solution_join_spark_simple.py --testcase case_join.json
```

SQL:

```powershell
python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

For SQL, use `easy_run.py`.
