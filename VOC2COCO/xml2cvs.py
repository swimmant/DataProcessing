"""
created by Kequan Chan
2021, 9.14
"""
import csv
import os
import xml.dom.minidom as md
from tqdm import tqdm



def xml2cvs(Name):
    # xmls = '../testXml/'
    xmls = '../../helmet/VOCdevkit/VOC2007/Annotations/'
    res = csv.writer(open(f'../{Name}.csv', 'w', newline=''))
    xml_name_list_file = open(f'../../helmet/VOCdevkit/VOC2007/ImageSets/Main/{Name}.txt')

    xml_name_list = xml_name_list_file.readlines()
    for index , xml in zip([i for i in range(len(xml_name_list))],xml_name_list):
        xml_name_list[index] = xml.split('\n')[0]+'.xml'

    for xml in tqdm(xml_name_list):
        DOMTree = md.parse(xmls + xml)
        collection = DOMTree.documentElement

        # 获取标签所有类别
        # categories = collection.getElementsByTagName('name')
        # boxes = collection.getElementsByTagName('point')  # Change this field to VOC tag
        # 获得当前单一图片中所有的框xml对象
        boxes = collection.getElementsByTagName('object')  # Change this field to VOC tag

        category_list = []
        box_list = {}

        # 获得当前单一图片中所有的框
        for box in boxes:
            # xmin = box.getElementsByTagName('xmin')[0].childNodes[0].data
            name = box.getElementsByTagName('name')[0].childNodes[0].data
            each = [box.getElementsByTagName(e)[0].childNodes[0].data for e in ['xmin', 'ymin', 'xmax', 'ymax']]
            if name not in category_list:
                category_list.append(name)
                box_list.setdefault(name, [])
            box_list[f"{name}"].append(each)

        # 一次性写
        for category in category_list:
            # modify this if is voc format
            for box in box_list[f"{category}"]:
                # csv文件打开数字开头会科学计算法，不影响后续读取
                res.writerow([xml.split('.')[0], box[0], box[1], box[2], box[3], category])


#按标准数据集训练生成train, trainval ,test ,val
#读取VOC数据集中txt文件依次索引
if __name__ == '__main__':
    name_List = ['test', 'train', 'trainval', 'val']
    for name in name_List:
        xml2cvs(name)


#或者随机划分xmlsList




