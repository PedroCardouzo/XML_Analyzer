from src.XMLFilter import *
from src.Structures import ConditionalTuple
import lxml.etree as ET
import operator
import constants
import src.XMLUtil as XMLUtil

def test__filter_xml_tree(in_file, out_file, list_condition_tuples):
    xml_tree = ET.ElementTree()
    xml_tree.parse(constants.base_filepath + in_file)
    xml = xml_tree.getroot()

    out = filter_xml_tree(list_condition_tuples, xml)

    data = XMLUtil.xml_to_string(out)
    with open(constants.base_filepath + out_file, 'w') as file:
        file.write(data)


if __name__ == "__main__":
    # OK
    # test__filter_xml_tree("filter_in.xml", "filter_out.xml",
    #                       [ConditionalTuple("paycompensation_recurring", "pay_component", operator.eq, "US_2_1003")])

    # OK, but empty tags are present (See todo in filter_xml_tree function)
    # test__filter_xml_tree("filter_in.xml", "filter_out2.xml",
    #                       [ConditionalTuple("paycompensation_recurring", "pay_component", operator.eq, "US_2_1003"),
    #                        ConditionalTuple("paycompensation_recurring", "end_date", operator.gt, "2018-05-20")])

    test__filter_xml_tree("xml_todos.xml", "real_work_test_filter.xml", [ConditionalTuple("Employee", "EmployeeIDExternal", operator.eq, '65818')])
    test__filter_xml_tree("xml_qse_todos.xml", "kinda_real_work_test_filter.xml", [ConditionalTuple("Employee", "EmployeeIDExternal", operator.eq, '36522')])


    #<Employee>
    #<EmployeeIDExternal>65818</EmployeeIDExternal>