### Author: KequanChen
### Data: 2021年11月11日


# 创建ImageNet数据集格式，并创建标签。
from glob import  glob
import os
import shutil
from PIL import Image
import random

#函数功能：传入层级 图片路径字典，根目录，目标文件夹
def Image2File(imageNet,target_dir,cls_labelList):

    for d in imageNet:
        #对train，val，test写标签
        lines = []
        for cls in imageNet[f'{d}']:
            os.makedirs(target_dir+d+'/'+cls,exist_ok=True)
            img_list = imageNet[f'{d}'][f'{cls}']
            for img in img_list:
                #将图片copy到类别文件夹
                img_name = img.split('\\')[-1]
                target_img_path = target_dir+d+'/'+cls+'/'+ img_name
                shutil.copy(img,target_img_path)
                print(f'当前在{d}中{cls},copy{img}到{target_img_path}')
                #写入标签
                cls_index = cls_labelList.index(f'{cls}')
                label_line = f'{img_name} {cls_index}'
                lines.append(label_line + '\n')

            os.makedirs(f'{target_dir}meta', exist_ok=True)
            txt_path = target_dir + 'meta' + '/' + d + '.txt'
            with open(txt_path, "w") as f:
                f.writelines(lines)

def data2ImageNet():
    # 读取当前数据，整理成统一列表， 训练集，验证集，测试集 列表
    cls2label = ['cat', 'dog']
    cls_dir_list = ['cats', 'dogs']
    root = 'F:/ChromeDown/archive/dataset/'
    # root = 'data/cats_dogs/'
    data_dir_list = ['training_set','test_set']

    # imageNet 划分文件列表
    imageNet = {'train': {}, 'val': {}, 'test': {}}

    # 按类别读取所有的图片路径，后续还需要shuffle
    All_data = {}
    for clsLbael in cls2label:
        imageNet['train'].update({f'{clsLbael}': []})
        imageNet['val'].update({f'{clsLbael}': []})
        imageNet['test'].update({f'{clsLbael}': []})
        All_data.update({f'{clsLbael}': []})


    for dataDir in data_dir_list:
        for cls in cls_dir_list:
            #读取文件夹下某个类别
            img_dir =f'{root}{dataDir}/{cls}/'
            img_list = glob(img_dir+'*.jpg')
            #判断是某一类的图片
            for clsLbael in cls2label:
                    if clsLbael in cls:
                        #和全部数据路径取并集,并打乱
                        All_data[f'{clsLbael}'] =list(set(All_data[f'{clsLbael}']).union(set(img_list)))
                        random.shuffle(All_data[f'{clsLbael}'])

    print(len(All_data['dog']))
    print(len(All_data['cat']))

    #按类别比例划分数据集， 分为 train:0.6，val:0.2 ，test:0.2
    train = 0.6
    val = 0.2
    test = 0.2
    #获得截取各类数据下标并分配给标准格式
    for cls in All_data:
        clsList = All_data[f'{cls}']
        imageNet['train'][f'{cls}'] = clsList[0:int(train*len(clsList))]
        imageNet['val'][f'{cls}'] = clsList[int(train*len(clsList)):int((train+val)*len(clsList))]
        imageNet['test'][f'{cls}'] = clsList[int((train+val)*len(clsList)):]
        print(len(imageNet['train'][f'{cls}']))
        print(len(imageNet['val'][f'{cls}']))
        print(len(imageNet['test'][f'{cls}']))
        print(len(imageNet['test'][f'{cls}'])+len(imageNet['val'][f'{cls}'])+len(imageNet['train'][f'{cls}']))


    # 创建ImageNet数据集 文件夹格式
    target_dir = './imagenet/'

    Image2File(imageNet,target_dir,cls2label)
    #


data2ImageNet()
# Image.open('data/cats_dogs/test_set/dogs/dog.4009.jpg')