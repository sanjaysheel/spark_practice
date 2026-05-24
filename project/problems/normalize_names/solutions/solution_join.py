def solve(inputs):
    """expects inputs to be a dict with keys 'person' and 'address' (parsed from labeled tables)
    Performs a left join person -> address on personId and returns list of rows dicts with keys firstName,lastName,city,state
    """
    person = inputs.get('person', [])
    address = inputs.get('address', [])
    # build address map by personId
    addr_map = {}
    for row in address:
        pid = row.get('personId')
        if pid is None:
            continue
        addr_map[pid] = row
    out = []
    for p in person:
        pid = p.get('personId')
        a = addr_map.get(pid, {})
        out.append({
            'firstName': p.get('firstName'),
            'lastName': p.get('lastName'),
            'city': a.get('city') or 'Null',
            'state': a.get('state') or 'Null'
        })
    return out
