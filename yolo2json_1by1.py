import os
import json
import base64
import cv2

'''读取标注文件，1.txt 2.txt 3.txt ...'''
def read_txt_file(txt_file):
    with open(txt_file, 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines:
        line = line.strip().split()
        class_name = line[0]
        bbox = [coord for coord in line[1:]]
        data.append({'class_name': class_name, 'bbox': bbox})
    return data

'''读取标签文件，classes.txt'''
def read_classes(classes_file):
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    return classes

'''转换'''
def convert_to_labelme(data, image_path, image_size, classes):
    labelme_data = {
        'version': '5.3.1',
        'flags': {},
        'shapes': [],
        'imagePath': json_image_path,
        'imageData': None,
        'imageHeight': image_size[0],
        'imageWidth': image_size[1]
    }
    for obj in data:
        dx = obj['bbox'][0]
        dy = obj['bbox'][1]
        dw = obj['bbox'][2]
        dh = obj['bbox'][3]

        w = eval(dw) * image_size[1]
        h = eval(dh) * image_size[0]
        center_x = eval(dx) * image_size[1]
        center_y = eval(dy) * image_size[0]
        x1 = center_x - w/2
        y1 = center_y - h/2
        x2 = center_x + w/2
        y2 = center_y + h/2

        ### 1.直接写入txt中的标签：如0，1，2，3，4
        # if obj['class_name'] == '0': #判断对应的标签名称，写入json文件中
        #     label = str('grape')
        # else:
        #     label = obj['class_name']
        ### 2.读取txt中的标签,根据标签匹配种类：如 0-->bus 1-->person ...
        class_index = int(obj['class_name'])  # 将类名转换为索引
        label = classes[class_index] if class_index < len(classes) else 'unknown'

        shape_data = {
            'label': label,
            'points': [[x1, y1], [x2, y2]],
            'group_id': None,
            'shape_type': 'rectangle',
            'flags': {}
        }
        labelme_data['shapes'].append(shape_data)
    return labelme_data

def save_labelme_json(labelme_data, image_path, output_file):
    # 不保存json文件中的图像数据，image_data数据太大且没屌用，如需保存，放开下方注释即可
    # with open(image_path, 'rb') as f:
    #     image_data = f.read()
    # labelme_data['imageData'] = base64.b64encode(image_data).decode('utf-8')

    with open(output_file, 'w') as f:
        json.dump(labelme_data, f, indent=4)



if __name__ == '__main__':
    # 设置文件夹路径和输出文件夹路径
    txt_folder = r"E:\CODE\zyx_tools\1\labels"  # 存放LabelImg标注的txt文件的文件夹路径
    output_folder = r"E:\CODE\zyx_tools\1\json"  # 输出LabelMe标注的json文件的文件夹路径
    img_folder = r"E:\CODE\zyx_tools\1\images"  # 存放对应标签的图片文件夹路径
    classes_file = r"E:\CODE\zyx_tools\1\classes.txt"  # 类别文件的路径

    # 读取类别
    classes = read_classes(classes_file)
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历txt文件夹中的所有文件
    for filename in os.listdir(txt_folder):
        if filename.endswith('.txt'):
            # 生成对应的输出文件名
            output_filename = os.path.splitext(filename)[0] + '.json'

            # 读取txt文件
            txt_file = os.path.join(txt_folder, filename)
            data = read_txt_file(txt_file)

            # 设置图片路径和尺寸
            image_filename = os.path.splitext(filename)[0] + '.jpg'  # 图片文件名与txt文件名相同，后缀为.jpg
            image_path = os.path.join(img_folder, image_filename)
            json_image_path = image_path.split('\\')[-1]
            image_size = cv2.imread(image_path).shape

            # 转化为LabelMe格式
            labelme_data = convert_to_labelme(data, image_path, image_size, classes)

            # 保存为LabelMe JSON文件
            output_file = os.path.join(output_folder, output_filename)
            save_labelme_json(labelme_data, image_path, output_file)