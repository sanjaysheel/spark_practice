# SQL Troubleshooting

## Error: Syntax error at or near `git`

Example error:

```text
[PARSE_SYNTAX_ERROR] Syntax error at or near 'git'
```

This means the `.sql` file contains text that is not SQL.

Example bad SQL file:

```sql
git commit -m "first commit"SELECT
  MAX(salary) AS SecondHighestSalary
FROM employee
```

Spark SQL reads the whole `.sql` file as a query, so terminal commands like `git commit`, `python ...`, or `cd ...` must not be inside the SQL file.

Correct SQL file:

```sql
SELECT
  MAX(salary) AS SecondHighestSalary
FROM employee
WHERE salary < (
  SELECT MAX(salary)
  FROM employee
)
```

## How To Run SQL Solutions

From the project folder:

```powershell
cd A:\Spark_practice\project
python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

Expected result:

```text
2/2 tests passed
```

## Important Rule

Only SQL goes inside `.sql` files.

Commands like these go in PowerShell, not inside the `.sql` file:

```powershell
git commit -m "first commit"
python easy_run.py solution_join.sql --problem Second_Highest_Sal
cd A:\Spark_practice\project
```

## Spark Logs

These lines are normal Spark/JVM logs:

```text
WARNING: Using incubator modules: jdk.incubator.vector
Setting default log level to "WARN"
SUCCESS: The process with PID ... has been terminated.
```

The important line is the test result:

```text
2/2 tests passed
```
