import json
import os
import cv2


ep = 12

src = json.load(open('cascade_rcnn_x101_64x64/cascade_rcnn_r2_101_fpn_20e_coco_icip.bbox_sec_%s.json' %ep, 'r'))

count_id = 0

result = {
    "annotations":[]
}

for sr in src :
    label = {}
    label["id"] = count_id
    label["bbox"] = sr["bbox"]
    label["category_id"] = sr["category_id"]
    label["file_name"] = '%s.jpg' % sr["image_id"]

    count_id += count_id
    result["annotations"].append(label)

json.dump(result, open('./submit/submit%s.json' % ep, 'w'), indent=4)




