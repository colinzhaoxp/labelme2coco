import os
import json
import PIL.Image
import PIL.ImageDraw
import numpy as np
from labelme2coco.utils import create_dir, list_jsons_recursively
from labelme2coco.image_utils import read_image_shape_as_dict


class labelme2coco(object):
    def __init__(self, labelme_folder='', save_json_path='./new.json', transfer_types = [0, 1, 2]):
        """
        Args:
            labelme_folder: folder that contains labelme annotations and image files
            save_json_path: path for coco json to be saved
        """
        self.save_json_path = save_json_path
        self.images = []
        self.categories = []
        self.annotations = []
        self.det_labels = []
        self.seg_labels = []
        self.class_labels = []
        self.label_list = []
        self.annID = 1
        self.height = 0
        self.width = 0
        self.directoryList = []
        self.num = 0
        self.class_flage = 0
        self.det_flage = 0
        self.seg_flage = 0
        # create save dir
        save_json_dir = os.path.dirname(save_json_path)
        create_dir(save_json_dir)
        contents = os.listdir(labelme_folder)
        # 通过transfer_types判断进行那种标签转换
        # get label from type file, Classification.txt, Detection.txt, Segmentation.txt
        if 0 in transfer_types:
            self.class_flage = 1
            if 'Classification.txt' not in contents:
                print("Classification.txt does not exist")
            else:
                with open(os.path.join(labelme_folder, 'Classification.txt'), 'r') as file:
                    for line in file:
                        self.class_labels.append(line.strip())
        if 1 in transfer_types:
            self.det_flage = 1
            if 'Detection.txt' not in contents:
                print("Detection.txt does not exist")
            else:
                with open(os.path.join(labelme_folder, 'Detection.txt'), 'r') as file:
                    for line in file:
                        self.det_labels.append(line.strip())
        if 2 in transfer_types:
            self.seg_flage = 1
            if 'Segmentation.txt' not in contents:
                print("Segmentation.txt does not exist")
            else:
                with open(os.path.join(labelme_folder, 'Segmentation.txt'), 'r') as file:
                    for line in file:
                        self.seg_labels.append(line.strip())

        # # get classification image directory
        # for item in contents:
        #     full_path = os.path.join(labelme_folder, item)
        #     # if os.path.isdir(full_path):
        #     # save child directory name, directory name is classification label
        #     #     self.directoryList.append(labelme_folder + "/" + item)
        #
        #     # get label from type file, Classification.txt, Detection.txt, Segmentation.txt
        #     if os.path.isfile(full_path):
        #         if item == 'Classification.txt':
        #             with open(full_path, 'r') as file:
        #                 for line in file:
        #                     self.class_labels.append(line.strip())
        #         if item == 'Detection.txt':
        #             with open(full_path, 'r') as file:
        #                 for line in file:
        #                     self.det_labels.append(line.strip())
        #         if item == 'Segmentation.txt':
        #             with open(full_path, 'r') as file:
        #                 for line in file:
        #                     self.seg_labels.append(line.strip())
        self.save_json(labelme_folder)

    #transfer classification label
    def classification_label_transfer(self, labelme_folder):
        for class_label in self.class_labels:
            # 遍历标签中的所有标签
            label = class_label
            dir = os.path.join(labelme_folder, class_label)
            for filename in os.listdir(dir):
                # 判断是否为图片文件，这里假设是.jpg格式，可以根据实际需求修改
                if filename.endswith('.jpg') or filename.endswith('.png'):  # 添加其他扩展名如 '.jpeg', '.gif', '.bmp' 等
                    img_path = os.path.join(dir, filename)
                    image = self.get_image(img_path, self.num)
                    self.images.append(image)
                    self.num += 1
                    shape_type = 'null'
                    points = [[0, self.height], [self.width, 0]]
                    if label not in self.label_list:
                        self.categories.append(self.category(label))
                        self.label_list.append(label)
                    self.annotations.append(self.annotation(points, label, self.num, shape_type, self.getcatid(label)))
                    self.annID += 1


    def detection_label_transfer(self, labelme_folder):
        for det_label in self.det_labels:
            # 遍历标签中的所有标签
            det_dir = os.path.join(labelme_folder, det_label)
        # get json list
        _, labelme_json = list_jsons_recursively(det_dir)
        self.data_transfer(labelme_json)

    def segmentation_label_transfer(self, labelme_folder):
        for seg_label in self.seg_labels:
            # 遍历标签中的所有标签
            seg_dir = os.path.join(labelme_folder, seg_label)
            # get json list
        _, labelme_json = list_jsons_recursively(seg_dir)
        self.data_transfer(labelme_json)

    #根据文件夹名称获取分类标签id
    def get_classlabel_dirname(self, dir_path):
        parent_dir = os.path.dirname(dir_path)
        parent_dir_name = os.path.basename(parent_dir)
        if parent_dir_name == 'label':
            parent_dir = os.path.dirname(parent_dir)
            parent_dir_name = os.path.basename(parent_dir)
        return self.getcatid(parent_dir_name)
    def data_transfer(self, labelme_json):
        for json_path in labelme_json:
            with open(json_path, 'r') as fp:
                class_id = self.get_classlabel_dirname(json_path)

                # load json
                data = json.load(fp)
#                (prefix, res) = os.path.split(json_path)
#                (file_name, extension) = os.path.splitext(res)
                self.images.append(self.image(data, self.num, json_path))
                self.num += 1
                for shapes in data['shapes']:
                    label = shapes['label']
                    shape_type = shapes['shape_type']
                    # if shape_type == 'rectangle':
                    #     if label not in self.de_label:
                    #         self.categories.append(self.category(label, shape_type))
                    #         self.de_label.append(label)
                    #
                    # if shape_type == 'polygon':
                    #     if label not in self.se_label:
                    #         self.categories.append(self.category(label, shape_type))
                    #         self.se_label.append(label)
                    #
                    # if shape_type == 'null':
                    #     if label not in self.class_label:
                    #         self.categories.append(self.category(label, shape_type))
                    #         self.class_label.append(label)
                    # 将label插入labe List
                    if label not in self.label_list:
                        self.categories.append(self.category(label))
                        self.label_list.append(label)

                    points = shapes['points']
                    self.annotations.append(self.annotation(points, label, self.num, shape_type, class_id))
                    self.annID += 1

    def image(self, data, num, json_path):
        image = {}
        # get image path
        _, img_extension = os.path.splitext(data["imagePath"])
        image_path = json_path.replace(".json", img_extension)

        return self.get_image(image_path, num)

    def get_image(self, image_path, num):
        image = {}
        img_shape = read_image_shape_as_dict(image_path)
        height, width = img_shape['height'], img_shape['width']

        image['height'] = height
        image['width'] = width
        image['id'] = int(num + 1)
        image['file_name'] = os.path.basename(image_path)

        self.height = height
        self.width = width

        return image

    def category(self, label):
        category = {}
        category['supercategory'] = label
        category['id'] = int(len(self.label_list) + 1)
        # if shape_type == 'rectangle':
        #     category['id'] = int(len(self.de_label) + 101)
        # if shape_type == 'polygon':
        #     category['id'] = int(len(self.se_label) + 201)
        # if shape_type == 'null':
        #     category['id'] = int(len(self.se_label) + 1)
        category['name'] = label

        return category

    def annotation(self, points, label, num, shape_type, class_id):
        annotation = {}
        annotation['iscrowd'] = 0
        annotation['image_id'] = num
        annotation['shape_type'] = shape_type


        if shape_type == 'rectangle':
            annotation['bbox'] = list(map(float, self.getbbox(points)))
            # coarsely from bbox to segmentation
            x = annotation['bbox'][0]
            y = annotation['bbox'][1]
            w = annotation['bbox'][2]
            h = annotation['bbox'][3]
            annotation['segmentation'] = [np.asarray(self.make_points2polygon(points)).flatten().tolist()]
            annotation['class_id'] = class_id

        if shape_type == 'polygon':
            new_points = self.points_seg2bbox(points)
            annotation['bbox'] = list(map(float, self.getbbox(new_points)))
            annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
            annotation['class_id'] = class_id


        if shape_type == 'null':
            new_points = [[1, points[0][1]-1], [points[1][0]-1, 1]]
            annotation['bbox'] = list(map(float, self.getbbox(new_points)))

            # coarsely from bbox to segmentation
            x = annotation['bbox'][0]
            y = annotation['bbox'][1]
            w = annotation['bbox'][2]
            h = annotation['bbox'][3]
            annotation['segmentation'] = [np.asarray(self.make_points2polygon(new_points)).flatten().tolist()]
            annotation['class_id'] = self.getcatid(label)


        annotation['category_id'] = self.getcatid(label)
        annotation['id'] = int(self.annID)
        # add area info
        annotation['area'] = self.height * self.width  # the area is not used for detection
        return annotation

   # 将分类、检测的坐标点修改成满足segmentation
    def make_points2polygon(self, points):
        seg_points = [[points[0][0], points[1][1]], points[0], [points[1][0], points[0][1]], points[1]]
        return seg_points

    def getcatid(self, label):
        for categorie in self.categories:
            if label == categorie['name']:
                return categorie['id']
            # if label[1]==categorie['name']:
            #     return categorie['id']
        return -1

    def getbbox(self,points):
        # img = np.zeros([self.height,self.width],np.uint8)
        # cv2.polylines(img, [np.asarray(points)], True, 1, lineType=cv2.LINE_AA)
        # cv2.fillPoly(img, [np.asarray(points)], 1)
        polygons = points
        mask = self.polygons_to_mask([self.height, self.width], polygons)
        return self.mask2box(mask)

    def mask2box(self, mask):
        # np.where(mask==1)
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]

        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]  # [x1,y1,w,h] for coco box format

    def polygons_to_mask(self, img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def data2coco(self):
        data_coco = {}
        data_coco['images'] = self.images
        data_coco['categories'] = self.categories
        data_coco['annotations'] = self.annotations
        return data_coco

    def save_json(self, labelme_folder):
        # self.data_transfer()
        if self.class_flage:
            self.classification_label_transfer(labelme_folder)
        if self.det_flage:
            self.detection_label_transfer(labelme_folder)
        if self.seg_flage:
            self.segmentation_label_transfer(labelme_folder)

        self.data_coco = self.data2coco()

        json.dump(self.data_coco, open(self.save_json_path, 'w', encoding='utf-8'), indent=4, separators=(',', ': '), cls=MyEncoder)

    def points_seg2bbox(self, points):
        xs = []
        ys = []
        for point in points:
            xs.append(point[0])
            ys.append(point[1])
        xs.sort()
        ys.sort()
        new_poinits = [[xs[0], ys[len(ys)-1]], [xs[len(xs)-1], ys[0]]]
        return new_poinits


# type check when save json files
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)



if __name__ == "__main__":
    labelme_folder = "tests/train2017/labelme_annot"
    save_json_path = "tests/train2017/test_coco.json"
    transfer_types = [0, 1, 2]
    labelme2coco(labelme_folder, save_json_path, transfer_types)
