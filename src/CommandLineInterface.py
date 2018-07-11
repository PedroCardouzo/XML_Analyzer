from src.Structures import ConditionalTuple
import re
from src.CommandLineInterfaceException import *
from xml.etree.ElementTree import ElementTree
import constants
from src.Structures import ConditionalTuple
import src.XMLExtractor as XMLExtractor
import src.XMLFilter as XMLFilter
import src.XMLUtil as XMLUtil
import src.CommandLineOperators as CommandLineOperators


def parse(input_string):
    if re.match('^extract from ', input_string):
        parse_for_call_extraction(input_string[13:])
    elif re.match('^:: ', input_string):
        call_extraction(input_string[:3].split(' '))
    elif re.match('^filter ', input_string):
        parse_for_call_filter(input_string)
    elif re.match('^\$ ', input_string):
        call_filter(input_string[2:].split(' '))
    elif input_string == 'help':
        print(constants.syntax_help)
    elif input_string == 'version':
        print(constants.version)
    elif input_string == 'exit':
        print("closing program")
        return input_string
    else:
        raise InvalidCommandException(input_string)


def call_extraction(args):
    try:
        input_file = args[0]
        template_name = args[1]
        output_file = args[2]

        # we wont limit passing more than 3 arguments.
        # It shouldn't be a problem, as we will make a GUI to replace this later
    except IndexError:
        raise MissingArgumentsException(3, args)

    xml_tree = ElementTree()
    xml_tree.parse(constants.base_filepath + input_file)

    template = XMLUtil.Template(template_name)

    extracted_xml = XMLExtractor.extract_template_data_from_xml(template.get_template(), xml_tree.getroot())

    out = XMLUtil.xml_to_string(extracted_xml, pretty_print=True)

    print(out)
    with open(constants.base_filepath + output_file, 'w') as file:
        file.write(out)


def parse_for_call_extraction(input_string):
    try:
        args = input_string.split(' using ')
        args = [args[0]] + args[1].split(' to ')
    except IndexError:
        raise InvalidCommandException(input_string)

    call_extraction(args)

def call_filter(args):
    try:
        input_file = args[0]
        output_file = args[1]
        candidate = args[2]
        field = args[3]
        # if you want to add comparison functions, take a look at src/CommandLineOperators.py
        comp = CommandLineOperators.get_comp_function_from_string(args[4])
        value = args[5]

        # we wont limit passing more than 6 arguments.
        # It shouldn't be a problem, as we will make a GUI to replace this later
    except IndexError:
        raise MissingArgumentsException(6, args)

    xml_tree = ElementTree()
    xml_tree.parse(constants.base_filepath + input_file)

    ct = ConditionalTuple(candidate, field, comp, value)

    extracted_xml = XMLFilter.filter_xml_tree([ct], xml_tree.getroot())

    out = XMLUtil.xml_to_string(extracted_xml)

    print(out)
    with open(constants.base_filepath + output_file, 'w') as file:
        file.write(out)


def parse_for_call_filter(input_string):
    try:
        args = input_string.split(' removing ')
        args = args[0].split(' to ') + args[1].split(' if ')
        args = args[:3] + args[3].replace(' is false', '').split(' ')
    except IndexError:
        raise InvalidCommandException(input_string)

    call_filter(args)
