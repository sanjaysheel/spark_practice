def solve(inputs):
    """Perform a left join between person and address tables using pandas.

    inputs: dict with keys 'person' and 'address' containing list-of-dicts rows.
    Returns: list-of-dicts rows with columns firstName, lastName, city, state
    """
    try:
        import pandas as pd
    except Exception as e:
        raise RuntimeError('pandas is required for this solution: ' + str(e))

    person = inputs.get('person', [])
    address = inputs.get('address', [])

    df_p = pd.DataFrame(person)
    df_a = pd.DataFrame(address)

    # Ensure personId exists; if not, try common alternatives
    if 'personId' not in df_p.columns and 'user_id' in df_p.columns:
        df_p = df_p.rename(columns={'user_id': 'personId'})
    if 'personId' not in df_a.columns and 'user_id' in df_a.columns:
        df_a = df_a.rename(columns={'user_id': 'personId'})

    if df_p.empty:
        return []

    joined = df_p.merge(df_a, on='personId', how='left')

    # select and rename columns as requested
    # person has firstName,lastName; address has city,state
    out = joined.copy()
    # ensure columns exist
    for col in ['firstName', 'lastName', 'city', 'state']:
        if col not in out.columns:
            out[col] = None

    out = out[['firstName', 'lastName', 'city', 'state']]
    out = out.fillna('Null')

    return out.to_dict(orient='records')
