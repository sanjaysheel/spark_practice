"""Short command runner for Python, PySpark, and SQL solutions.

Examples:
  python easy_run.py solution_join_spark_simple.py --testcase case_join.json
  python easy_run.py solution1.py --problem nth_highest_salary --testcase case1.json
  python easy_run.py solution_second_highest.sql --problem Second_Highest_Sal
"""

import argparse
import os
import sys
from pathlib import Path

from spark_judge.loader import load_testcases
from spark_judge.runner import run_solution

BASE = Path(__file__).resolve().parent
PROBLEMS_DIR = BASE / "problems"


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Run a solution by filename. Auto-detects Python, PySpark, or SQL."
    )
    parser.add_argument("solution", help="Solution filename or path")
    parser.add_argument("--problem", help="Problem folder name, needed when filenames repeat")
    parser.add_argument("--testcase", help="Optional testcase filename, for example case1.json")
    return parser.parse_args()


def _candidate_solution_dirs():
    return {"solutions", "sql_solutions"}


def _find_solution(solution_arg, problem=None):
    supplied = Path(solution_arg)
    if supplied.exists():
        return supplied.resolve()

    if not supplied.is_absolute():
        relative = (BASE / supplied)
        if relative.exists():
            return relative.resolve()

    name = supplied.name
    matches = []
    for path in PROBLEMS_DIR.rglob(name):
        if path.is_file() and path.parent.name in _candidate_solution_dirs():
            if problem and not _problem_name_from_path(path).lower() == problem.lower():
                continue
            matches.append(path.resolve())

    if not matches:
        raise SystemExit(f"Solution not found: {solution_arg}")
    if len(matches) > 1:
        print("More than one solution matched. Add --problem.")
        for match in matches:
            print(f"  {match}")
        raise SystemExit(2)
    return matches[0]


def _problem_name_from_path(solution_path):
    parts = list(solution_path.parts)
    try:
        index = next(i for i, part in enumerate(parts) if part.lower() == "problems")
    except StopIteration:
        raise SystemExit("Could not infer problem name. Put the solution under problems/<problem>/...")
    if index + 1 >= len(parts):
        raise SystemExit("Could not infer problem name from solution path")
    return parts[index + 1]


def _find_testcase_dir(problem_name):
    problem_dir = PROBLEMS_DIR / problem_name
    if not problem_dir.is_dir():
        raise SystemExit(f"Problem folder not found: {problem_name}")

    for child in problem_dir.iterdir():
        if child.is_dir() and child.name.lower() == "testcases":
            return child

    raise SystemExit(f"No testcases folder found for problem: {problem_name}")


def _load_cases(problem_name, testcase_name=None):
    testcase_dir = _find_testcase_dir(problem_name)
    cases = load_testcases(str(testcase_dir))
    if testcase_name:
        basename = os.path.basename(testcase_name)
        cases = [case for case in cases if case.get("__source__") == basename]
        if not cases:
            raise SystemExit(f"Testcase not found: {basename}")
    return cases


def _looks_like_spark_solution(solution_path):
    text = solution_path.read_text(encoding="utf-8", errors="ignore")
    return "def solve(spark" in text or "pyspark" in text


def _format_table(data):
    """Format list of dicts as a simple table."""
    if not data or not isinstance(data, list):
        return str(data)
    
    if not isinstance(data[0], dict):
        return str(data)
    
    # Get all keys from all rows
    keys = []
    for row in data:
        for key in row.keys():
            if key not in keys:
                keys.append(key)
    
    if not keys:
        return "[]"
    
    # Calculate column widths
    col_widths = {}
    for key in keys:
        col_widths[key] = len(str(key))
        for row in data:
            col_widths[key] = max(col_widths[key], len(str(row.get(key, ""))))
    
    # Build table
    lines = []
    
    # Header
    header = " | ".join(str(key).ljust(col_widths[key]) for key in keys)
    lines.append(header)
    lines.append("-" * len(header))
    
    # Rows
    for row in data:
        row_str = " | ".join(str(row.get(key, "")).ljust(col_widths[key]) for key in keys)
        lines.append(row_str)
    
    return "\n".join(lines)


def _show_differences(expected, actual):
    """Show detailed differences between expected and actual output."""
    if not isinstance(expected, list) or not isinstance(actual, list):
        return
    
    if len(expected) != len(actual):
        print(f"  ⚠️  Row count mismatch: Expected {len(expected)} rows, got {len(actual)} rows")
        return
    
    # Check each row
    for i, (exp_row, act_row) in enumerate(zip(expected, actual)):
        if exp_row != act_row:
            print(f"  ⚠️  Row {i} differs:")
            
            # Get all keys
            all_keys = set(exp_row.keys()) | set(act_row.keys())
            
            for key in sorted(all_keys):
                exp_val = exp_row.get(key)
                act_val = act_row.get(key)
                
                if exp_val != act_val:
                    exp_type = type(exp_val).__name__
                    act_type = type(act_val).__name__
                    print(f"      {key}:")
                    print(f"        Expected: {repr(exp_val)} ({exp_type})")
                    print(f"        Got:      {repr(act_val)} ({act_type})")


def _print_results(results):
    """Format and print test results clearly."""
    for i, result in enumerate(results, 1):
        passed = result["passed"]
        status = "✓ PASSED" if passed else "✗ FAILED"
        
        print(f"\nTest Case {i}: {status}")
        
        if not passed:
            actual = result.get("actual")
            if isinstance(actual, str) and actual.startswith("<error:"):
                # Extract and highlight the error message
                error_msg = actual[8:-1] if actual.endswith(">") else actual[8:]
                print(f"  ERROR: {error_msg}")
                # Still show expected output even on error
                expected = result.get('expected')
                if expected is not None:
                    print(f"\n  Expected Output:")
                    print(_format_table(expected))
            else:
                print(f"  Your Output:")
                print(_format_table(actual))
                print(f"\n  Expected:")
                print(_format_table(result.get('expected')))
                print(f"\n  Differences:")
                _show_differences(result.get('expected'), actual)
        else:
            # Show expected and actual output tables for passed tests
            expected = result.get("expected")
            actual = result.get("actual")
            print(f"  Expected Output:")
            print(_format_table(expected))
            print(f"\n  Actual Output:")
            print(_format_table(actual))


def _run(solution_path, problem_name, testcases):
    suffix = solution_path.suffix.lower()
    if suffix == ".sql":
        from spark_judge.sql_runner import run_solution_sql

        mode = "sql"
        results = run_solution_sql(str(solution_path), testcases)
    elif _looks_like_spark_solution(solution_path):
        from spark_judge.pyspark_runner import run_solution_spark

        mode = "pyspark"
        results = run_solution_spark(str(solution_path), testcases)
    else:
        mode = "python"
        results = run_solution(str(solution_path), testcases)

    passed = sum(1 for result in results if result["passed"])
    print(f"\n{'='*60}")
    print(f"Mode: {mode}")
    print(f"Problem: {problem_name}")
    print(f"Solution: {solution_path}")
    print(f"Result: {passed}/{len(results)} tests passed")
    
    if mode == "pyspark" and results:
        app_id = results[0].get('app_id')
        if app_id:
            print(f"Spark UI: http://localhost:4040")
            print(f"App ID: {app_id}")
            print(f"Exact Job Links:")
            for i, result in enumerate(results, 1):
                case_idx = result.get('case_idx', i-1)
                job_id = case_idx
                print(f"  Test Case {i}: http://localhost:4040/jobs/job/?id={job_id}")
    print(f"{'='*60}")
    
    _print_results(results)


def main():
    args = _parse_args()
    solution_path = _find_solution(args.solution, args.problem)
    problem_name = args.problem or _problem_name_from_path(solution_path)
    testcases = _load_cases(problem_name, args.testcase)
    _run(solution_path, problem_name, testcases)


if __name__ == "__main__":
    main()
