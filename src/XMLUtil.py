from src.XMLExtractorException import NoUniqueRootElementException, NotUniqueTemplateException, \
     InnerTemplateNotFoundException, TemplateNotFoundException
import re
import lxml.etree as ET
import constants
import xml.dom.minidom as minidom


# find_first_common_parent :: Element String -> Element | context: lxml.etree.Element
# finds the first Element (going from leaves to root) that contains every occurrence of an Element with tag 'tag'
def find_first_common_parent(xml, tag):
    candidates = xml.findall('.//' + tag)
    acc = '/..'
    while len(candidates) > 1:
        candidates = set(xml.findall('.//' + tag + acc))
        acc += '/..'

    # here we have the higher level element which is unique and contains every occurrence of the cond.candidate
    top_level = next(iter(candidates))
    if top_level is None:
        raise NoUniqueRootElementException(candidates)
    else:
        return top_level


# given a string that is a valid xml, transforms it into a compacted xml notation, removing whitespaces.
def compress_xml(xml):
    if type(xml) is str:
        return re.sub(">[\n\t\s]*<", '><', xml)
    elif type(xml) is ET._Element:
        return ET.fromstring(compress_xml(xml_to_string(xml)))
        # todo: maybe a recursion removing text and tail if text and tail matches '>[\n\t\s]*<', but has children
    else:
        raise TypeError


# given a string that is a valid xml, it indents it
def indent_xml(xml):
    if type(xml) is str:
        return minidom.parseString(compress_xml(xml)).toprettyxml()
    elif type(xml) is ET._Element:
        return ET.fromstring(indent_xml(xml_to_string(xml)))
    else:
        raise TypeError


# xml_to_string :: Element -> String | context: lxml.etree.Element
# transforms XML Object to string format
def xml_to_string(extracted_xml):
    return ET.tostring(extracted_xml, method='html').decode(constants.codification)


def repeating_structure_tag_match(pattern_from_templ, string_from_xml):
    # if you said "any namespace" (that is, '{*}'), this changes it to actual regex that accepts any namespace
    comparing_tag = pattern_from_templ.replace('{*}', '^{.*}')
    return re.match('^'+comparing_tag+'$', string_from_xml)

class Template:
    def __init__(self, template_name):

        self.template = None
        self.post_process_queue = None

        with open(constants.config_filepath) as file:
            # get child with template name
            root = ET.fromstring(file.read()).findall('./' + template_name)
            if len(root) == 1:
                root = root[0]  # unwrap
            elif len(root) == 0:
                raise TemplateNotFoundException(template_name)
            else:
                raise NotUniqueTemplateException(template_name)

        self.set_template(root)
        self.create_post_processing_queue(root)

    def set_template(self, element_tree):
        self.template = element_tree.findall('./template')
        if len(self.template) == 1:
            self.template = self.template[0]  # unwrap
        else:
            raise InnerTemplateNotFoundException(element_tree.tag)

    def create_post_processing_queue(self, element_tree):
        self.post_process_queue = element_tree.findall('./post_processing')
        if len(self.post_process_queue) == 1:
            self.post_process_queue = self.post_process_queue[0]  # unwrap
        elif len(self.post_process_queue) == 0:
            self.post_process_queue = '<post_processing>default</post_processing>'
        else:
            print("more than one post processing found. Assuming default post processing")
            self.post_process_queue = '<post_processing>default</post_processing>'

    def get_template(self):
        return self.template

    def get_config(self):
        return self.post_process_queue
