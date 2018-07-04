from src.XMLExtractorException import NoUniqueRootElementException
import re
from xml.etree import ElementTree
import xml.dom.minidom

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
