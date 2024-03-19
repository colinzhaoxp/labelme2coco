import os
import json

# 指定图像文件夹的路径
IMAGE_FOLDER = "F:\\SDU\\data\\flower_photos"
# 指定输出路径
OUTPUT_PATH = "F:\\SDU\\data\\flower_photos\\flower_photos.json"

# 定义超级类别列表
SUPER_CATEGORIES = ["canxian", "dianduan", "dianhanok", "dianlie","handianlianxi", "handianlouhan","hanpanpianxie",
                    "shaohan","shuangyinxian","wuyinxian","xuhan","yinxiandianqing","yinxianguochang",
                    "yinxianguoduan","yinxianlouhan","yinxianpianxie","yinxianweihan","zazhi","zhuhanji"]

def get_image_info(image_folder):
    image_info = []
    categories = []
    annotations = []
    idx = 1  # 图像ID从1开始
    annotation_id = 1  # 注释ID从1开始

    for root, dirs, files in os.walk(image_folder):
        if os.path.basename(root).startswith('.ipynb_checkpoints') or os.path.basename(root).startswith('jiguanghan'):
            continue
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                image_path = os.path.join(root, file)
                height, width = get_image_dimensions(image_path)
                image_info.append({
                    "height": height,
                    "width": width,
                    "id": idx,
                    "file_name": file  # 只写入图片名称
                })

                # 添加图像的注释信息
                folder_name = os.path.basename(root)
                category_name = folder_name.lower()
                if category_name not in [cat["name"] for cat in categories]:
                    categories.append({
                        "supercategory": category_name,
                        "id": len(categories) + 201,  # id从201开始递增
                        "name": category_name
                    })
                category_id = next((cat["id"] for cat in categories if cat["name"] == category_name), None)

                annotations.append({
                    "iscrowd": 0,
                    "image_id": idx,
                    "shape_type": None,
                    "bbox": [0, 0, width, height],
                    "segmentation": [],
                    "category_id": category_id,
                    "id": annotation_id,
                    "area": width * height
                })

                idx += 1
                annotation_id += 1

    return image_info, categories, annotations

def get_image_dimensions(image_path):
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            width, height = img.size
        return height, width
    except Exception as e:
        print(f"Error getting dimensions for {image_path}: {e}")
        return None, None

def main():
    image_info, categories, annotations = get_image_info(IMAGE_FOLDER)

    with open(OUTPUT_PATH, "w") as f:
        json.dump({"images": image_info, "categories": categories, "annotations": annotations}, f, indent=4)

    print(f"Image info saved to {OUTPUT_PATH}.")

if __name__ == "__main__":
    main()
