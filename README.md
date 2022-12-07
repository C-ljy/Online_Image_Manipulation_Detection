# 在线图像篡改检测

## 配置虚拟环境

软件运行在操作系统：`Ubuntu 22.04.1 LTS`上。

使用Anaconda创建虚拟环境，这里提供了虚拟环境的导出文件`imd.yaml`和`imd_pip.txt`。

你可能会需要的安装步骤：

```
pip install matplotlib
pip install opencv-python

pip install tf_slim
sudo apt install build-essential
pip install cython
pip install cython_bbox
```



## 数据迁移

数据库使用Ubuntu自带的SQLite，若`imdNet`文件夹下不含`db.sqlite3`文件，请执行以下命令：

```
python manage.py makemigrations
python manage.py migrate
```



## 模型-百度网盘链接

链接: https://pan.baidu.com/s/1Mp5a56H4CP9Et5yDu0GDnQ?pwd=qrzj 提取码: qrzj 复制这段内容后打开百度网盘手机App，操作更方便哦

载模型后请将`imdNet/upimg/utils.py`中的`model_path`改为模型所在**文件夹**路径。



## 执行

在终端中进入与manage.py文件同级目录，输入命令如下：

```
conda activate <虚拟环境名>
python manage.py runserver
```

在浏览器中输入http://127.0.0.1:8000/，进入应用页面。

ImageForTest文件夹中提供了一些可做测试的图片。



