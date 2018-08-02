def exclude_keys(excluded_keys, dict):
    return { x: dict[x] for x in dict if x not in excluded_keys }
