"""Simple parser for SQL-like solution files.
This stub reads a .sql file and returns its contents as a string.
"""

def parse_solution(path: str) -> str:
    """Read and return SQL from a file path."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
