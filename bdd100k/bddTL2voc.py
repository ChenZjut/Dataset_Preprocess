from cgi import print_arguments
import os
import os.path as osp

import json
import cv2

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

from PIL import Image

from tqdm import tqdm

DEBUG = False

BDD_FOLDER = "."

if DEBUG:
    XML_PATH = "./xml"
else:
    XML_PATH = BDD_FOLDER + "/BDDVOC/Annotations"


def bdd_to_voc(bdd_folder, xml_folder):
    image_path = bdd_folder + "/Images/100k/%s"
    label_path = bdd_folder + "/Labels/bdd100k_labels_images_%s.json"
    save_img_path = bdd_folder + "/BDDVOC/JPEGImages"

    classes = set()

    for trainval in ['train', 'val']:
        image_folder = image_path % trainval
        json_path = label_path % trainval
        xml_folder_ = osp.join(xml_folder, trainval)
        save_img_folder = osp.join(save_img_path, trainval)

        if not os.path.exists(xml_folder_):
            os.makedirs(xml_folder_)

        if not os.path.exists(save_img_folder):
            os.makedirs(save_img_folder)


        with open(json_path) as f:
            j = f.read()
        data = json.loads(j)
        for datum in tqdm(data):
            tmp_list = []
            annotation = Element('annotation')
            SubElement(annotation, 'folder').text ='VOC2007'
            SubElement(annotation, 'filename').text = datum['name']
            source = get_source()
            annotation.append(source)
            size = get_size(osp.join(image_folder, datum['name']))
            annotation.append(size)
            SubElement(annotation, 'segmented').text ='0'
            # additional information
            #for key, item in datum['attributes'].items():
            #    SubElement(annotation, key).text = item

            # bounding box
            for label in datum['labels']:
                if label['category'] != "traffic light":
                    continue
                else:
                    tmp_list.append(1)
                color = label['attributes']["trafficLightColor"]
                try:
                    box2d = label['box2d']
                except KeyError:
                    continue
                else:
                    bndbox = get_bbox(box2d)

                object_ = Element('object')
                if color == 'none':
                    color = 'unknown'
                #SubElement(object_, 'name').text = label['category']
                SubElement(object_, 'name').text = color
                SubElement(object_, 'pose').text = "Unspecified"
                SubElement(object_, 'truncated').text = '0'
                SubElement(object_, 'difficult').text = '0'
                #classes.add(label['category'])
                classes.add(color)

                object_.append(bndbox)
                annotation.append(object_)
            if len(tmp_list) == 0:
                continue
            

            xml_filename = osp.splitext(datum['name'])[0] + '.xml'
            image_filename = osp.join(image_folder, datum['name'])
            # print(image_filename)
            image = cv2.imread(image_filename, cv2.IMREAD_COLOR)
            cv2.imwrite(f"{save_img_folder}/{xml_filename.replace('xml', 'jpg')}", image)
            with open(osp.join(xml_folder_, xml_filename), 'w') as f:
                f.write(prettify(annotation))
    print(classes)

def get_source():
    source = Element('source')
    SubElement(source, 'database').text ='vocbdd'
    SubElement(source, 'annotation').text ='VOC2007'
    return source

def get_size(image_path):
    i = Image.open(image_path)
    sz = Element('size')
    SubElement(sz, 'width').text = str(i.width)
    SubElement(sz, 'height').text = str(i.height)
    SubElement(sz, 'depth').text = str(3)
    return sz


def get_bbox(box2d):
    bndbox = Element('bndbox')
    SubElement(bndbox, 'xmin').text = str(int(round(box2d['x1'])))
    SubElement(bndbox, 'ymin').text = str(int(round(box2d['y1'])))
    SubElement(bndbox, 'xmax').text = str(int(round(box2d['x2'])))
    SubElement(bndbox, 'ymax').text = str(int(round(box2d['y2'])))
    return bndbox


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


if __name__ == "__main__":
    bdd_to_voc(BDD_FOLDER, XML_PATH)

