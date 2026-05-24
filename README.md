# Spark Practice Judge

A tiny local judge for SQL/Python solutions for practice problems.

Structure:
- `spark_judge/` - runner, loader, parser, validator stubs
- `problems/` - each problem has `solutions/` and `testcases/`

Try it:

```powershell
python run.py second_highest_salary problems\\second_highest_salary\\solutions\\solution1.py
```

Simpler runner:

```powershell
python easy_run.py solution1.py --problem second_highest_salary --testcase case1.json
```

For how to run Python, PySpark, and SQL solutions, read:

```text
HOW_TO_RUN_SOLUTIONS.md
```

For when to use `--spark` and when not to use it, read:

```text
RUN_GUIDE.md
```

For SQL errors like `Syntax error at or near 'git'`, read:

```text
SQL_TROUBLESHOOTING.md
```
