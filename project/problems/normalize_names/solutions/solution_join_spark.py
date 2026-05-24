def solve(spark, inputs):
    """Perform a left join between person and address tables using PySpark DataFrames.

    Expected inputs (parsed from LeetCode-style paste):
      inputs = {
        'person': DataFrame or list-of-dicts,
        'address': DataFrame or list-of-dicts
      }

    Returns a DataFrame with columns: firstName, lastName, city, state
    Missing city/state values are filled with the string 'Null'.
    """
    # import here to avoid top-level dependency issues
    try:
        from pyspark.sql import DataFrame
    except Exception:
        DataFrame = type('DF', (), {})

    person = inputs.get('person')
    address = inputs.get('address')

    # If person/address are provided as Python lists, convert to DataFrames
    if not isinstance(person, DataFrame):
        # assume it's a list of dicts
        person = spark.createDataFrame(person or [])
    if not isinstance(address, DataFrame):
        address = spark.createDataFrame(address or [])

    # Helper: choose the first matching column name from candidates
    def choose_col(df, candidates):
        cols = [c for c in candidates if c in df.columns]
        return cols[0] if cols else None

    # Common variants
    pid_candidates = ['personId', 'person_id', 'user_id', 'id']
    first_candidates = ['firstName', 'first_name', 'firstname', 'first']
    last_candidates = ['lastName', 'last_name', 'lastname', 'last']
    city_candidates = ['city']
    state_candidates = ['state']

    pid_col = choose_col(person, pid_candidates) or choose_col(address, pid_candidates)
    first_col = choose_col(person, first_candidates)
    last_col = choose_col(person, last_candidates)
    city_col = choose_col(address, city_candidates)
    state_col = choose_col(address, state_candidates)

    from pyspark.sql import functions as F

    # Build join condition; if pid_col is missing, do a cartesian-like join (not recommended)
    if pid_col and pid_col in person.columns and pid_col in address.columns:
        join_cond = person[pid_col] == address[pid_col]
    else:
        # no join key found; return person rows with Nulls for address
        join_cond = None

    if join_cond is not None:
        joined = person.join(address, join_cond, how='left')
    else:
        # add placeholder null columns to address then cross join by adding address once per person
        # safer behavior: left join with no match -> keep person and nulls
        joined = person

    # Prepare selected columns, using literals when columns are missing
    def col_or_lit(df, colname, lit_val=None):
        if colname and colname in df.columns:
            return df[colname]
        return F.lit(lit_val)

    sel_first = col_or_lit(person, first_col, None).alias('firstName')
    sel_last = col_or_lit(person, last_col, None).alias('lastName')
    sel_city = col_or_lit(address, city_col, None).alias('city')
    sel_state = col_or_lit(address, state_col, None).alias('state')

    # If joined is just person (no address table), select person cols and add Nulls
    if isinstance(joined, DataFrame) and (join_cond is None):
        result = person.select(sel_first, sel_last, sel_city, sel_state)
    else:
        result = joined.select(sel_first, sel_last, sel_city, sel_state)

    result = result.fillna({'city': 'Null', 'state': 'Null'})

    return result
