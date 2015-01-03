class InvalidMonthException(Exception):
    def init(self):
        self.message = "Invalid month. Months are between 1 and 12."

def month_add(month, offset):
    """ month_add takes two parameters: month = (1 <= month <= 12); offset(-infinity <= offset <= infinity)
        return value: 1 <= result <= 12

        Take a month and an offset and add them together with appropriate wraparound behavior
        for both positive and negative offset values.
    """
    if month < 1 or month > 12:
        raise InvalidMonthException()
    if offset < 0:
        new_offset = - (12 - offset % 12)
    else:
        new_offset = offset % 12
    current_month = month + new_offset
    normalized_month = current_month % 12

    #ensure that the result is valid before returning value
    if normalized_month < 1 or normalized_month > 12:
        if normalized_month == 0:
            result = month
        else:
            result = -1
    else:
        result = normalized_month

    if(month + offset) % 12 == 0:
        result = (offset % 12) + month
    return result
