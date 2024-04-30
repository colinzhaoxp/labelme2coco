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

Demo见 labelme2coco/test 文件中


> 需要注意的是：Classification.txt文件夹中需要包含Detection.txt和Segmentation.txt文件中的超类。(但是目前（2024年4月30日）还有一点bug)

#### 运行文件修改

convert2coco.py

```python
labelme_folder #labelme标签主文件夹，文件夹中包含各个分类的子文件夹和分类、检测、分割的配置文件
save_json_path #转换后的coco标签文件存储路径
transfer_types #所要进行的转换类型，types 0:Classification, 1:Detection, 2:Segmentation 
               #例：进行分类和分割的转换 transfer_types = [0, 2] 只进行检测转换 transfer_types = [1]
```

## 待做事项
- [ ]  bug：当数据过大时，labelme2coco.py的290行和291行代码会报错，报错信息是rows为空。
- [ ]  bug：json中的area项的数值不准确。
- [ ]  待优化：当待转换的labelme数据量过大（两万多张图片，每张图片平均有3个标注的时候）时，转换的速度过慢，用了近10个小时？
- [ ]  待优化：增加异常处理，当图片不存在的时候，读取会报错，导致程序崩溃，浪费了之前处理的大量时间。