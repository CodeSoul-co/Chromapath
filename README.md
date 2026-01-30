<p align="center">
   <img src="chromapath.png" alt="Chromapath" width="320" />
 </p>
 
 # Chromapath

**中文** | [English](README_EN.md)

图像颜色分析工具包 - 用于提取、分析和可视化图像中的颜色信息。

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 工具概览

本工具包包含 5 个功能模块，形成一个完整的颜色分析流水线：

| 工具 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **Palette Generator** | 为每张图片生成色卡 | 图片文件夹 | 每张图片对应的色卡图 |
| **Color Extractor** | 分析多张图片的整体颜色分布 | 图片文件夹 | 颜色列表 + 百分比 |
| **Co-occurrence Analyzer** | 计算颜色共现频率 | 图片文件夹 + 颜色列表 | 共现频率矩阵 |
| **Network Viewer** | 可视化颜色关系网络 | 颜色数据 + 频率矩阵 | 网络关系图 |
| **Genetic Optimizer** | 交互式优化配色方案 | 单张图片 | 优化后的配色方案 |

## 典型工作流程

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          完整分析流程                                    │
└─────────────────────────────────────────────────────────────────────────┘

步骤 1: 准备图片
    └── 将待分析的图片放入一个文件夹

步骤 2: 生成色卡 (Palette Generator)
    ├── 输入: 图片文件夹
    ├── 设置: 提取颜色数量、灰度过滤阈值
    └── 输出: 每张图片的色卡 (保存为 PNG)

步骤 3: 提取整体颜色 (Color Extractor)
    ├── 输入: 图片文件夹
    ├── 处理: 对所有图片进行 K-Means 聚类
    └── 输出: 颜色列表 + 占比百分比
            例如: [([255, 128, 64], 0.25), ([32, 64, 128], 0.18), ...]

步骤 4: 计算共现频率 (Co-occurrence Analyzer)
    ├── 输入: 图片文件夹 + 步骤3的颜色列表
    ├── 处理: 统计哪些颜色经常同时出现
    └── 输出: N×N 共现频率矩阵

步骤 5: 可视化网络 (Network Viewer)
    ├── 输入: 颜色数据 + 频率矩阵
    └── 输出: 颜色关系网络图
            - 节点 = 颜色 (大小表示占比)
            - 边 = 共现关系 (红色=强关联)
```

### 独立使用: 遗传算法优化 (Genetic Optimizer)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       遗传算法配色优化                                   │
└─────────────────────────────────────────────────────────────────────────┘

1. 打开一张图片
2. 系统生成多个配色方案 (种群)
3. 你为每个方案打分 (0-10)
4. 系统根据评分进化出下一代方案
5. 重复 3-4 直到满意
6. 导出最佳配色方案
```

## 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/chromapath.git
cd chromapath

# 创建虚拟环境 (推荐)
conda create -n color python=3.10
conda activate color

# 安装依赖
pip install -r requirements.txt
```

## 快速开始

```bash
# 启动主界面
python main.py

# 或直接启动特定工具
python main.py --tool palette      # 色卡生成
python main.py --tool extractor    # 颜色提取
python main.py --tool cooccurrence # 共现分析
python main.py --tool network      # 网络可视化
python main.py --tool genetic      # 遗传算法优化
```

## 详细使用说明

### 1. Palette Generator (色卡生成器)

**用途**: 批量为图片生成色卡

**操作步骤**:
1. 选择包含图片的文件夹
2. 选择色卡输出文件夹
3. 设置参数:
   - **灰度过滤阈值**: 过滤接近灰色的像素 (默认 1)
   - **提取颜色数量**: 每张图提取多少种主色 (默认 8)
4. 点击 "Generate Palettes"

### 2. Color Extractor (颜色提取器)

**用途**: 分析多张图片的整体颜色分布

**操作步骤**:
1. 选择图片文件夹
2. 设置颜色数量 (默认 18)
3. 点击 "Analyze Images"
4. 查看颜色分布柱状图
5. 复制底部的颜色数据 (用于下一步)

**输出格式**:
```
[
    ([R, G, B], 百分比),
    ([255, 128, 64], 0.2534),
    ...
]
```

### 3. Co-occurrence Analyzer (共现分析器)

**用途**: 分析哪些颜色经常同时出现在同一张图片中

**操作步骤**:
1. 选择图片文件夹
2. 粘贴颜色数据 (来自 Color Extractor)
3. 点击 "Analyze Co-occurrence"
4. 查看共现频率矩阵

**矩阵解读**: 
- `matrix[i][j]` = 颜色 i 和颜色 j 同时出现的频率
- 值越大表示这两种颜色越常一起出现

### 4. Network Viewer (网络可视化)

**用途**: 将颜色关系可视化为网络图

**操作步骤**:
1. 输入颜色数据 (格式: `R G B 大小`)
   ```
   255 128 64 25
   32 64 128 18
   ...
   ```
2. 输入频率矩阵
3. 设置阈值:
   - **Base Threshold**: 显示边的最低权重
   - **Highlight Threshold**: 红色高亮的权重阈值
4. 点击 "Generate Network"

### 5. Genetic Optimizer (遗传算法优化)

**用途**: 通过交互式进化找到最佳配色方案

**操作步骤**:
1. 点击 "Open Image" 选择图片
2. 设置参数:
   - **Colors**: 配色方案中的颜色数量
   - **Grid**: 每代显示的方案数量 (行×列)
   - **Mutation**: 变异率
   - **Elite Threshold**: 保留精英的分数阈值
3. 为每个方案拖动滑块打分 (0-10)
4. 点击 "Evolve Next Generation" 进化
5. 重复打分和进化直到满意
6. 点击 "Show Best" 查看最佳方案

## 作为库使用

```python
from color_analyzer.core import ColorExtractor, CooccurrenceAnalyzer
from color_analyzer.visualization import ColorCardGenerator
import numpy as np

# 提取颜色
extractor = ColorExtractor(n_colors=8, gray_threshold=1)
colors, percentages = extractor.extract_from_image("image.jpg")

# 生成色卡
card_gen = ColorCardGenerator()
card_gen.save_card(colors, percentages, "palette.png")

# 分析共现
analyzer = CooccurrenceAnalyzer(distance_threshold=10)
color_list = [np.array(c) for c in colors]
matrix = analyzer.analyze_folder("images/", color_list)
print(analyzer.format_matrix(matrix))
```

## 项目结构

```
chromapath/
├── main.py                 # Main entry point
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
├── pyproject.toml         # Modern Python packaging
├── README.md              # 中文文档
├── README_EN.md           # English documentation
├── LICENSE                # MIT License
└── color_analyzer/        # Main package
    ├── __init__.py
    ├── core/              # Core algorithms
    │   ├── __init__.py
    │   ├── image_processor.py   # Image loading & preprocessing
    │   ├── clustering.py        # K-Means color clustering
    │   ├── color_extractor.py   # High-level color extraction
    │   ├── cooccurrence.py      # Co-occurrence analysis
    │   └── genetic.py           # Genetic algorithm
    ├── visualization/     # Visualization tools
    │   ├── __init__.py
    │   ├── color_card.py        # Color palette cards
    │   └── network_plot.py      # Network graphs
    └── ui/                # PyQt5 GUI applications
        ├── __init__.py
        ├── main_window.py       # Main launcher
        ├── palette_generator.py # Palette generation UI
        ├── color_extractor.py   # Color extraction UI
        ├── cooccurrence_analyzer.py
        ├── network_viewer.py
        └── genetic_optimizer.py
```

## Requirements

- Python 3.8+
- NumPy
- OpenCV (opencv-python)
- scikit-learn
- Matplotlib
- PyQt5

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- K-Means clustering powered by scikit-learn
- GUI built with PyQt5
- Visualization with Matplotlib
