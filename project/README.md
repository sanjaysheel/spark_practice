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

For when to use `--spark` and when not to use it, read:

```text
RUN_GUIDE.md
```
