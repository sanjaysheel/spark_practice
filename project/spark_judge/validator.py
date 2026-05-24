"""Validator stub: checks solution SQL for disallowed keywords and simple sanity checks."""

def validate_sql(sql: str) -> bool:
    """Return True if sql is acceptable, False otherwise."""
    disallowed = ["DROP", "DELETE", "UPDATE", "ALTER", "CREATE TABLE"]
    upper = sql.upper()
    for kw in disallowed:
        if kw in upper:
            return False
    return True
