import xml.etree.ElementTree as ET


def main():
    templ = """<?xml version="1.0"?>
<template_name>
    <address_information>
        <start_date></start_date>
        <address_type></address_type>
        <address2></address2>
        <zip_code></zip_code>
        <end_date></end_date>
    </address_information>
</template_name>
"""
    xml = """<?xml version="1.0"?>
<address_information>
	<start_date>02-09-1998</start_date>
	<address_type>none</address_type>
	<address2>secret</address2>
	<zip_code>XXXXX-XXX</zip_code>
	<end_date>infinity</end_date>
	<random>NOOO</random>
</address_information>
"""

    root = ET.fromstring(xml)
    print([x.text for x in root])
    template = ET.fromstring(templ)
    template = [x for x in template]
    this = extract(template, root)
    print([x.text for x in this])
    pass


# todo: handle exception that will occur when trying to access a set of tags when xml actually have a value
# example: template has <abc><d></d><e></e></abc> but xml has <abc>10</abc>
def extract(template, xml):
    if xml.tag in [y.tag for y in template]:
        templ = [y for y in template if y.tag == xml.tag]
        templ_children = [x for x in templ[0]]  # take a deeper look here, can we really always access tepl[0]? I think so
        if templ_children == []:
            return xml
        else:
            new_el = ET.Element(xml.tag)
            template_children = [x for x in templ[0]]

            for xml_child in xml:
                sub_element = extract(template_children, xml_child)
                if sub_element is not None:
                    new_el.append(sub_element)
            return new_el
    else:
        return None  # tag is not in template





if __name__ == '__main__':
    main()
