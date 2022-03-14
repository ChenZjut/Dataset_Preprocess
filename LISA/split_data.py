
import os
import random
import sys
import shutil
root_path = '/home/cyk/data_cyk/dataset/Lisa_dataset/'
#X%用来训练，1-X%用来测试
train_ratio = 1          
#训练中的Y%用来验证   
trainval_ratio = 0.1    

xml_path = os.path.join(root_path,'labels')
img_path = os.path.join(root_path,'images')

train_path = os.path.join(root_path,'train')
val_path = os.path.join(root_path,'val')
test_path = os.path.join(root_path,'test')

if not os.path.exists(train_path):
    os.mkdir(train_path)
    os.mkdir(os.path.join(train_path,'Annotations'))
    os.mkdir(os.path.join(train_path,'JPEGImages'))
if not os.path.exists(val_path):
    os.mkdir(val_path)
    os.mkdir(os.path.join(val_path,'Annotations'))
    os.mkdir(os.path.join(val_path,'JPEGImages'))
if not os.path.exists(test_path):
    os.mkdir(test_path)
    os.mkdir(os.path.join(test_path,'Annotations'))
    os.mkdir(os.path.join(test_path,'JPEGImages'))

imgsfile = os.listdir(img_path)
xmlsfile = os.listdir(xml_path)

datanumber = int(len(imgsfile))
datalist = range(datanumber)
trainlist = random.sample(datalist,int(datanumber*train_ratio))
vallist = random.sample(trainlist,int(datanumber*train_ratio*trainval_ratio))

for i in datalist:
    imgname = imgsfile[i]
    xmlname = imgname.split('.')[0]+'.txt'
    print(imgname)
    if i in vallist:
        shutil.move(os.path.join(img_path,imgname),os.path.join(val_path,'JPEGImages',imgname))
        shutil.move(os.path.join(xml_path,xmlname),os.path.join(val_path,'Annotations',xmlname))
    elif i in trainlist:
        shutil.move(os.path.join(img_path,imgname),os.path.join(train_path,'JPEGImages',imgname))
        shutil.move(os.path.join(xml_path,xmlname),os.path.join(train_path,'Annotations',xmlname))
    else:
        shutil.move(os.path.join(img_path,imgname),os.path.join(test_path,'JPEGImages',imgname))
        shutil.move(os.path.join(xml_path,xmlname),os.path.join(test_path,'xml',xmlname))
