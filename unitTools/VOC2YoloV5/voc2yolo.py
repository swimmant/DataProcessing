#----------------------------------------------------------------------#
#   验证集的划分在train.py代码里面进行
#   test.txt和val.txt里面没有内容是正常的。训练不会使用到。
#----------------------------------------------------------------------#
'''
#--------------------------------注意----------------------------------#
如果在pycharm中运行时提示：
FileNotFoundError: [WinError 3] 系统找不到指定的路径。: './VOCdevkit/VOC2007/Annotationstxt'
这是pycharm运行目录的问题，最简单的方法是将该文件复制到根目录后运行。
可以查询一下相对目录和根目录的概念。在VSCODE中没有这个问题。
#--------------------------------注意----------------------------------#
'''
import os
import random 
random.seed(0)

xmlfilepath=r'./VOCdevkit/VOC2007/Annotations/'
saveBasePath=r"./VOCdevkit/VOC2007/ImageSets/Main/"
 
#----------------------------------------------------------------------#
#   想要增加测试集修改trainval_percent
#   train_percent不需要修改
#----------------------------------------------------------------------#
trainval_percent=1
train_percent= 1
test_percent = 0

temp_xml = os.listdir(xmlfilepath)
total_xml = []
for xml in temp_xml:
    if xml.endswith(".xml"):
        total_xml.append(xml)

num=len(total_xml)  
list=range(num)

tv=int(num*trainval_percent)  
tr=int(tv*train_percent)
te = int(num*test_percent)

trainval= random.sample(list,tv)  
train=random.sample(trainval,tr)
test = random.sample(list,te)
 
print("train and val size",tv)
print("train size",tr)
print("test size",te)

#训练验证集
ftrainval = open(os.path.join(saveBasePath,'trainval.txt'), 'w')
#测试集
ftest = open(os.path.join(saveBasePath,'test.txt'), 'w')
#训练集
ftrain = open(os.path.join(saveBasePath,'train.txt'), 'w')
#验证集
fval = open(os.path.join(saveBasePath,'val.txt'), 'w')  
 
for i  in list:  
    name=total_xml[i][:-4]+'\n'  
    if i in trainval:  
        ftrainval.write(name)  
        if i in train:  
            ftrain.write(name)  
        else:  
            fval.write(name)  
    else:  
        ftest.write(name)  
  
ftrainval.close()  
ftrain.close()  
fval.close()  
ftest .close()
