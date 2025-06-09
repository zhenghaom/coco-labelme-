# coco-labelme-
#coco数据集提取类别，并转换为labelme格式的运行脚本
#多脚本原因为：
#	数据集中分了训练集以及测试集，为了更好的方便多终端并行而已，实际上1234四个步骤只需要各一个脚本即可
#本脚本命名为：
#	前两字段表示作用，如substract---xml为提取为xml文件，xml---JSONS为xml整合为一个整体json文件，JSONS---json为拆分为一个个json文件，COCO---labelme为COCO的json格式转换为labelme的json格式，而最前面的1234便是步骤顺序，后两字段的yes和no是因为本次任务是animal with person 和 animnal #without person，是否即表示有无人这个类别。
#本脚本先设置好类别以及筛选条件，从coco数据集的instance标注文件中遍历筛选出对应的数据并先保存为xml文件，第二个脚本再把xml文件重新集合为coco格式的json文件，第三个脚本即把coco格式的json单一文件分成了各个图片对应的小json文件，最后的脚本再把每个json文件转换为lalbelme格式的json文件。
