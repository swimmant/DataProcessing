import json

import os

rootPath = "../dataSet/train/annotations/"
f = json.load(open((rootPath+'trainval.json'), 'r'))
if not os.path.exists('../dataSet/train/Annotation/'):
    os.makedirs('../dataSet/train/Annotation/')

for i in f['images']:
    with open('../dataSet/train/Annotation/'+str(i['id'])+'.txt', 'w') as lable:
        for j in f['annotations']:
            if j['image_id'] == i['id']:
                lable.write(
                    str(j['category_id']-1) + ' ' + str((j['bbox'][0]+0.5*j['bbox'][2])/i['width']) + ' ' + str((j['bbox'][1]+0.5*j['bbox'][3])/i['height']) + ' ' + str(j['bbox'][2]/i['width']) + ' ' + str(j['bbox'][3]/i['height']) + '\n'
                    )