from src import CommandLineInterface
from src import XMLUtil
import constants


def test__parse(query, target_output_filename, hints_for_manual=[]):
    for hint in hints_for_manual:
        print(hint)
    out = CommandLineInterface.parse(query)
    with open(constants.base_filepath + target_output_filename) as file:
        file_content = file.read()

    try:
        assert (XMLUtil.compress_xml(out) == XMLUtil.compress_xml(file_content))  # for now we wont look at xml format
    except AssertionError as ae:
        print(ae)
        print("content of " + target_output_filename + " was:")
        print(file_content)
        print("output of query " + query + " was:")
        print(out)


if __name__ == '__main__':
    test__parse('extract from payr.xml using IT0000 to None', 'payr_out.xml')
    test__parse('extract from xml_todos.xml using legacy_empl_extraction to None', 'out_legacy_empl_extraction.xml', ['try id as 65818'])
    test__parse('extract from in.xml using pay_comp_template to None', 'out.xml')
    test__parse('filter filter_in.xml to None keeping paycompensation_recurring if pay_component == US_2_1003', 'filter_out.xml')

