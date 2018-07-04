from src.XMLExtractor import *
from constants import c_base_filepath


def main():
    templ = """<?xml version="1.0"?>
<template_name>
    <compensation_information>
        <paycompensation_recurring>
            '<end_date></end_date>
            <start_date></start_date>
            <pay_component></pay_component>
            <paycompvalue></paycompvalue>
        </paycompensation_recurring>
    </compensation_information>
</template_name>
"""

    try:
        xml_tree = ET.ElementTree()
        xml_tree.parse(c_base_filepath + 'in.xml')
        extracted_xml = extract_template_data_from_xml(ET.fromstring(templ), xml_tree.getroot())
        extracted_xml = fuse_into_old_xml(extracted_xml, xml_tree.getroot())
    except NotChildOfSameParentException as e:
        print(e)
    # test = extracted_xml.findall('.//address_information')
    # print("final test::")
    # for this in test:
    #     print([x.tag if x.tag != 'test_out' else x[0].tag for x in this])
    #     print([x.tag if x.tag != 'test_out' else x[0].tag for x in this])

    xml_tree = ET.ElementTree(extracted_xml)
    xml_tree.write(c_base_filepath + 'out2.xml')

    pass


if __name__ == '__main__':
    main()
