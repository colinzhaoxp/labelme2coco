import labelme2coco

# set directory that contains labelme annotations and image files
#labelme_folder = "E:/workspace/dataset/coco2017_1000/coco2017_1000/test/car/label"
labelme_folder = "E:/workspace/dataset/coco2017_1000/coco2017_1000/test/"

# set export json path
save_json_path = "E:/workspace/dataset/coco2017_1000/coco2017_1000/test/instance_all.json"
#save_json_path = "E:/workspace/dataset/coco2017_1000/coco2017_1000/test/instance_person.json"

# set transfer types 0:Classification, 1:Detection, 2:Segmentation
transfer_types = [0, 1, 2]
# convert labelme annotations to coco
labelme2coco.convert(labelme_folder, save_json_path, transfer_types)