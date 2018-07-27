from src.Structures import ConditionalTuple
import re
from src.XMLAnalyzerException import *
import lxml.etree as ET
import constants
from src.Structures import *
from src import XMLExtractor
from src import XMLFilter
from src import XMLUtil
from src import PostProcessing


def parse(input_string):
    if re.match('^extract from ', input_string):
        return parse_for_call_extraction(input_string[13:])
    elif re.match('^:: ', input_string):
        return call_extraction(input_string[:3].split(' '))
    elif re.match('^filter ', input_string):
        return parse_for_call_filter(input_string[7:])
    elif re.match('^\$ ', input_string):
        return call_filter(input_string[2:].split(' '))
    elif re.match('^template(s?)$', input_string):
        return get_templates()
    elif input_string == 'help':
        return constants.syntax_help
    elif input_string == 'version':
        return constants.version
    elif input_string == 'exit':
        return input_string
    else:
        raise InvalidCommandException(input_string)


def call_extraction(args):
    if len(args) == 3:
        input_file = args[0]
        template_name = args[1]
        output_file = args[2]
    else:
        raise IncorrectArgumentNumberException(3, args)

    xml_tree = ET.ElementTree()
    with open(constants.base_filepath + input_file) as file:
        data = file.read()
    try:
        xml_tree = ET.fromstring(data)
    except ET.XMLSyntaxError as e:

        data = re.sub('<\\?.*?\\?>', '', data)
        xml_tree = ET.fromstring(data)

    template = XMLUtil.Template(template_name)

    extracted_xml = XMLExtractor.extract_template_data_from_xml(template.get_template(), xml_tree)

    extracted_xml = PostProcessing.apply_all(extracted_xml, template.post_process_queue)

    out = XMLUtil.xml_to_string(extracted_xml)

    if output_file != 'None':
        with open(constants.base_filepath + output_file, 'w') as file:
            file.write(out)

    return out


def parse_for_call_extraction(input_string):
    try:
        args = input_string.split(' using ')
        args = [args[0]] + args[1].split(' to ')
    except IndexError:
        raise InvalidCommandException(input_string)

    return call_extraction(args)

def call_filter(args):
    if len(args) == 6:
        input_file = args[0]
        output_file = args[1]

        candidate = args[2]
        field = args[3]
        # if you want to add comparison functions, take a look at src/Structures.py,
        # under 'get_comp_function_from_string' function
        comp = args[4]
        value = args[5]

        ct = makeConditionalTuple(candidate, field, comp, value)

    else:
        raise IncorrectArgumentNumberException(6, args)

    xml_tree = ET.ElementTree()
    xml_tree.parse(constants.base_filepath + input_file)

    extracted_xml = XMLFilter.filter_xml_tree([ct], xml_tree.getroot())

    out = XMLUtil.xml_to_string(extracted_xml)

    if output_file != 'None':
        with open(constants.base_filepath + output_file, 'w') as file:
            file.write(out)
    return out


def parse_for_call_filter(input_string):
    try:
        args = input_string.split(' keeping ')
        args = args[0].split(' to ') + args[1].split(' if ')
        args = args[:3] + args[3].split(' ')
    except IndexError:
        raise InvalidCommandException(input_string)

    return call_filter(args)

def get_templates():
    with open(constants.config_filepath) as file:
        config = ET.fromstring(file.read())
    return [template.tag for template in config]
