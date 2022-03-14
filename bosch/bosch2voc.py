'''
把我想要的label找出来,这里我只要'red','yellow','green',转成VOC的xml

Example usage:
    python3 bosch2voc.py
'''
import os
import sys
import cv2
import yaml
from lxml import etree
import os.path
import xml.etree.cElementTree as ET

save_path = '../BoschVOC/'

if not os.path.exists(save_path + 'Annotations'):
    os.makedirs(save_path + 'Annotations')
if not os.path.exists(save_path + 'JPEGImages/'):
    os.makedirs(save_path + 'JPEGImages')


def write_xml(savedir, image, imgWidth, imgHeight,
              depth=3, pose="Unspecified"):

    boxes = image['boxes']
    impath = image['path']
    imagename = impath.split('/')[-1]
    currentfolder = savedir.split("\\")[-1]
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, 'folder').text = str(currentfolder)
    ET.SubElement(annotation, 'filename').text = str(imagename)
    imagename = imagename.split('.')[0]
    size = ET.SubElement(annotation, 'size')
    ET.SubElement(size, 'width').text = str(imgWidth)
    ET.SubElement(size, 'height').text = str(imgHeight)
    ET.SubElement(size, 'depth').text = str(depth)
    ET.SubElement(annotation, 'segmented').text = '0'

    flag = 0
    for box in boxes:
         if box['label'] == 'Red' or box['label'] == 'Yellow' or box['label'] == 'Green':
             if box['label'] == 'Red':
                box['label'] = 'red'
             if box['label'] == 'Yellow':
                box['label'] = 'yellow'
             if box['label'] == 'Green':
                box['label'] = 'green'

             obj = ET.SubElement(annotation, 'object')
             ET.SubElement(obj, 'name').text = str(box['label'])
             ET.SubElement(obj, 'pose').text = str(pose)
             ET.SubElement(obj, 'occluded').text = str(box['occluded'])
             ET.SubElement(obj, 'difficult').text = '0'
             
             bbox = ET.SubElement(obj, 'bndbox')
             ET.SubElement(bbox, 'xmin').text = str(int(box['x_min']))
             ET.SubElement(bbox, 'ymin').text = str(int(box['y_min']))
             ET.SubElement(bbox, 'xmax').text = str(int(box['x_max']))
             ET.SubElement(bbox, 'ymax').text = str(int(box['y_max']))

             flag = 1
        

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root, pretty_print=True)
    if flag == 1:
        save_path = os.path.join(savedir, imagename + ".xml")
        image = cv2.imread(impath, cv2.IMREAD_COLOR)
        cv2.imwrite(f"../BoschVOC/JPEGImages/{imagename}.png", image)
        with open(save_path, 'wb') as temp_xml:
            temp_xml.write(xml_str)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(-1)
    yaml_path = sys.argv[1]
    out_dir = sys.argv[2]
    images = yaml.load(open(yaml_path, 'rb').read())

    for image in images:
        write_xml(out_dir, image, 1280, 720, depth=3, pose="Unspecified")
