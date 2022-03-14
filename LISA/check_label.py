import os
import xml.dom.minidom
import shutil

removeXmlAndJson = False #是否移除无效标注文件

pathJPEG = "/home/cyk/data_cyk/dataset/Lisa_dataset/LISAVOC/JPEGImages/"
pathXml = "/home/cyk/data_cyk/dataset/Lisa_dataset/LISAVOC/Annotations/"
pathJson = "D:\\@CODE\\DataSet\\All_3DVision_Object\\json"
classname = ["green", "red", "left,red", "left,green", "yellow", "left,yellow"]

checkXml = True
checkJson = False

listJPEG = os.listdir(pathJPEG)
if checkXml:
    listXml = os.listdir(pathXml)
if checkJson:
    listJson = os.listdir(pathJson)
print("check xml and json files..")
for jpegName in listJPEG:
    xmlName = jpegName.split('.')[0]+'.xml'
    jsonName = jpegName.split('.')[0]+'.json'
    if checkXml:
        if not xmlName in listXml:
            print(xmlName + ' not found!')
            continue
        DOMTree = xml.dom.minidom.parse(os.path.join(pathXml,xmlName))
        collection = DOMTree.documentElement
        obj_list = collection.getElementsByTagName('object')

        for obj in obj_list:
            try:
                obj_name = obj.getElementsByTagName('name')[0].childNodes[0].data
                if not obj_name in  classname:
                    print("[%s] has a illegal object name [%s]" %(xmlName,obj_name))
            except:
                print('this file [%s] has a error' % (xmlName))

    if checkJson:
        if not jsonName in listJson:
            print(jsonName + ' not found!')
            continue
print("done!")

print("check jpeg files from xml..")
if checkXml:
    for xmlName in listXml:
        jpegName = xmlName.split('.')[0]+'.jpg'
        if not jpegName in listJPEG:
            print(jpegName + ' not found!')
            if removeXmlAndJson:
                print('delete file '+xmlName)
                os.remove(os.path.join(pathXml,xmlName))
print("done!")
print("check jpeg files from json..")
if checkJson:
    for jsonName in listJson:
        jpegName = jsonName.split('.')[0]+'.jpg'
        if not jpegName in listJPEG:
            print(jpegName + ' not found!')
            if removeXmlAndJson:
                print('delete file '+jsonName)
                os.remove(os.path.join(pathJson,jsonName))
print("done!")
