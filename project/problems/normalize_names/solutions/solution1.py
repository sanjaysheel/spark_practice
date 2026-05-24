def solve(table_rows):
    # table_rows: list of dicts [{'user_id': int, 'name': str}, ...]
    out = []
    for row in table_rows:
        name = row.get('name','')
        # Normalize capitalization: first letter uppercase, rest lowercase
        normalized = name.capitalize()
        out.append({'user_id': row.get('user_id'), 'name': normalized})
    return out
