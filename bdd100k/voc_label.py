import os.path
import xml.etree.ElementTree as ET
import os
class_names = ['red', 'yellow', 'green', 'none']
 
xmlpath='/home/cyk/data_cyk/dataset/bdd100k_dataset/bdd100k/train/Annotations/'         #原xml路径
txtpath='/home/cyk/data_cyk/yolov5/data/traffic_light/labels/train/'     #转换后txt文件存放路径
if not os.path.exists(txtpath):
    os.mkdir(txtpath)
files = []
 
for root, dirs, files in os.walk(xmlpath):
    None

number = len(files)
print(number)
i = 0
while i < number:
 
    name = files[i][0:-4]
    xml_name = name + ".xml"
    txt_name = name + ".txt"
    xml_file_name = xmlpath + xml_name
    txt_file_name = txtpath + txt_name
 
    xml_file = open(xml_file_name,encoding='UTF-8')
    tree = ET.parse(xml_file)
    root = tree.getroot()
    filename = root.find('filename').text
 
    image_name = root.find('filename').text
    w = int(root.find('size').find('width').text)
    h = int(root.find('size').find('height').text)
 
    f_txt = open(txt_file_name, 'w+',encoding='UTF-8')
    content = ""
 
    first = True
 
    for obj in root.iter('object'):
 
        name = obj.find('name').text
        class_num = class_names.index(name)
 
        xmlbox = obj.find('bndbox')
 
        

        x1 = int(float(xmlbox.find('xmin').text))
        x2 = int(float(xmlbox.find('xmax').text))
        y1 = int(float(xmlbox.find('ymin').text))
        y2 = int(float(xmlbox.find('ymax').text))
 
        if first:
            content += str(class_num) + " " + \
                       str((x1 + x2) / 2 / w) + " " + str((y1 + y2) / 2 / h) + " " + \
                       str((x2 - x1) / w) + " " + str((y2 - y1) / h)
            first = False
        else:
            content += "\n" + \
                       str(class_num) + " " + \
                       str((x1 + x2) / 2 / w) + " " + str((y1 + y2) / 2 / h) + " " + \
                       str((x2 - x1) / w) + " " + str((y2 - y1) / h)
 
    #print(content)
    f_txt.write(content)
    f_txt.close()
    xml_file.close()
    i += 1
 
print("done!")
