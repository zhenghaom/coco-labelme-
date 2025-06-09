# -*- coding: utf-8 -*-

import json
import cv2
import numpy as np
import os

colors = {#方框的颜色
    'person':(255, 0, 0),# 红色
    'cat':(0, 255, 0),# 绿色
    'dog':(0, 0, 255),# 蓝色
    'horse':(255, 255, 0),# 黄色
    'sheep':(255, 0, 255),  # 粉色
    'cow':(0, 255, 255),  # 青色
    'elephant':(150, 150, 50),  # 灰色
    'bear':(150, 50, 150),
    'zebra':(50, 150, 150),
    'giraffe':(128, 128, 128),
    'teddy bear':(0, 0, 0)
}

#用一个labelme格式的json作为参考，因为很多信息都是相同的，不需要修改。
def reference_labelme_json():
    ref_json_path = 'C:/Users/郑浩铭/Desktop/facecheck/282555,11edfd00010ac6abd.json'#第二幅
    data=json.load(open(ref_json_path))    
    return data
    
def labelme_shapes(data,data_ref):
    shapes = []
    group_id=0
    for ann in data['annotations']:
        shape = {}
        class_name = [i['name'] for i in data['categories'] if i['id'] == ann['category_id']]
        shape['label'] = class_name[0]
        
        #"rectangle"这里是由不规则的分割形状转为了方形框选，可自己修改

        # 获取多边形的顶点坐标
        points = np.array(ann['segmentation'][0]).reshape(-1, 2)
        
        # 计算外接矩形
        x, y, w, h = cv2.boundingRect(points)
        shape['points'] = [[x, y], [x + w, y + h]]
        shape['shape_type'] = 'rectangle'
        shape['fill_color'] = None

        shape['group_id'] = group_id  # 使用类别对应的 group_id
        group_id=group_id+1
        # 为不同标签设置不同颜色的方框
        shape['line_color'] = colors[class_name[0]]
        shape['flags'] = data_ref['shapes'][0]['flags']
        shape['confidence']=1
        shapes.append(shape)
    return shapes
        
 
def Coco2labelme(json_path,data_ref):
    with open(json_path,'r') as fp:
        data = json.load(fp)  # 加载json文件
        data_labelme={}
        #视情况修改，具体看目标的lalbelme格式是怎么样的
        data_labelme['version'] = data_ref['version']
        data_labelme['flags'] = data_ref['flags']   
        data_labelme['shapes'] = labelme_shapes(data,data_ref)
        data_labelme['imagePath'] = data['images'][0]['file_name']
        data_labelme['imageData'] = None      
        data_labelme['imageHeight'] = data['images'][0]['height']
        data_labelme['imageWidth'] = data['images'][0]['width']
        return data_labelme
 
if __name__ == '__main__':
#源目录
    root_dir = 'D:/tempdata/generate_xml/animal_with_person/images/val_json'                                                                       #000

    json_list = os.listdir(root_dir)
    #参考的json
    data_ref = reference_labelme_json()
    
    for json_path in json_list:
        if json_path.split('.')[-1] == 'json':
            print('当前文件： ', json_path)
            data_labelme= Coco2labelme(os.path.join(root_dir,json_path), data_ref)
            file_name = data_labelme['imagePath']
           #目标路径
            json.dump(data_labelme,open('D:/tempdata/generate_xml/animal_and_person/labelme_val/%s.json' % file_name.split('.')[0],'w'),indent=4)  #000
