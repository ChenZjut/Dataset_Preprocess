'''
统计转化成voc的格式后label的数量

Example usage:
    python3 counter_labels.py
'''
import xml.etree.ElementTree as ET
import os

def xyxyFromXML(path):
    # "./voc/1.xml"
    tree = ET.parse(path)
    # 文档根元素
    root = tree.getroot()

    ret = []  # shape:[num, 5]  5:[xmin, ymin, xmax, ymax, name]
    for element in root.findall('object'):
        labelname = element.find('name').text  # 访问Element文本
        # print(name)
        for xywh in element.findall('bndbox'):
            xmin = xywh.find('xmin').text
            ymin = xywh.find('ymin').text
            xmax = xywh.find('xmax').text
            ymax = xywh.find('ymax').text
            ret.append([xmin, ymin, xmax, ymax, labelname])
    return ret

def main():
    save_xmls_path = './Bosch/Annotations/'

    count = {}

    for f in os.listdir(save_xmls_path):
        xyxys = xyxyFromXML(os.path.join(save_xmls_path, f))
        # print(f)
        # print(xyxys)
        for i in range(len(xyxys)):
            xyxy = xyxys[i]
            if xyxy[4] in count:
                count[xyxy[4]] += 1
            else:
                count[xyxy[4]] = 1

    for c in count.items():
            print("{}: {}".format(c[0], c[1]))

if __name__ == "__main__":
    main()
