from src import XMLAnalyzerException
import lxml.etree as ET
from src.XMLUtil import *
from src.xml_decoder import html_deentitize

def apply_all(xml, pre_processes):
    for pre_process in pre_processes:
        xml = apply(xml, pre_process)
    return xml


def apply(xml, pre_process):

    if pre_process.tag == 'html_deentitize':
        sso = xml.find('.//{*}' + pre_process.text)
        content = ET.fromstring(re.sub('<\?.*?\?>', '', html_deentitize(sso.text)))
        sso.append(content)
        return xml
    else:
        raise XMLAnalyzerException.InvalidPreProcessTag(pre_process.tag)

