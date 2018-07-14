import lxml.etree as ET
from src.XMLExtractorException import *
import src.XMLUtil as XMLUtil


def fuse_into_old_xml(extracted_xml_portion, xml):

    # extracted_xml_portion should be the parent of all the first-level template elements
    parent = xml.find('.//' + extracted_xml_portion.tag + '/..')

    # remove all children from parent node
    for x in list(parent):  # do not iterate over the list you're modifying, therefore, list(parent)
        parent.remove(x)

    for x in extracted_xml_portion:
        parent.append(x)

    return xml


def get_top_level_common_parent(template, xml):
    common_parent = set()
    for x in template:
        common_parent.add(XMLUtil.find_first_common_parent(xml, x.tag))

    if len(common_parent) == 1:
        return next(iter(common_parent))
    else:
        raise NoCommonParentInTemplateTopLevelException([x for x in template])


# extract_template_data_from_xml :: Element Element -> Element | context: xml.etree.ElementTree.Element
# given an template and an xml, it extracts the repeating occurrences of the template in the xml
# template should be the tag that is the template name in the template xml, containing the tags with the actual data
# you want to extract
def extract_template_data_from_xml(template, xml):

    data = []

    all_father = get_top_level_common_parent(template, xml)
    # a template can contain multiple repeating structures

    for repeating_structure in template:

        common_parent = XMLUtil.find_first_common_parent(xml, repeating_structure.tag)

        # (only in debugging mode): weird exception is thrown in the case I sent the output of
        # extract_from_xml_section to a variable. In case I print it, for example, no exception is thrown
        data.append(extract_from_xml(repeating_structure, common_parent))

    extracted_xml_portion = ET.Element(all_father.tag)
    extracted_xml_portion.text = all_father.text

    # in this case all_father == common_parent, therefore we can just return the only one content of data
    if len(data) == 1:
        return data[0]
    else:
        for x in data:
            extracted_xml_portion.append(x)

        return extracted_xml_portion

# extract_from_xml :: Element Element -> Element | context: xml.etree.ElementTree.Element
# recurses through xml_section until it finds a match for the top level element
# from the template and then extracts data from it using the template
def extract_from_xml(repeating_structure, xml_section):

    if XMLUtil.repeating_structure_tag_match(repeating_structure.tag, xml_section.tag):
        return extract_from_xml_section([repeating_structure], xml_section)
    else:
        contentless = True
        new_parent = ET.Element(xml_section.tag)
        new_parent.text = xml_section.text
        for child in xml_section:
            extracted_data = extract_from_xml(repeating_structure, child)
            if extracted_data is not None:
                new_parent.append(extracted_data)
                contentless = False

        if not contentless:
            return new_parent
        else:
            return None


# todo: handle exception that will occur when trying to access a set of tags when xml actually have a value
# example: template has <abc><d></d><e></e></abc> but xml has <abc>10</abc>
# todo: handle exception that will occur when trying to access a tag that doesn't exists in the current level
# example: template has <a><c></c><d></d></a> but xml has <a><b><c></c></b><d></d></a> -> output = <a><d></d></a>
# extract_from_xml_section :: [Element] Element | context: xml.etree.ElementTree.Element
# complexity :: O(N . n . d)
#     where
#       N -> number of children in the current level in the XML
#       n -> number of children in the current level of template
#       d -> max level of template (how deep the XML parsed tree of the template is)
def extract_from_xml_section(template, xml):
    # each template tag should be unique, therefore templ should have size <= 1 after this
    templ = [y for y in template if XMLUtil.repeating_structure_tag_match(y.tag, xml.tag)]

    # validation ::
    if templ == []:  # XML tag is not in the current level of template
        return None
    else:
        if len(templ) == 1:
            templ = templ[0]  # templ has only 1 element, therefore we can unwrap it
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
                sub_element = extract_from_xml_section(template_children, xml_child)

                # recursive call could've returned None (i.e.: XML tag is not in the specific level of the template)
                if sub_element is not None:
                    new_el.append(sub_element)

            return new_el


