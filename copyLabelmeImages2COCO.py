import os
import shutil
import tqdm

save_dir_path = r'./val2017'

os.makedirs(save_dir_path, exist_ok=True)

labelme_floder = r'./test'

# need_copy.txt文件中存放的是需要复制的文件夹名称，一行一个文件夹名
txt_path = os.path.join(labelme_floder, 'need_copy.txt')

with open(txt_path, 'r') as f:
    lines = f.readlines()

    for line in lines:
        line = line.strip()
        imgs_dir_path = os.path.join(labelme_floder, line)
        
        for img_name in os.listdir(imgs_dir_path):
            if not img_name.endswith('.jpg'): continue
            img_path = os.path.join(imgs_dir_path, img_name)
            shutil.copy(img_path, save_dir_path)
