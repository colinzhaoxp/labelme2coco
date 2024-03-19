import os
import json
from PIL import Image

def get_image_size(file_path):
    with Image.open(file_path) as img:
        width, height = img.size
        return [width, height]

# 指定图片所在的文件夹路径
image_folder = 'E:/workspace/dataset/coco2017_1000/coco2017_1000/test/person'

# 遍历文件夹中的每一个图片文件
for dir_name, _, files in os.walk(image_folder):
    for file_name in files:
        if file_name.endswith(('.jpg', '.png', '.jpeg')):  # 这里可以根据实际情况添加更多的图片格式
            image_path = os.path.join(dir_name, file_name)
            label = os.path.basename(dir_name)

            # 获取图片尺寸
            points = get_image_size(image_path)

            # 创建单个shape的JSON数据
            shape_data = {
                "label": label,
                "points": [[0, points[1]], points],
                "group_id": None,
                "description": "",
                "shape_type": "null",
                "flags": {},
                "mask": None
            }

            # 创建整个JSON对象
            json_data = {
                "version": "5.4.1",
                "flags": {},
                "shapes": [shape_data],
                "imagePath": "..\\"+file_name,
            }

            # 生成JSON文件名，例如与图片同名但扩展名为.json
            json_filename = os.path.splitext(file_name)[0] + ".json"
            json_filepath = os.path.join(dir_name, json_filename)

            # 写入JSON文件
            with open(json_filepath, 'w') as json_file:
                json.dump(json_data, json_file, indent=2)

print("JSON文件已成功生成。")