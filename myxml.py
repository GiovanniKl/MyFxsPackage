"""
Small module for converting XML files to Python datastructures
(e.g. dicts) and vice versa.

Created by Jan Klíma on 2024/07/09.
Updated on 2024/07/09.
"""

from collections import defaultdict
from xml.etree import ElementTree as ET
from pprint import pprint


def etree2dict(t):
    """Convert an xml.etree.ElementTree to dict.

    Based on the @K3--rnc 's answer at:
    https://stackoverflow.com/a/10077069/21824242

    Usually takes in the root of the etree (see the example).
    
    """
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree2dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def dict2etree(d):
    """Convert an XML in dict representation (as returned by
    `etree2xml()`) to an etree representation.
    To get the etree as an XML string, use `ET.tostring(etree)`
    (this usually does not include escape chars like linefeeds and
    tabs, see the example).

    Based on the @K3--rnc 's answer at:
    https://stackoverflow.com/a/10077069/21824242

    The dict structure should comply with the XML-to-JSON structure
    specified at:
    https://www.xml.com/pub/a/2006/05/31/converting-between-xml-and-json.html
    
    """
    def _to_etree(d, root):
        if not d:
            pass
        elif isinstance(d, str):
            root.text = d
        elif isinstance(d, dict):
            for k,v in d.items():
                assert isinstance(k, str)
                if k.startswith('#'):
                    assert k == '#text' and isinstance(v, str)
                    root.text = v
                elif k.startswith('@'):
                    assert isinstance(v, str)
                    root.set(k[1:], v)
                elif isinstance(v, list):
                    for e in v:
                        _to_etree(e, ET.SubElement(root, k))
                else:
                    _to_etree(v, ET.SubElement(root, k))
        else:
            raise TypeError('invalid type: ' + str(type(d)))
    assert isinstance(d, dict) and len(d) == 1
    tag, body = next(iter(d.items()))
    node = ET.Element(tag)
    _to_etree(body, node)
    # return ET.tostring(node)
    return node


def example():
    """Example of usage."""
    xmlstr = '''
<root>
  <e />
  <e>text</e>
  <e name="value" />
  <e name="value">text</e>
  <e> <a>text</a> <b>text</b> </e>
  <e> <a>text</a> <a>text</a> </e>
  <e> text <a>text</a> </e>
</root>
    '''
    print("\n*** original XML string ***")
    pprint(xmlstr)

    e = ET.XML(xmlstr)
    print("\n*** etree as a string ***")
    pprint(ET.tostring(e).decode("utf-8"))

    d = etree2dict(e)
    print("\n*** dict made from the etree ***")
    pprint(d)
    
    ee = dict2etree(d)
    print("\n*** back-converted XML string (from dict to etree) ***")
    pprint(ET.tostring(ee).decode("utf-8"))


# for simpler usage
def xmlfile2dict(source):
    """Reads an XML file and converts it to a JSON-like dict.
    *source* - path to the XML file to read.
    """
    return etree2dict(ET.parse(source).getroot())


def save_xml_dict(d, target):
    """Saves the XML dict `d` to an XML file `target`."""
    e = dict2etree(d)
    e.write(target)


if __name__ == "__main__":
    example()
