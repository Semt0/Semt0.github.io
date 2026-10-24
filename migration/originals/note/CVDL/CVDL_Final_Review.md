---
title: CVDL 期末复习笔记（精炼版）
date: 2026-06-25
summary: |
  以 2026 CVDL 期末考试 12 道参考题为纲，串联 Recognition、Detection、Pixel Computing、Generative Models、3D Vision 等章节核心知识点，并附 3D Vision 计算题例题与解法总结。
key_points:
  - 12 道参考题的精简答案与关联知识点
  - 3D Vision 八点法计算题例题
  - 高频公式与易混点速查
---

## 0 复习策略与知识主线

### 0.1 先抓主线，再记细节

本课程可压缩成三条主线：

1. **识别主线**：局部特征（Harris / SIFT） → 量化聚合（BoW） → 加入空间（SPM） → 深度学习识别（AlexNet / VGG / ResNet）。
2. **检测主线**：滑窗 + 手工特征（HOG + SVM） → 两阶段深度检测（R-CNN / Fast / Faster） → 单阶段（YOLO / SSD / RetinaNet） → 多尺度（FPN）。
3. **像素 / 3D 主线**：像素聚类 / 图割 → 交互式分割 / Matting → 语义 / 实例分割 → 相机模型 → 双视图几何 → 重建与 Stereo。

考试 12 题基本覆盖这三条线，答题时先讲“任务 / 动机”，再讲“核心公式 / 流程”，最后讲“优缺点 / 与别的方法关系”。

### 0.2 名词缩写速查

| 缩写 | 含义 | 缩写 | 含义 |
|------|------|------|------|
| BoW | Bag-of-Words | SPM | Spatial Pyramid Matching |
| SIFT | Scale-Invariant Feature Transform | DoG | Difference of Gaussians |
| R-CNN | Regions with CNN features | RPN | Region Proposal Network |
| FPN | Feature Pyramid Network | IoU | Intersection over Union |
| GAN | Generative Adversarial Network | VAE | Variational AutoEncoder |
| Diffusion | 扩散模型 | LSTM | Long Short-Term Memory |
| Transformer | 自注意力架构 | ViT | Vision Transformer |
| DETR | Detection Transformer | Swin | Swin Transformer |
| F | Fundamental Matrix | E | Essential Matrix |
| DLT | Direct Linear Transform | SVD | Singular Value Decomposition |

---

## 1 题目精答

### 题目 1：深度神经网络中梯度后向传播的原理

**一句话**：反向传播（Back Propagation, BP）是用链式法则把损失函数对输出层的梯度逐层向前传递，从而计算每一层参数梯度的算法。

**详细过程**：

1. **前向传播**：输入 $x$ 经过各层计算得到预测 $\hat y$ 和损失 $L$。
2. **计算输出层梯度**：$\partial L / \partial \hat y$。
3. **链式法则回传**：对第 $l$ 层，已知 $\partial L / \partial z^{(l)}$，则

    $$
    \frac{\partial L}{\partial W^{(l)}} = \frac{\partial L}{\partial z^{(l)}} \cdot \frac{\partial z^{(l)}}{\partial W^{(l)}} = \delta^{(l)} \, a^{(l-1)\top},
    $$

    $$
    \frac{\partial L}{\partial b^{(l)}} = \delta^{(l)},
    $$

    其中 $z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}$，$a^{(l)} = \sigma(z^{(l)})$。
4. **误差向下一层传递**：

    $$
    \delta^{(l-1)} = \left(W^{(l)\top} \delta^{(l)}\right) \odot \sigma'(z^{(l-1)}).
    $$

**关键要点**：

- 本质是 **链式法则 + 动态规划**，避免重复计算。
- 对 RNN 同样适用，把时间展开后沿展开图反向传播，称为 **BPTT（BackPropagation Through Time）**。
- 深层网络容易出现梯度消失 / 爆炸，是 ResNet、LSTM 等结构出现的动机之一。

**关联**：

- LeNet-5 确立 CNN 基本结构；AlexNet 让深度网络实用化；ResNet 用残差连接缓解梯度消失。

---

### 题目 2：Visual Bag-of-Words 模型的基本思路

**一句话**：把图像看成一组局部特征描述子的集合，通过“视觉词典”量化成词频直方图，再用分类器（如 SVM）做识别。

**完整流程**：

1. **兴趣点检测**：在图像中找到稳定局部位置（如 Harris / SIFT / DoG 极值点）。
2. **局部特征提取**：每个兴趣点周围计算描述子（典型为 SIFT 128 维）。
3. **视觉词典学习**：用 K-means 对所有训练图像的描述子聚类，得到 $K$ 个视觉词中心 $c_1,\dots,c_K$。
4. **特征量化**：对每个描述子 $x_i$，找最近的视觉词

    $$
    q(x_i) = \arg\min_k \|x_i - c_k\|_2.
    $$
5. **直方图聚合**：统计每张图像中每个视觉词出现的频率

    $$
    h_k = \frac{1}{N}\sum_{i=1}^{N} \mathbf{1}[q(x_i)=k].
    $$
6. **分类**：用 $h = [h_1,\dots,h_K]^\top$ 训练 SVM 等分类器。

**为什么有效**：

- **局部性假设**：图像整体相似是因为局部模式统计分布相似。
- 对几何变化、遮挡、光照变化有一定鲁棒性。

**局限**：

- **丢失空间信息**：相同局部特征不同布局的图像会得到相同直方图。
- **量化误差**：硬分配导致边界信息损失。

**关联**：

- SPM 用空间金字塔解决空间信息丢失；VLAD / Fisher Vector 用高阶统计量缓解量化损失；深度网络用端到端卷积替代手工特征 + 词典。

---

### 题目 3：Harris Corner 的基本原理

**一句话**：Harris 角点检测器通过结构张量分析局部窗口向各方向移动时的强度变化，两个方向变化都大且接近的点被判定为角点。

**数学推导**：

1. 窗口向 $(u,v)$ 偏移时的强度变化：

    $$
    E(u,v) = \sum_{(x,y)\in W} w(x,y)[I(x+u,y+v)-I(x,y)]^2.
    $$

2. 一阶泰勒展开：

    $$
    E(u,v) \approx \begin{bmatrix} u & v \end{bmatrix} M \begin{bmatrix} u \\ v \end{bmatrix},
    $$

    其中结构张量为

    $$
    M = \sum_{(x,y)\in W} w(x,y) \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}.
    $$

3. Harris 响应函数（避免显式求特征值）：

    $$
    R = \det(M) - k \cdot \mathrm{tr}(M)^2.
    $$

4. 通过 $R$ 的阈值和非极大值抑制（NMS）得到角点。

**特征值解释**：

| 区域类型 | 特征值条件 | 说明 |
|----------|------------|------|
| 平坦区 | $\lambda_1 \approx \lambda_2 \approx 0$ | 各方向变化都小 |
| 边缘 | $\lambda_1 \gg \lambda_2 \approx 0$ | 仅垂直边缘方向变化大 |
| 角点 | $\lambda_1 \approx \lambda_2 \gg 0$ | 两个正交方向变化都大 |

**Shi-Tomasi 改进**：直接用 $R = \min(\lambda_1, \lambda_2)$，两个特征值都大于阈值才认为是好角点。

**局限**：

- **对尺度敏感**：固定窗口大小无法适应图像缩放，这是 SIFT 引入尺度空间的原因。

**关联**：

- Harris / Shi-Tomasi 是 KLT 跟踪中“好特征选择”的理论基础；SIFT 用 DoG + 尺度空间解决尺度敏感问题。

---

### 题目 4：Spatial Pyramid Matching 的基本原理

**一句话**：SPM 在 BoW 基础上把图像划分成多分辨率空间网格，在每个网格单元内独立统计 BoW 直方图，再拼接成固定长度向量，从而引入粗到细的空间布局信息。

**过程**：

1. 在 $L$ 个层次上划分图像：
    - Level 0：$1\times 1$（整幅图，等价于 BoW）
    - Level 1：$2\times 2$
    - Level 2：$4\times 4$
    - ...
2. 每个网格单元内独立做 BoW 量化并统计直方图。
3. 把所有层所有单元的直方图按固定顺序拼接。

**总维度**：

$$
\dim = K \sum_{l=0}^{L} 4^l = K \cdot \frac{4^{L+1}-1}{3}.
$$

例如 $K=200, L=2$ 时，维度为 $200 \times 21 = 4200$。

**为什么比 BoW 好**：

- 保留了粗到细的空间布局信息，能区分“相同局部特征但空间排布不同”的图像。

**权重**：

- 细层通常给更高权重（如 $w_l = 1/2^{L-l}$），因为定位更精确。

**关联**：

- PMK（Pyramid Match Kernel）是 SPM 的理论基础，用多分辨率直方图交集近似最优部分匹配；深度学习中的 SPP-Net 继承了空间金字塔池化思想。

---

### 题目 5：ResNet 的基本原理

**一句话**：ResNet 通过残差连接让网络学习“残差映射” $\mathcal{F}(x) = H(x) - x$，而不是直接学习完整映射 $H(x)$，从而缓解深层网络的梯度消失与退化问题。

**核心公式**：

$$
\mathcal{F}(x) = H(x) - x, \qquad y = \mathcal{F}(x) + x.
$$

**为什么有效**：

1. **梯度传播更顺畅**：残差连接提供 shortcut，梯度可以直接沿恒等映射回传，不易消失。
2. **不会比浅层网络差**：如果深层某层学不到更好特征，可以让 $\mathcal{F}(x) \approx 0$，等价于恒等映射，不会比浅层更差。
3. **可以训练非常深的网络**：从几十层到上百层都能训练。

**残差块结构**：

- 两个 / 三个卷积层 + BatchNorm + ReLU
- 输入 $x$ 通过 shortcut 与卷积输出相加
- 最后再过一次 ReLU

**关联**：

- VGG：深度串行堆叠；GoogLeNet / Inception：多分支并行；DenseNet：进一步用密集连接复用特征。
- ResNet 成为现代检测 / 分割 backbone（Faster R-CNN、FPN、RetinaNet 等）的标准选择。

---

### 题目 6：目标检测中 Cascade 方法的基本原理

**一句话**：Cascade 把多个分类器按复杂度逐级排列，前几级用极少计算快速拒绝大量简单负样本，后几级逐步加强对难分样本的判别，从而在保持高检测率的同时把误检率压到极低。

**典型代表**：Viola-Jones 人脸检测中的 Attentional Cascade。

**核心思想**：

- 大多数窗口是负样本，应尽早被简单分类器淘汰。
- 每级追求高召回（不错杀正样本），允许一定误检率；因为正样本稀少，所以整体误检率会乘法级下降。

**整体指标（乘法效应）**：

$$
D_{\text{all}} = \prod_i d_i, \qquad F_{\text{all}} = \prod_i f_i,
$$

其中 $d_i$ 是第 $i$ 级检测率，$f_i$ 是第 $i$ 级误检率。

**例子**：10 级级联，每级 $d_i \approx 0.99, f_i \approx 0.30$，则

- 整体检测率 $\approx 0.99^{10} \approx 0.9$
- 整体误检率 $\approx 0.3^{10} \approx 6 \times 10^{-6}$

**为什么快**：

1. Haar-like 矩形特征计算简单。
2. 积分图让任意矩形和 O(1) 计算。
3. AdaBoost 从海量特征中挑选有效少数。
4. Cascade 让大部分窗口在前几级就被拒绝，平均每个窗口只评估约 10 个特征。

**关联**：

- Cascade 是“如何在保证精度的前提下提速”的经典工程思想；现代 two-stage 检测器（Faster R-CNN）的 RPN + detection head 也有类似“先粗筛再精修”的级联精神。

---

### 题目 7：Faster R-CNN 的基本设计

**一句话**：Faster R-CNN = Fast R-CNN + RPN，把候选区域生成也交给神经网络，并与检测头共享 backbone 特征，形成端到端的两阶段检测框架。

**演进脉络**：

| 方法 | proposal 来源 | 卷积共享 | 训练方式 |
|------|--------------|----------|----------|
| R-CNN | Selective Search（外部） | 否（每个 proposal 单独 CNN） | 多阶段 |
| Fast R-CNN | Selective Search（外部） | 是（整图一次卷积） | 端到端检测头 |
| Faster R-CNN | RPN（网络内部） | 是 | 四步交替 / 近似联合训练 |

**核心组件**：

1. **Backbone**：提取整张图像的 feature map。
2. **RPN（Region Proposal Network）**：
    - 在共享 feature map 上滑动 3x3 小网络。
    - 每个位置预设 $k$ 个 anchors（典型 3 尺度 × 3 长宽比 = 9）。
    - 对每个 anchor 预测：
        - **objectness**：前景 / 背景二分类
        - **bbox 偏移** $(t_x, t_y, t_w, t_h)$
    - 经 NMS 筛选后输出约 2000 个 proposals。
3. **RoI Pooling**：把不同大小的 proposal 映射成固定尺寸特征。
4. **Detection Head**：对每个 RoI 做类别分类和 bounding box 回归。

**Anchor 到预测框的参数化**：

$$
\begin{aligned}
t_x &= \frac{x^\star - x}{w}, & t_y &= \frac{y^\star - y}{h}, \\
t_w &= \log\frac{w^\star}{w}, & t_h &= \log\frac{h^\star}{h}.
\end{aligned}
$$

**RPN 损失**：

$$
L = \frac{1}{N_{\text{cls}}}\sum_i L_{\text{cls}}(p_i, p_i^\star) + \lambda \frac{1}{N_{\text{reg}}}\sum_i p_i^\star L_{\text{reg}}(t_i, t_i^\star).
$$

**优势**：

- proposal 生成几乎“免费”（共享 backbone）。
- 精度高，成为两阶段检测的经典基线。

**关联**：

- YOLO / SSD：单阶段直接回归，速度更快但精度通常略低。
- FPN：解决多尺度问题，常与 Faster R-CNN 结合。
- Mask R-CNN：在 Faster R-CNN 上加 mask 分支做实例分割，并用 RoIAlign 替代 RoIPool 解决量化误差。

---

### 题目 8：Mean Shift 算法求解图像分割问题的基本原理和过程

**一句话**：Mean Shift 是一种基于密度峰值的 mode-seeking 算法，通过把每个样本点反复移动到其局部邻域的加权均值位置，最终收敛到密度模态，落入同一模态吸引域的点归为一类。

**核心公式**：

局部加权均值：

$$
m(x) = \frac{\sum_j K\!\left(\frac{\|x_j - x\|^2}{h^2}\right) x_j}{\sum_j K\!\left(\frac{\|x_j - x\|^2}{h^2}\right)}.
$$

Mean Shift 向量：

$$
v(x) = m(x) - x.
$$

**与 KDE 的关系**：

- Mean Shift 向量的方向与核密度估计（KDE）的梯度方向一致，因此它本质上是 **带自适应步长的梯度上升**，在找概率密度函数的局部极大值。

**分割流程**：

1. 把每个像素表示成特征空间中的点（常用 $(r,g,b,x,y)$ 或 $(L,a,b,x,y)$）。
2. 对每个点，在当前位置放置核窗口（带宽 $h$）。
3. 计算窗口内样本的加权均值 $m(x)$，把中心移到 $m(x)$。
4. 重复直到收敛到某个 mode。
5. 收敛到同一 mode 的点归为同一区域。

**关键参数**：

- **带宽 $h$**：决定分割粒度。
    - $h$ 小：mode 多，分割细，易碎片化。
    - $h$ 大：mode 少，分割粗，易过合并。

**优缺点**：

- 优点：不需要预设类别数 $K$；能处理非球形簇。
- 缺点：对 $h$ 敏感；大数据集计算开销高。

**关联**：

- Mean Shift 也用于目标跟踪（Mean-Shift Tracking），在下一帧中找与目标描述子分布最相似的候选区域；K-means 分割需要预设 $K$，且偏好球形簇。

---

### 题目 9：Graph Cut 算法求解交互式图像分割问题的过程

**一句话**：Graph Cut 把交互式分割建模为图上的二值 MRF 能量最小化问题，数据项来自用户标注的前 / 背景颜色模型，平滑项鼓励相邻相似像素标签一致，最后用 s-t min-cut / max-flow 求解最优标签。

**能量函数**：

$$
E(L) = \sum_i D_i(L_i) + \sum_{(i,j)\in \mathcal{E}} V_{ij}(L_i, L_j),
$$

其中 $L_i \in \{0,1\}$（背景 / 前景）。

**两项含义**：

- **数据项 $D_i(L_i)$**：像素 $i$ 属于标签 $L_i$ 的代价，通常用前景 / 背景颜色模型（如直方图或 GMM）的负对数似然。
- **平滑项 $V_{ij}(L_i, L_j)$**：相邻像素标签不一致时的惩罚，常用

    $$
    V_{ij}(L_i, L_j) = \lambda \, [L_i \neq L_j] \exp\!\left(-\beta \|I_i - I_j\|^2\right).
    $$

    颜色越接近，惩罚越大；强边缘处惩罚小，允许切割沿边界通过。

**交互方式**：

- 用户用 strokes 标注部分前景和背景像素。
- 被标注像素的标签硬约束到图中（连向 source / sink 的无穷大 / 大权重边）。

**求解**：

- 把 MRF 能量转化为 s-t 图的最小割问题。
- 用 max-flow / min-cut 算法在多项式时间内求解全局最优。

**GrabCut 扩展**：

- 用 bounding box 初始化，减少用户交互。
- 用 GMM 建模前景 / 背景颜色分布。
- 迭代：GMM 估计 → Graph Cut 分割 → 重新估计 GMM，直到收敛。

**关联**：

- Graph Cut 是二值标签优化；Matting 是连续 $\alpha$ 估计；Ncut 是无监督图分割，用特征向量求解。

---

### 题目 10：GAN 的基本模型图、目标函数和优化方法

**一句话**：GAN 由生成器 $G$ 和判别器 $D$ 组成对抗博弈，$G$ 从噪声 $z$ 生成样本并试图骗过 $D$，$D$ 试图区分真实样本与生成样本。

**基本结构**：

```
       z ~ p(z)                      x ~ p_data(x)
          |                                 |
          v                                 v
    [Generator G]                    [Real Data]
          |                                 |
          v                                 v
    G(z) = fake                       real sample
          \                               /
           \                             /
            v                           v
         [Discriminator D]  ──→  output: 1 (real) or 0 (fake)
```

**目标函数（Minimax）**：

$$
\min_G \max_D V(D,G) = \mathbb{E}_{x\sim p_{\text{data}}} [\log D(x)] + \mathbb{E}_{z\sim p(z)} [\log(1-D(G(z)))].
$$

**优化过程**：

1. 固定 $G$，更新 $D$：最大化判别真实与生成样本的能力。
2. 固定 $D$，更新 $G$：最小化 $\log(1-D(G(z)))$（工程上常用 $-\log D(G(z))$ 避免早期梯度消失）。
3. 交替迭代。

**典型问题**：

- **梯度消失**：$D$ 太强时 $G$ 梯度很小。
- **Mode Collapse**：$G$ 只生成少数几类样本。

**关联**：

- VAE：显式建模概率分布，通过 KL 正则化学习可采样 latent space；Diffusion：逐步去噪生成，训练更稳定。

---

### 题目 11：八点法求解 Fundamental Matrix $F$ 的过程

**一句话**：八点法利用 8 对（或更多）对应点在两张未标定图像上的坐标，通过线性约束 $x'^\top F x = 0$ 构造线性方程组，再用 SVD 求解 Fundamental Matrix。

**完整推导**：

1. **极线约束**：

    对于一对对应点 $x = [u, v, 1]^\top$ 和 $x' = [u', v', 1]^\top$，满足

    $$
    x'^\top F x = 0.
    $$

2. **Kronecker 展开**：

    设 $F$ 的 9 个元素为向量 $f = [F_{11}, F_{12}, F_{13}, F_{21}, F_{22}, F_{23}, F_{31}, F_{32}, F_{33}]^\top$，则每对点提供一条线性方程：

    $$
    [u'u,\ u'v,\ u',\ v'u,\ v'v,\ v',\ u,\ v,\ 1] \, f = 0.
    $$

3. **构造 $A$ 矩阵**：

    对 $N$ 对点， stacking 得到

    $$
    A = \begin{bmatrix}
    u_1' u_1 & u_1' v_1 & u_1' & v_1' u_1 & v_1' v_1 & v_1' & u_1 & v_1 & 1 \\
    \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
    u_N' u_N & u_N' v_N & u_N' & v_N' u_N & v_N' v_N & v_N' & u_N & v_N & 1
    \end{bmatrix} \in \mathbb{R}^{N \times 9},
    $$

    求解 $A f = 0$。

4. **SVD 求解**：

    对 $A$ 做 SVD：$A = U \Sigma V^\top$。最小奇异值对应的右奇异向量 $v_9$ 即为 $f$ 的解，重排成 $3 \times 3$ 矩阵 $\hat F$。

5. **强制秩 2 约束**：

    真实的 $F$ 秩为 2。对 $\hat F$ 再做 SVD：$\hat F = U \Sigma V^\top$，然后把最小奇异值置 0：

    $$
    F = U \, \mathrm{diag}(\sigma_1, \sigma_2, 0) \, V^\top.
    $$

**为什么叫“八点法”**：

- $F$ 有 7 个自由度（$3\times 3$ 齐次矩阵，秩 2 约束再减 1）。
- 理论上 7 对点即可求解，但 8 点法把问题线性化，更稳定实用。
- 实际中通常用 8 对以上点 + RANSAC 抗外点。

**与 Essential Matrix 的关系**：

- Essential Matrix $E$ 用于已标定相机（归一化相机坐标），$E = [t]_\times R$。
- Fundamental Matrix $F$ 用于未标定相机（像素坐标），二者关系为 $E = K'^\top F K$。

**3D Vision 计算题专题见第 3 节**。

---

### 题目 12：扩散模型的基本模型图、目标函数和优化方法

**一句话**：扩散模型通过前向过程逐步给数据加噪，再学习反向过程逐步去噪，从纯噪声中恢复数据；训练目标通常是预测噪声或预测 $x_0$ 的变分下界。

**基本结构**：

```
x_0 ──→ x_1 ──→ x_2 ──→ ... ──→ x_T  (forward: 加噪，固定)
                                     ↑
                                     │
                              纯噪声 ~ N(0,I)
                                     │
x_0 ←── x_1 ←── x_2 ←── ... ←── x_T  (reverse: 去噪，学习)
```

**前向过程（Fixed）**：

$$
q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t I).
$$

通过重参数化，可以直接采样任意时刻 $t$：

$$
x_t = \sqrt{\bar\alpha_t} x_0 + \sqrt{1 - \bar\alpha_t} \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I),
$$

其中 $\alpha_t = 1 - \beta_t$，$\bar\alpha_t = \prod_{s=1}^t \alpha_s$。

**反向过程（Learned）**：

模型学习条件分布

$$
p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t)).
$$

**训练目标（简化版）**：

常见做法是训练网络 $\\epsilon_\theta$ 预测前向过程中加入的噪声：

$$
\mathcal{L} = \mathbb{E}_{x_0, t, \epsilon} \left[ \|\epsilon - \epsilon_\theta(x_t, t)\|^2 \right].
$$

**采样过程**：

1. 从 $x_T \sim \mathcal{N}(0,I)$ 开始。
2. 对 $t = T, T-1, \dots, 1$，迭代

    $$
    x_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( x_t - \frac{1-\alpha_t}{\sqrt{1-\bar\alpha_t}} \epsilon_\theta(x_t, t) \right) + \sigma_t z,
    $$

    其中 $z \sim \mathcal{N}(0,I)$（当 $t>1$）。

**Latent Diffusion**：

- 先在 autoencoder / VAE 压缩后的 latent space 做 diffusion，降低计算量。
- Stable Diffusion、Sora 等现代系统多采用此路线。

**与 GAN / VAE 对比**：

| 模型 | 生成方式 | 优势 | 劣势 |
|------|----------|------|------|
| VAE | 从 prior 采样 → decoder | 可解释、可插值 | 样本质量中等 |
| GAN | 一次性从噪声生成 | 样本锐利 | 训练不稳定、mode collapse |
| Diffusion | 多步去噪 | 质量高、训练稳定 | 采样步数多 |

---

## 2 高频知识点串联

### 2.1 识别：从 Harris / SIFT 到 ResNet

**演进链**：

1. **Harris**：用结构张量找角点，**尺度敏感**。
2. **SIFT**：在尺度空间用 DoG 找关键点，分配主方向，构造 128 维描述子，具备 **尺度、旋转、光照不变性**。
3. **BoW**：把 SIFT 描述子量化成视觉词直方图，丢失空间信息。
4. **SPM**：在金字塔网格中统计 BoW，加入空间布局。
5. **深度识别**：AlexNet → VGG → ResNet，端到端学习特征、量化和分类。

**经典流水线**：SIFT 提特征 → K-means 学视觉词典 → SPM 编码 → SVM 分类。

### 2.2 检测：从 HOG + SVM 到 Faster R-CNN / YOLO

**演进链**：

1. **Viola-Jones**：矩形特征 + 积分图 + AdaBoost + Cascade，实现实时人脸检测。
2. **HOG + SVM**：滑窗 + 梯度方向直方图 + 线性 SVM + hard negative mining + NMS。
3. **DPM**：root + parts + deformation penalty，用 Latent SVM 训练。
4. **R-CNN**：Selective Search + 每个 proposal 单独 CNN + SVM + bbox 回归（慢、非端到端）。
5. **Fast R-CNN**：整图一次卷积 + RoI Pooling + 多任务损失。
6. **Faster R-CNN**：RPN 内生 proposals + 共享 backbone + anchor 机制。
7. **YOLO / SSD**：单阶段直接回归，更快但早期精度较低。
8. **FPN + Focal Loss（RetinaNet）**：多尺度特征 + 解决类别不平衡，让单阶段达到两阶段精度。

### 2.3 像素级理解：从聚类到分割网络

**演进链**：

1. **K-means / Mean Shift**：无监督聚类分割，前者需预设 $K$，后者由 bandwidth 控制粒度。
2. **Ncut**：把分割看作图划分，解广义特征值问题 $(D-W)y = \lambda Dy$。
3. **GraphCut / GrabCut**：交互式二值分割，能量 = 数据项 + 平滑项，用 max-flow 求解。
4. **Matting**：$I = \alpha F + (1-\alpha)B$，从二值 mask 升级到连续透明度，Poisson Matting 在梯度域求解。
5. **FCN / SegNet / DeepLab / Mask R-CNN**：深度网络端到端像素级预测，分别解决上采样、编码器-解码器、大感受野、实例分割等问题。

### 2.4 3D Vision：从相机模型到重建

**主线**：

1. **相机模型**：$x \sim PX$，$P = K[R \mid t]$。
2. **Epipolar Geometry**：对应点落在极线上，匹配从一维搜索。
3. **Essential / Fundamental Matrix**：$x'^\top E x = 0$（已标定），$x'^\top F x = 0$（未标定），$E = K'^\top F K$。
4. **两视图重建**：$F \to E \to (R,t) \to \text{triangulation}$，用 cheirality（正深度）筛选四组候选位姿。
5. **Stereo**：rectification 把极线拉水平，$Z = bf/d$，再用 block matching 或全局能量最小化求 disparity map。

### 2.5 序列与生成模型

**演进链**：

1. **RNN**：用隐状态压缩历史，BPTT 训练，长程依赖难。
2. **LSTM**：cell state + 门控机制，更稳定保留长期记忆。
3. **Seq2Seq + Attention**：动态选择相关上下文，不再压缩成固定向量。
4. **Transformer**：Self-Attention $= \mathrm{softmax}(QK^\top/\sqrt{d_k})V$，并行性强、全局依赖短。
5. **ViT / DETR / Swin**：把 Transformer 扩展到图像分类、检测和通用视觉 backbone。
6. **VAE / GAN / Diffusion**：三种主流生成范式，分别走概率编码、对抗博弈、逐步去噪路线。

---

## 3 3D Vision 计算题专题

### 3.1 八点法计算题：给定对应点求 Fundamental Matrix

**题目**：给定 8 对对应点（像素坐标）：

| 点 | 左图 $(u, v)$ | 右图 $(u', v')$ |
|----|--------------|----------------|
| 1 | $(100, 200)$ | $(120, 205)$ |
| 2 | $(300, 150)$ | $(310, 155)$ |
| 3 | $(150, 400)$ | $(165, 405)$ |
| 4 | $(500, 300)$ | $(515, 310)$ |
| 5 | $(200, 100)$ | $(215, 105)$ |
| 6 | $(400, 450)$ | $(420, 460)$ |
| 7 | $(600, 200)$ | $(620, 210)$ |
| 8 | $(50, 350)$ | $(60, 355)$ |

不考虑 $F$ 的尺度与矩阵秩问题，简述求解过程。

**解法**：

**Step 1：写出每对点的线性约束**

对每一对 $(u_i, v_i)$ 和 $(u_i', v_i')$，展开 $x'^\top F x = 0$：

$$
u_i' u_i F_{11} + u_i' v_i F_{12} + u_i' F_{13} + v_i' u_i F_{21} + v_i' v_i F_{22} + v_i' F_{23} + u_i F_{31} + v_i F_{32} + F_{33} = 0.
$$

**Step 2：构造 $A$ 矩阵**

把 8 个方程 stacking 成 $A \in \mathbb{R}^{8 \times 9}$：

$$
A = \begin{bmatrix}
u_1' u_1 & u_1' v_1 & u_1' & v_1' u_1 & v_1' v_1 & v_1' & u_1 & v_1 & 1 \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
u_8' u_8 & u_8' v_8 & u_8' & v_8' u_8 & v_8' v_8 & v_8' & u_8 & v_8 & 1
\end{bmatrix}.
$$

代入第一对点 $(100, 200), (120, 205)$：

$$
[120 \times 100,\ 120 \times 200,\ 120,\ 205 \times 100,\ 205 \times 200,\ 205,\ 100,\ 200,\ 1]
= [12000,\ 24000,\ 120,\ 20500,\ 41000,\ 205,\ 100,\ 200,\ 1].
$$

其余各行同理。

**Step 3：SVD 求解齐次线性方程组**

对 $A$ 做 SVD：

$$
A = U \Sigma V^\top.
$$

取最小奇异值对应的右奇异向量 $f = v_9$，重排成 $3 \times 3$ 矩阵：

$$
\hat F = \begin{bmatrix}
f_1 & f_2 & f_3 \\
f_4 & f_5 & f_6 \\
f_7 & f_8 & f_9
\end{bmatrix}.
$$

**Step 4（若题目要求真实 $F$）：强制秩 2**

对 $\hat F$ 再做 SVD：$\hat F = U \Sigma V^\top$，令

$$
F = U \, \mathrm{diag}(\sigma_1, \sigma_2, 0) \, V^\top.
$$

此时 $F$ 满足真实 Fundamental Matrix 的秩 2 约束。

**Step 5：验证**

任取一对点，例如第 1 对，计算 $x'^\top F x$，结果应接近 0（在数值误差范围内）。

---

### 3.2 八点法计算题解法总结

**核心步骤口诀**：

> 一对一点一条线，九点未知八对解；
> SVD 取最小奇异，再压秩二得真 $F$。

**详细 checklist**：

1. **坐标必须用齐次坐标**：$x = [u, v, 1]^\top$，$x' = [u', v', 1]^\top$。
2. **每对点展开成一行 9 维向量**：

    $$
    [u'u,\ u'v,\ u',\ v'u,\ v'v,\ v',\ u,\ v,\ 1].
    $$

3. **$A$ 矩阵维度**：$N \times 9$，$N$ 为点数；八点法 $N=8$，实际常用 $N \ge 8$ 并用 RANSAC。
4. **求解 $Af = 0$**：
    - SVD 取最小奇异值对应的右奇异向量。
    - 等价于最小化 $\|Af\|^2$，约束 $\|f\|=1$。
5. **强制秩 2**：真实 $F$ 秩为 2，所以再做一次 SVD 并把最小奇异值置 0。
6. **尺度不定**：$F$ 只能确定到尺度，乘以非零常数仍是合法解。

**易错点**：

- 不要把 $x$ 和 $x'$ 的位置写反。公式是 $x'^\top F x = 0$，所以 $A$ 的每一行是先 $x'$ 坐标再 $x$ 坐标。
- 如果题目说“不考虑 $F$ 的尺度和矩阵秩的问题”，则做到 Step 3 即可；若要求真实 $F$，必须做秩 2 投影。
- 如果相机已标定，则应先归一化坐标 $x_K = K^{-1} x$，再求 Essential Matrix $E$。

---

### 3.3 Essential Matrix 与相机位姿分解（计算题补充）

**若已知 $E$ 或 $F$ 且内参已知，如何求相对位姿 $(R, t)$？**

1. 由 $F$ 求 $E$：

    $$
    E = K'^\top F K.
    $$

2. 对 $E$ 做 SVD：

    $$
    E = U \Sigma V^\top.
    $$

3. 构造两个候选旋转：

    $$
    R_1 = U \begin{bmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix} V^\top,
    \qquad
    R_2 = U \begin{bmatrix} 0 & 1 & 0 \\ -1 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix} V^\top.
    $$

4. 平移方向为 $t = \pm u_3$（$U$ 的第三列）。

5. 共得到 4 组 $(R, t)$ 候选解，用 **cheirality constraint**（三角化后点在两相机前方）筛选唯一正确解。

**三角化公式**：

已知 $P = K[I \mid 0]$，$P' = K'[R \mid t]$，对对应点 $x, x'$，解

$$
\begin{bmatrix}
u P_{3\cdot} - P_{1\cdot} \\
v P_{3\cdot} - P_{2\cdot} \\
u' P'_{3\cdot} - P'_{1\cdot} \\
v' P'_{3\cdot} - P'_{2\cdot}
\end{bmatrix} X = 0,
$$

再用 SVD 求 $X$。

---

### 3.4 Stereo 深度计算题

**题目**：平行双目系统，基线 $b = 10\,\text{cm}$，焦距 $f = 500\,\text{pixels}$，某点在左右图中的水平坐标分别为 $u_L = 320$，$u_R = 290$，求该点深度 $Z$。

**解法**：

视差

$$
d = u_L - u_R = 320 - 290 = 30\,\text{pixels}.
$$

深度

$$
Z = \frac{b f}{d} = \frac{10 \times 500}{30} = \frac{5000}{30} \approx 166.67\,\text{cm}.
$$

**注意单位统一**：若 $b$ 用 cm，$f$ 用 pixels，则 $Z$ 的单位为 cm（因为 $d$ 无量纲比例，其实更准确是 $b$ 和 $Z$ 同单位，$f$ 和 $d$ 同单位）。

---

## 4 高频公式速查

### 4.1 识别与特征

**Harris 响应**：

$$
R = \det(M) - k \cdot \mathrm{tr}(M)^2.
$$

**SIFT 描述子维度**：

$$
4 \times 4 \times 8 = 128.
$$

**BoW 直方图**：

$$
h_k = \frac{1}{N}\sum_{i=1}^N \mathbf{1}[q(x_i)=k].
$$

**SPM 维度**：

$$
K \cdot \frac{4^{L+1}-1}{3}.
$$

### 4.2 检测

**IoU**：

$$
\mathrm{IoU}(B, \hat B) = \frac{|B \cap \hat B|}{|B \cup \hat B|}.
$$

**Faster R-CNN bbox 回归**：

$$
\begin{aligned}
t_x &= \frac{x^\star - x}{w}, & t_y &= \frac{y^\star - y}{h}, \\
t_w &= \log\frac{w^\star}{w}, & t_h &= \log\frac{h^\star}{h}.
\end{aligned}
$$

**Focal Loss**：

$$
\mathrm{FL}(p_t) = -\alpha_t (1-p_t)^\gamma \log(p_t).
$$

### 4.3 像素级理解

**GraphCut 能量**：

$$
E(L) = \sum_i D_i(L_i) + \sum_{(i,j)} V_{ij}(L_i, L_j).
$$

**Ncut**：

$$
\mathrm{Ncut}(A,B) = \frac{\mathrm{cut}(A,B)}{\mathrm{assoc}(A,V)} + \frac{\mathrm{cut}(A,B)}{\mathrm{assoc}(B,V)}.
$$

**广义特征值问题**：

$$
(D-W)y = \lambda Dy.
$$

**Matting 方程**：

$$
I = \alpha F + (1-\alpha)B.
$$

**语义分割 IoU**：

$$
\mathrm{IoU} = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}+\mathrm{FN}}.
$$

### 4.4 生成模型

**VAE 损失**：

$$
\mathcal{L}_{\text{VAE}} = \mathbb{E}_{q_\phi(z|x)}[-\log p_\theta(x|z)] + \mathrm{KL}(q_\phi(z|x) \| p(z)).
$$

**重参数化技巧**：

$$
z = \mu + \sigma \odot \epsilon, \qquad \epsilon \sim \mathcal{N}(0,I).
$$

**GAN 目标函数**：

$$
\min_G \max_D \mathbb{E}_{x\sim p_{\text{data}}}[\log D(x)] + \mathbb{E}_{z\sim p(z)}[\log(1-D(G(z)))].
$$

**Diffusion 前向采样**：

$$
x_t = \sqrt{\bar\alpha_t} x_0 + \sqrt{1-\bar\alpha_t} \epsilon.
$$

### 4.5 3D Vision

**相机矩阵**：

$$
P = K[R \mid t].
$$

**极线约束**：

$$
x'^\top F x = 0, \qquad x'^\top E x = 0 \text{（已标定）}.
$$

**Essential Matrix**：

$$
E = [t]_\times R.
$$

**Fundamental 与 Essential 关系**：

$$
E = K'^\top F K.
$$

**Stereo 深度**：

$$
Z = \frac{bf}{d}.
$$

**八点法 $A$ 矩阵每行**：

$$
[u'u,\ u'v,\ u',\ v'u,\ v'v,\ v',\ u,\ v,\ 1].
$$

---

## 5 易混点总结

| 对比项 | A | B | 关键区别 |
|--------|---|---|----------|
| Harris | SIFT | Harris 尺度敏感，SIFT 尺度不变 | 是否在尺度空间检测 |
| BoW | SPM | BoW 无空间信息，SPM 有空间金字塔 | 是否保留空间布局 |
| Homography | Essential/Fundamental | H 点到点，E/F 点到线 | 应用场景不同 |
| Essential | Fundamental | E 用于归一化相机坐标，F 用于像素坐标 | 是否已知内参 |
| GraphCut | Matting | GraphCut 二值标签，Matting 连续 $\alpha$ | 输出类型 |
| R-CNN | Fast R-CNN | Fast 共享卷积 + RoI Pooling | 是否每个 proposal 单独 CNN |
| Fast R-CNN | Faster R-CNN | Faster 用 RPN 替代 Selective Search | proposal 来源 |
| YOLO | Faster R-CNN | YOLO 单阶段回归，Faster 两阶段 | 速度与精度权衡 |
| RoIPool | RoIAlign | RoIPool 有量化误差，RoIAlign 双线性插值 | 空间对齐精度 |
| VAE | GAN | VAE 概率重构 + KL，GAN 对抗博弈 | 训练目标 |
| GAN | Diffusion | GAN 一次生成，Diffusion 多步去噪 | 生成过程 |
| RNN | Transformer | RNN 顺序递推，Transformer 自注意力并行 | 依赖路径与并行性 |
| FCN | Mask R-CNN | FCN 语义分割，Mask R-CNN 实例分割 | 是否区分同类不同实例 |

---

## 6 最后冲刺：建议背诵顺序

1. **先背 12 道题的框架**：每道题用“是什么 → 核心公式 / 流程 → 优缺点 / 关联”三段式回答。
2. **再背高频公式**：Harris、SPM 维度、IoU、GraphCut 能量、GAN 目标、八点法 $A$ 矩阵、$Z=bf/d$、Diffusion 前向采样。
3. **3D Vision 计算题**：默写八点法完整流程，并自己构造一组 8 对点练一次矩阵构造。
4. **易混点过一遍**：特别区分 E/F、RoIPool/Align、GraphCut/Matting、one-stage/two-stage。

---

**祝考试顺利！**
