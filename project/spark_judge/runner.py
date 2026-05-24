"""Runner stub: executes a Python solution file against testcases.
This is a minimal runner that imports a `solve()` function from a solution file and runs it.
"""

import importlib.util
import sys
import types
from typing import Any, List, Dict


def run_solution(solution_path: str, testcases: List[Dict]) -> List[Dict]:
    """Runs `solve(input_data)` for each testcase and returns results list with expected/actual."""
    spec = importlib.util.spec_from_file_location("solution_module", solution_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)  # type: ignore

    if not hasattr(module, 'solve'):
        raise RuntimeError('Solution module must define a solve(input_data) function')

    results = []
    for case in testcases:
        inp = case.get('input')
        expected = case.get('expected')
        # Call solve intelligently based on input shape
        try:
            if isinstance(inp, list):
                # Try positional unpacking first (solve(*inp)), then fall back to single-argument (solve(inp)).
                try:
                    actual = module.solve(*inp)
                except TypeError:
                    actual = module.solve(inp)
            elif isinstance(inp, dict):
                # try calling as module.solve(inp) first, then with kwargs
                try:
                    actual = module.solve(inp)
                except TypeError:
                    actual = module.solve(**inp)
            else:
                actual = module.solve(inp)
        except Exception as e:
            actual = f"<error: {e}>"
        results.append({'input': inp, 'expected': expected, 'actual': actual, 'passed': actual == expected})
    return results
