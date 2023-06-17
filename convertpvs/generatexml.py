import xml.etree.ElementTree
import logging
import xmltodict, json

logger = logging.getLogger('convertpvs')

def generate_xml(xml_file_path, json_file_path):
    try:
        sample = '<sample>sampledata</sample>'

        # with open(xml_file_path, 'r') as xml_file:
        #     xml_data = xml_file.read()
        #     xml_file .close()

        et = xml.etree.ElementTree.parse(xml_file_path)

        # Append new tag: <a x='1' y='abc'>body text</a>
        new_tag = xml.etree.ElementTree.SubElement(et.getroot(), 'a')
        new_tag.text = 'body text'
        new_tag.attrib['x'] = '1'  # must be str; cannot be an int
        new_tag.attrib['y'] = 'abc'

        # Write back to file
        # et.write('file.xml')
        et.write(json_file_path)
        # Convert the XML data to a dictionary
        # xml_dict = xmltodict.parse(xml_data)
        #
        # # Write the dictionary as JSON to the file
        # with open(json_file_path, 'w') as json_file:
        #     json.dump(xml_dict, json_file)
        #     json_file.close()


        return True

    except Exception as e:
        logger.error(f"{xml_file_path} {e}")
        return False

