def solve(data):
    """data: list of dicts with 'id' and 'salary' keys
    Return the second highest salary value or None
    """
    if not data:
        return None
    salaries = sorted({row['salary'] for row in data}, reverse=True)
    if len(salaries) < 2:
        return None
    return salaries[1]
