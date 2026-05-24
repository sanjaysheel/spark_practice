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
    print(f"Mode: {mode}")
    print(f"Problem: {problem_name}")
    print(f"Solution: {solution_path}")
    print(f"{passed}/{len(results)} tests passed")
    for result in results:
        print(result)


def main():
    args = _parse_args()
    solution_path = _find_solution(args.solution, args.problem)
    problem_name = args.problem or _problem_name_from_path(solution_path)
    testcases = _load_cases(problem_name, args.testcase)
    _run(solution_path, problem_name, testcases)


if __name__ == "__main__":
    main()
