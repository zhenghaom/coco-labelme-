# -*- coding: utf-8 -*-
from __future__ import print_function
import matplotlib.pyplot as plt
import os, sys, zipfile
import urllib.request
import shutil
import numpy as np
import skimage.io as io
import pylab
import json
from pycocotools.coco import COCO

#修改源目录以及目的地址即可
pylab.rcParams['figure.figsize'] = (8.0, 10.0)
 
#源目录
json_file='D:/tempdata/generate_xml/animal_no_person/annotations_json/instances_train2017.json' # # Object Instance 类型的标注    


 
data=json.load(open(json_file,'r'))
for i in range(len(data['images'])):
    print(i)
    data_2={}
    data_2['images']=[data['images'][i]] 
    data_2['categories']=data['categories']
    annotation=[]
 
# 通过imgID 找到其所有instance
    imgID=data_2['images'][0]['id']
    coco=COCO(json_file)
    img = coco.loadImgs([imgID])
    for ann in data['annotations']:
        if ann['image_id']==imgID:
            annotation.append(ann)
    data_2['annotations']=annotation
 
# 保存到新的json
    #目的地址
    json.dump(data_2,open('D:/tempdata/generate_xml/animal_no_person/images/train_json/{}.json'.format(str(img[0]['file_name']).split('.')[0]),'w'),indent=4)   #000




