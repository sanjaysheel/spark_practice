"""PySpark-aware runner.

This module will try to import pyspark and create a SparkSession. It exposes
run_solution_spark(solution_path, testcases) which will call a solution module's
solve function with a SparkSession and inputs converted to DataFrames.

Contract / behavior:
- If a testcase input is a dict of tables (list-of-dicts), they are converted to DataFrames and passed as a dict.
- The solution should accept either solve(spark, inputs) or solve(inputs, spark).
- The solution should return either a list-of-dicts or a DataFrame. The runner will collect the result and compare with expected.
"""

from typing import List, Dict, Any
import importlib.util
import os
import sys

def _java_major(java_home):
    import re
    import subprocess

    java_exe = os.path.join(java_home, 'bin', 'java.exe')
    if not os.path.isfile(java_exe):
        return None
    try:
        result = subprocess.run([java_exe, '-version'], capture_output=True, text=True, timeout=5)
    except Exception:
        return None
    output = result.stderr or result.stdout
    match = re.search(r'"(?:1\.)?(\d+)', output)
    return int(match.group(1)) if match else None


def _set_compatible_java_home():
    # Set JAVA_HOME before importing pyspark. Python 3.14-compatible PySpark 4.x
    # requires Java 17+, so prefer newer JDKs when present.
    common_java_paths = [
        'C:\\Program Files\\Eclipse Adoptium',
        'C:\\Program Files\\Java',
        'C:\\Program Files\\Eclipse Adoptium\\jdk-21',
        'C:\\Program Files\\Eclipse Adoptium\\jdk-17',
        'C:\\Program Files\\Java\\jdk-17',
        'C:\\Tools\\temurin-17',
        'C:\\Tools\\temurin-11\\jdk-11.0.23+9',
        'C:\\Program Files\\Java\\jdk-1.8',
    ]
    expanded = []
    for path in common_java_paths:
        if os.path.isdir(path):
            expanded.append(path)
            try:
                expanded.extend(
                    os.path.join(path, name)
                    for name in os.listdir(path)
                    if os.path.isdir(os.path.join(path, name))
                )
            except OSError:
                pass

    current_home = os.environ.get('JAVA_HOME')
    min_major = 17 if sys.version_info >= (3, 14) else 8
    if current_home and (_java_major(current_home) or 0) >= min_major:
        return

    for path in expanded:
        major = _java_major(path)
        if major and major >= min_major:
            os.environ['JAVA_HOME'] = path
            os.environ['PATH'] = os.path.join(path, 'bin') + os.pathsep + os.environ.get('PATH', '')
            return


_set_compatible_java_home()

# Avoid mixing pip-installed PySpark with an older standalone Spark install.
# A stale SPARK_HOME can make PySpark 4.x load Spark 3.x jars and fail with
# "JavaPackage object is not callable" during SparkSession startup.
os.environ.pop('SPARK_HOME', None)
os.environ['PYSPARK_PYTHON'] = sys.executable

try:
    from pyspark.sql import SparkSession
    from pyspark.sql import DataFrame as SparkDataFrame
except Exception:
    SparkSession = None  # type: ignore
    SparkDataFrame = None  # type: ignore


def _to_spark_df(spark, rows: List[Dict[str, Any]]):
    # simple conversion: rely on Spark to infer schema
    return spark.createDataFrame(rows)


def _from_spark_df(df: 'SparkDataFrame') -> List[Dict[str, Any]]:
    # collect to list of dicts
    return [row.asDict() for row in df.collect()]


def run_solution_spark(solution_path: str, testcases: List[Dict]) -> List[Dict]:
    if SparkSession is None:
        raise RuntimeError('PySpark is not installed or failed to import')

    spec = importlib.util.spec_from_file_location("solution_module", solution_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)  # type: ignore

    # ensure solution has solve
    if not hasattr(module, 'solve'):
        raise RuntimeError('Solution module must define a solve(...) function')

    try:
        spark = SparkSession.builder.master('local[*]').appName('local_judge').getOrCreate()
    except Exception as e:
        # Provide a clearer, actionable error for common Windows/Java issues
        msg = (
            "Failed to create SparkSession (PySpark). Common causes on Windows:\n"
            " - Java is not installed, or JAVA_HOME is not set correctly.\n"
            " - JAVA_HOME points to a JRE instead of a JDK, or Java version is incompatible.\n"
            " - PySpark can't find the Java gateway.\n\n"
            "Quick checks you can run in PowerShell:\n"
            "  java -version\n"
            "  echo $Env:JAVA_HOME\n\n"
            "If java is missing, install a JDK (OpenJDK 8 or 11 recommended). Then set JAVA_HOME, e.g.:\n"
            "  setx JAVA_HOME 'C:\\\\Path\\to\\jdk'\n"
            "  $Env:JAVA_HOME = 'C:\\\\Path\\to\\jdk'  # for current session\n\n"
            "If Java is installed and the above doesn't help, ensure your Java and pyspark versions are compatible and restart your shell/IDE.\n\n"
            f"Original error: {e}"
        )
        raise RuntimeError(msg)

    results = []
    for case in testcases:
        inp = case.get('input')
        expected = case.get('expected')

        # Convert named tables (dict of lists) into DataFrames
        spark_inputs = None
        if isinstance(inp, dict):
            spark_inputs = {}
            for k, v in inp.items():
                if isinstance(v, list):
                    spark_inputs[k] = _to_spark_df(spark, v)
                else:
                    spark_inputs[k] = v
        elif isinstance(inp, list):
            # list of tables -> convert elements that are list-of-dicts
            converted = []
            for v in inp:
                if isinstance(v, list):
                    converted.append(_to_spark_df(spark, v))
                else:
                    converted.append(v)
            spark_inputs = converted
        else:
            spark_inputs = inp

        # Call the solution: try both signatures
        try:
            try:
                actual_raw = module.solve(spark, spark_inputs)
            except TypeError:
                actual_raw = module.solve(spark_inputs, spark)
        except Exception as e:
            results.append({'input': inp, 'expected': expected, 'actual': f'<error: {e}>', 'passed': False})
            continue

        # Normalize actual result: DataFrame -> list-of-dicts
        if SparkDataFrame is not None and isinstance(actual_raw, SparkDataFrame):
            actual = _from_spark_df(actual_raw)
        else:
            actual = actual_raw

        # If expected is a DataFrame or list-of-dicts string, normalize similarly
        exp_norm = expected
        if isinstance(expected, list):
            exp_norm = expected

        results.append({'input': inp, 'expected': exp_norm, 'actual': actual, 'passed': actual == exp_norm})

    spark.stop()
    return results
