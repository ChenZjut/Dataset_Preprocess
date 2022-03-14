'''
把yellow的xml和图片单独分出来

Example usage:
    python3 split_yellow.py
'''
import os
import shutil
import xml.etree.ElementTree as ET

def xyxyFromXML(path):
    # "./voc/1.xml"
    tree = ET.parse(path)
    # 文档根元素
    root = tree.getroot()

    ret = []  # shape:[num, 1]  1:[name]
    for element in root.findall('object'):
        labelname = element.find('name').text  # 访问Element文本
        # print(name)
        ret.append([labelname])
    return ret

def main():
    xmls_path = './BoschVOC/Annotations'
    image_path = './BoschVOC/JPEGImages'
    save_xml_path = './Bosch/Annotations'
    save_image_path = './Bosch/JPEGImages'

    labels = {
        'yellow'
    }

    for f in os.listdir(xmls_path):
        xyxys = xyxyFromXML(os.path.join(xmls_path, f))
        # print(f)
        # print(xyxys)
        for i in range(len(xyxys)):
            xyxy = xyxys[i]
            if xyxy[0] in labels:
                xml_name = os.path.join(xmls_path, f)
                shutil.copy(xml_name, save_xml_path)
                image_name = os.path.join(image_path, f.replace('xml', 'png'))
                shutil.copy(image_name, save_image_path)
if __name__ == "__main__":
    main()
