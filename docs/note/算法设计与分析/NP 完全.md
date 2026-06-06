---
title: NP 完全性
date: 2025-06-05
---

## 1 易解与难解问题

### 1.1 多项式时间算法

**函数多项式相关**：函数 $f$ 和 $g$ 是多项式相关的，如果存在多项式 $p$ 和 $q$ 使得对任意的 $n \in \mathbb{N}$，$f(n) \leq p(g(n))$ 且 $g(n) \leq q(f(n))$。

例如 $n \log n$ 与 $n^2$、$n^2 + 2n + 5$ 与 $n^{10}$ 都是多项式相关的；$\log n$ 与 $n$、$n^5$ 与 $2^n$ 不是多项式相关的。

**问题实例的规模**：实例 $I$ 的二进制编码的长度，记作 $|I|$。

**时间复杂度定义**：如果存在函数 $f: \mathbb{N} \rightarrow \mathbb{N}$ 使得对任意的规模为 $n$ 的实例 $I$，算法 $A$ 对 $I$ 的运算在 $f(n)$ 步内停止，则称算法 $A$ 的时间复杂度为 $f(n)$。

- **多项式时间算法**：以多项式为时间复杂度
- **易解的问题**：有多项式时间算法
- **难解的问题**：不存在多项式时间算法

### 1.2 几点说明

!!! info "编码与操作指令集的约定"
    1. 当采用合理的编码时，输入的规模都是多项式相关的。"合理的"是指在编码中不故意使用许多冗余的字符。
    2. 自然数应采用 $k$（$k \geq 2$）进制编码，不能采用一进制编码。$n$ 的二进制编码有 $\lceil \log_2(n+1) \rceil$ 位，一进制编码有 $n$ 位，两者不是多项式相关的。
    3. 时间复杂度常表成计算对象的某些自然参数的函数，如图的顶点数或边数的函数。实例的二进制编码的长度与这些自然参数通常是多项式相关的。
    4. 运行时间通常是计算执行的操作指令数，执行的指令数与实际运行时间是多项式相关的。

在上述约定下，**算法是否是多项式时间的与采用的编码和操作指令集无关**，从而一个问题是易解的、还是难解的也与采用的编码和操作指令集无关。

### 1.3 易解与难解问题的分类

| 类别 | 示例 |
|------|------|
| **易解的问题** | 排序、最小生成树、单源最短路径等 |
| **已证明的难解问题** | 不可计算的（希尔伯特第十问题）、至少需要指数时间/空间的问题（带幂运算的正则表达式的全体性） |
| **尚未确定的问题** | 哈密顿回路问题、货郎问题、背包问题等 |

## 2 判定问题与组合优化问题

### 2.1 判定问题

**判定问题**：答案只有两个 —— 是 / 否。

判定问题 $\Pi = \langle D_\Pi, Y_\Pi \rangle$，其中 $D_\Pi$ 是实例集合，$Y_\Pi \subseteq D_\Pi$ 是所有答案为 "Yes" 的实例。

!!! abstract "哈密顿回路（HC）"
    任给无向图 $G$，问 $G$ 有哈密顿回路吗？

!!! abstract "货郎问题（TSP）"
    任给 $n$ 个城市，城市 $i$ 与城市 $j$ 之间的正整数距离 $d(i, j)$（$i \neq j$，$1 \leq i, j \leq n$），以及正整数 $D$，问有一条每一个城市恰好经过一次最后回到出发点且长度不超过 $D$ 的巡回路线吗？
    
    即，存在 $1, 2, \ldots, n$ 的排列 $\sigma$ 使得：
    
    $$
    \sum_{i=1}^{n-1} d_{\sigma_i, \sigma_{i+1}} + d_{\sigma_n, \sigma_1} \leq D
    $$

!!! abstract "0-1背包的判定问题"
    任给 $n$ 件物品和一个背包，物品 $i$ 的重量为 $w_i$，价值为 $v_i$（$1 \leq i \leq n$），以及背包的重量限制 $B$ 和价值目标 $K$，其中 $w_i, v_i, B, K$ 均为正整数，问能在背包中装入总价值不少于 $K$ 且总重量不超过 $B$ 的物品吗？
    
    即，存在子集 $T \subseteq \{1, 2, \ldots, n\}$ 使得：
    
    $$
    \sum_{i \in T} w_i \leq B \quad \text{且} \quad \sum_{i \in T} v_i \geq K
    $$

!!! tip "搜索/优化与判定的关系"
    如果搜索问题、组合优化问题有多项式时间算法，则对应的判定问题也有多项式时间算法；通常反之亦真。

### 2.2 组合优化问题与判定问题的对应

组合优化问题 $\Pi^*$ 由3部分组成：

1. 实例集 $D_{\Pi^*}$
2. $\forall I \in D_{\Pi^*}$，有一个有穷非空集 $S(I)$，其元素称作 $I$ 的 **可行解**
3. $\forall s \in S(I)$，有一个正整数 $c(s)$，称作 $s$ 的 **值**

如果 $s^* \in S(I)$，对所有的 $s \in S(I)$，当 $\Pi^*$ 是最小（大）化问题时，$c(s^*) \leq c(s)$（$c(s^*) \geq c(s)$），则称 $s^*$ 是 $I$ 的 **最优解**，$c(s^*)$ 是 $I$ 的 **最优值**，记作 $OPT(I)$。

$\Pi^*$ 对应的判定问题 $\Pi = \langle D_\Pi, Y_\Pi \rangle$ 定义如下：

- $D_\Pi = \{ (I, K) \mid I \in D_{\Pi^*}, K \in \mathbb{Z}^* \}$
- 当 $\Pi^*$ 是最小化问题时，$Y_\Pi = \{ (I, K) \mid OPT(I) \leq K \}$
- 当 $\Pi^*$ 是最大化问题时，$Y_\Pi = \{ (I, K) \mid OPT(I) \geq K \}$

## 3 P 类与 NP 类

### 3.1 P 类

!!! abstract "定义：P 类"
    所有多项式时间可解的判定问题组成的问题类称作 **P 类**。

### 3.2 NP 类

!!! abstract "定义：多项式时间可验证"
    设判定问题 $\Pi = \langle D, Y \rangle$，如果存在两个输入变量的多项式时间算法 $A$ 和多项式 $p$，对每一个实例 $I \in D$，$I \in Y$ 当且仅当存在 $t$，$|t| \leq p(|I|)$，且 $A$ 对输入 $I$ 和 $t$ 输出 "Yes"，则称 $\Pi$ 是 **多项式时间可验证的**，$A$ 是 $\Pi$ 的 **多项式时间验证算法**，而当 $I \in Y$ 时，称 $t$ 是 $I \in Y$ 的 **证据**。

!!! abstract "定义：NP 类"
    由所有多项式时间可验证的判定问题组成的问题类称作 **NP 类**（nondeterministic polynomial）。

### 3.3 非确定型多项式时间算法

**非确定型多项式时间算法**：

1. 对给定的实例 $I$，首先"猜想"一个 $t$，$|t| \leq p(|I|)$
2. 然后检查 $t$ 是否是证明 $I \in Y$ 的证据
3. 猜想和检查可以在多项式时间内完成
4. 当且仅当 $I \in Y$ 时能够正确地猜想到一个证据 $t$

!!! warning "注意"
    非确定型多项式时间算法 **不是真正的算法**。

!!! abstract "定理"
    $P \subseteq NP$

!!! tip "开放问题"
    **$P = NP$？** 这是计算机科学中最重要的未解决问题之一。

## 4 多项式时间变换与 NP 完全性

### 4.1 多项式时间变换

!!! abstract "定义"
    设判定问题 $\Pi_1 = \langle D_1, Y_1 \rangle$，$\Pi_2 = \langle D_2, Y_2 \rangle$。如果函数 $f: D_1 \rightarrow D_2$ 满足条件：
    
    1. $f$ 是多项式时间可计算的
    2. 对所有的 $I \in D_1$，$I \in Y_1 \Leftrightarrow f(I) \in Y_2$
    
    则称 $f$ 是 $\Pi_1$ 到 $\Pi_2$ 的 **多项式时间变换**。如果存在 $\Pi_1$ 到 $\Pi_2$ 的多项式时间变换，则称 $\Pi_1$ 可多项式时间变换到 $\Pi_2$，记作 $\Pi_1 \leq_p \Pi_2$。

!!! abstract "例：HC $\leq_p$ TSP"
    对 HC 的每一个实例 $I$：无向图 $G = \langle V, E \rangle$，TSP 对应的实例 $f(I)$ 为：
    
    - 城市集 $V$
    - 任意两个不同的城市 $u$ 和 $v$ 之间的距离：
    
    $$
    d_{u,v} = \begin{cases} 1 & \text{if } (u, v) \in E \\ 2 & \text{else} \end{cases}
    $$
    
    - 界限 $D = |V|$

### 4.2 NP 完全性

!!! abstract "定义：NP 完全（NPC）"
    设判定问题 $\Pi$，如果：
    
    1. $\Pi \in NP$
    2. 对所有的 $\Pi' \in NP$，$\Pi' \leq_p \Pi$
    
    则称 $\Pi$ 是 **NP 完全的**（NP-Complete，记作 NPC）。

!!! abstract "Cook 定理"
    **SAT 是 NP 完全的**。

!!! tip "NPC 证明方法"
    要证明一个问题 $\Pi$ 是 NP 完全的：
    
    1. 证明 $\Pi \in NP$（通常容易）
    2. 选择一个已知的 NP 完全问题 $\Pi'$，证明 $\Pi' \leq_p \Pi$

## 5 几个 NP 完全问题

### 5.1 SAT 与 3-SAT

!!! abstract "SAT（可满足性问题）"
    给定布尔变元 $x_1, x_2, \ldots, x_n$ 的合取范式 $F = C_1 \wedge C_2 \wedge \cdots \wedge C_m$，问 $F$ 是否可满足？

!!! abstract "3-SAT"
    每个子句恰好有3个文字的 SAT 问题。

!!! abstract "定理"
    **3-SAT 是 NP 完全的**。

    **证明思路**：SAT $\leq_p$ 3-SAT。将每个子句 $C_j$ 变换为等价的 3 文字子句集合 $F_j'$：
    
    - $C_j = z_1$：引入两个新变元 $y_{j1}, y_{j2}$
    
    $$
    F_j' = (z_1 \vee y_{j1} \vee y_{j2}) \wedge (z_1 \vee \neg y_{j1} \vee y_{j2}) \wedge (z_1 \vee y_{j1} \vee \neg y_{j2}) \wedge (z_1 \vee \neg y_{j1} \vee \neg y_{j2})
    $$
    
    - $C_j = z_1 \vee z_2$：引入一个新变元 $y_j$
    
    $$
    F_j' = (z_1 \vee z_2 \vee y_j) \wedge (z_1 \vee z_2 \vee \neg y_j)
    $$
    
    - $C_j = z_1 \vee z_2 \vee z_3$：$F_j' = C_j$
    
    - $C_j = z_1 \vee z_2 \vee \cdots \vee z_k$（$k \geq 4$）：引入 $k-3$ 个新变元
    
    $$
    F_j' = (z_1 \vee z_2 \vee y_{j1}) \wedge (\neg y_{j1} \vee z_3 \vee y_{j2}) \wedge \cdots \wedge (\neg y_{j(k-3)} \vee z_{k-1} \vee z_k)
    $$
    
    $$\square$$

### 5.2 顶点覆盖、团与独立集

设无向图 $G = \langle V, E \rangle$，$V' \subseteq V$：

- **顶点覆盖**：$G$ 的每一条边都至少有一个顶点在 $V'$ 中
- **团**：对任意的 $u, v \in V'$ 且 $u \neq v$，都有 $(u, v) \in E$
- **独立集**：对任意的 $u, v \in V'$，都有 $(u, v) \notin E$

!!! abstract "引理"
    对任意的无向图 $G = \langle V, E \rangle$ 和子集 $V' \subseteq V$，下述命题是等价的：
    
    1. $V'$ 是 $G$ 的顶点覆盖
    2. $V - V'$ 是 $G$ 的独立集
    3. $V - V'$ 是补图 $G^c = \langle V, E^c \rangle$ 的团

!!! abstract "顶点覆盖（VC）"
    任给一个无向图 $G = \langle V, E \rangle$ 和非负整数 $K \leq |V|$，问 $G$ 有顶点数不超过 $K$ 的顶点覆盖吗？

!!! abstract "团（Clique）"
    任给一个无向图 $G = \langle V, E \rangle$ 和非负整数 $J \leq |V|$，问 $G$ 有顶点数不小于 $J$ 的团吗？

!!! abstract "独立集（IS）"
    任给一个无向图 $G = \langle V, E \rangle$ 和非负整数 $J \leq |V|$，问 $G$ 有顶点数不小于 $J$ 的独立集吗？

!!! abstract "定理"
    **顶点覆盖（VC）是 NP 完全的**。

    **证明**：
    
    1. VC 的非确定型多项式时间算法：任意猜想一个子集 $V' \subseteq V$，$|V'| \leq K$，检查 $V'$ 是否是一个顶点覆盖。
    2. 证 3-SAT $\leq_p$ VC。
    
    任给变元 $x_1, x_2, \ldots, x_n$ 的 3 元合取范式 $F = C_1 \wedge C_2 \wedge \cdots \wedge C_m$，构造 VC 的实例 $f(F)$：
    
    - $G = \langle V, E \rangle$，$K = n + 2m$
    - $V = V_1 \cup V_2$
    - $E = E_1 \cup E_2 \cup E_3$
    
    其中：
    
    - **变元构件**（$V_1$）：对每个 $x_i$，引入两个顶点 $x_i$ 和 $\bar{x}_i$，边 $(x_i, \bar{x}_i) \in E_1$
    - **析取式构件**（$V_2$）：对每个 $C_j = z_{j1} \vee z_{j2} \vee z_{j3}$，引入三角形顶点 $[z'_{j1}, j], [z'_{j2}, j], [z'_{j3}, j]$，边 $E_2$ 连接三角形的三条边
    - **联络边**（$E_3$）：连接变元构件和析取式构件
    
    任何顶点覆盖 $V'$ 至少有 $n + 2m$ 个顶点，故恰好含 $K$ 个顶点。在 $x_i$ 和 $\bar{x}_i$ 中取一个，对应 $x_i$ 的赋值。三角形 $C_j$ 的顶点中取2个，剩下顶点对应的变量满足 $C_j$。
    
    $$\square$$

!!! tip "推论"
    根据引理，**独立集和团也是 NP 完全的**。

### 5.3 其他基本 NPC 问题

| 问题 | 描述 |
|------|------|
| **有向哈密顿回路** | 任给有向图 $D$，问 $D$ 中有哈密顿回路吗？ |
| **恰好覆盖** | 给定有穷集 $A$ 和 $A$ 的子集的集合 $W$，问是否存在子集 $U \subseteq W$ 使得 $U$ 中子集彼此不交且并集等于 $A$？ |
| **子集和** | 给定正整数集合 $X$ 及正整数 $N$，问存在 $X$ 的子集 $T$ 使得 $T$ 中元素之和等于 $N$ 吗？ |
| **装箱** | 给定 $n$ 件物品和箱子数 $K$，每只箱子装入物品总重量不超过 $B$，问能用 $K$ 只箱子装入所有物品吗？ |
| **双机调度** | 有2台机器和 $n$ 项作业，作业 $J_i$ 的处理时间为 $t_i$，截止时间为 $D$，问能在截止时间 $D$ 内完成所有作业吗？ |
| **整数线性规划（ILP）** | 给定 $m \times n$ 维整数矩阵 $A$ 和 $m$ 维向量 $b$，问 $AX \geq b$，$X \geq 0$ 且 $X$ 为整数是否有解？ |

### 5.4 NPC 证明方法小结

| 已知 NPC 问题 | 目标问题 | 方法 |
|--------------|----------|------|
| SAT | 3-SAT | 局部替换法 |
| 3-SAT | VC | 构件设计法 |
| 3-SAT | 团、独立集 | 问题等价 |
| VC | 有向 HC | 构件设计法 |
| 3-SAT | 子集和 | 构件设计法 |
| 子集和 | 双机调度 | 构件设计法 |
| 子集和 | 0-1 背包 | 构件设计法 |
| 3-SAT | 装箱 | 构件设计法 |
| 3-SAT | ILP | 限制法 |

## 6 NP 完全性理论的应用

### 6.1 子问题的计算复杂性

!!! tip "努力扩大已知区域，缩小未知区域"
    当 $P \neq NP$ 时，存在不属于 NPC 也不属于 $P$ 的问题。

### 6.2 搜索问题与优化问题

**Turing 归约**：用 NP 完全问题的判定版本作为子程序来求解优化版本。

!!! abstract "货郎优化问题（TSO）到判定问题（TSE）的 Turing 归约"
    设 $s(C, d, \sigma, B)$ 是解 TSE 的子程序，其中 $C$ 为城市集，$d$ 为距离函数，$\sigma$ 为部分旅行，$B$ 为长度限制。

    **算法 Minlength**（二分法确定最短旅行长度 $B^*$）：
    
    $$
    \begin{aligned}
    & \textbf{算法: } \text{Minlength} \\
    & 1. \quad B_{\min} \leftarrow m, \quad B_{\max} \leftarrow m \cdot \max\{ d(c_i, c_j) : c_i, c_j \in C \} \\
    & 2. \quad \textbf{if } B_{\max} - B_{\min} = 1 \textbf{ then } B^* \leftarrow B_{\max}, \text{结束} \\
    & 3. \quad B \leftarrow \lfloor (B_{\min} + B_{\max}) / 2 \rfloor \\
    & 4. \quad s(C, d, \langle c_1 \rangle, B) \\
    & 5. \quad \textbf{if } \text{回答"Yes"} \textbf{ then } B_{\max} \leftarrow B \textbf{ else } B_{\min} \leftarrow B \\
    & 6. \quad \text{转 2}
    \end{aligned}
    $$

    **算法 FindSolution**（找解）：
    
    $$
    \begin{aligned}
    & \textbf{算法: } \text{FindSolution} \\
    & 1. \quad i \leftarrow 2, \quad M \leftarrow \{ 2, 3, \ldots, m \} \\
    & 2. \quad j \leftarrow M \text{ 中的最小值} \\
    & 3. \quad \sigma = \langle c_1, c_j \rangle \\
    & 4. \quad s(C, d, \sigma, B^*) \\
    & 5. \quad \textbf{if } \text{回答"Yes"} \textbf{ then} \\
    & 6. \quad \quad i \leftarrow i + 1, \quad M \leftarrow M - \{ j \} \\
    & 7. \quad \textbf{else} \\
    & 8. \quad \quad \text{从 } \sigma \text{ 中去掉 } c_j \\
    & 9. \quad \quad \text{从 } M \text{ 中选择大于 } j \text{ 的最小值 } k \\
    & 10. \quad \quad \text{将 } c_k \text{ 加入到 } \sigma \text{ 的最后项} \\
    & 11. \quad \textbf{if } i \leq m \textbf{ then 转 4；否则停机}
    \end{aligned}
    $$

    调用 $s$ 的总次数至多为 $\frac{(m-1)(m-2)}{2}$，为 $m$ 的多项式。因此 TSO Turing 归约到 NP 问题 TSE，从而证明了 **TSO 是 NP-easy**，即 TSO 是 **NP 等价的**。

### 6.3 NP-hard 与 NP-easy

- **NP-hard**：所有 NP 问题都可以多项式时间变换到它（不要求本身在 NP 中）
- **NP-easy**：可以 Turing 归约到某个 NP 问题
- **NP 等价**：既是 NP-hard 又是 NP-easy

!!! tip "结论"
    六个基本 NPC 问题对应的优化问题都是 **NP 等价的**。

## 7 处理难解问题的策略

### 7.1 固定参数算法

**固定参数算法**：输入中带有一个参数 $k$，当输入规模为 $n$ 时运行时间为 $O(f(k) \cdot n^c)$ 的算法，其中 $f(k)$ 是与 $n$ 无关的函数，$c$ 是与 $n$ 和 $k$ 都无关的常数。

!!! abstract "例：顶点覆盖的固定参数算法"
    VC：给定图 $G$，正整数 $K$（不超过 $G$ 的顶点数），问是否存在不超过 $K$ 的顶点覆盖？
    
    固定常数 $k$，输入为 $(G, k)$。穷举所有 $k$ 元顶点子集，看看是否存在顶点覆盖。算法复杂度大约是 $O(kn \cdot C_n^k) = O(kn^{k+1})$。
    
    存在 $O(2^k \cdot kn)$ 的算法。

### 7.2 改进的指数时间算法

$O^*$ 表示忽略了多项式因子，如 $O^*(2^n) = O(n^{O(1)}2^n)$。

- 当一个问题的蛮力算法为 $O^*(2^n)$ 时间时，对任何满足 $1 < c < 2$ 的常数 $c$，时间复杂度为 $O^*(c^n)$ 的指数时间算法称为 **非平凡的指数时间算法**
- 可证明在 $O^*(1.8393^n)$ 时间内正确求解 3-SAT
- **指数时间假设**：对每个正整数 $k$，都存在常数 $c_k > 0$，使得求解 $k$-SAT 的精确算法时间复杂性不低于 $O^*(c_k^n)$

### 7.3 其他策略

| 策略 | 说明 |
|------|------|
| **启发式方法** | 回溯与分支限界法、局部搜索法、模拟退火、遗传算法等 |
| **平均情况复杂度** | 有些 NP 完全问题在平均复杂性度量下是易解的 |
| **难解算例生成** | 确定紧的实例 |
| **消息传递算法** | 基于统计物理的方法 |

## 8 总结

| 主题 | 核心内容 |
|------|----------|
| 易解与难解 | 多项式时间算法、判定问题、P 与 NP |
| 多项式变换 | $\Pi_1 \leq_p \Pi_2$ 的定义与性质 |
| NPC 证明 | Cook 定理、3-SAT、VC、团、独立集 |
| 应用 | 子问题分析、Turing 归约、NP-hard / NP-easy |
| 处理策略 | 固定参数、指数时间算法、启发式方法 |
