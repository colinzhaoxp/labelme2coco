# Lableme2coco

将labelme格式的数据转换成coco格式

## 开始使用

下载

```bash
git clone https://github.com/colinzhaoxp/labelme2coco
```

安装必要的包

```bash
pip install -r requirements.txt
```

修改convert2coco中的文件路径

```python
python convert2coco.py
```

## 运行

### 转换标签文件夹

#### 目录结构：

```
---labelme_folder
   |---folder1
   |---folder2
   |---forder3
   |---forder4
   |---forder5
   |---Classification.txt
   |---Detection.txt
   |---Segmentation.txt
```



#### 子文件文件夹内容：

分类：训练图片

检测、分割：训练图片及labelme标签json文件，图片与json在**同一目录**下，对应图片和json**同名**



#### 配置文件Classification.txt，Detection.txt，Segmentation.txt 结构：

需要进行标签转换的文件夹名称，**每行一个**

```
folder1
folder2
forder3
forder4
forder5
```



#### 运行文件修改

convert2coco.py

```python
labelme_folder #labelme标签主文件夹，文件夹中包含各个分类的子文件夹和分类、检测、分割的配置文件
save_json_path #转换后的coco标签文件存储路径
transfer_types #所要进行的转换类型，types 0:Classification, 1:Detection, 2:Segmentation 
               #例：进行分类和分割的转换 transfer_types = [0, 2] 只进行检测转换 transfer_types = [1]
```
