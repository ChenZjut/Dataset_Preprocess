'''
Quick sample script that displays the traffic light labels within
the given images.

Example usage:
    python3 show_labels.py
'''
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import os.path as osp
import os
import cv2
import random



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


def drawImg(img, xyxys):
    imgRect = img.copy()

    _colors = ((0, 255, 0),
               (255, 0, 255),
               (255, 69, 0),
               (0, 250, 154),
               (255, 165, 0),
               (205, 133, 63))

    for i in range(len(xyxys)):
        xyxy = xyxys[i]
        xmin = int(xyxy[0])
        ymin = int(xyxy[1])
        xmax = int(xyxy[2])
        ymax = int(xyxy[3])
        labelname = str(xyxy[4])

        color = _colors[i % 6]
        imgRect = cv2.rectangle(imgRect, (xmin, ymin), (xmax, ymax), color, 2)
        imgRect = cv2.putText(imgRect, labelname, (xmin, ymin-5), cv2.FONT_HERSHEY_SIMPLEX, 1.4, color, 2)

    return imgRect



def showImg(imgPath, xyxys, showSrc=True, showDst=True, resize=None):
    img = cv2.imread(imgPath)
    imgRect = drawImg(img, xyxys)

    if resize != None:
        _shape = (int(img.shape[1]*resize), int(img.shape[0]*resize))
        img = cv2.resize(img, _shape)
        imgRect = cv2.resize(imgRect, _shape)

    if showSrc:
        cv2.imshow('src', img)
    if showDst:
        cv2.imshow('imgRect', imgRect)

    cv2.waitKey(1000)



def main():
    # 要显示的数量
    # {num}.jpg 根据实际情况要修改
    save_imgs_path = '../BoschVOC/JPEGImages/'
    save_xmls_path = '../BoschVOC/Annotations/'

    showNum = 300
    img_name_list = os.listdir(save_imgs_path)

    for i in range(showNum):
        name = img_name_list[i].split('.')[0]

        imgPath = osp.join(save_imgs_path, name + '.png')
        xmlPath = osp.join(save_xmls_path, name + '.xml')

        # [num, 5]
        xyxys = xyxyFromXML(xmlPath)
        showImg(imgPath, xyxys, showSrc=True, showDst=True, resize=0.5)


if __name__ == "__main__":
    main()
