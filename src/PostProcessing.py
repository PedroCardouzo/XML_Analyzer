from src import XMLAnalyzerException
import lxml.etree as ET
from src.Structures import *
from src import XMLFilter
from src import XMLUtil
import constants
import re
from src.xml_decoder import html_entitize

def apply_all(xml, post_processes):
    for post_process in post_processes:
        xml = apply(xml, post_process)
    return xml


def apply(xml, post_process):
    if post_process.tag == 'filter':
        return apply_filter(xml, post_processing_string_splitter(post_process.text))
    elif post_process.tag == 'text_formatting':
        if post_process.text == 'compress':
            return XMLUtil.compress_xml(xml)
        elif post_process.text == 'indent':
            return XMLUtil.indent_xml(xml)
    elif post_process.tag == 'html_entitize':
        tag_to_entitize = xml.find('.//{*}'+post_process.text)
        if len(tag_to_entitize) > 1:
            raise XMLAnalyzerException.TooManyChildrenException(tag_to_entitize.tag, [x.tag for x in tag_to_entitize], 1)
        content=ET.tostring(tag_to_entitize[0]).decode()
        tag_to_entitize.text = html_entitize(content)
        tag_to_entitize.remove(tag_to_entitize[0])  # remove child
        return xml
    else:
        raise XMLAnalyzerException.InvalidPostProcessTagException(post_process.tag)


def apply_filter(extracted_xml, args, args_stack=[]):
    if len(args) == 4:
        # readying up arguments
        for i in range(len(args)):
            if re.match('^\$param\(.*\)$', args[i]):
                if args_stack == []:
                    args[i] = input(args[i][8:-2])
                else:
                    args[i] = args_stack.pop(0)

        ct = makeConditionalTuple(args[0], args[1], args[2], args[3])
    else:
        raise XMLAnalyzerException.IncorrectArgumentNumberException(4, args)

    XMLFilter.filter_xml_tree(ct, extracted_xml)

    return extracted_xml


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
