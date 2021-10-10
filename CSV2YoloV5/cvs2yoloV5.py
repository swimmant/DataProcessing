##------------
# Author: Chen Kequan
# Date : 2021年10月10日
##------------

import csv
import os
import pandas as pd
import cv2


#为了后续程序的通用性和可移植性，以固定函数格式输入

#获取唯一类别信息字典
def DataFormClass(clsList):
    tempDict  = {}
    for index , cls in enumerate(clsList):
        tempDict.update({f"{cls}":index})
    return tempDict

#整合类别编号信息
def addClassId(csvFile,clsDict):
    def setCategory(c):
        if c["class_name"] == 'fruit_woodiness':
            return 0
        elif c['class_name'] == 'fruit_brownspot':
            return 1
        elif c['class_name'] == 'fruit_healthy':
            return 2
        else:
            return -1

    csvFile['class_id'] = csvFile.apply(setCategory, axis=1)
    # print(clsDict[f'{csvFile.class_name}'.split("\\")[0]])
    # csvFile["class_id"] = clsDict["fruit_woodiness"]
    return csvFile
#整合图片大小信息
def addImagesSize(csvFile):
    # 整合图片size
    def setImageSize(row):
        # 读取图片
        # img = cv2.imread(f"{row.image_path}")     #使用cv2读取图片，获取图片高，宽
        #     print(img.shape)
        # hig, wid, _ = img.shape
        row['img_hig'] = 512          #这里全部为512
        row['img_wid'] = 512
        return row
    csvFile = csvFile.apply(setImageSize, axis=1)
    return csvFile

#截取必要信息的DataForm
def DataFormSplit(csvFile):
    # 将box按比例压缩
    csvFile['box_xmin'] = csvFile.apply(lambda row: (row.xmin) / row.img_wid, axis=1)
    csvFile['box_ymin'] = csvFile.apply(lambda row: (row.ymin) / row.img_hig, axis=1)
    csvFile['box_xmax'] = csvFile.apply(lambda row: (row.xmin + row.width) / row.img_wid, axis=1)
    csvFile['box_ymax'] = csvFile.apply(lambda row: (row.ymin + row.height) / row.img_hig, axis=1)

    csvFile['box_xmid'] = csvFile.apply(lambda row: (row.box_xmin + row.box_xmax) / 2, axis=1)
    csvFile['box_ymid'] = csvFile.apply(lambda row: (row.box_ymin + row.box_ymax) / 2, axis=1)

    csvFile['w'] = csvFile.apply(lambda row: (row.box_xmax - row.box_xmin), axis=1)
    csvFile['h'] = csvFile.apply(lambda row: (row.box_ymax - row.box_ymin), axis=1)

    keyFeaturn = ['Image_ID','class_id','box_xmid','box_ymid','w','h']
    return  csvFile[keyFeaturn]

###yolov5标签格式说明: 类别，目标中心点比例(x,y)，目标框的宽高的比例 和图片size比

#处理列表写入label文件
def List2TxtFile(keyList):
    for eachFile in keyList:
        line = "%d %.6f %.6f %.6f %.6f\n" % (eachFile[1], eachFile[2], eachFile[3], eachFile[4], eachFile[5])
        with open(f'./labels/train/{eachFile[0]}.txt','a') as labelTxt:
            labelTxt.writelines(line)


if __name__ == "__main__":
    #csv文件存放图片路径和相关bbox信息
    train_csv = "Train.csv"

    #创建存放的文件夹
    os.makedirs('./labels/train', exist_ok=True)



    csvFile = pd.read_csv(train_csv)
    print(csvFile.head())
    cls = list(csvFile["class"].unique())
    #生成字典
    clsDict = DataFormClass(cls)
    print(clsDict)

    #修改标题名
    csvFile = csvFile.rename(columns={"class":"class_name"})
    csvFile = addClassId(csvFile,clsDict)
    print(csvFile.head())
    csvFile = addImagesSize(csvFile)
    print(csvFile.head())
    #整理关键信息DataForm
    #关键信息包含： image_name ,cls_id ,xmin,ymin,xmax,ymax
    KeyDataForm = DataFormSplit(csvFile)
    print(KeyDataForm.head())
    #写入txt文件
    KeyList = KeyDataForm.values
    print(KeyList)
    List2TxtFile(KeyList)



