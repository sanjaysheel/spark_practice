"""Top-level runner to execute problems' solutions against their testcases.

Usage:
  python run.py [--spark] <problem_name> <solution_file> [--testcase <filename>]

If --spark is provided the runner will attempt to create a SparkSession and
convert table-like inputs into Spark DataFrames. The solution contract for
Spark mode is flexible; recommended signature is solve(spark, inputs) where
inputs is a dict mapping table names to DataFrames.
"""
import os
import sys
from typing import Optional

from spark_judge.loader import load_testcases
from spark_judge.runner import run_solution

BASE = os.path.dirname(__file__)
PROBLEMS_DIR = os.path.join(BASE, 'problems')


def _parse_args(argv) -> (bool, Optional[str], Optional[str], Optional[str]):
    # returns (use_spark, problem, solution, testcase_filename)
    use_spark = False
    testcase_file = None
    args = [a for a in argv[1:]]
    if '--spark' in args:
        use_spark = True
        args.remove('--spark')
    # optional --testcase <filename>
    if '--testcase' in args:
        idx = args.index('--testcase')
        if idx + 1 < len(args):
            testcase_file = args[idx + 1]
            del args[idx:idx+2]
        else:
            print('Usage: --testcase requires a filename')
            sys.exit(2)

    if len(args) < 2:
        print('Usage: python run.py [--spark] <problem_name> <solution_file> [--testcase <filename>]')
        sys.exit(2)
    problem = args[0]
    solution = args[1]
    return use_spark, problem, solution, testcase_file


def main():
    use_spark, problem, solution, testcase_file = _parse_args(sys.argv)

    tc_dir = os.path.join(PROBLEMS_DIR, problem, 'testcases')
    if not os.path.isdir(tc_dir):
        print('Problem not found:', problem)
        sys.exit(1)

    testcases = load_testcases(tc_dir)
    if testcase_file:
        # filter to only that file (by filename)
        basename = os.path.basename(testcase_file)
        testcases = [t for t in testcases if t.get('__source__') == basename]
        if not testcases:
            print('Testcase not found:', basename)
            sys.exit(1)

    solution_path = os.path.abspath(solution)

    if use_spark:
        try:
            from spark_judge.pyspark_runner import run_solution_spark
        except Exception as e:
            print('PySpark runner is not available or failed to import:', e)
            print('Install pyspark and try again: pip install pyspark')
            sys.exit(1)
        results = run_solution_spark(solution_path, testcases)
    else:
        results = run_solution(solution_path, testcases)

    passed = sum(1 for r in results if r['passed'])
    print(f"{passed}/{len(results)} tests passed")
    for r in results:
        print(r)


if __name__ == '__main__':
    main()
