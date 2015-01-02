def month_add(month, offset):
    """ Take a month and an offset and add them together with approriate wraparound behavior
        for both postiive and negative offset values. Offset should be between -12 and 12
        inclusive, however.
    """
    result = month
    if offset == 0:
        return result
    elif month + offset < 1:
        result = 12 + (month + offset)
    elif month + offset > 12:
        result = offset - (12 - month)
    else:
        result = month + offset
    return result
