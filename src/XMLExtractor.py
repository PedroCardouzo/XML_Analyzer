import xml.etree.ElementTree as ET
from src.XMLExtractorException import *


def fuse_into_old_xml(extracted_xml_portion, xml):

    # extracted_xml_portion should be the parent of all the first-level template elements
    parent = xml.find('.//' + extracted_xml_portion.tag)

    # remove all children from parent node
    for x in list(parent):  # do not iterate over the list you're modifying, therefore, list(parent)
        parent.remove(x)

    for x in extracted_xml_portion:
        parent.append(x)

    return xml


# extract_from_xml :: Element Element Boolean | context: xml.etree.ElementTree.Element
# template should be the tag that is the template name in the template xml
def extract_from_xml(template, xml):
    # todo: find better name or comment explaining
    set_of_parents = set()
    data = []
    for repeating_structure in template:
        root = xml.find(".//" + repeating_structure.tag + "/..")
        set_of_parents.add(root.tag)
        if len(set_of_parents) > 1:
            raise NotChildOfSameParentException(template.tag, root.tag)

        for xml_section in root:

            # weird exception is thrown in the case I sent the output of extract_directly_from_section to a variable
            # in case I print it, for example, not exception is thrown (only in debugging mode)
            this = extract_directly_from_section([repeating_structure], xml_section)

            if this is not None:
                data.append(this)
                # print([x.tag for x in this])
                # print([x.text for x in this])

    parent = xml.find('.//' + next(iter(set_of_parents)))  # set_of_parents should contain only one parent

    extracted_xml_portion = ET.Element(parent.tag)
    extracted_xml_portion.text = parent.text
    for x in data:
        extracted_xml_portion.append(x)

    return extracted_xml_portion


# todo: handle exception that will occur when trying to access a set of tags when xml actually have a value
# example: template has <abc><d></d><e></e></abc> but xml has <abc>10</abc>
# todo: handle exception that will occur when trying to access a tag that doesn't exists in the current level
# example: template has <a><c></c><d></d></a> but xml has <a><b><c></c></b><d></d></a> -> output = <a><d></d></a>
# extract_directly_from_section :: [Element] Element | context: xml.etree.ElementTree.Element
# complexity :: O(N . n . d)
#     where
#       N -> number of children in the current level in the XML
#       n -> number of children in the current level of template
#       d -> max level of template (how deep the XML parsed tree of the template is)
def extract_directly_from_section(template, xml):
    # each template tag should be unique, therefore templ should have size <= 1 after this
    templ = [y for y in template if y.tag == xml.tag]

    # validation ::
    if templ == []:  # XML tag is not in the current level of template
        return None
    else:
        if len(templ) == 1:
            templ = templ[0]  # templ have only 1 element, therefore this makes it clearer to access
        else:
            # templ has more than one element, this is not supposed to happen
            raise DuplicateTagInTemplateException(xml.tag)

    # logic ::
        template_children = [x for x in templ]
        if template_children == []:
            return xml
        else:
            new_el = ET.Element(xml.tag)
            new_el.text = xml.text
            for xml_child in xml:
                sub_element = extract_directly_from_section(template_children, xml_child)

                # recursive call could've returned None (i.e.: XML tag is not in the specific level of the template)
                if sub_element is not None:
                    new_el.append(sub_element)

            return new_el


