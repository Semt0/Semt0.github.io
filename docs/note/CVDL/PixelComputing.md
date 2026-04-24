---
title: Pixel Computing - I
date: 2026-04-17
---


本讲内容围绕 **pixel-level understanding / pixel labeling** 展开：从无监督分割（聚类、图分割）到交互式抠图（GraphCut/GrabCut/Lazy Snapping），再到更细粒度的 **图像 Matting**，以及相关任务（co-segmentation、inpainting/completion）。

## 1 Pixel Computing 与 Pixel Labeling

![Pixel Computing - I](pictures/pixel_computing_slide_01.png){ width="650" }

![Outline](pictures/pixel_computing_slide_02.png){ width="650" }

“Pixel Labeling” 强调把一张图像理解到像素级别：每个像素都对应某种标签/解释（所属区域、前景/背景、透明度、语义类别、深度等）。

![Pixel Labeling](pictures/pixel_computing_slide_03.png){ width="650" }

从建模角度看，pixel labeling 常见有三类输出：

- **离散标签**：如前景/背景、语义类别（道路/行人/车）。
- **连续值**：如 matting 的 $\alpha$、深度估计值。
- **结构关系**：如像素之间是否应属于同一区域（图模型/能量模型中的 pairwise 关系）。

这也是为什么本讲会同时出现聚类、图割、MRF、PDE（Poisson）和 patch 匹配等不同技术路线：它们在“像素级决策”的角度上是同一问题的不同解法。

## 2 任务与应用图景

### 2.1 无监督分割（Unsupervised Segmentation）

无监督分割通常希望把图像分解为“连贯的区域”，作为后续处理（识别、交互、重建）的基础。

![Superpixel 动机](pictures/pixel_computing_slide_04.png){ width="650" }

![BSD 分割标注示意](pictures/pixel_computing_slide_05.png){ width="650" }

### 2.2 交互式抠图与 Matting

抠图（cutout）更关注“把目标从背景中分离出来”。当目标边界存在 **半透明/细毛发/反光** 时，需要 Matting（估计透明度 $\alpha$）而不只是二值分割。

![Blue/Green screen](pictures/pixel_computing_slide_06.png){ width="650" }

![User interaction as input](pictures/pixel_computing_slide_07.png){ width="650" }

![Image Matting for hair](pictures/pixel_computing_slide_08.png){ width="650" }

Matting 中常见输入是 **trimap**：明确标注“前景确定 / 背景确定 / 未知区域”。

![Trimap](pictures/pixel_computing_slide_09.png){ width="650" }

### 2.3 相关任务：Co-segmentation / Parsing / Depth / Inpainting

![Image Co-Segmentation](pictures/pixel_computing_slide_10.png){ width="650" }

![Image Parsing (semantic labeling)](pictures/pixel_computing_slide_11.png){ width="650" }

![Depth estimation as pixel labeling](pictures/pixel_computing_slide_12.png){ width="650" }

## 3 无监督分割：把 Segmentation 看成 Clustering

### 3.1 K-means（向量量化视角）

一个最直接的想法是：把像素映射为特征向量，然后做聚类。

![Segmentation as clustering](pictures/pixel_computing_slide_13.png){ width="650" }

仅用强度/颜色做聚类能得到“颜色一致”的簇，但不保证空间连贯：同色但分散在图像不同位置的像素可能被分到同一类。

![Intensity vs color based clusters](pictures/pixel_computing_slide_14.png){ width="650" }

![K-means segmentation example](pictures/pixel_computing_slide_15.png){ width="650" }

把空间坐标也加入特征（例如用 $(r,g,b,x,y)$）能显式地鼓励空间连贯性。

![Add (x,y) to enforce coherence](pictures/pixel_computing_slide_16.png){ width="650" }

K-means 的典型目标函数是最小化类内平方误差：

$$
\min_{\{\mu_k\}, \{z_i\}}
\sum_{i=1}^{n}\left\|x_i - \mu_{z_i}\right\|_2^2,
\quad z_i \in \{1,\dots,K\}
$$

其中 $x_i$ 是第 $i$ 个像素（或 superpixel）的特征，$\mu_k$ 是第 $k$ 个簇的中心。

K-means 在分割中的实际运行可总结为：

1. 初始化 $K$ 个簇中心（随机或 k-means++）。
2. 把每个像素分配给最近中心（assignment）。
3. 重新计算每个簇中心（update）。
4. 重复 2-3 直到簇中心变化很小或达到迭代上限。

在图像任务中，一个常见细节是 **特征归一化与权重平衡**。例如用 $(r,g,b,x,y)$ 时，若不缩放坐标，空间项或颜色项可能“压过”另一方，导致分割过碎或过粗。工程上常写成 $(r,g,b,\lambda x,\lambda y)$，用 $\lambda$ 控制空间连贯程度。

!!! info "K-means 的优缺点（分割场景）"
    优点：实现简单、收敛到局部最优、速度快。

    缺点：需要指定 $K$、对初始化/异常点敏感、偏好“球状簇”（各向同性），对复杂形状与尺度变化不鲁棒。

![K-means pros/cons](pictures/pixel_computing_slide_17.png){ width="650" }

### 3.2 Mean Shift（找密度模态）

Mean Shift 把聚类理解为“在特征空间的密度峰值（mode）附近聚合”，不需要预先指定簇数。

![Mean shift intro](pictures/pixel_computing_slide_18.png){ width="650" }

直觉：对每个点，从一个局部窗口出发，不断把窗口中心移动到窗口内数据的“质心”，最终会收敛到某个密度峰值；落入同一吸引域（attraction basin）的点属于同一簇。

如果写成公式，Mean Shift 的更新可理解为：

$$
x^{(t+1)} = \frac{\sum_j K\left(\frac{\|x_j-x^{(t)}\|^2}{h^2}\right)x_j}{\sum_j K\left(\frac{\|x_j-x^{(t)}\|^2}{h^2}\right)}
$$

其中 $h$ 是窗口尺度（bandwidth）。它几乎决定了结果粒度：

- $h$ 小：模态数量多，分割更细，容易碎片化。
- $h$ 大：模态数量少，分割更粗，可能把不同物体并到一起。

所以 Mean Shift 虽然“不用指定 $K$”，但并不等于“无参数”，其核心控制参数就是 bandwidth。

![Mean shift seeks modes](pictures/pixel_computing_slide_19.png){ width="650" }

![Mean shift step 1](pictures/pixel_computing_slide_20.png){ width="650" }

![Mean shift step 2](pictures/pixel_computing_slide_21.png){ width="650" }

![Mean shift step 3](pictures/pixel_computing_slide_22.png){ width="650" }

![Mean shift step 4](pictures/pixel_computing_slide_23.png){ width="650" }

![Mean shift step 5](pictures/pixel_computing_slide_24.png){ width="650" }

![Mean shift step 6](pictures/pixel_computing_slide_25.png){ width="650" }

![Mean shift convergence](pictures/pixel_computing_slide_26.png){ width="650" }

![Attraction basin / clustering](pictures/pixel_computing_slide_27.png){ width="650" }

Mean Shift 的流程可概括为：

![Mean shift algorithm steps](pictures/pixel_computing_slide_28.png){ width="650" }

![Mean shift segmentation results](pictures/pixel_computing_slide_29.png){ width="650" }

![More mean shift results](pictures/pixel_computing_slide_30.png){ width="650" }

![More mean shift results](pictures/pixel_computing_slide_31.png){ width="650" }

!!! info "Mean Shift 的优缺点"
    优点：不假设簇是球形、参数相对少（主要是窗口大小）、可得到可变数量的模态、对异常点相对鲁棒。

    缺点：对窗口大小敏感、计算开销大、特征维数升高后更难扩展。

![Mean shift pros/cons](pictures/pixel_computing_slide_32.png){ width="650" }

## 4 图分割：Normalized Cut（Ncut）

Normalized Cut 把分割建模为 **图的划分（graph partitioning）**：像素/超像素是节点，边权是相似度（affinity），希望切断“弱连接”而保留“强连接”。

![Ncut question](pictures/pixel_computing_slide_33.png){ width="650" }

![Graphical view](pictures/pixel_computing_slide_34.png){ width="650" }

![Edge weight as similarity](pictures/pixel_computing_slide_35.png){ width="650" }

![Cut through thin edges](pictures/pixel_computing_slide_36.png){ width="650" }

### 4.1 图表示与相似度（affinity）

![Images as graphs](pictures/pixel_computing_slide_37.png){ width="650" }

![Segmentation by graph partitioning](pictures/pixel_computing_slide_38.png){ width="650" }

常见相似度构造：把两点距离通过 Gaussian kernel 映射成亲和力：

$$
w_{ij} = \exp\left(-\frac{\mathrm{dist}(x_i,x_j)^2}{2\sigma^2}\right)
$$

![Affinity with Gaussian kernel](pictures/pixel_computing_slide_39.png){ width="650" }

尺度 $\sigma$ 决定“邻近”的范围：$\sigma$ 小只连接很近的点，$\sigma$ 大会把更远的点也连接起来。

实践里，相似度常同时考虑 **颜色差异 + 空间距离**，例如：

$$
w_{ij}
=
\exp\left(-\frac{\|I_i-I_j\|^2}{2\sigma_I^2}\right)
\exp\left(-\frac{\|p_i-p_j\|^2}{2\sigma_p^2}\right)
$$

并只在局部邻域连边（而非全连接图），否则图太大、存储和求解都会很重。

![Scale affects affinity](pictures/pixel_computing_slide_40.png){ width="650" }

### 4.2 Min-Cut 的问题与 Normalized Cut

最小割（min-cut）倾向于切掉很小、孤立的区域（因为切一小块的边权和可能很小），不符合“语义上合理的分割”。

![Graph cut and min cut](pictures/pixel_computing_slide_41.png){ width="650" }

![Minimum cut example](pictures/pixel_computing_slide_42.png){ width="650" }

![Minimum cut example](pictures/pixel_computing_slide_43.png){ width="650" }

Ncut 用归一化来抑制“切一小块”的偏置。设 $A,B$ 为两部分，$V$ 为全体节点：

- $\mathrm{cut}(A,B)=\sum_{i\in A, j\in B} w_{ij}$
- $\mathrm{assoc}(A,V)=\sum_{i\in A, j\in V} w_{ij}$

则：

$$
\mathrm{Ncut}(A,B)
=
\frac{\mathrm{cut}(A,B)}{\mathrm{assoc}(A,V)}
+
\frac{\mathrm{cut}(A,B)}{\mathrm{assoc}(B,V)}
$$

![Normalized cut motivation](pictures/pixel_computing_slide_44.png){ width="650" }

![Normalized cut cost](pictures/pixel_computing_slide_45.png){ width="650" }

![Ncut example](pictures/pixel_computing_slide_46.png){ width="650" }

### 4.3 松弛与特征向量解法（广义特征值问题）

令 $W$ 为邻接矩阵，$D$ 为度矩阵（$D_{ii}=\sum_j W_{ij}$）。对指示向量做连续松弛后，Ncut 的优化可转化为解广义特征值问题：

$$
(D-W)y = \lambda Dy
$$

通常取 **第二小** 特征值对应的特征向量作为划分依据（第一小对应平凡解）。

这里的“第二小特征向量”可理解为图上的“最平滑非平凡划分方向”：它让强连接节点取值更接近，弱连接两侧取值差异更大。再对该向量做阈值切分（如 0、median 或搜索最优阈值）即可得到二分结果。

![Ncut relaxation](pictures/pixel_computing_slide_47.png){ width="650" }

![Generalized eigenvalue problem](pictures/pixel_computing_slide_48.png){ width="650" }

Ncut 的基本算法流程：

![Ncut algorithm](pictures/pixel_computing_slide_49.png){ width="650" }

多类扩展常见做法：

- 递归二分（recursive bipartition）
- 取多个特征向量后做 k-means

![Ncut example](pictures/pixel_computing_slide_50.png){ width="650" }

![Ncut result](pictures/pixel_computing_slide_51.png){ width="650" }

!!! info "Normalized Cut 的优缺点"
    优点：框架通用，特征/相似度的定义灵活，能捕获全局一致性（相对局部聚类而言）。

    缺点：时间和存储开销大；存在倾向把图划成“大小相近”区域的偏置。

![Ncut pros/cons](pictures/pixel_computing_slide_52.png){ width="650" }

最后，讲义强调 Ncut 缺少“全局的前景/背景建模”能力，这也是后续交互式 GraphCut/GrabCut 的动机之一。

![What is missing](pictures/pixel_computing_slide_53.png){ width="650" }

## 5 交互式抠图：Graph Cut / GrabCut / Lazy Snapping

![Interactive cutout](pictures/pixel_computing_slide_54.png){ width="650" }

### 5.1 Boykov & Jolly：交互式 Graph Cut

GraphCut 典型输入是用户 strokes（例如蓝色表示前景、红色表示背景），目标是得到一个二值分割。

![User strokes](pictures/pixel_computing_slide_55.png){ width="650" }

![GraphCut formulation](pictures/pixel_computing_slide_56.png){ width="650" }

GraphCut 的能量函数常写为二元 MRF：

$$
E(L)
=
\sum_i D_i(L_i) + \sum_{(i,j)\in\mathcal{E}} V_{ij}(L_i,L_j)
$$

- $L_i\in\{0,1\}$ 表示像素 $i$ 的前景/背景标签
- $D_i$ 是 unary term（数据项/区域项），通常由颜色直方图或概率模型给出
- $V_{ij}$ 是 pairwise term（平滑项），鼓励相似且相邻的像素获得相同标签

一个常见的平滑项写法是：

$$
V_{ij}(L_i,L_j)=\lambda\,[L_i\neq L_j]\exp\left(-\beta\|I_i-I_j\|^2\right)
$$

含义是：当两个像素颜色很接近时，给它们不同标签会被更强惩罚；在强边缘（颜色突变处）惩罚变小，从而允许切割沿真实边界通过。

![Edge weights](pictures/pixel_computing_slide_57.png){ width="650" }

数据项可用用户标注区域的颜色统计（如直方图）来定义；平滑项常同时依赖颜色相似度与空间邻接。

![Unary + pairwise](pictures/pixel_computing_slide_58.png){ width="650" }

该类二值能量在满足一定条件时可转为 s-t min-cut / max-flow 求解。

![Binary energy + maxflow](pictures/pixel_computing_slide_59.png){ width="650" }

### 5.2 GrabCut：GMM + Iterated Graph Cut

GrabCut 用一个 bounding box 作为交互输入，避免用户精细描边；并用 GMM 建模前景/背景颜色分布，通过迭代（类似 EM）交替更新模型与分割。

![GrabCut](pictures/pixel_computing_slide_60.png){ width="650" }

![GMM color model](pictures/pixel_computing_slide_61.png){ width="650" }

GrabCut 的典型循环：

1. 用 bbox 初始化“可能前景/背景”集合
2. 分别对前景/背景拟合 GMM（通常 5–8 个高斯分量）
3. 用当前 GMM 得到每像素的 unary term（负对数似然）
4. 加上平滑项构图，做一次 graph cut 得到分割
5. 用新分割重新估计 GMM，继续迭代直到收敛

GrabCut 的关键价值在于把“用户交互负担”从精细描边降到“框选 + 少量修正笔刷”。在很多自然图像中，仅 bbox 初始化就能得到可用结果；困难样本再通过少量前/背景笔刷增强 GMM 的可分性。

![Iterated graph cut](pictures/pixel_computing_slide_62.png){ width="650" }

![Iterated graph cut](pictures/pixel_computing_slide_63.png){ width="650" }

![GrabCut result](pictures/pixel_computing_slide_64.png){ width="650" }

### 5.3 Lazy Snapping：更轻量的交互与加速

Lazy Snapping 依然基于 GraphCut，但强调交互式体验与速度：用户标注少量前景/背景 strokes，先做一次 Boykov & Jolly 风格 graphcut，再支持边界编辑（Edit Boundary）。

![Lazy Snapping](pictures/pixel_computing_slide_65.png){ width="650" }

![Lazy Snapping overview](pictures/pixel_computing_slide_66.png){ width="650" }

讲义中将其能量拆成两部分：

- $E_1(X)$：用 K-means 对已知前景/背景颜色聚类，得到代表色（辅助构建数据项）
- $E_2(X)$：与 Boykov & Jolly 类似的 MRF 能量（unary + pairwise），用 graph cut 求解

但逐像素 graphcut 在交互式 refinement 中可能太慢，因此引入 superpixels 做加速。

本质上，Lazy Snapping 通过“先过分割成区域单元，再在区域图上优化”减少变量规模。代价是边界精度受 superpixel 粒度影响，因此通常会保留边界编辑步骤来做局部修补。

![Lazy Snapping issue](pictures/pixel_computing_slide_67.png){ width="650" }

![Lazy Snapping speedup](pictures/pixel_computing_slide_68.png){ width="650" }

![More results](pictures/pixel_computing_slide_69.png){ width="650" }

## 6 Image Matting：从二值到连续透明度

### 6.1 合成模型与 matting 方程

Matting 用 $\alpha\in[0,1]$ 表示每个像素的透明度。合成模型是：

$$
I = \alpha F + (1-\alpha)B
$$

其中 $I$ 是观测像素颜色（RGB），$F$ 是前景颜色，$B$ 是背景颜色。

这个模型说明了 matting 与分割的核心区别：分割只决定“属于谁”，而 matting 还要估计“混合比例”。因此像头发丝、纱布、运动模糊边缘等场景，单纯二值 mask 往往会出现锯齿、黑边、漏抠。

![Matting and compositing](pictures/pixel_computing_slide_70.png){ width="650" }

![Matting equations](pictures/pixel_computing_slide_71.png){ width="650" }

二值分割可以看作 $\alpha\in\{0,1\}$ 的特殊情形；Matting 允许边界/细毛发区域出现连续过渡。

![Hard segmentation vs matting](pictures/pixel_computing_slide_73.png){ width="650" }

### 6.2 为什么 matting 难

单个像素的未知量很多：$F$（3 维）、$B$（3 维）、$\alpha$（1 维），总计 7 个未知量，但观测只有 $I$ 的 3 个通道。

![Why is matting hard](pictures/pixel_computing_slide_74.png){ width="650" }

![Why is matting hard](pictures/pixel_computing_slide_75.png){ width="650" }

![Why is matting hard](pictures/pixel_computing_slide_76.png){ width="650" }

![7 unknowns vs 3 knowns](pictures/pixel_computing_slide_77.png){ width="650" }

因此 Matting 必须引入额外信息，例如：

- trimap（已知前景/背景区域提供边界条件）
- 局部平滑/颜色线性模型等先验
- 多张不同背景的图像（蓝/绿幕或多背景拍摄）增加方程数

实际流程通常是：

1. 用户给 trimap（或由分割模型自动提供粗 trimap）。
2. 在未知区域估计 $\alpha$（和/或 $F,B$）。
3. 可选地再做前景颜色精修，避免合成时边缘发灰。

这也是工业流程里“分割模型 + matting 模型”常常串联使用的原因。

![Multiple backgrounds give more equations](pictures/pixel_computing_slide_79.png){ width="650" }

## 7 Poisson Matting（梯度域求解）

Poisson Matting 的核心思路是把问题转到梯度域：与其直接在颜色域估计 $\alpha$，不如估计（或构造）一个与真实 $\nabla \alpha$ 接近的向量场，然后通过 Poisson 方程恢复 $\alpha$。

![Poisson Matting](pictures/pixel_computing_slide_80.png){ width="650" }

![Gradient domain](pictures/pixel_computing_slide_81.png){ width="650" }

![Poisson Matting](pictures/pixel_computing_slide_82.png){ width="650" }

![Poisson Matting](pictures/pixel_computing_slide_83.png){ width="650" }

一个常见形式是解带 Dirichlet 边界条件的 Poisson 方程：

$$
\Delta \alpha = \mathrm{div}(v) \quad \text{in } \Omega
$$

$$
\alpha = 0 \ \text{on } \Omega_B,\quad \alpha = 1 \ \text{on } \Omega_F
$$

其中 $\Omega$ 是未知区域，$\Omega_F,\Omega_B$ 由 trimap 给出；$v$ 是从观测图像与 $F,B$ 估计得到的梯度场近似。

![Poisson formulation](pictures/pixel_computing_slide_84.png){ width="650" }

![Poisson Matting results](pictures/pixel_computing_slide_85.png){ width="650" }

## 8 Related Topics：Co-segmentation 与 Inpainting / Completion

### 8.1 Image Co-Segmentation

Co-segmentation 希望从一组图像中分割出“共同的前景对象”，即使背景不同。

![Co-segmentation task](pictures/pixel_computing_slide_86.png){ width="650" }

早期代表性工作通过加入 **全局约束（例如直方图匹配）** 把 “跨图像一致性” 融入 MRF 能量中。

![First work reference](pictures/pixel_computing_slide_87.png){ width="650" }

应用之一是更鲁棒的图像距离度量：用“共同前景”的匹配而不是整图的像素差异。

![Robust image distance](pictures/pixel_computing_slide_88.png){ width="650" }

![Robust image distance](pictures/pixel_computing_slide_89.png){ width="650" }

### 8.2 Image Inpainting / Image Completion

Inpainting/Completion 的目标是“把缺失区域补全到看起来真实且无缝”，常用于去除物体、修复照片等。

![Inpainting motivation](pictures/pixel_computing_slide_90.png){ width="650" }

![Examples](pictures/pixel_computing_slide_91.png){ width="650" }

![Examples](pictures/pixel_computing_slide_92.png){ width="650" }

![The difficulties](pictures/pixel_computing_slide_94.png){ width="650" }

直观上我们希望：

- 延拓进入洞区域的结构线（边缘、曲线）
- 用周围纹理在洞里“长”出来
- 无明显接缝/伪影

这类任务的难点在于“欠约束”：同一个洞可能有多种看起来都合理的补法。传统方法依赖局部统计与先验，而现代生成模型会进一步引入语义先验（例如“天空应该平滑、建筑边缘应连续”）。

![Intuitive solution](pictures/pixel_computing_slide_95.png){ width="650" }

#### 8.2.1 结构 vs 纹理

Inpainting 通常需要同时处理两类信息：结构（几何、边缘、曲线）与纹理（重复的局部模式）。

![Structure vs texture](pictures/pixel_computing_slide_98.png){ width="650" }

#### 8.2.2 Exemplar-based Inpainting（Criminisi et al.）

经典方法通过“从已知区域复制相似 patch”来填洞，填充顺序非常关键。

![Criminisi 2003](pictures/pixel_computing_slide_99.png){ width="650" }

![Onion skin order](pictures/pixel_computing_slide_100.png){ width="650" }

![Order is crucial](pictures/pixel_computing_slide_101.png){ width="650" }

简单的“洋葱皮”顺序（从边界往内一圈圈填）可能破坏线性结构。

![Onion skin may lose structure](pictures/pixel_computing_slide_102.png){ width="650" }

更好的策略是优先填那些处在结构延拓方向上的区域，让边缘/曲线先被补全。

![Filling order is crucial](pictures/pixel_computing_slide_103.png){ width="650" }

![Algorithm pipeline](pictures/pixel_computing_slide_104.png){ width="650" }

填充优先级通常由“置信度 + 数据项（结构强度）”构成（例如边界处强梯度方向的延拓给更高优先级）。

经典 Criminisi 优先级写作：

$$
P(p)=C(p)\,D(p)
$$

- $C(p)$（confidence）：该 patch 已知像素比例越高，说明可参考信息越可靠。
- $D(p)$（data term）：与等照线（isophote）延拓相关，倾向优先延续强结构。

因此它不是简单“从外向内填”，而是先补最能延续结构的边界位置。

![Determining filling priority](pictures/pixel_computing_slide_105.png){ width="650" }

![Onion skin vs structure keeping](pictures/pixel_computing_slide_106.png){ width="650" }

![Kanizsa triangle](pictures/pixel_computing_slide_107.png){ width="650" }

![Do we create something new](pictures/pixel_computing_slide_109.png){ width="650" }

![More results](pictures/pixel_computing_slide_110.png){ width="650" }

![More results](pictures/pixel_computing_slide_111.png){ width="650" }

#### 8.2.3 Structure-first Completion：图标注 + DP/BP

讲义给出的关键观察是：自然图像里最显著的缺失结构通常可由少数曲线近似；并且应先补结构、后补纹理。

![Major observations](pictures/pixel_computing_slide_113.png){ width="650" }

该类方法通常引入用户交互来指定结构曲线，先沿曲线做结构传播，再对剩余区域做纹理传播。

![Graph labeling formulation](pictures/pixel_computing_slide_115.png){ width="650" }

对应地可以构造能量函数（由结构项、完成项、连贯项等组成），把“给每个 anchor 选择哪个 source patch”视为一个图上的标签分配问题。

![Energy terms](pictures/pixel_computing_slide_116.png){ width="650" }

当结构拓扑是链状（1-D chain）时可用动态规划（DP）；更一般的图结构可用 belief propagation（BP）近似求解。

![DP solver](pictures/pixel_computing_slide_117.png){ width="650" }

![BP algorithm](pictures/pixel_computing_slide_118.png){ width="650" }

![An example](pictures/pixel_computing_slide_119.png){ width="650" }

![Sampled results](pictures/pixel_computing_slide_120.png){ width="650" }

![Sampled results](pictures/pixel_computing_slide_121.png){ width="650" }

![Layer-sensitive completion](pictures/pixel_computing_slide_122.png){ width="650" }

## 9 复习与易错点

### 9.1 方法之间的主线关系

- **K-means / Mean Shift**：偏“特征空间聚类”，从像素统计相似性出发。
- **Ncut / GraphCut**：偏“图优化”，显式建模像素之间关系与全局能量。
- **GrabCut / Lazy Snapping**：在 GraphCut 框架中加入交互和颜色模型，强调可用性。
- **Matting / Poisson Matting**：从离散标签升级到连续 $\alpha$，专攻半透明边界。
- **Inpainting / Completion**：关注缺失区域重建，核心是结构与纹理的协调。

### 9.2 高频易错点

- 把分割当成 matting：二值 mask 无法表达半透明过渡。
- 认为 Mean Shift 无需调参：其实 bandwidth 是关键参数。
- 认为 min-cut 一定合理：会偏向切小块，才需要 Ncut 归一化。
- 忽略 GraphCut 的 unary/pairwise 平衡：$\lambda$ 过大可能过度平滑、吞掉细节边界。
- Inpainting 只重视纹理匹配：若结构线先断裂，后续纹理再好也会“假”。

## 考试重点
- **Mean shift 算法**