# AI模型文件说明

本目录应包含以下YOLO模型文件：

## 所需模型文件

### 1. classify.pt
- **用途**: 产品图片分类
- **输入**: 产品图片
- **输出**: 24类产品分类(Compressor, Mainboard, Fan等)
- **说明**: 需要使用产品图片数据集训练YOLO分类模型

### 2. best.pt
- **用途**: 产品标签目标检测
- **输入**: 产品图片
- **输出**: 标签区域边界框
- **说明**: 需要使用标注的产品标签数据训练YOLO检测模型

## 模型训练说明

由于模型文件很大(通常>100MB)且需要专门的训练数据集，本项目不包含预训练模型。

您需要：
1. 准备产品图片数据集
2. 使用Ultralytics YOLO框架训练模型
3. 将训练好的模型文件放置到本目录

## 占位实现

在没有真实模型文件的情况下，系统将使用占位实现：
- `classify()` - 返回固定分类 "Compressor"
- `yolo_ocr()` - 返回固定型号 "DZ120V1D"

这允许系统在没有模型文件时仍可运行和测试其他功能。

## 参考链接

- Ultralytics YOLO: https://github.com/ultralytics/ultralytics
- PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
