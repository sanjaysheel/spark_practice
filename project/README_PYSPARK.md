# Spark Practice Judge - PySpark Setup & Usage

## Current Setup

This workspace is ready for local PySpark runs with:

- Python 3.14
- Java 17
- PySpark 4.1.x

The runner clears stale `SPARK_HOME` and sets `PYSPARK_PYTHON` to the active Python executable so pip-installed PySpark is not mixed with an older standalone Spark install.

## Setup

From `A:\Spark_practice\project`:

```powershell
python setup_spark.py
```

Verify:

```powershell
python -c "import pyspark; print('PySpark:', pyspark.__version__)"
```

Expected version: `4.1.x`.

## Run The PySpark Join Example

```powershell
python run.py --spark normalize_names problems\normalize_names\solutions\solution_join_spark.py --testcase case_join.json
```

Expected result:

```text
1/1 tests passed
```

## Run The Simple Join Solution

From `A:\Spark_practice\project`:

```powershell
python run.py --spark normalize_names .\problems\normalize_names\solutions\solution_join_spark_simple.py
```

Current result:

```text
1/3 tests passed
```

Only `case_join.json` is correct for this simple join solution. The other two testcases, `case1.json` and `case_ascii.json`, test name normalization (`aLice` -> `Alice`, `bOB` -> `Bob`) and do not contain the `person` and `address` tables that this solution expects.

To run only the correct testcase for this solution:

```powershell
python run.py --spark normalize_names .\problems\normalize_names\solutions\solution_join_spark_simple.py --testcase case_join.json
```

## Manual Spark Smoke Test

```powershell
python -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.master('local[1]').appName('test').getOrCreate(); print(spark.version); spark.createDataFrame([{'id': 1, 'name': 'Alice'}]).show(); spark.stop()"
```

## Troubleshooting

If you see `TypeError: 'JavaPackage' object is not callable`, check for a stale standalone Spark install:

```powershell
echo $Env:SPARK_HOME
```

For this project, run through `run.py`; the Spark runner removes stale `SPARK_HOME` for the current process.

If Java is missing, install Temurin/OpenJDK 17+ and rerun:

```powershell
python setup_spark.py
```

## Key Files

- `setup_spark.py` - detects Java/Python and installs a compatible PySpark version
- `spark_judge/pyspark_runner.py` - creates the SparkSession and runs Spark solutions
- `run.py` - main entry point; use `--spark` for Spark mode
- `problems/normalize_names/solutions/solution_join_spark.py` - PySpark join example
