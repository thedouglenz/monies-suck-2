def month_add(month, offset):
    """ month_add takes two paramaters: month = (1 <= month <= 12); offset(-infinity <= offset <= infinity)
        return value: 1 <= result <= 12

        Take a month and an offset and add them together with appropriate wraparound behavior
        for both positive and negative offset values.
    """
    if(month < 1 OR month > 12)
        return month;#return bad value and hopefully have it be noticed.
    current_month = month + offset;
    normalized_month = current_month % 12

    #ensure that the result is valid before returning value
    if normalized_month < 1 OR normalized_month > 12:
        result = -1
    else
        result = normalized_month
    return result
