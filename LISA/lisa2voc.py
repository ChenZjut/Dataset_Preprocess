'''
Change LISA to Pascal VOC

Example usage:
    python3 lisa2voc.py
'''
import os
import cv2
import glob
import pandas as pd
from PIL import Image

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom

from tqdm import tqdm

save_path = './LISAVOC/'

if not os.path.exists(save_path + 'Annotations'):
    os.makedirs(save_path + 'Annotations')
if not os.path.exists(save_path + 'JPEGImages/'):
    os.makedirs(save_path + 'JPEGImages')

root_folder_names = ['dayTrain', 'nightTrain']
root_folder_names_mapper = {
    'dayTrain':'dayClip',
    'nightTrain':'nightClip'
}

annotations_root = './Annotations/Annotations'
image_root = './'
total_images = 0

def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

for root_folder_name in root_folder_names:
    folder_names = os.listdir(f"{annotations_root}/{root_folder_name}")
    # print(folder_names)
    num_folders = len(folder_names)
    # print(num_folders)
    mapped_clip = root_folder_names_mapper[root_folder_name]
    # print(mapped_clip)

    for i in range(1, num_folders+1):
        print("##### New csv and images #####")
        df = pd.read_csv(f"{annotations_root}/{root_folder_name}/{mapped_clip}{i}/frameAnnotationsBOX.csv", ';')
        print(df)
        image_paths = glob.glob(f"{image_root}/{root_folder_name}/{root_folder_name}/{mapped_clip}{i}/frames/*.jpg")
        image_paths.sort()

        total_images += len(image_paths)

        tags = df['Annotation tag'].values
        x_min = df['Upper left corner X'].values
        y_min = df['Upper left corner Y'].values
        x_max = df['Lower right corner X'].values
        y_max = df['Lower right corner Y'].values

        file_counter = 0
        for i, image_path in tqdm(enumerate(image_paths), total=len(image_paths)):
            image_name = image_path.split(os.path.sep)[-1]
            annotation = Element('annotation') 
            SubElement(annotation, 'folder').text = 'VOC2007'
            SubElement(annotation, 'filename').text = image_name
            source = Element('source')
            SubElement(source, 'database').text = 'LISAtoVOC'
            SubElement(source, 'annotation').text = 'VOC2007'
            annotation.append(source)
            size = Element('size')
            SubElement(size, 'width').text = str(1280)
            SubElement(size, 'height').text = str(960)
            SubElement(size, 'depth').text = str(3)
            annotation.append(size)
            SubElement(annotation, 'segmented').text ='0'

            for j in range(len(df)):
                
                if file_counter < len(df):
                    file_name = df.loc[file_counter]['Filename'].split('/')[-1]
                    
                    # csv里面可能有多条label数据指向同一张图的，所以要判断一下是不是同一张图里面的label，在VOC里面只要增加一个Object就可以
                    '''
                    <object>
                        <name>green</name>
                        <pose>Unspecified</pose>
                        <truncated>0</truncated>
                        <difficult>0</difficult>
                        <bndbox>
                            <xmin>698</xmin>
                            <ymin>333</ymin>
                            <xmax>710</xmax>
                            <ymax>358</ymax>
                        </bndbox>
                    </object>                  
                    '''
                    if file_name == image_name:
                        bndbox = Element('bndbox')
                        SubElement(bndbox, 'xmin').text = str(x_min[file_counter])
                        SubElement(bndbox, 'ymin').text = str(y_min[file_counter])
                        SubElement(bndbox, 'xmax').text = str(x_max[file_counter])
                        SubElement(bndbox, 'ymax').text = str(y_max[file_counter])
                        object_ = Element('object')

                        # 原数据集里面是go,stop等，换成green,red等
                        if tags[file_counter] == 'go' or tags[file_counter] == 'stop' or tags[file_counter] == 'warning':
                            if tags[file_counter] == 'go':
                                label = 'green'
                            elif tags[file_counter] == 'stop':
                                label = 'red'
                            elif tags[file_counter] == 'warning':
                                label = 'yellow'
                            SubElement(object_, 'name').text = label
                            SubElement(object_, 'pose').text = "Unspecified"
                            SubElement(object_, 'truncated').text = '0'
                            SubElement(object_, 'difficult').text = '0'
                            object_.append(bndbox)
                            annotation.append(object_)
                         
                        
                            f = open(f"LISAVOC/Annotations/{image_name.split('.')[0]}.xml",'w')
                            f.write(prettify(annotation))
                            f.close()

                            image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                            cv2.imwrite(f"LISAVOC/JPEGImages/{image_name}", image)
                        file_counter += 1

                    if file_name != image_name:
                        break
print(f"Total images parsed through: {total_images}")