import pandas as pd;
import os
import glob
import cv2

from tqdm import tqdm

show_info = False
total_images = 0
labels = {
    'go':0,
    'stop':1,
    'stopLeft':2,
    'goLeft':3,
    'warning':4,
    'warningLeft':5

}

root_folder_names = ['dayTrain', 'nightTrain']
root_folder_names_mapper = {
    'dayTrain':'dayClip',
    'nightTrain':'nightClip'
}

annotations_root = './Annotations/Annotations'
image_root = './'

def get_cords(tag, x_min, y_min, x_max, y_max):
    if tag in labels:
        if tag == 'go':
            label = labels['go']
        elif tag == 'stop':
            label = labels['stop']
        elif tag == 'stopLeft':
            label = labels['stopLeft']
        elif tag == 'goLeft':
            label = labels['goLeft']
        elif tag == 'warning':
            label = labels['warning']
        elif tag == 'warningLeft':
            label = labels['warningLeft']

        x_center = ((x_max + x_min) / 2) / 1280
        y_center = ((y_max + y_min) / 2) / 960
        w = (x_max - x_min) / 1280
        h = (y_max - y_min) / 960
    else:
        label = ''
        x_center = ''
        y_center = ''
        w = ''
        h = ''
    return label, x_center, y_center, w, h

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
        # print(df)
        image_paths = glob.glob(f"{image_root}/{root_folder_name}/{root_folder_name}/{mapped_clip}{i}/frames/*.jpg")
        # print(images_paths)
        image_paths.sort()

        total_images += len(image_paths)

        if show_info:
            print('NUMBER OF IMAGE AND UNIQUE CSV FILE NAMES MAY NOT MATCH')
            print('NOT A PROBLEM')
            print(f"Total objects in current CSV file: {len(df)}")
            print(f"Unique Filenames: {len(df['Filename'].unique())}")
            print(df.head())
            print(f"Total images in current folder: {len(image_paths)}")

        
        tags = df['Annotation tag'].values
        x_min = df['Upper left corner X'].values
        y_min = df['Upper left corner Y'].values
        x_max = df['Lower right corner X'].values
        y_max = df['Lower right corner Y'].values

        file_counter = 0
        for i, image_path in tqdm(enumerate(image_paths), total=len(image_paths)):
            # 把地址以'/'区分开。同时取最末尾，即图片的命名如xxx.jpg
            image_name = image_path.split(os.path.sep)[-1]
            # print(image_name)
            f = open(f"./labels/{image_name.split('.')[0]}.txt",'w')
            for j in range(len(df)):
                if file_counter < len(df):
                    file_name = df.loc[file_counter]['Filename'].split('/')[-1]
                    # print(file_name)
                    if file_name == image_name:
                        label, x, y, w, h = get_cords(tags[file_counter], x_min[file_counter], y_min[file_counter], x_max[file_counter], y_max[file_counter])
                        if type(label) == int:
                            f.writelines(f"{label} {x} {y} {w} {h}\n")
                        else:
                            f.writelines(f"")
                        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                        cv2.imwrite(f"./images/{image_name}", image)
                        file_counter += 1
                    if file_name != image_name:
                        break
            f.close()

print(f"Total images parsed through: {total_images}")