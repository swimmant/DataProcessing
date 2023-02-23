import os
import glob
import cv2
import json


def cocoAndyoloChangeScale(sign_list,root_path,result_path):
    json_dir = os.path.join(root_path,"annotations")
    for sign in sign_list:
        json_path = os.path.join(json_dir,"instances_{}.json".format(sign))
        print(json_path)
        # 读取数据
        f = json.load(open(json_path, 'r'))
        # YOLO结果存放路径
        textDir_rs = os.path.join(result_path, 'Annotation/{}/'.format(sign))
        os.makedirs(textDir_rs, exist_ok=True)
        # coco结果存放路径
        json_dir_rs = os.path.join(result_path, 'annotations/')
        os.makedirs(json_dir_rs, exist_ok=True)
        # 图片的读取文件夹
        image_dir = os.path.join(root_path, 'images/{}/'.format(sign))

        # 图片的存放文件夹
        images_dir_rs = os.path.join(result_path, 'images/{}/'.format(sign))
        os.makedirs(images_dir_rs, exist_ok=True)
        # 处理数据
        images = []
        annotations = []
        categories = f['categories']

        for i in f['images']:
            # 修改 image 属性
            width = i['width']
            height = i['height']
            i['width'] = targetWidth
            i['height'] = targetHeight
            images.append(i)

            # 处理图片大小，并另存到结果集
            # 当前图片路径
            image_path = os.path.join(image_dir, i['file_name'])
            save_image_path = os.path.join(images_dir_rs, i['file_name'])
            # 读取图片
            img = cv2.imread(image_path)
            img_new = cv2.resize(img, (targetHeight, targetWidth))
            # 保存
            cv2.imwrite(save_image_path, img_new)
            with open(textDir_rs + str(i['id']) + '.txt', 'w') as lable:
                for j in f['annotations']:
                    if j['image_id'] == i['id']:
                        # 获取图片的高宽 ， coco 的格式  lefttopX ， lefttopY ， bbox_width ， bbox_height ； yoloTXT 格式 ： 'box_xmid / 宽','box_ymid / 高','w','h'
                        # 修改COCO的 数据 将 高 框 压缩成 或者放大 640 * 640 ， 并将标签也同比例放大和缩小

                        # 修改COCO的 标签
                        lefttopX = j['bbox'][0]
                        lefttopY = j['bbox'][1]
                        bbox_width = j['bbox'][2]
                        bbox_height = j["bbox"][3]

                        j['bbox'][0] = lefttopX / width * targetWidth
                        j['bbox'][1] = lefttopY / height * targetHeight
                        j['bbox'][2] = bbox_width / width * targetWidth
                        j['bbox'][3] = bbox_height / height * targetHeight
                        annotations.append(j)
                        # COCO 转 YOLO ：  中心点_X / 宽  = （ leftTopX + bboxW / 2）/ width           中心点_Y / 高  = （ leftTopY + bboxH / 2）/ width
                        lable.write(
                            str(j['category_id']) + ' ' + str(
                                (j['bbox'][0] + 0.5 * j['bbox'][2]) / i['width']) + ' ' + str(
                                (j['bbox'][1] + 0.5 * j['bbox'][3]) / i['height']) + ' ' + str(
                                j['bbox'][2] / i['width']) + ' ' + str(j['bbox'][3] / i['height']) + '\n'
                        )
                        # lable.write(
                        #     str(j['category_id']) + ' ' + str((j['bbox'][0]+0.5*j['bbox'][2])/i['width']) + ' ' + str((j['bbox'][1]+0.5*j['bbox'][3])/i['height']) + ' ' + str(j['bbox'][2]/i['width']) + ' ' + str(j['bbox'][3]/i['height']) + '\n'
                        #     )

        instance = {}
        instance['info'] = 'Kequan created'
        instance['license'] = ['license']
        instance['images'] = images
        instance['annotations'] = annotations
        instance['categories'] = categories
        # 保存数据
        json_rs = os.path.join(json_dir_rs, "instances_{}2017.json".format(sign))
        json.dump(instance, open(json_rs, 'w'), ensure_ascii=False, indent=2)  # indent=2 更加美观显示


if __name__ == '__main__':
    # 准备数据
    root_path = ".\helmet_dataset"
    result_path = ".\helmet_rs"
    os.makedirs(result_path, exist_ok=True)
    #目标宽度 =
    targetWidth = 640
    targetHeight = 640


    sign_list = ['train', "val",'test']

    cocoAndyoloChangeScale(sign_list,root_path,result_path)




