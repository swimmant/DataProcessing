# --Author : Kequan Chan
# --Date: 2022年03月23日

import os
import random
import shutil
import xml.etree.ElementTree as ET

random.seed(0)


def xml_reader(filename):
    """ Parse a PASCAL VOC xml file """
    tree = ET.parse(filename)
    size = tree.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(float(bbox.find('xmin').text)),
                              int(float(bbox.find('ymin').text)),
                              int(float(bbox.find('xmax').text)),
                              int(float(bbox.find('ymax').text))]
        objects.append(obj_struct)
    return width, height, objects


# 单张图片xml文件转化和imageCopy
def voc2yolo5(source_dir, target_dir, img_name, classes_dict, place):
    img_path = f"{source_dir}JPEGImages/{img_name}"
    xml_path = img_path.replace("JPEGImages", "Annotations").replace(".jpg", ".xml")
    width, height, objects = xml_reader(xml_path)

    lines = []

    for obj in objects:
        x, y, x2, y2 = obj['bbox']
        class_name = obj['name']
        label = classes_dict[class_name]
        cx = (x2 + x) * 0.5 / width
        cy = (y2 + y) * 0.5 / height
        w = (x2 - x) * 1. / width
        h = (y2 - y) * 1. / height
        line = "%d %.6f %.6f %.6f %.6f\n" % (int(label) - 1, cx, cy, w, h)
        lines.append(line)

    img_path_copy = img_path.replace(source_dir, target_dir).replace('JPEGImages', 'images').split('/')
    img_path_copy.insert(-1, place)
    img_path_copy = '/'.join(img_path_copy)
    print(img_path)
    print(img_path_copy)
    txt_path = xml_path.replace(source_dir, target_dir).replace('Annotations', 'labels').split('/')
    txt_path.insert(-1, place)
    txt_path = '/'.join(txt_path).replace(".xml", ".txt")
    print(xml_path)
    print(txt_path)
    shutil.copy(img_path, img_path_copy)
    with open(txt_path, "w") as f:
        f.writelines(lines)


def divide(source_dir, targetPath, classes_dict):
    # --获取所有VOC标签的名称

    # saveBasePath yolov5数据集存放的第一层 ./helmet/
    # 创建yolo5文件夹
    for firstLayer in ['labels', 'images']:
        if not os.path.exists(targetPath + f'{firstLayer}'):
            os.makedirs(targetPath + f'{firstLayer}')
        for secondLayer in ['train', 'test', 'val']:
            if not os.path.exists(targetPath + f'{firstLayer}' + f'/{secondLayer}'):
                os.makedirs(targetPath + f'{firstLayer}' + f'/{secondLayer}')

    # 数据集划分完成，文件夹创建完成，开始copyImages,写入label
    train_xml = []
    val_xml = []
    test_xml = []
    for cls in ['train', 'test', 'val']:
        indexFile = open(source_dir + 'ImageSets/Main/' + f'{cls}.txt')
        indexList = indexFile.readlines()
        for index in indexList:
            if cls == 'train':
                train_xml.append(index.split('\n')[0] + '.xml')
            if cls == 'val':
                val_xml.append(index.split('\n')[0] + '.xml')
            if cls == 'test':
                test_xml.append(index.split('\n')[0] + '.xml')
    for file in train_xml:
        img_name = str(file.split('.')[0]) + '.jpg'
        voc2yolo5(source_dir, targetPath, img_name, classes_dict, 'train')
    for file in val_xml:
        img_name = str(file.split('.')[0]) + '.jpg'
        voc2yolo5(source_dir, targetPath, img_name, classes_dict, 'val')
    for file in test_xml:
        img_name = str(file.split('.')[0]) + '.jpg'
        voc2yolo5(source_dir, targetPath, img_name, classes_dict, 'test')


if __name__ == '__main__':
    sourcePath = r'/Users/kequan/Desktop/kequan/小型项目/yolov5训练/traffic_signs/VOCdevkit/VOC2007/'
    targetPath = r"/Users/kequan/Desktop/kequan/小型项目/yolov5训练/yolov4DataSet/"

    classes_dict = {'straight': 1, 'nohonk': 2,'stop':3,'left':4,'right':5,'crosswalk':6}
    # --yolov5划分数据集
    # 数据集已近划分完成
    divide(sourcePath, targetPath, classes_dict)
