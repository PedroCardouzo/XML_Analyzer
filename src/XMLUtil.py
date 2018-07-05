from src.XMLExtractorException import NoUniqueRootElementException, NotUniqueTemplateException, \
    TemplateNotFoundException
import re
from xml.etree import ElementTree
import xml.dom.minidom
import constants

# find_first_common_parent :: Element String -> Element | context: xml.etree.ElementTree.Element
# finds the first Element (going from leaves to root) that contains every occurrence of an Element with tag 'tag'
def find_first_common_parent(xml, tag):
    candidates = xml.findall('.//' + tag)
    acc = '/..'
    while len(candidates) > 1:
        candidates = xml.findall('.//' + tag + acc)
        acc += '/..'

    # here we have the higher level element which is unique and contains every occurrence of the cond.candidate
    top_level = candidates[0]
    if top_level is None:
        raise NoUniqueRootElementException(candidates)
    else:
        return top_level


# xml_to_string :: Element Boolean=False -> String | context: xml.etree.ElementTree.Element
# given an Element, transforms it into a compacted xml notation, removing whitespaces.
# if optional argument pretty_print is set as True, it indents the xml in a more visual appealing way
# todo: not the best way because if the content for a tag is only composed of \n or \t or \s it will be removed
# todo: add option to clean up empty-content tags
# fix stuff this later, but testing is more important as of now
def xml_to_string(extracted_xml, pretty_print=False):
    data = ElementTree.tostring(extracted_xml).decode('utf-8')
    data = re.sub(">[\n\t\s]*<", '><', data)
    if pretty_print:
        return xml.dom.minidom.parseString(data).toprettyxml()
    else:
        return data

class Template:
    def __init__(self, template_name):

        self.template = None
        self.config = None

        with open(constants.config_filepath + 'config.xacfg') as file:
            # get child with template name
            root = ElementTree.fromstring(file.read()).findall('./' + template_name)
            if len(root) == 1:
                root = root[0]  # unwrap
            else:
                raise NotUniqueTemplateException(template_name)

        self.set_template(root)
        self.set_config(root)

    def set_template(self, element_tree):
        self.template = element_tree.findall('./template')
        if len(self.template) == 1:
            self.template = self.template[0]  # unwrap
        else:
            raise TemplateNotFoundException(element_tree.tag)

    def set_config(self, element_tree):
        self.config = element_tree.findall('./config')
        if len(self.template) == 1:
            self.config = self.template[0]  # unwrap
        elif len(self.template) == 0:
            self.config = '<config>default</config>'
        else:
            print("more than one config found. Assuming default config")
            self.config = '<config>default</config>'

    def get_template(self):
        return self.template

    def get_config(self):
        return self.config
