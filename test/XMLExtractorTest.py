from src.XMLExtractor import *
import lxml.etree as ET
import constants
from src.XMLUtil import xml_to_string

def test__extract_from_xml():
    templ = """<?xml version="1.0"?>
    <template_name>
        <paycompensation_recurring>
            <end_date></end_date>
            <start_date></start_date>
            <pay_component></pay_component>
            <paycompvalue></paycompvalue>
        </paycompensation_recurring>
    </template_name>
    """

    try:
        xml_tree = ET.ElementTree()
        xml_tree.parse(constants.base_filepath + 'in.xml')
        extracted_xml = extract_template_data_from_xml(ET.fromstring(templ), xml_tree.getroot())
        # extracted_xml = fuse_into_old_xml(extracted_xml, xml_tree.getroot())
    except NotChildOfSameParentException as e:
        print(e)
        extracted_xml = "<ErrorMessage>" + str(e) + "</ErrorMessage>"

    data = xml_to_string(extracted_xml, pretty_print=True)
    with open(constants.base_filepath + 'regression_test_out.xml', 'w') as file:
        file.write(data)


if __name__ == "__main__":
    # OK
    test__extract_from_xml()