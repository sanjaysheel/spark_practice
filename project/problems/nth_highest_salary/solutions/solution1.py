def solve(params):
    """params: dict with 'n' and 'data' keys
    Return the nth highest salary value or None
    """
    n = params.get('n')
    data = params.get('data', [])
    if not data or n is None or n <= 0:
        return None
    salaries = sorted({row['salary'] for row in data}, reverse=True)
    if len(salaries) < n:
        return None
    return salaries[n-1]
