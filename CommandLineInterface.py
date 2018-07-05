import re
from CommandLineInterfaceException import *
from xml.etree.ElementTree import ElementTree
import constants
from Structures import ConditionalTuple
import XMLExtractor as XMLExtractor
import XMLFilter as XMLFilter
import XMLUtil as XMLUtil
import CommandLineOperators as CommandLineOperators

syntax_help = """
# extracts from file using template
extract from <source_file> using <template_file> to <output_file>
:: <source_file> <template_file> <output_file>  # shortcut for the above
# example: extract from in.xml using templ.xml to out.xml
------------------ in.xml ------------------
<root>
    <b>
        <x>5</x>
        <y>teste</y>
    </b>
    <b>
        <x>not5</x>
        <y>teste2</y>
    </b>
</root>
------------------ templ.xml ------------------
<b>
    <y></y>
</b>
------------------ out.xml ------------------
<b>
    <y>teste</y>
</b>
<b>
    <y>teste2</y>
</b>

# filters from <source_file> the occurrences of <candidate> which do not pass the restraining '<field> <comp> <value>'
filter <source_file> to <output_file> removing <candidate> if <field> <comp> <value> is false
$ <source_file> <output_file> <candidate> <field> <comp> <value>  # shortcut for the above
    where
        <comp> is the comparison operator operator, which can be ==, =, !=, /=, >, >=, <, <=
# example: filter in.xml to out.xml removing b if x != 5 is false
------------------ in.xml ------------------
<root>
    <b>
        <x>5</x>
        <y>teste</y>
    </b>
    <b>
        <x>not5</x>
        <y>teste2</y>
    </b>
</root>
------------------ out.xml ------------------
<root>
    <b>
        <x>not5</x>
        <y>teste2</y>
    </b>
</root>
"""


def parse(input_string):
    if re.match('^extract from ', input_string):
        parse_for_call_extraction(input_string[13:])
    elif re.match('^:: ', input_string):
        call_extraction(input_string[:3].split(' '))
    elif re.match('^filter ', input_string):
        parse_for_call_filter(input_string)
    elif re.match('^\$ ', input_string):
        call_filter(input_string[2:].split(' '))
    elif input_string == 'exit':
        return input_string
    elif input_string == 'help':
        print(syntax_help)
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
        args = args[:3] + args[3].replace(' is false').split(' ')
    except IndexError:
        raise InvalidCommandException(input_string)

    call_filter(args)
