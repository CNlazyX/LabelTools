# LabelTools
Used for deep learning label format modification

* yolo2json_1by1.py   -----> 将yolo格式的.txt标签转化成.json格式的标签，1个.txt转换成1个.json文件
* random_jpg&label.py -----> 随机划分数据集：8：1：1
* json2yolo_1by1.py   -----> 将.json格式转化为.txt格式，该文件针对固定任务的标签转换，如一个框内存在两种类别的关键点情况，通过判断标识符解决关键点归属问题
