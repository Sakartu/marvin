def get_channel(line):
    if line.startswith('#'):
        return line
    else:
        return '#' + line


def are_equal_lower(l1, l2):
    '''
    A method that returns True if both lists contain only strings and each
    lowercased string in l1 is also in the lowercased version of l2
    '''
    try:
        l1l = map(str.lower, l1)
        l2l = map(str.lower, l2)
        return set(l1l) == set(l2l)
    except:
        return False
