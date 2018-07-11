from src.XMLFilter import *
from src.Structures import ConditionalTuple
import xml.etree.ElementTree as ET
import operator
import constants
from lxml import etree as lxml_ElementTree


def test__filter_xml_tree(in_file, out_file, list_condition_tuples):
    xml_tree = ET.ElementTree()
    xml_tree.parse(constants.base_filepath + in_file)
    dict_root = lxml_ElementTree.parse(constants.base_filepath + in_file)
    xml = xml_tree.getroot()

    out = filter_xml_tree(list_condition_tuples, xml)

    xml_tree = ET.ElementTree(out)
    xml_tree.write(constants.base_filepath + out_file)


if __name__ == "__main__":
    # OK
    # test__filter_xml_tree("filter_in.xml", "filter_out.xml",
    #                       [ConditionalTuple("paycompensation_recurring", "pay_component", operator.eq, "US_2_1003")])

    # OK, but empty tags are present (See todo in filter_xml_tree function)
    # test__filter_xml_tree("filter_in.xml", "filter_out2.xml",
    #                       [ConditionalTuple("paycompensation_recurring", "pay_component", operator.eq, "US_2_1003"),
    #                        ConditionalTuple("paycompensation_recurring", "end_date", operator.gt, "2018-05-20")])

    test__filter_xml_tree("xml_todos.xml", "real_work_test_filter.xml", [ConditionalTuple("Employee", "EmployeeIDExternal", operator.eq, '65818')])
    # test__filter_xml_tree("xml_qse_todos.xml", "kinda_real_work_test_filter.xml", [ConditionalTuple("Employee", "EmployeeIDExternal", operator.eq, '36522')])


    #<Employee>
    #<EmployeeIDExternal>65818</EmployeeIDExternal>