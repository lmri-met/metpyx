def my_function(flag1=True, flag2=False):
    """
    Print a message based on the combination of flag1 and flag2 values.

    Parameters
    ----------
    flag1 : bool, optional
        First flag, defaults to True.
    flag2 : bool, optional
        Second flag, defaults to False.

    Notes
    -----
    This function prints a message based on the combination of flag1 and flag2 values.

    Examples
    --------
    >>> my_function()
    both true
    >>> my_function(flag1=False, flag2=False)
    both false
    >>> my_function(flag2=True)
    first true, second true
    """
    if flag1 and flag2:
        print("both true")
    elif not flag1 and not flag2:
        print("both false")
    elif flag1 and not flag2:
        print("first true, second false")
    else:
        print("first false, second true")
