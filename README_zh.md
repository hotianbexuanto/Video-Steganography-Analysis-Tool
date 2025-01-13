# 视频隐写分析工具 (Video Steganography Analysis Tool)

一个功能强大的视频隐写分析工具，可以将视频分解为不同的颜色通道、位平面和各种隐写分析视图。

## 功能特点

- 基础颜色通道分离（红、绿、蓝、灰度）
- 饱和度调整分析
- 位平面分析（0-7位）
- Stegsolve 风格分析
- 通道运算分析（XOR、加法、减法）
- 颜色滤镜分析
- 自动音频同步
- 保持原视频帧率

## 安装说明

1. 确保已安装 Python 3.7+
2. 克隆或下载本项目
3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. Windows系统：
```bash
# 双击运行 run.bat
# 或在命令行中运行：
python video_color_separator.py
```

2. Linux/MacOS系统：
```bash
# 添加执行权限
chmod +x run.sh
# 运行脚本
./run.sh
# 或直接运行Python文件
python3 video_color_separator.py
```

3. 在弹出的文件选择对话框中选择要分析的视频文件
4. 选择输出目录
5. 等待处理完成

## 输出结构

```
output_dir/
├── frames/                    # 所有帧图片
│   ├── basic/                # 基础颜色通道
│   │   ├── blue/            # 蓝色通道
│   │   ├── green/           # 绿色通道
│   │   ├── red/             # 红色通道
│   │   └── grayscale/       # 灰度图
│   ├── saturation/           # 饱和度分析
│   │   ├── low_sat/         # 低饱和度
│   │   ├── normal_sat/      # 原始饱和度
│   │   └── high_sat/        # 高饱和度
│   ├── bit_planes/           # 位平面分析
│   │   ├── bit_plane_0/     # 第0位平面
│   │   └── .../             # 到第7位平面
│   ├── stegsolve/            # Stegsolve风格分析
│   │   ├── red_plane/       # 红色平面
│   │   ├── green_plane/     # 绿色平面
│   │   ├── blue_plane/      # 蓝色平面
│   │   └── .../             # 其他分析
│   └── steganography/        # 其他隐写分析
│       ├── xor_analysis/     # 异或分析
│       ├── channel_operations/# 通道运算
│       └── color_filters/    # 颜色滤镜
└── videos/                    # 处理后的视频文件
```

## 注意事项

- 确保有足够的磁盘空间（建议至少原视频大小的50倍）
- 处理大视频可能需要较长时间
- 输出的视频将保持原视频的帧率和音频
- **所有过程均按顺序执行，处理速度较为缓慢**。建议在处理大文件时耐心等待。
- **此脚本由AI创建，并在Windows 10上测试过。应能在其他系统上运行，但请自行测试或修改。**

## 系统要求

- Windows/Linux/MacOS
- Python 3.7+
- 4GB+ RAM（建议）
- 足够的磁盘空间

## 依赖库

- OpenCV (图像处理)
- NumPy (数值计算)
- MoviePy (视频音频处理) 