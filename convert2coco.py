import labelme2coco

# set directory that contains labelme annotations and image files
labelme_folder = "./labelme-data"

# set export json path
save_json_path = "./instances_train2017.json"

# convert labelme annotations to coco
labelme2coco.convert(labelme_folder, save_json_path)