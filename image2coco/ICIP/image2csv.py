# author Kequan chan
# date : 2022.3.12
import os, csv
import random
import json

# splite dataset to train and val

train_ratio = 0.8
val_ratio = 0.2

random.seed(0)

#find box in lable
with open('./labels.json') as f:
    lable_json = json.load(f)
    images_info = lable_json['images']
    annotation_info = lable_json['annotations']



f_train = open('/media/snnu/dataset/chenkequan/Chula-ParasiteEgg-11/test/train.csv', 'w', newline='')

f_val = open('/media/snnu/dataset/chenkequan/Chula-ParasiteEgg-11/test/val.csv', 'w', newline='')

images = os.listdir('/media/snnu/dataset/chenkequan/Chula-ParasiteEgg-11/Chula-ParasiteEgg-11/data/')

images_index = [i for i in range(len(images))]

random.shuffle(images_index)

csv_writer_train = csv.writer(f_train)
csv_writer_val = csv.writer(f_val)

# split train
images_index_train = images_index[0:int(train_ratio * len(images))]
images_index_val = images_index[int(train_ratio * len(images)):-1]


def data2csv(csv_writer, images_index,images):
    for index in images_index:
        # print(i)
        name = os.path.splitext(images[index])[0]
        csv_writer.writerow([("'" + name), 1, 1, 1, 1, "Trichuris trichiura"])
        print(name)


data2csv(csv_writer_train, images_index_train,images)

data2csv(csv_writer_val, images_index_val,images)

f_train.close()
f_val.close()
