---
title: CVDL 期中复习笔记
date: 2026-04-23
---

本笔记覆盖当前课程笔记中的三部分内容：

- `Recognition-1`（视觉识别基础、局部特征、BoW/SPM）
- `PixelComputing`（像素级分割、GraphCut/Matting、Inpainting）
- `Detection`（传统检测到深度检测：R-CNN/YOLO/SSD/FPN）

---

## 0. 复习策略（先看这个）

- 第一轮：看“任务定义 + 核心公式 + 方法优缺点”。
- 第二轮：按“方法演进链”串起来（为什么前者不够、后者解决了什么）。
- 第三轮：重点记高频概念：`Harris/SIFT`、`BoW-SPM`、`GraphCut/GrabCut`、`RPN/Anchor/FPN`、`one-stage vs two-stage`。

---

## 1. Recognition（识别）

### 1.1 任务与挑战

- 图像分类目标：学习 $f: \mathbb{R}^{H\times W\times C} \to \{0,1\}^K$。
- 难点来源：
- 几何变化：尺度、旋转、视角。
- 外观变化：光照、形变、遮挡。
- 语义变化：类别粒度与上下文依赖。

核心词：`semantic gap`（像素到语义鸿沟）。

### 1.2 BoW（Bag-of-Words）视觉模型

流程：

1. 兴趣点检测
2. 局部描述子提取
3. 词典学习（K-means）
4. 量化与直方图聚合
5. 分类（如线性 SVM）

核心公式：

$$
q(x)=\arg\min_k\|x-c_k\|_2,\quad
h_k=\frac{1}{N}\sum_{i=1}^N \mathbf{1}[q(x_i)=k]
$$

优缺点：

- 优点：结构清晰、可解释性强、在小数据和传统任务中有效。
- 缺点：硬量化有误差，空间结构信息丢失。

### 1.3 兴趣点与描述子（Harris + SIFT）

#### Harris 角点

结构张量：

$$
M=\sum w(x,y)\begin{bmatrix}I_x^2&I_xI_y\\I_xI_y&I_y^2\end{bmatrix}
$$

响应函数：

$$
R=\det(M)-k\cdot \mathrm{tr}(M)^2
$$

判别直觉：

- 平坦区：$\lambda_1,\lambda_2$ 都小
- 边缘：一大一小
- 角点：都大且接近

局限：对尺度变化敏感。

#### SIFT（重点）

四步：

1. DoG 尺度空间极值检测
2. 关键点精定位（去低对比度点、去边缘响应）
3. 主方向分配（旋转不变）
4. 128 维描述子构建（4x4x8）

关键公式：

$$
D(x,y,\sigma)=L(x,y,k\sigma)-L(x,y,\sigma)
$$

匹配常用比值检验（Lowe ratio）：

$$
\frac{d_1}{d_2}<\tau\ (\tau\approx0.8)
$$

### 1.4 空间信息：SPM / PMK

SPM 解决 BoW 不含位置信息的问题：

- Level 0: $1\times1$
- Level 1: $2\times2$
- Level 2: $4\times4$

总维度：

$$
K\sum_{l=0}^{L}4^l=K\cdot\frac{4^{L+1}-1}{3}
$$

考试常问：为什么 SPM 比纯 BoW 好。答：保留了粗到细的空间布局信息。

### 1.5 SIFT / PMK / SPM 三者关系（必会）

一句话概括：

1. `SIFT`：提“稳定局部特征”。
2. `PMK`：比“两个特征集合”的多分辨率相似度。
3. `SPM`：把 PMK 思想放到图像空间网格中，形成可训练向量。

从直觉到流程：

- `SIFT`：DoG 找关键点 -> 去不稳定点 -> 主方向对齐 -> 128 维描述子。
- `PMK`：粗层到细层做直方图交集，细层更精确、权重更高。
- `SPM`：`SIFT -> BoW 量化 -> 1x1/2x2/4x4... 分层统计 -> 拼接/加权`。

经典识别管线（高频）：

1. 用 `SIFT` 提描述子  
2. K-means 量化成视觉词（BoW）  
3. 用 `SPM` 加入粗到细空间信息  
4. 用 SVM 分类

维度速记：

$$
\dim(\mathrm{SPM})=K\cdot(1+4+4^2+\cdots+4^L)
$$

例：`K=200, L=2`，维度 `4200`。

### 1.6 玩具数据流（手算思维）

设 `K=4, L=1`，图像 A 的 BoW 统计是：

$$
H_{1x1}=[2,3,1,2]
$$

再统计四个象限（`2x2`）并拼接，得到固定长度 SPM 向量：

$$
\mathrm{SPM}(A)=[H_{1x1}\ |\ H_{TL}\ |\ H_{TR}\ |\ H_{BL}\ |\ H_{BR}]
$$

若比较图像 A 与 B，在两层上的直方图交集分别为 $I_0$（粗层）与 $I_1$（细层），常见二层 PMK 可记为：

$$
K_{PMK}=I_1+\frac12(I_0-I_1)
$$

直觉：粗层给“兜底相似”，细层给“位置一致性”。

---

## 2. Pixel Computing（像素级理解）

### 2.1 Pixel labeling 的三类输出

- 离散标签：前景/背景、语义类
- 连续值：$\alpha$ matting、深度
- 结构关系：图模型里的 pairwise 约束

### 2.2 无监督分割

#### K-means 分割

思路：像素特征聚类（常见 $(r,g,b,\lambda x,\lambda y)$）。

目标：

$$
\min \sum_i\|x_i-\mu_{z_i}\|^2
$$

注意：$\lambda$ 控制空间连贯性，过小会碎，过大会过平滑。

#### Mean Shift

思路：向密度峰值迭代移动；不需预设 K，但需带宽 $h$。

要点：`h` 决定粒度，比 K 更关键。

详细版（建议按“窗口均值漂移”去理解）：

1. 把每个像素/点看作特征空间中的点（可含颜色+位置）
2. 在当前点周围放一个核窗口（带宽 $h$）
3. 计算窗口内样本的加权均值，作为新位置
4. 重复直到位移很小（收敛到某个 mode）
5. 收敛到同一 mode 的点归为一类

常见更新公式：

$$
x^{(t+1)}=
\frac{\sum_j K\!\left(\frac{\|x_j-x^{(t)}\|^2}{h^2}\right)x_j}
{\sum_j K\!\left(\frac{\|x_j-x^{(t)}\|^2}{h^2}\right)}
$$

参数直觉（高频）：

- $h$ 小：mode 多，分割细，易碎片化
- $h$ 大：mode 少，分割粗，易过合并

优缺点：

- 优点：不预设簇数；能处理非球形簇；思想直观
- 缺点：对 $h$ 敏感；高维/大样本下计算开销高

一句话：Mean Shift 不是“无参数”，只是“无 K”，核心参数是带宽 $h$。

### 2.3 图分割：Normalized Cut（Ncut）

图建模：节点=像素/超像素，边权=相似度。

$$
\mathrm{Ncut}(A,B)=
\frac{\mathrm{cut}(A,B)}{\mathrm{assoc}(A,V)}+
\frac{\mathrm{cut}(A,B)}{\mathrm{assoc}(B,V)}
$$

松弛后求解广义特征值问题：

$$
(D-W)y=\lambda Dy
$$

常取第二小特征向量划分。

### 2.4 交互式抠图：GraphCut / GrabCut / Lazy Snapping

#### GraphCut（二值分割）

MRF 能量：

$$
E(L)=\sum_i D_i(L_i)+\sum_{(i,j)}V_{ij}(L_i,L_j)
$$

- `D_i`：数据项（前景/背景颜色模型）
- `V_ij`：平滑项（相邻像素标签一致性）

#### GrabCut（重点）

- 输入：bounding box（再配合少量笔刷）
- 核心：`GMM + iterated graph cut`（类似 EM 交替优化）
- 优势：交互负担低、实用性强

#### Lazy Snapping

- 用少量 strokes + superpixel 加速
- 速度更好，但边界精度受 superpixel 粒度影响

### 2.5 Matting 与 Poisson Matting

合成模型：

$$
I=\alpha F+(1-\alpha)B
$$

难点：单像素 7 个未知（$F$3 + $B$3 + $\alpha$1）但仅 3 个观测（RGB）。

Poisson Matting 走梯度域：

$$
\Delta\alpha=\mathrm{div}(v)
$$

配合 trimap 的边界条件求解。

### 2.6 Inpainting（图像修补）

Exemplar-based（Criminisi）关键不是“往里填”，而是“按结构优先填”：

$$
P(p)=C(p)D(p)
$$

- $C(p)$：置信度
- $D(p)$：结构延拓项（等照线方向）

---

## 3. Detection（检测）

### 3.1 基本概念

- 检测 = 分类 + 定位
- 输出：$(b_i,c_i,s_i)$
- 几何评估：IoU

$$
\mathrm{IoU}(B,\hat B)=\frac{|B\cap\hat B|}{|B\cup\hat B|}
$$

### 3.2 传统检测

#### Viola-Jones

三件套：

- 积分图（矩形特征 O(1) 求和）
- AdaBoost（特征选择 + 强分类器）
- Cascade（前级快筛负样本）

为什么经典：在当年实现了实时与极低误检。

为什么快（考试建议按这条背）：

1. `Haar-like` 特征：矩形亮暗差，候选很多但计算简单。
2. `Integral Image`：任意矩形和四次访问即可得到，单特征近似 `O(1)`。
3. `AdaBoost`：从十万级候选特征中迭代挑出有效少数。
4. `Cascade`：大部分背景窗口前几级就淘汰，省掉后续开销。

积分图矩形和速记：

$$
\mathrm{sum}=A-B-C+D
$$

级联整体指标（乘法效应）：

$$
D_{all}=\prod_i d_i,\quad F_{all}=\prod_i f_i
$$

其中 $d_i$ 是单级检测率，$f_i$ 是单级误检率。

### 3.2.1 AdaBoost 如何筛“有效特征”

每轮在所有候选弱分类器中，找当前加权错误率最小者：

$$
\epsilon_j=\sum_i w_i\,\mathbf{1}[h_j(x_i)\neq y_i]
$$

选中后赋权：

$$
\alpha_t=\frac12\ln\frac{1-\epsilon_t}{\epsilon_t}
$$

更新样本权重（错分样本权重上升）：

$$
w_i\leftarrow w_i\exp(-\alpha_t y_i h_t(x_i))
$$

最终强分类器：

$$
H(x)=\mathrm{sign}\left(\sum_{t=1}^{T}\alpha_t h_t(x)-\tau\right)
$$

一句话：Boost 是“迭代式特征筛选”，每轮都更关注难样本。

#### HOG + SVM

HOG 三步：

1. 梯度
2. cell 方向直方图
3. block 归一化

线性分类：

$$
s(x)=w^\top x+b
$$

加 hard negative mining 与 NMS 构成完整检测系统。

HOG 从图到框的完整流程（会问）：

1. 建图像金字塔（多尺度）
2. 每尺度滑窗
3. 每窗口提 HOG（梯度 -> cell 直方图 -> block 归一化）
4. SVM 打分：$w^\top x+b$
5. 阈值筛候选
6. NMS 去重得最终框

经典参数速记（行人）：

- `window=64x128`
- `cell=8x8`
- `block=2x2 cells`
- `bins=9`

维度来源：

- cells 数：`8x16`
- blocks 数：`7x15=105`
- 每 block：`2x2x9=36`
- 总维度：`105x36=3780`

L2-Hys 归一化：

$$
v_1=\frac{v}{\sqrt{\|v\|_2^2+\epsilon^2}},\quad
v_2=\mathrm{clip}(v_1,\max=0.2),\quad
v=\frac{v_2}{\sqrt{\|v_2\|_2^2+\epsilon^2}}
$$

#### DPM（可形变部件模型）

- root + parts + deformation penalty
- latent SVM 训练（部件位置是潜变量）

意义：在深度学习前把“形变建模”做到了很强。

### 3.3 深度检测演进（高频主线）

`R-CNN -> Fast R-CNN -> Faster R-CNN`

#### R-CNN

- Selective Search 出 proposals
- 每个 proposal 单独过 CNN
- SVM 分类 + bbox 回归
- 问题：慢、训练分裂、存储重

#### Fast R-CNN

- 整图一次卷积
- RoI Pooling 抽固定大小特征
- 分类与回归联合训练
- 瓶颈仍在外部 proposal

#### Faster R-CNN（核心考点）

- 引入 RPN 生成 proposals
- 与检测头共享 backbone
- Anchor 机制覆盖多尺度多比例

RPN 对每个 anchor 预测：

- objectness（前景/背景）
- bbox 偏移 $(t_x,t_y,t_w,t_h)$

bbox 参数化：

$$
t_x=\frac{x^\star-x}{w},\ 
t_y=\frac{y^\star-y}{h},\ 
t_w=\log\frac{w^\star}{w},\ 
t_h=\log\frac{h^\star}{h}
$$

### 3.3.1 R-CNN / Fast R-CNN / Faster R-CNN 详细讲解

先记主线：三代方法本质都在做两件事

1. 找候选区域（proposal）
2. 对区域做分类 + 框回归

差异在于：`proposal 怎么来`、`卷积特征是否共享`、`能否端到端训练`。

#### A. R-CNN（2014）：把 CNN 首次成功引入检测

为什么出现：  
传统 HOG/DPM 表达能力不够，R-CNN 用预训练 CNN 特征替代手工特征，大幅提升精度。

流程（四步）：

1. 用 Selective Search 生成约 2k proposals
2. 每个 proposal 裁剪/warp 到固定大小（如 224x224）
3. 每个 proposal 单独跑一遍 CNN，取 fc 特征
4. 类别 SVM 分类 + 类别相关 bbox 回归

训练是分阶段的：

1. 先在分类数据上预训练 CNN
2. 再在检测数据上 fine-tune CNN
3. 冻结特征后训练每类 SVM
4. 最后训练 bbox regressor

优点：

- 精度相对传统方法显著提升（里程碑）

缺点（致命）：

1. 极慢：每张图每个 proposal 都要独立 CNN forward
2. 存储开销大：常把每个 proposal 特征离线落盘
3. 训练管线碎片化：多阶段，不是端到端

一句话：`精度上去了，但计算和工程代价太高`。

#### B. Fast R-CNN（2015）：共享卷积，解决“重复计算”

核心改进：

1. 整张图只做一次 CNN，得到 feature map
2. proposal 映射到 feature map 上，用 RoI Pooling 取固定尺寸特征
3. 在一个网络里同时做 softmax 分类和 bbox 回归（multi-task）

RoI Pooling 做什么：

- 输入任意大小 RoI
- 划分为固定网格（如 7x7）
- 每格 max pooling
- 输出固定形状特征给全连接层

多任务损失（常见形式）：

$$
L = L_{cls}(p,u) + \lambda\mathbf{1}[u\ge1]L_{loc}(t^u,t^\star)
$$

直觉：背景只算分类损失，前景再算定位损失。

Fast R-CNN 相比 R-CNN 的提升：

1. 速度快很多（卷积共享）
2. 不需要离线存储 proposal 特征
3. 能端到端训练检测头

仍有瓶颈：

- proposal 还依赖 Selective Search（CPU 慢），整体被外部 proposal 拖住

一句话：`检测网络快了，但 proposal 仍慢`。

#### C. Faster R-CNN（2015）：把 proposal 也学出来

核心创新：RPN（Region Proposal Network）

1. 在共享 feature map 上滑动小网络（常见 3x3 conv）
2. 每个位置放 k 个 anchors（尺度 + 长宽比组合）
3. 对每个 anchor 预测：
- objectness（前景/背景）
- bbox offset（4 个回归量）
4. 经 NMS 筛出高质量 proposals，送入 RoI Pooling + 检测头

anchor 机制作用：

- 显式覆盖多尺度与多长宽比
- 网络只需学习“相对偏移”，比直接生框更稳定

RPN 标注规则（经典）：

- 正样本：IoU > 0.7 或与某 GT 最高 IoU
- 负样本：IoU < 0.3

RPN 损失（常见写法）：

$$
L(\{p_i\},\{t_i\})=
\frac{1}{N_{cls}}\sum_i L_{cls}(p_i,p_i^\star)+
\lambda\frac{1}{N_{reg}}\sum_i p_i^\star L_{reg}(t_i,t_i^\star)
$$

其中 $p_i^\star=1$ 才计算回归项。

训练方式（论文经典）：四步交替训练（RPN 与 Fast R-CNN 交替微调）；工程上也常见近似联合训练。

优势：

1. proposal 几乎“免费”（共享 backbone）
2. 真正形成统一高效的两阶段检测框架
3. 精度和速度都很均衡，长期作为强基线

#### D. 三者对比（考试直接背）

1. `R-CNN`：proposal 外部 + 每个 proposal 独立 CNN  
优点：首次把深度特征引入检测并大幅提精度  
缺点：慢、重、非端到端

2. `Fast R-CNN`：proposal 外部 + 全图共享卷积 + RoI Pooling  
优点：大幅加速，训练更统一  
缺点：仍受 Selective Search 速度限制

3. `Faster R-CNN`：proposal 内生（RPN）+ 共享特征  
优点：速度/精度/工程性最平衡，经典两阶段范式  
缺点：相较单阶段（如 YOLO）通常仍更慢

可记成一句话：

`R-CNN 解决“特征不强”，Fast R-CNN 解决“重复卷积”，Faster R-CNN 解决“proposal 太慢”。`

#### E. 易错点补充

1. RPN 只做“前景/背景 + 框”，不做最终多类别识别。  
2. Anchor 不是最终框，只是参考框。  
3. RoI Pooling 有量化误差，RoI Align 是后续改进。  
4. 两阶段并不是“先分类后回归”，而是每个 RoI 上分类与回归联合学习。  
5. Faster R-CNN 是 two-stage：`RPN stage + RoI head stage`。

### 3.4 One-stage：YOLO / SSD

#### YOLO v1

- 把检测视作单次回归（grid 负责中心落入目标）
- 快（实时），但小目标与定位精度较弱

详细版（考试常问）：

核心思想：

1. 将图像划分为 `S x S` 网格
2. 若目标中心落在某 grid，该 grid 负责预测该目标
3. 每个 grid 预测 `B` 个框和 `C` 类概率

经典 v1 设定（VOC）：

- `S=7, B=2, C=20`
- 输出张量维度：$7\times7\times(B\cdot5+C)=7\times7\times30$

每个框输出：

$$
(x,y,w,h,\text{confidence})
$$

其中 `confidence` 常可理解为目标存在概率与定位质量（IoU）相关量。

YOLO v1 损失直觉：

1. 位置损失：中心点坐标误差
2. 尺寸损失：对 $w,h$ 用开方（减弱大框主导）
3. 置信度损失：区分有目标/无目标
4. 类别损失：只在负责目标的网格上计算

为何快：

- 单阶段，端到端，一次前向同时出分类与定位
- 不需要 RPN/Selective Search 这类外部 proposal

v1 局限（高频）：

1. 每个网格可表达目标数量有限，密集小目标吃亏
2. 对小目标和精细定位较弱
3. 用统一回归损失，分类/定位权衡不够细

一句话：YOLO 把检测从“proposal+分类”改成“全图直接回归”，速度极强。

### 3.4.1 YOLO 与 Faster R-CNN 对比速记

1. 范式：YOLO 单阶段；Faster R-CNN 两阶段  
2. 速度：YOLO 通常更快  
3. 精度：经典设定下 Faster R-CNN 通常更高（尤其小目标/定位）  
4. 工程取舍：实时场景偏 YOLO，高精度场景偏两阶段  
5. 共性：都依赖特征图上的位置语义，并都使用 NMS 做后处理

#### SSD

- default boxes（anchor）
- 多层 feature map 多尺度预测
- hard negative mining 缓解正负不平衡

结论：比 YOLO v1 更稳，精度速度折中更好。

### 3.5 FPN 与类别不平衡

#### FPN

- top-down + lateral connection
- 融合“深层语义强”和“浅层分辨率高”
- 多尺度检测几乎标配组件

#### Focal Loss（RetinaNet）

$$
\mathrm{FL}(p_t)=-\alpha_t(1-p_t)^\gamma\log(p_t)
$$

目的：降低易分类负样本权重，强调难例，提升 one-stage 精度。

---

## 4. 高频考点清单（冲刺版）

- `Harris` 与 `SIFT` 的关系与区别（尺度不变性来自哪里）
- `BoW` 的局限，`SPM` 如何补空间信息
- `SIFT -> BoW -> SPM -> SVM` 经典识别流水线
- `PMK` 与 `SPM` 关系（一般集合核 vs 图像空间特化）
- `K-means / Mean Shift / Ncut` 的建模差异
- `GraphCut` 的 unary/pairwise 含义与 maxflow 求解思想
- `GrabCut` 为什么实用（bbox + GMM + 迭代）
- Matting 方程 `I=\alpha F+(1-\alpha)B` 的欠定性来源
- `HOG+SVM` 管线与 hard negative mining
- HOG 经典参数与 `3780` 维来源
- `Viola-Jones` 为什么快（积分图 + Boost + Cascade）
- AdaBoost 特征筛选机制（错率最小 + 权重更新）
- `R-CNN -> Fast -> Faster` 每一步解决的瓶颈
- `RPN + Anchor + Proposal + NMS` 全流程
- `YOLO/SSD/Faster` 的精度速度取舍
- `FPN` 的结构与作用
- `Focal Loss` 解决的一阶段类别不平衡问题

---

## 5. 易混点速记

- `Anchor` 不是最终框，是参考框；回归后才是 proposal/pred box。
- `RoI Pooling` 有量化误差，`RoI Align` 用插值缓解。
- `NMS` 是后处理去重，不是训练损失。
- `IoU` 用于匹配与评估，和分类分数不是同一件事。
- `BoW` 是统计词频，不建模词序；`SPM` 通过网格层次加入粗空间结构。
- `GraphCut` 是二值标签优化；`Matting` 是连续 $\alpha$ 估计。

---

## 6. 最后 1 天背诵顺序（建议）

1. 检测主线：Viola-Jones → HOG/DPM → R-CNN 家族 → YOLO/SSD/FPN/RetinaNet  
2. 识别主线：Harris → SIFT → BoW → SPM  
3. 像素主线：K-means/MeanShift/Ncut → GraphCut/GrabCut → Matting/Inpainting  
4. 把所有“高频公式”默写一遍（IoU、Harris、Ncut、GraphCut、bbox reg、Focal Loss）
