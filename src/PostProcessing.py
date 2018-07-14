from src import XMLAnalyzerException
from src.Structures import *
from src import XMLFilter
import re

def apply(extracted_xml, post_process):
    if post_process.tag == 'filter':
        apply_filter(extracted_xml, post_processing_string_splitter(post_process.text))
    else:
        raise XMLAnalyzerException.InvalidPostProcessTag(post_process.tag)


def apply_filter(extracted_xml, args):
    if len(args) == 4:
        # readying up arguments
        for i in range(len(args)):
            if re.match('^\$param\(.*\)$', args[i]):
                args[i] = input(args[i])

        ct = makeConditionalTuple(args[0], args[1], args[2], args[3])
    else:
        raise XMLAnalyzerException.IncorrectArgumentNumberException(4, args)

    XMLFilter.filter_xml_tree(ct, extracted_xml)


# split at every space, except if it is inside "$param('<here>') statement
def post_processing_string_splitter(string):
    in_param = False
    markers = []
    i = 0
    while i < len(string):
        if not in_param:
            if string[i] == ' ':
                markers.append(i)

            if string[i:i+8] == "$param('":
                i += 8
                in_param = True
            else:
                i += 1
        else:
            if string[i] == "'" and string[i+1] == ')':
                i += 2
                markers.append(i)
                in_param = False
            else:
                i += 1
    out = []
    base = 0
    for mark in markers:
        out.append(string[base:mark])
        base = mark+1
    return out

# todo: move to tests file
# string_splitter("Employee EmployeeIDExternal == $param('please provide the EmployeeIDExternal you want to keep: ')")
# string_splitter("Employee $param('test param with spaces') == $param('please  want to keep: ')")
# both passed
