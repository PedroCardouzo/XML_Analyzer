from operator import eq, lt, gt, ge, le, ne
from CommandLineInterfaceException import InvalidOperatorException

# get_comp_function_from_string :: String -> (a b -> Boolean) | a, b extends Comparable
def get_comp_function_from_string(string):
    if string == '==' or string == '=':
        return eq
    elif string == '!=' or string == '/=':
        return ne
    elif string == '>':
        return gt
    elif string == '>=':
        return ge
    elif string == '<':
        return lt
    elif string == '<=':
        return le
    else:
        raise InvalidOperatorException(string)
