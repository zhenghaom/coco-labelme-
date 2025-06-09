from pycocotools.coco import COCO
import os
import shutil
from tqdm import tqdm
import skimage.io as io
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw
#多脚本原因为：数据集中分了训练集以及测试集，为了更好的方便多终端并行而已，实际上1234四个步骤只需要各一个脚本即可
#本脚本命名为：前两字段表示作用，如substract---xml为提取为xml文件，xml---JSONS为xml整合为一个整体json文件，JSONS---json为拆分为一个个json文件，COCO---labelme为COCO的json格式转换为labelme的json格式
#             后两字段的yes和no是因为本次任务是animal with person 和 animnal without person，是否即表示有无人这个类别
#本脚本的作用为筛选出对应类别的数据转换为xml文件，可修改路径，提取类别以及check_image函数实现筛选目的

# 需要设置的路径
savepath="D:/tempdata/generate_xml/animal_no_person/" 

img_dir=savepath+'images/'
anno_dir=savepath+'annotations/'
datasets_list=['train2017', 'val2017']

#coco有80类，这里写要提取类的名字， 
classes_names = ['cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','teddy bear'] 


#包含所有类别的原coco数据集路径
dataDir= 'D:/tempdata/COCO/' 
'''
目录格式如下：
$COCO_PATH
----|annotations
----|train2017
----|val2017
----|test2017
'''

 
headstr = """\
<annotation>
    <folder>VOC</folder>
    <filename>%s</filename>
    <source>
        <database>My Database</database>
        <annotation>COCO</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""
objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""
 
tailstr = '''\
</annotation>
'''
 

def mkr(path):
    if not os.path.exists(path):
        os.makedirs(path)  

def id2name(coco):
    classes=dict()
    for cls in coco.dataset['categories']:
        classes[cls['id']]=cls['name']
    return classes
 
def write_xml(anno_path,head, objs, tail):
    f = open(anno_path, "w")
    f.write(head)
    for obj in objs:
        f.write(objstr%(obj[0],obj[1],obj[2],obj[3],obj[4]))
    f.write(tail)
 

 
def save_annotations_and_imgs(coco,dataset,filename,objs):
    #将图片转为xml，例:COCO_train2017_000000196610.jpg-->COCO_train2017_000000196610.xml
    dst_anno_dir = os.path.join(anno_dir, dataset)
    mkr(dst_anno_dir)
    anno_path=dst_anno_dir + '/' + filename[:-3]+'xml'
    img_path=dataDir+dataset+'/'+filename
    print("img_path: ", img_path)
    dst_img_dir = os.path.join(img_dir, dataset)
    mkr(dst_img_dir)
    dst_imgpath=dst_img_dir+ '/' + filename
    print("dst_imgpath: ", dst_imgpath)
    img=cv2.imread(img_path)
    shutil.copy(img_path, dst_imgpath)
 
    head=headstr % (filename, img.shape[1], img.shape[0], img.shape[2])
    tail = tailstr
    write_xml(anno_path,head, objs, tail)
 
 
def showimg(coco,dataset,img,classes,cls_id,show=True):
    global dataDir
    I=Image.open('%s/%s/%s'%(dataDir,dataset,img['file_name']))
    #通过id，得到注释的信息
    annIds = coco.getAnnIds(imgIds=img['id'], catIds=cls_id, iscrowd=None)
    anns = coco.loadAnns(annIds)
    objs = []
    for ann in anns:
        class_name=classes[ann['category_id']]
        if class_name in classes_names:
            print(class_name)
            if 'bbox' in ann:
                bbox=ann['bbox']
                xmin = int(bbox[0])
                ymin = int(bbox[1])
                xmax = int(bbox[2] + bbox[0])
                ymax = int(bbox[3] + bbox[1])
                obj = [class_name, xmin, ymin, xmax, ymax]
                objs.append(obj)
                draw = ImageDraw.Draw(I)
                draw.rectangle([xmin, ymin, xmax, ymax])
    if show:
        plt.figure()
        plt.axis('off')
        plt.imshow(I)
        plt.show()
 
    return objs
 

# 检查图片是否包含人且只包含列表中的其他动物
def check_image(coco, img_id, classes, classes_names):
    ann_ids = coco.getAnnIds(imgIds=img_id)
    anns = coco.loadAnns(ann_ids)
    has_person = False
    has_animal = False
    other_animals = False

    for ann in anns:
        class_name = classes[ann['category_id']]
        if class_name == 'person':
            has_person = True
        elif class_name in classes_names:
            has_animal = True
        else:
            other_animals = True
            break
    return not has_person and has_animal and not other_animals


# 主程序
for dataset in datasets_list:
    annFile = '{}/annotations/instances_{}.json'.format(dataDir, dataset)
    coco = COCO(annFile)
    classes = id2name(coco)
    classes_ids = coco.getCatIds(catNms=classes_names)
    img_ids = coco.getImgIds()
    for img_id in tqdm(img_ids):
        if check_image(coco, img_id, classes, classes_names):

            img = coco.loadImgs(img_id)[0]
            filename = img['file_name']
            objs = showimg(coco, dataset, img, classes, classes_ids, show=False)
            save_annotations_and_imgs(coco, dataset, filename, objs)
#python C:\Users\郑浩铭\Desktop\file\1substract---xml--no.py