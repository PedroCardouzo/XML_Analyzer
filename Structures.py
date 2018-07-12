from collections import namedtuple

# namedtuple(String, String, Comparison, builtin_function_or_method, String)
#       where builtin_function_or_method is a comparison function
ConditionalTuple = namedtuple("ConditionalTuple", "candidate, field, comp, value")
#    where
#        candidate is the element that will be removed in case the test is false
#        field     is the field that will be tested
#        comp      is the comparison function (example, >, >=, etc., but their function versions)
#        value     is the value the field will be compared to as in 'field comp value'

# important: if you change this structure, be sure to alter comments in functions inside XMLFilter file
# especially filter_xml_tree which mentions this structure in its documentation
