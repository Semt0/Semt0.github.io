---
icon: lucide/rocket
title: 常微分方程
date: 2026-02-25
authors:
    - name: Semt0
categories:
---



# 第一章：初等积分法



## 特殊方程

### 变量可分离方程

$$
\frac{dy}{dx} = f(x)g(y)
$$

分离变量两边同时积分即可。



### 齐次方程及其变种

$$
\frac{dy}{dx} = \frac{ax + by + c}{dx + ey + f}
$$

- 非齐次转化为齐次（通过坐标平移）

- 变量替换 
  $$
  u = \frac{y}{x} \implies \frac{dy}{dx} = u + x \frac{du}{dx}
  $$
  



## 一阶线性方程

$$
\frac{dy}{dx} = p(x)y + q(x)
$$

- (LH)通解为

$$
y = Ce^{\int p(x)dx}
$$

- (NH) 通解为
  $$
  y = e^{\int p(x)dx}(C + \int q(x)e^{-\int p(x)dx})
  $$

- 注一：初值问题 $y(x_0) = y_0$ 的表达式
- 注二：已知  $p(x),q(x)$ 的某种性质，讨论解的某种性质，通常用定积分表示





## 伯努利方程

$$
\frac{dy}{dx} = p(x)y + q(x)y^n
$$

- 两边同时除以 $y^n$，转化为一阶线性方程
- 注意观察，有的时候有点难看出来





## 恰当方程与积分因子

### 恰当方程

$$
M(x,y)dx + N(x,y)dy = 0
$$

为恰当方程：$\exists U(x, y)$ 使得：
$$
dU(x,y) = M(x, y)dx + N(x, y)dy = 0
$$
充要条件为：
$$
\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}
$$

- 解法：令
  $$
  U(x,y) = \int M(x,y)dx + \varphi(y)
  $$
  再用
  $$
  \frac{\partial U(x,y)}{\partial y} = N(x,y)
  $$
  解出 $\varphi(y)$ 即可



### 积分因子

$\mu(x,y)$ 为积分因子，如果 
$$
\mu M(x,y)dx + \mu N(x,y)dy = 0
$$
为恰当方程。

- 方程有只与 $x$ 有关的积分因子
  $$
  \frac{M_y - N_x}{N} = g(x)
  $$
  积分因子
  $$
  \mu(x) = e^{\int g(x)dx}
  $$

- 方程有只与 $y$ 有关的积分因子
  $$
  \frac{M_y - N_x}{-M} = g(y)
  $$
  积分因子
  $$
  \mu (x) = e^{\int g(x)dx}
  $$
  
- 性质：若 $\mu(x,y)$ 是 $M(x,y)dx + N(x,y)dy = 0$ 的积分因子，则 $\mu(x,y)\Phi(U(x,y))$ 也是方程的积分因子。

  - 用途：解 
    $$
    (M_1dx + N_1dy) + (M_2dx + N_2dy) = 0
    $$





## 一阶隐方程 $F(x,y,y^{'}) = 0$
1. $y = f(x, y^{'})$
   - 令 $y^{'} = p$，两边同时对 $x$ 求导
2. $x = f(y, y^{'})$
   - 令 $y^{'} = p$，两边同时对 $y$ 求导
3. $F(x, y^{'}) = 0$ 和 $F(y, y^{'}) = 0$
   - 都是想办法用参数 $t$ 表示出 $x = \varphi(t), y^{'} = \phi(t)$ 或 $y = \varphi(t), y^{'} = \phi(t)$ 
     - 常见的有线性替换 $y^{'} = tx$ 代入 $F(x, y^{'})$ 后解出 $x$ 等等
     - 要注意观察
   - 然后求出 $y$ 或 $x$ 对应的关于 $t$ 的积分表达式，得到参数解
   - 有很多其他方程也有类似的解法（用参数表示），例如拉格朗日方程



**例：**

求 **拉格朗日(Lagrange, 1736-1813)方程**
$$
y = xf(y^{'}) + \varphi(y^{’})
$$
的通解，其中 $f(p)$ 和 $\varphi(p$) 都是连续可微的函数。

- 令 $p = y^{'}$，两边对 $x$ 求导，转化为关于 $x$ 的一阶线性方程，解出 $x$ 关于 $p$ 为自变量的表达式 $x = \phi(p)$
- $y = \phi(p)f(p) + \varphi(p), x = \phi(p)$ 就是参数解 



## 高阶方程的几种可积类型

1. $y^{(n)} = f(x)$ 

2. $F(x, y^{(n)}) = 0$ 

3. $F(x, y^{(n-2)}, y^{(n-1)}, y^{(n)}) = 0$ 
   1. 令 $z = y^{(n-2)}$，则 $F(x, z, z', z'') = 0$

   2. $F(z, z', z'') = 0$ 

   3. $F(x, z', z'') = 0$ 

4. $F(x, tz, tz', tz'') = t^m F(t, z, z', z'')$ 
5. $F(tx, t^m z, t^{m-1} z', t^{m-2} z'') = t^k F(t, z, z', z'')$

- 4,5 应该不考，仅要求了解





---



# 第二章：线性方程组与线性方程



## 线性方程组

$$
x^{'} = A(t)x + f(t)
$$

其中矩阵函数 $A(t)$ 和向量函数 $f(t)$ 在 $(a, b)$ 上连续。



### 存在唯一性定理（叙述，条件，结论）

- 设 $A(t)$ 和 $f(t)$ 于区间 $I$ 连续，则对任意 $\tau \in I$ 和任意 $n$ 维常向量 $\xi$，初值问题 (NH) 的解于 $I$ 上存在且唯一。

- 证明方法：用逐步逼近法构造 **皮卡序列(Picard, 1856-1841)**
  $$
  \begin{align}
  \varphi_0(t) &= \xi, \\
  \varphi_k(t) &= \xi + \int_\tau^t(A(s)\varphi_{k - 1}(s) + f(s))ds, \qquad k = 1,2, \dots
  \end{align}
  $$

- 证明序列 ${\varphi_k(t)}$ 于 $I$ 内部一致收敛（即于 $I$ 的任意有限闭子区间上一致收敛），且其极限函数是积分方程组
  $$
  x(t) = \xi + \int_\tau^t (A(s)x(s) + f(s))ds
  $$
  在 $I$ 上的连续解。

  由序列与级数的关系，使用魏尔斯特拉斯判别法，只需证明无穷级数
  $$
  \sum\limits_{m = 1}^{\infty}(\varphi_m(t) - \varphi_{m - 1}(t))
  $$
  在其定义区间上一致收敛。运用数学归纳法即可。

  最后证明唯一性。（使用反证法，假设存在另外解，证明二者相同）

- 从更高观点来看，$A(t)x + f(t) = f(t,x)$，其中 $f(t, x)$ 在其定义区间上连续可微，满足利普希兹条件，于是 $x^{'} = f(t,x)$ 的解在任意初值所在区间附近存在且唯一。又由解的延拓性和整体存在性，可以进一步扩大解的存在范围。



#Weierstrass判别法

### Weierstrass 判别法

设函数项级数 $\sum_{n = 1}^{\infty}u_{n}(x)(x \in D)$ 的每一项 $u_{n}(x)$ 满足 
$$
|u_{n}(x)| \leq a_{n}, x \in D
$$
并且数项级数 $\sum_{n = 1}^{\infty} a_{n}$ 收敛，则 $\sum_{n=1}^{\infty}u_{n}(x)$ 在 $D$ 一致收敛。





### 齐次线性方程组（LH）的通解的结构

- 方程组（LH）的解的全体构成一个 $n$ 维线性空间，任意 $n$ 个线性无关的解合起来称为它的一个 **基本解组**，$n$ 个解作为列向量排列成的 $n$ 阶方阵称为方程组（LH）的一个 **基本解矩阵**
- 设 $\Phi(t)$ 是基本解矩阵
  - $\frac{d\Phi(t)}{dt} = A(t)\Phi(t)$
  - $\det \Phi(t) \neq 0$
  - 通解为 $x = \Phi(t)c$，其中 $c = (c_1, c_2, \dots, c_n)^T$ 是任意的 $n$ 维常向量。
- 朗斯基行列式（Wronski，1776-1853）
  - 齐次方程的解 $x_1(t), x_2(t), \dots, x_n(t)$ 线性无关的充要条件为它们构成的朗斯基行列式在某一点处不为零






### 刘维尔公式

若 $\varphi_1(t) , \varphi_2(t), \dots, \varphi_n(t)$ 是方程组（LH）的解，则它们的朗斯基行列式 $W(t)$ 可表示为
$$
W(t) = W(t_0)e^{\int_{t_0}^t trA(s)ds}
$$





### 非齐次线性方程组（NH）的通解的结构

$$
x^{'} = A(t)x + f(t)
$$



设 $\Phi(t)$ 是（LH）的基本解矩阵，（NH）通解表达式为
$$
x = \Phi(t)(C + \int\Phi^{-1}(s)f(s)ds)
$$

- 一阶线性方程 $\frac{dy}{dx} = p(x)y + q(x)$ 的通解表达式就是一种特殊情况

- 齐次线性方程组的所有解构成 $n$ 维线性空间，但是非齐次线性方程组的所有解 **不构成线性空间**！
- 非齐次线性方程组有且最多有 $n+1$ 个线性无关解






#齐次函数

## 齐次函数

一个函数 $f: \mathbb{R}^n \to \mathbb{R}$ 为 **m 次齐次函数**，如果对于所有  $t > 0$ 和所有 $\mathbf{x} = (x_1, \dots, x_n)$ 在其定义域内，满足以下基本性质：



### 核心定义

$$
f(t\mathbf{x}) = f(tx_1, tx_2, \dots, tx_n) = t^m f(\mathbf{x})
$$



#欧拉齐次函数定理



### 欧拉齐次函数定理

如果一个 $m$ 次齐次函数 $f$ 是可微的，那么它的所有一阶偏导数满足以下关系：

$$
x_1 \frac{\partial f}{\partial x_1} + x_2 \frac{\partial f}{\partial x_2} + \dots + x_n \frac{\partial f}{\partial x_n} = m f(x_1, x_2, \dots, x_n)
$$

（$f(tx_1, tx_2, \dots, tx_n) = t^m f(\mathbf{x})$ 两边同时对t求导即可。）

用更简洁的向量记号（梯度 $\nabla f$）表示为：

$$
\mathbf{x} \cdot \nabla f(\mathbf{x}) = m f(\mathbf{x})
$$



### 偏导数的齐次性

如果 $f(\mathbf{x})$ 是 $m$ 次齐次的，那么它的一阶偏导数 $\frac{\partial f}{\partial x_i}$ 是 $(m-1)$ 次齐次的。

$$
\frac{\partial f}{\partial x_i}(t\mathbf{x}) = t^{m-1} \frac{\partial f}{\partial x_i}(\mathbf{x})
$$

更一般地，$k$ 阶偏导数是 $(m-k)$ 次齐次的。





## 边值问题和周期解

###  定理 5.1

齐次方程组（LH）只有平凡解 $x = 0$ 满足两点边值条件 $Lx(a) + Nx(b) = 0$ 当且仅当 $L\Phi(a) + N\Phi(b)$ 是非奇异矩阵，其中 $\Phi(t)$ 是方程组（LH）的基本解矩阵。



### 定理 5.2

若齐次方程组（LH）只有零解 $x=0$ 满足两点边值条件，则对任何 $f(t)$，方程组（NH）恒有解满足两点边值条件。



### 定理 5.3 （马赛拉（Massera）准则）

若 $A(t)$ 和 $f(t)$ 是 $R$ 上连续的 $\omega$-周期函数，则方程组（NH）存在 $\omega$-周期解的充要条件是方程组（NH）有一个 $R$ 上的有界解。 





## 高阶线性方程

形如
$$
x^{(n)} + a_1(t)x^{(n-1)} + \cdots + a_n(t)x = f(t)
$$
的 **$n$ 阶线性微分方程**，其中 $a_1(t), a_2(t), \dots, a_n(t), f(t)$ 都是区间 $I$ 上的纯量函数。

$f(t) = 0$ 时变为齐次方程。



### 通解的结构

作代换
$$
x_1 = x, x_2 = \frac{dx}{dt}, \dots, x_n = \frac{d^{n - 1}x}{d^{n - 1}t}
$$
转化为等价线性微分方程组。

利用等价关系可以运用前面得到的结论。

- 存在唯一性定理

  设 $a_1(t), a_2(t), \dots, a_n(t)$ 和 $f(t)$ 于区间 $I$ 连续，则对任意 $\tau \in I$ 和任意常数 $\xi_0, \xi_1, \dots, \xi_{n  - 1}$，方程满足初值条件
  $$
  x(\tau) = \xi_0, \space x^{'}(\tau) = \xi_1,\dots,\space x^{(n-1)}(\tau) = \xi_{n - 1}
  $$
  的解在 $I$ 上存在且唯一。

- 齐次、非齐次线性方程的通解结构类似

- 刘维尔公式
  $$
  W(t) = W(t_0)e^{-\int_{t_0}^t a_1(s)ds}
  $$
  ，由 $n$ 阶线性微分方程变量替换后转化得到的线性方程组的结构决定（$A(t)$ 的对角线上除了最后一个 $-a_1(t)$ 其他全为 $0$ 

- 常数变易法求解非齐次方程：

  - 齐次方程的基本解矩阵为 $\Phi(t)$

  - 设非齐次方程的解为 $x = \Phi(t)c(t)$
    $$
    \begin{align}
    \frac{dx}{dt} &= \frac{d \Phi(t)}{dt} c(t) + \Phi(t)\frac{dc(t)}{dt} \\
    &= A(t)\Phi(t)c(t) + \Phi(t)c^{'}(t) \\
    &= A(t)x + f(t) \\
    &= A(t)\Phi(t)c(t) + f(t) \\
    &\Rightarrow c^{'}(t) = \Phi^{-1}(t)f(t)
    \end{align} \\
    $$
    求出一组 $c_i(t)$，最后利用通解结构定理写出通解。

- 求解高阶方程的降阶法

  已知一个解 $x = \varphi(t)$，令 $x = \varphi(t)y$，可化为 $y$ 的低一阶的方程。特别对于二阶非齐次线性方程只需知道对应齐次方程的一个解，即可求出通解。（两种方法：其一，利用上述变换；其二，利用刘维尔公式）

- 利用常数变易法解得特解，得到 **拉格朗日常数变易公式**
  $$
  x = c_1\varphi_1(t) + c_2\varphi_2(t) + \dots + c_n\varphi_n(t) + \int_{\tau}^t \frac{\Delta(t, s)}{W(s)}f(s)ds，
  $$
  其中 $\varphi_i(t)$ 是齐次方程的一个基本解组，$W(t)$ 是 $\varphi_i(t)$ 的朗斯基行列式，$\Delta(t, s)$ 是这样一个 $n$ 阶行列式：前 $n - 1$ 行是 $W(t)$ 的前 $n - 1$ 行相应元素，而第 $n$ 行是 $W(t)$ 第一行的相应元素。



## 线性方程的复值解

容易证明：一个复值向量函数
$$
\varphi(t) = u(t) + iv(t)
$$

- 是 （NH）的解
  - $u(t)$ 是（NH）的解
  - $v(t)$ 是（LH）的解
- 是（LH）的解
  - $u(t), v(t)$ 都是（LH）的解





---



# 第三章：常系数线性方程



## $n$ 阶常系数齐次线性方程

$$
\frac{d^n x}{dt^n} + a_1 \frac{d^{n-1} x}{dt^{n-1}} + \cdots + a_{n-1} \frac{dx}{dt} + a_n x = 0
$$



### 特征方程及其性质

引入微分算子 $D = \frac{d}{dt}$，$D x = \frac{dx}{dt}$，$D^2 x = \frac{d^2 x}{dt^2}$，$\cdots$。

方程化为 $(D^n + a_1 D^{n-1} + \cdots + a_{n-1} D + a_n) x = 0$。

记 $P(D) = D^n + a_1 D^{n-1} + \cdots + a_n$，则 $P(D) x = 0$。

**特征方程**：$P(\lambda) = \lambda^n + a_1 \lambda^{n-1} + \cdots + a_n = 0$。



1. 若 $P(\lambda_0) = 0$，那么 $x = e^{\lambda_0 t}$ 是解。

   > $P(D) e^{\lambda_0 t} = P(\lambda_0) e^{\lambda_0 t} = 0$。

   

2. 若 $P(\lambda)$ 有 $n$ 个不同的根 $\lambda_1, \lambda_2, \cdots, \lambda_n$，则 $e^{\lambda_1 t}, e^{\lambda_2 t}, \cdots, e^{\lambda_n t}$ 是基本解组。

   >  证明：朗斯基行列式 $W(t) = W(0) e^{-\int_0^t a_1 ds} = W(0) e^{-a_1 t}$。
   >
   > 而 $W(0)$ 是范德蒙行列式，$\prod_{1 \le i < j \le n} (\lambda_j - \lambda_i) \neq 0$，所以 $W(t) \neq 0$。

   

3. 若 $\lambda_0$ 是 $P(\lambda) = 0$ 的 $k$ 重根，则 $e^{\lambda_0 t}, t e^{\lambda_0 t}, \ldots, t^{k-1} e^{\lambda_0 t}$ 是原方程 $k$ 个线性无关的解。

   $P(\lambda) = Q(\lambda)(\lambda - \lambda_0)^k$，$Q(\lambda_0) \neq 0$。

   $P(D) x = Q(D)(D - \lambda_0)^k x$

   > 引理：对于复数 $s$ 和整数 $m$，$D^m (e^{s t} x(t)) = e^{s t} (D + s)^m x(t)$。
   >
   > 证明（归纳法）：$m=1$，$D(e^{s t} x) = s e^{s t} x + e^{s t} D x = e^{s t} (D + s) x$。假设 $m$ 时成立，$D^m (e^{s t} x) = e^{s t} (D+s)^m x$。$D^{m+1} (e^{s t} x) = D [ e^{s t} (D+s)^m x ] = e^{s t} (D+s) (D+s)^m x = e^{s t} (D+s)^{m+1} x$。现在，令 $s = -\lambda_0$，则 $(D - \lambda_0)^k x = e^{\lambda_0 t} D^k (e^{-\lambda_0 t} x)$。所以 $P(D) x = Q(D) e^{\lambda_0 t} D^k (e^{-\lambda_0 t} x) = 0$。由于 $Q(D)$ 和 $e^{\lambda_0 t}$ 可逆（在解空间中），等价于 $D^k (e^{-\lambda_0 t} x) = 0$。$\Rightarrow e^{-\lambda_0 t} x$ 为任意次数不超过 $k-1$ 的多项式：$C_0 + C_1 t + \cdots + C_{k-1} t^{k-1}$。$\Rightarrow x = e^{\lambda_0 t} (C_0 + C_1 t + \cdots + C_{k-1} t^{k-1})$。取 $C_i=1$，其余为 $0$，得到 $k$ 个线性无关解 $e^{\lambda_0 t}, t e^{\lambda_0 t}, \ldots, t^{k-1} e^{\lambda_0 t}$。

   

### 解的结构

 如果特征多项式 $P(\lambda)$ 可分解为
$$
P(\lambda) = (\lambda - \lambda_1)^{n_1} (\lambda - \lambda_2)^{n_2} \cdots (\lambda - \lambda_r)^{n_r}
$$

其中 $n_1 + n_2 + \cdots + n_r = n$，$\lambda_i \neq \lambda_j (i \neq j)$，

则函数组

$$
e^{\lambda_1 t}, t e^{\lambda_1 t}, \ldots, t^{n_1-1} e^{\lambda_1 t} \\
e^{\lambda_2 t}, t e^{\lambda_2 t}, \ldots, t^{n_2-1} e^{\lambda_2 t} \\
\cdots \\
e^{\lambda_r t}, t e^{\lambda_r t}, \ldots, t^{n_r-1} e^{\lambda_r t}
$$

为基本解组。

- 注意实系数方程组（方程）都要求求出实值解





## 矩阵指数函数

引入的主要目的是为了研究常系数齐次线性方程组
$$
\frac{dx}{dt} = Ax
$$
的解法及其解的性质



- 矩阵的指数函数定义：

$$
e^A \triangleq \sum_{n=0}^{\infty} \frac{1}{n!} A^n = E + A + \frac{1}{2!} A^2 + \cdots
$$

$$
e^{A t} \triangleq \sum_{n=0}^{\infty} \frac{1}{n!} (A t)^n = E + A t + \frac{1}{2!} A^2 t^2 + \cdots
$$

- 性质：
    - $\frac{d}{dt} e^{A t} = A e^{A t}$。
    - 若 $AB = BA$，则 $A e^{B t} = e^{B t} A$，且 $e^{(A+B)t} = e^{A t} e^{B t} = e^{B t} e^{A t}$。
    - $e^{A t}$ 可逆，$(e^{A t})^{-1} = e^{-A t}$。
    - 若 $T$ 可逆，则 $e^{(T A T^{-1}) t} = T e^{A t} T^{-1}$。



1.  $e^{A t}$ 是 $\frac{dx}{dt} = A x$ 的基本解矩阵 ($\Phi(0)=E$)。
2.  $\frac{dx}{dt} = A x + f(t)$ 的通解：$x = e^{A t} C + e^{A t} \int_{t_0}^{t} e^{-A s} f(s)  ds$。

    若初值 $x(t_0) = x_0$，则 $C = e^{-A t_0} x_0$，

    $x = e^{A (t-t_0)} x_0 + \int_{t_0}^{t} e^{A (t-s)} f(s)  ds$。（这是一个卷积，与信号与系统内容相关）





### $e^{A t}$ 的计算（若当标准型法）

设 $A = T J T^{-1}$，$J$ 为若当标准型。

则 $e^{A t} = T e^{J t} T^{-1}$。

$e^{J t} = \operatorname{diag}( e^{J_1 t}, e^{J_2 t}, \cdots, e^{J_r t} )$

对于若当块 $J_i = \lambda_i E + N$ ($N$ 为幂零矩阵)，

$$
e^{J_i t} = e^{\lambda_i t} (E + N t + \frac{N^2 t^2}{2!} + \cdots + \frac{N^{k-1} t^{k-1}}{(k-1)!})
$$
~~考算这个的话算我输~~





## 常系数线性齐次线性方程组的求解

### $A$ 可对角化

则 $A$ 有 $n$ 个线性无关的特征向量。令 $\lambda_1, \lambda_2, \dots, \lambda_n$ 对应的特征向量为 $c_1, c_2, \dots, c_n$ （可以有相同的特征值），则
$$
e^{\lambda_1t}c_1, e^{\lambda_2t}c_2, \dots, e^{\lambda_nt}c_n
$$
为基本解组





### $A$ 不可对角化

**引理：**设 $A$ 有互异特征根 $\lambda_1, \lambda_2, \dots, \lambda_s$，重数分别为 $n_1, n_2, \dots, n_s$，$n_1 + n_2 + \dots + n_s = n$，$V$ 是 $n$ 维欧氏空间，则对于 $i = 1, 2, \dots, s$，
$$
V_i = \{v \in V \mid (A - \lambda_iE)^{n_i}v = 0\}
$$
是 $A$ 的 $n_i$ 维不变子空间，并且有直和分解 
$$
A = V_1 \oplus V_2 \oplus \dots \oplus V_s
$$
即 $(A - \lambda_iE)^{n_i}v = 0$ 有 $n_i$ 个线性无关的解，它们构成不变子空间 $V_i$ 的一组基向量。



根据引理，针对 $A$ 的特征值 $\lambda_i$，设它的代数重数为 $n_i$

1. 求 $(A - \lambda_iE)^{n_i}v = 0$ 的 $n_i$ 个线性无关的解 $v_j^i, \space j = 1, 2, \dots, n_i$

2. 求对应于 $v_j^i$ 的解 （对每个 $\lambda_i$，中间那一坨只用求一次）
   $$
   \varphi_j^i = e^{\lambda_it}[\sum\limits_{k = 0}^{n_i - 1}\frac{t^k}{k!}(A - \lambda_iE)^k]v_j^i
   $$

3. 重复所有的 $\lambda_i$，得到 $n$ 个线性无关的解。



- 也可以用算子解法求解常系数微分方程组：克莱姆法则——化为高阶线性方程





## 常系数方程解的渐近性质（稳定性）

$$
\frac{dx}{dt} = A x
$$

- 若 $A$ 的所有特征根实部都小于零，即 $\operatorname{Re}(\lambda_i) < 0, \forall i$，则方程组的任意解 $\lim\limits_{t \to +\infty} X(t) = 0$。
- 若 $A$ 至少有一个特征根实部大于零，即 $\exists i, \operatorname{Re}(\lambda_i) > 0$，则存在解 $\lim\limits_{t \to +\infty} |X(t)| = \infty$。
- 若 $A$ 的所有特征根实部都小于等于零，且实部为零的特征根对应的初等因子是一次的（即若当块均为 $1\times 1$），则所有解有界。





## 非齐次方程解法

有常数变易法，待定系数法，算子解法，拉普拉斯变换法等解法

**算子解法** 比较好用

把非齐次微分方程 
$$
P(D)x = f(t)
$$
的解族记作
$$
\frac{1}{P(D)}f(t)
$$
即用 $\frac{1}{P(D)}$ 表示这样一个函数，以 $P(D)$ 作用后等于 $f(t)$

**性质**：
$$
\begin{cases}
\displaystyle \frac{1}{P(D)} e^{\lambda t} = \frac{1}{P(\lambda)} e^{\lambda t}, \quad P(\lambda) \neq 0 \\[15pt]
\displaystyle \frac{1}{P(D^2)} \cos \alpha t = \cos \alpha t \frac{1}{P(-\alpha^2)}, \quad P(-\alpha^2) \neq 0 \\[15pt]
\displaystyle \frac{1}{P(D^2)} \sin \alpha t = \sin \alpha t \frac{1}{P(-\alpha^2)}, \quad P(-\alpha^2) \neq 0 \\[15pt]
\displaystyle \frac{1}{P(D)} e^{\lambda t} v(t) = e^{\lambda t} \frac{1}{P(D + \lambda)} v(t) \\[15pt]
\text{设 } f_k(t) = b_0 + b_1 t + \cdots + b_k t^k, \quad P(0) = a_n \neq 0 \\[10pt]
\displaystyle \frac{1}{P(D)} f_k(t) = Q_k(t) f_k(t) \\[10pt]
\text{其中 } Q_k(t) \text{ 是 } \displaystyle \frac{1}{P(D)} \text{ 在 } D=0 \text{ 附近泰勒展开式的前 } k+1 \text{ 项}
\end{cases}
$$
最后一项：不妨设 $P(0) \neq 0$，否则 $P(D) = D^rP_1(D)$，$P_1(0) \neq 0$，用 $P_1(D)$ 代替 $P(D)$

$Q_k(D)$ 是 $D$ 的 $k$ 次多项式，它是将 $P(D)$ 按 $D$ 的升幂排列后用通常的多项式除法去除 $1$，在第 $k + 1$ 步上得到的商式。

原理是 
$$
1 = Q_k(D)P(D) + R(D)
$$
其中 $R(D)$ 是余式，它的最低次数为 $k + 1$

上式两端同时作用于 $f_k(t)$，即有
$$
f_k(t) = P(D)Q_k(D)f_k(D)
$$


**注意灵活运用**

**例**：
$$
\begin{align}
\frac{1}{D^2 + 3D + 2}e^{e^t} &= \frac{1}{D+2} \cdot \frac{1}{D + 1}e^{e^t} \\
&= \frac{1}{D + 2}\cdot (e^{-t}\frac{1}{D}e^te^{e^t}) \\
&= \frac{1}{D + 2}e^{-t}e^{e^t} \\
&= e^{-2t}\frac{1}{D}e^te^{e^t} \\
&= e^{-2t}e^{e^t}
\end{align}
$$


- 算子解法解出的是非齐次方程的一个特解，要得到通解，还需要解 $P(D) = 0$ 得出齐次方程的通解。



## Euler 方程

$$
t^nx^{(n)} + a_1 t^{n - 1}x^{(n - 1)} + \dots + a_nx = 0
$$

变量替换：$t = e^s$，即 $s = \ln |t|$ 

并记 $D_0 = \frac{d}{ds}$，则有
$$
t^mD^mx = D_0(D_0 - 1)\dots (D_0 - m + 1)x
$$


**例**：

解方程
$$
(t^2D^2 - 2tD + 2)x = 4 \ln t
$$
作变量替换 $t = e^s$，

得到
$$
(D_0(D_0 - 1) - 2D_0 + 2)x = 4s
$$
解出特解 $x = 2s + 3$，

齐次方程通解 $x = c_1e^s + c_2 e^{2s}$

非齐次方程通解为 $x = c_1e^s + c_2 e^{2s} + 2s + 3$

带回 $t = e^s$，得到原方程解为
$$
x = c_1t + c_2 t^2 + 2 \ln |t|  + 3
$$





## 拉式变换法

不考，懒得写了





## 例题

例：设 $y = \varphi(x)$ 是二阶齐次线性微分方程 $y'' + p(x)y' + q(x)y = 0$ 的一个非零解，其中 $p(x), q(x)$ 在 $[a,b]$ 上连续，求方程的通解。

解：由降阶法公式，（刘维尔公式）

$$
y = \varphi(x) \left[ C_1 + C_2 \int \frac{e^{-\int p(x) dx}}{\varphi^2(x)} dx \right]
$$





例：$y_1 = -e^{x^2}, y_2 = e^{x^2}(e^x - 1)$ 为非齐次方程 $y'' - 4x y' + q(x) y = f(x)$ 的解。求通解。





例：$x = \varphi(t)$ 是 $\frac{dx}{dt} = A(t) x$ 的解，$y = \psi(t)$ 是 $\frac{dy}{dt} = -A^T(t) y$ 的解。证明 $\psi^T(t) \varphi(t)$ 为常数。



证明：$\frac{d}{dt} (\psi^T \varphi) = (\frac{d\psi}{dt})^T \varphi + \psi^T \frac{d\varphi}{dt} = (-A^T \psi)^T \varphi + \psi^T (A \varphi) = -\psi^T A \varphi + \psi^T A \varphi = 0$。

故 $\psi^T(t) \varphi(t)$ 为常数。




---



# 第四章：一般理论



## 引言

一阶正规形非线性方程组
$$
\begin{cases} 
\frac{dx_1}{dt} = f_1(t,x_1,x_2,\dots,x_n), \\
\frac{dx_2}{dt}=f_2(t,x_1,x_2,\dots,x_n), \\
\dots\dots\dots \\
\frac{dx_n}{dt}=f_n(t,x_1,x_2,\dots,x_n).
\end{cases}
(E)
$$
任意正规形高阶方程
$$x^{(n)} = f(t,x,x^{'},\dots,x^{(n - 1)})(E_n)$$
都可以变为等价的一阶正规形方程组，因此关于一阶正规形方程组 $(E)$ 的所有结论都可以转移到正规形高阶方程 $E_n$ 上。

方程组 $(E)$ 可简记为 $$\frac{dx}{dt} = f(t,x)$$，其中 $$\frac{dx}{dt} = \begin{pmatrix} \frac{dx_1}{dt} \\ \frac{dx_2}{dt} \\ \vdots \\ \frac{dx_n}{dt}\end{pmatrix},x = \begin{pmatrix} x_1 \\ x_2 \\ \vdots \\ x_n\end{pmatrix},f(t,x) = \begin{pmatrix} f_1(t,x_1,x_2, \dots, x_n) \\ f_2(t, x_1, x_2, \dots, x_n) \\ \vdots \\ f_n(t,x_1,x_2,\dots,x_n)\end{pmatrix}.$$
方程组 $(E)$ 的最基本的定解问题是初值问题，也称为 **柯西问题**。设初值条件为 $$x(\tau) = \xi$$，其中 $\xi$ 是 $n$ 维列向量。





## 皮卡存在与唯一性定理


### Lipschitz 条件
函数 $f(t,x)$ 在闭域 
$$
R = \{(t,x)| |t - \tau| \leq a,|x - \xi| \leq b\}
$$
上满足利氏条件，如果 $\exists N > 0$，使得对任意点 $(t, x_1), (t, x_2) \in R$，都有 
$$
|f(t,x_1) - f(t,x_2)|\leq N|x_1 - x_2|
$$
，其中 $N$ 称为**利氏常数**。



> [!tip]
>
> 由中值定理知，若 $f(t,x)$ 在 $R$ 上关于 $x$ 的各个分量的偏微商都存在且有界，则 $f(t,x)$ 在 $R$ 上满足利氏条件。 



 

### 皮卡定理

若 $f(t,x)$ 在闭域 $R$ 上连续，且满足利氏条件，则初值问题于区间 $I_0 = \{t||t - \tau| \leq h\}$ 上存在唯一解，其中
$$
h = min\{a, \frac{b}{M}\}
$$
，$M$ 是 $|f(t,x)|$ 于 $R$ 的一个上界。



> [!tip]
>
> 区间 $I_0$ 和 $h$ 的构造是为了使得构造的皮卡迭代序列 $\{\varphi_k(t)\}$ 不超出 $I_0$，从而 $f(t,\varphi_k(t))$ 不超出 $R$，从而能使用 Lipschitz 条件。




> [!tip]
>
> 1. 归结为证明等价的积分方程组 $$x(t) = \xi + \int_{\tau}^t f(s, x(s))ds$$ 于 $I_0$ 上存在唯一连续解
>
> 2. 在 $I_0$ 上构造皮卡迭代序列 $\{\varphi_k(t)\}$ 并证明其一致收敛。令
>    $$
>    \begin{align}
>    \varphi_0(t) &= \xi \\
>    \varphi_k(t) &= \xi + \int_{\tau}^t f(s,\varphi_{k - 1}(s))ds, k = 1,2, \dots
>    \end{align}
>    $$
>    
>
> 3. 证明唯一性。
>
>    假设有两个解 $\varphi(t)$ 和 $\phi(t)$，令 $u(t) = |\varphi(t) - \phi(t)|$，则 
>    $$
>    u(t) \leq N|\int_\tau^tu(s)ds| = 0 + |\int_\tau^tNu(s)ds|
>    $$
>    由 Bellman-Gronwell 不等式，
>    $$
>    u(t) \leq 0\cdot e^{\int_\tau^tNds} = 0
>    $$
>    于是 $u(t) = 0$



> [!tip]
>
> 皮卡序列的构造过程实质上是一边在证明[[压缩映像原理]]，一边在用它解决常微分方程问题。



设 $G$ 是 $(t,x)$ 空间的域，若对任意 $(\tau,\xi) \in G$，都存在闭域 $R \subset G$，使得 $f(t,x)$ 在 $R$ 上满足利氏条件（对 $G$ 上不同的点 $(\tau,\xi)$，常数 $a,b$ 和利氏常数 $N$ 可能不同），则称 $f(t,x)$ 于域 $G$ 上**局部地满足利氏条件**。



> [!tip]
>
> 若 $f(t,x)$ 在域 $G$ 上关于 $x$ 的各个分量的偏微商均存在且连续，则 $f(t,x)$ 于 $G$ 上局部地满足利氏条件。



- 利氏条件可以加强为 **奥斯古德（Osgood，1864-1943）条件**：对任意 $(t, x_1), (t, x_2) \in R$，有
  $$
  |f(t, x_1) - f(t, x_2)| \leq G(||x_1 - x_2||)
  $$
  其中 $G(s)$ 在 $0 < s \leq s_0(s_0 > 0)$ 上连续，$G(s) > 0$，且
  $$
  \int_0^{s_0}\frac{ds}{G(s)} = + \infty
  $$
  



### 推论

若 $f(t,x)$ 在域 $G$ 内连续，且局部地满足利氏条件，则对任意 $(\tau,\xi) \in G$，初值问题的解在含 $\tau$ 的某一区间上的存在且唯一。





### 定理（解的整体唯一性）

若对任意 $(t_0,\xi_0) \in G$，初值问题 $(E),x(t_0) = \xi_0$ 的解在含 $t_0$ 的某区间上唯一，则对任意 $(\tau, \xi) \in G$，初值问题的任意两个解在其共同存在区间上恒等。

保证 $(E)$ 的局部解唯一的任何条件，也能保证 $(E)$ 的整体解唯一。





### 解不唯一的情况，奇解

若 $f(t,x)$ 在 $(t,x)$ 空间的域 $G$ 内连续，且局部地满足利氏条件或其他更一般的条件，则对任何 $(\tau,\xi) \in G$，初值问题的解不仅存在，而且是唯一的。

然而，如果只假设 $f(t,x)$ 连续，那么初值问题的解依然存在，但不一定唯一。例如初值问题 
$$
\frac{dx}{dt} = 2|x|^{\frac{1}{2}},x(0) = 0
$$
就有无穷多个解。

从几何上看，初值问题的解唯一，就是只有一条积分曲线经过点 $(\tau,\xi)$，初值问题有无穷多个解，就是有无穷多条积分曲线经过点 $(\tau,\xi)$，所有这些积分曲线都在点 $(\tau,\xi)$ 相切。

考虑一阶隐方程
$$
F(t,x,x^{'}) = 0,(2.13)
$$
设 $x = \varphi(t)$ 是方程 $(2.13)$ 在区间 $I$ 上的解，若在它相应的积分曲线上任何一点都有方程 $(2.13)$ 的另一条积分曲线经过并在该点与之相切，则称 $x = \varphi(t)$ 为方程 $(2.13)$ 在 $I$ 上的 **奇解**。

设 $F(t,x,p)$ 是 $(t,x,p)$ 的连续可微函数，则 $x = \varphi(t)$ 是方程 $(2.13)$ 在 $I$ 上的奇解的必要条件是
$$
\begin{align}
&F(t,\varphi(t),\varphi^{'}(t)) = 0 \\
&F_p(t,\varphi(t),\varphi^{'}(t))= 0 
\end{align}
$$
必要条件表明，方程 $(2.13)$ 的奇解包含在由方程组
$$
\begin{cases}
F(t,x,p) = 0 \\
F_p(t,x,p) = 0
\end{cases}
$$
消去 $p$ 而得到的曲线中，该曲线称为方程 $(2.13)$ 的 **$p$-判别曲线**。$p$-判别曲线是不是奇解，需要进一步验证。





### 定理

**克莱罗(Clairaut,1713-1765)方程**
$$
x = tx^{'} + g(x^{'})
$$
恒有奇解，这里函数 $g(p)$ 两次连续可微，且 $g^{''}(p) \neq 0$。





## 佩亚诺存在定理

### 定理
设 $f(t,x)$ 于闭域 $R = \{(t,x) | |t - \tau| \leq a, |x -\xi| \leq b\}$ 上连续，则初值问题有定义于区间 $I_0 = \{t | |t - \tau| \leq h\}$ 上的解，其中 $h = min\{a, \frac{b}{M}\}$，$M$ 是 $|f(t,x)|$ 在 $R$ 上的一个上界。






### 阿尔泽拉(Arzela)-阿斯科利(Ascoli)引理
意义与证明方法类似数学分析中的聚点原理。





#### 定义
若存在常数 $M_0 > 0$，使得对任意 $f(t) \in F$，都有
$$|f(t)| \leq M_0, t \in I,$$
则称函数族 $F$ 在区间 $I$ 上是 **一致有界** 的。





#### 定义

若对任意 $\epsilon > 0$，都存在只与 $\epsilon$ 相关的常数 $\delta > 0$，使得对任意 $f(t) \in F$，只要 $t_1,t_2 \in I, |t_1 - t_2| \leq \delta$，就有 $$|f(t_1) - f(t_2)| \leq \epsilon$$，则称函数族 $F$ 在区间 $I$ 上是 **等度连续** 的。





#### 引理

假设 $F = \{f(t)\}$ 是有限区间 $I = [c, d]$ 上一致有界，等度连续的函数族，则 $F$ 必有于区间 $I$ 上一致收敛的子序列。





#### 推论 3.1

若函数 $f(t,x)$ 于 $(t,x)$ 空间的域 $G$ 内连续，则对任意 $(\tau, \xi) \in G$，初值问题有定义于含 $\tau$ 的某区间（其长度一般与 $(\tau, \xi)$ 有关）上的解。





#### 推论 3.2

若函数 $f(t,x)$ 于 $(t,x)$ 空间的域 $G$ 内连续，$D$ 是 $(t, x)$ 空间的有界域，且 $\overline{D} \subset G$，则存在 $h > 0$，使得对任意 $(\tau, \xi) \in D$，初值问题有定义在区间 $[\tau - h, \tau + h]$ 上的解。 

> [!tip] 闭包
> [[数学分析]]





## 解的延展与解的整体存在性

### 定理 5.1
设 $f(t,x)$ 于 $(t,x)$ 空间域 $G$ 内连续。若对任意 $(\tau, \xi) \in G$，初值问题的解在含 $\tau$ 的某一区间上是唯一的（可以使用解的整体唯一性），则 $\dot{x} = f(t,x)$ 的任何非饱和解都可以延展成为饱和解。





### 定理 5.2

设 $f(t,x)$ 于 $(t,x)$ 空间域 $G$ 内连续，$D$ 是 $(t,x)$ 空间中一有界域，且 $\overline{D} \subset G$。则方程组 $\dot{x} = f(t,x)$ 经过 $D$ 中任一点的解曲线，经向左和向右延展，都可以达到 $D$ 的边界。

> [!tip]
>
> 使用 引理 3.2 证明（对每个 $(\tau, \xi) \in D$, 有 **固定的 $h$** 使得方程组有定义在 $[\tau - h, \tau + h]$ 上的解。）





### 比较定理

解的存在定理告诉我们，微分方程的解的初值问题可以延拓到边界，但是解的存在区间的大小对于具体问题来说还是费解的，有了比较定理之后，我们会收获一个计算解的存在区间的强有力的工具。





#### 第一比较定理

设函数 $f(x, y)$ 和 $F(x, y)$ 均在区域 $G$ 内连续，且 $$f(x,y) < F(x, y), (x,y) \in G,$$
又设函数 $y = \phi(x)$ 和 $y = \Phi(x)$ 在区间 $(a,b)$ 上分别是初值问题 $$y^{'}=f(x,y),y(x_0)=y_0$$
和 $$y^{'}=F(x,y),y(x_0) = y_0$$
的解，其中 $(x_0,y_0) \in G$，则 
$$
\begin{cases} 
\phi(x) < \Phi(x), x_0 < x < b, \\
\phi(x) > \Phi(x), a < x < x_0.
\end{cases}
$$

> [!tip]
> 第一比较定理要求 $F(x,y)$ 严格地大于 $f(x,y)$，要是不严格的话我们可以取 $f(x,y) = F(x,y)$ 为反例，它们的解是无法比较大小的。





---

假设 $f(t,x)$ 在域 $G = \{(t,x) | T_0 < t < T_1, |x| < +\infty\}$ 内连续。根据延展定理容易证明，若方程组的任意饱和解 $x = \varphi(t)$ 是有界的，即存在常数 $C$ 使得 $|\varphi(t)| \leq C$，则 $x = \varphi(t)$ 的存在区间是 $(T_0, T_1)$。事实上，对充分小的 $\delta > 0$，记 $D = \{(t,x) | T_0 + \delta < t < T_1 - \delta, |x| < 2C\}$，由定理 5.2 知解曲线 $x = \varphi(t)$ 向左、右延展都可以达到 $D$ 的边界。但是 $|\varphi(t)| \leq C$，所以它不可能达到 $|x| = 2C$，于是它一定可以达到 $t = T_0 + \delta$ 和 $t = T_1 - \delta$，即 $x = \varphi(t)$ 至少在 $[T_0+ \delta,T_1 - \delta]$ 上有定义，此时我们称方程组 $(E)$ 存在整体解。





### 定理 5.6

若 $f(t,x)$ 在域 $G$ 内连续，且 $$|f(t,x)| \leq A|x| + B$$，其中 $A,B$ 是常数，则方程组 $(E)$ 的任何饱和解 $x = \varphi(t)$ 都在区间 $(T_0, T_1)$ 上存在。



> [!tip]
>
> **证明：**
>
> 设 $\varphi(t) = (\varphi_1(t), \varphi_2(t),\dots,\varphi_n(t))$ 的存在区间为 $(a, b)$，其中 $T_0 < a < b < T_1$。存在 $\delta > 0$，使得 $T_0 + \delta < a < b < T_1 - \delta$，也即 $(a, b) \subseteq [T_0 + \delta, T_1 - \delta]$，若 $\varphi(t)$ 在其存在区间内有界，也即 $\exists C > 0, |\varphi(t)| \leq C$，考虑域 $G$ 内有界域 
> $$
> D = \{(t,x) | t \in [T_0 + \delta, T_1 - \delta], |x| \leq 2C\}
> $$
> ，则 $\varphi(t)$ 是 $D$ 内的解曲线 $\Rightarrow \varphi(t)$ 可以拓展到 $D$ 的边界，又 $|\varphi(t)| \leq C \Rightarrow \varphi(t)$ 不可能达到 $|x| = 2C \Rightarrow \varphi(t)$ 可拓展到 $[T_0 + \delta, T_1 - \delta]$。由 $\delta \rightarrow 0$ 得到 $\varphi(t)$ 存在区间为 $(T_0, T_1)$。故只需证明 $\varphi(t)$ 在其存在区间 $(a,b)$ 内有界。
>
> 假设 $x = \varphi(t)$ 在 $[t_0, b)$ 无界（这里 $t_0 \in (a,b)$。令 $$r(t) = (\sum\limits_{i = 1}^n {\varphi_i^2(t)})^{\frac{1}{2}}$$，则 $r(t)$ 在 $[t_0,b)$ 上连续，且在其不为零的点处连续可微。因为 $\varphi(t)$ 在 $[t_0,b)$ 上无界，所以对任意 $K > r(t_0) + 1$，都有 $t_k \in (t_0, b)$，使得 $r(t_k) \geq K$。根据 $r(t)$ 的连续性，存在 $\tau_k \in (t_0, t_k)$，使得 $r(\tau_k) = r(t_0) + 1$，且当 $t \in [\tau_k, t_k]$ 时，$r(t) > 0$。又由 Cauchy 不等式知 $|\varphi(t)| \leq \sqrt{n}r(t)$，
> $$
> \begin{align}
> \frac{dr(t)}{dt} &= \frac{1}{r(t)}\sum\limits_{i = 1}^n {\varphi_i(t) f_i(t,\varphi(t))}  \\
&\leq \frac{1}{r(t)} \sum\limits_{i = 1}^n {|\varphi_i(t)||f(t,\varphi(t)|}  \\
&\leq \sqrt{n}|f(t,\varphi(t)|  \\
&\leq \sqrt{n}(A|\varphi(t)| + B) & \\
&\leq \sqrt{n}(A\sqrt{n}r(t) + B)
> \end{align}
> $$
> ，上式两端从 $\tau_k$ 到 $t_k$ 积分得 
> $$
> ln(A\sqrt{n}r(t_k)+B) - ln(A\sqrt{n}r(\tau_k)+B)) \leq An(t_k - \tau_k) \leq An(b - t_0)
> $$
> ，上式右端是有限的，而由 $t(\tau_k) \geq K$ 知，当 $K$ 充分大时，上式左端可以任意大，矛盾！这说明 $x = \varphi(t)$ 在 $[t_0, b)$ 有界。



定理 5.6 中的条件可以推广为
$$
|f(t,x)| \leq G(||x||),(t,x) \in G,
$$
其中 $G(s)$ 在 $s \geq 0$ 上连续，当 $s > 0$ 时，$G(s) > 0$，且
$$
\int_{s_0}^{+\infty} \frac{ds}{G(s)} = +\infty,s_0 > 0
$$




### 定理 5.7

若 $f(t,x)$ 在 $G$ 内连续且满足上述条件，则 $\dot{x} = f(t,x)$ 的任何饱和解 $x = \varphi(t)$ 都在区间 $(T_0, T_1)$ 上存在。

![image-20251128130927795](C:\Users\浪涛依旧铭记\AppData\Roaming\Typora\typora-user-images\image-20251128130927795.png)

> [!tip]
> 若不存在 $t_0$ 使得 $\lim\limits_{t \rightarrow t_0}|x(t)| \rightarrow + \infty$，则可以构造有界域 $D = \{(t,x)| -h < t < h,|x| < 2 \cdot M$，$M$ 是 $x(t)$ 在有限区间 $(-h, h)$ 的一个上界。则 $x(t)$ 可以拓展到 $D$ 的边界，而 $x(t)$ 达不到 $|x| = 2 \cdot M\}$，故 $x(t)$ 可以拓展到 $(-h, h)$，由 $h$ 的任意性知 $x(t)$ 可以拓展到 $(-\infty,+\infty)$。
> 由 $p \rightarrow q \Leftrightarrow \neg q \rightarrow \neg p$ 知不能拓展到 $(-\infty,+\infty)\Rightarrow$ 存在 $t_0 > 0$，使 $\lim\limits_{t \rightarrow t_0} |x(t)| \rightarrow + \infty$。 

![image-20251128130934942](C:\Users\浪涛依旧铭记\AppData\Roaming\Typora\typora-user-images\image-20251128130934942.png)

![image-20251128130940762](C:\Users\浪涛依旧铭记\AppData\Roaming\Typora\typora-user-images\image-20251128130940762.png)






## 解对初值和参数的连续性

以下我们假设 $f(t,x)$ 在 $(t,x)$ 空间的域 $G$ 内连续，且局部地满足利氏条件。

根据推论 2.1 和 定理 5.1，对任意 $(\tau,\xi) \in G$，方程组 $(E) : \dot{x} = f(t,x)$ 的满足初值条件 $x(\tau) = \xi$ 的饱和解存在且唯一，记为 $$x = \varphi(t, \tau, \xi)$$，设其存在区间为 $(a(\tau,\xi),b(\tau,\xi))$，则 $\varphi(t,\tau,\xi)$ 是集合 
$$
S = \{(t,\tau,\xi)|t\in(a(\tau,\xi),b(\tau,\xi)),(\tau,\xi) \in G\},(6.1)
$$
上的 $n + 2$ 元向量函数。（$t, \tau$ 为一元，$\xi$ 为 $n$ 元）





### 定理 6.1

若 $x = \psi(t)$ 是方程组 $(E)$ 的解，$[\alpha,\beta]$ 是其存在区间的任一有限子区间，则存在 $\delta > 0$，使得当 $$\tau \in [\alpha, \beta]，|\xi - \psi(\tau)| \leq \delta$$ 时，方程组 $(E)$ 的解 $x = \varphi(t, \tau, \xi)$ 至少在 $[\alpha, \beta]$ 上有定义，并且对 $(t, \tau, \xi)$ 是闭域
$$
V = \{(t, \tau, \xi)| t\in [\alpha, \beta], \tau \in [\alpha,\beta], |\xi - \psi(\tau)| \leq \delta\}
$$
上的连续函数。

定理 6.1 在理论和应用上都有重要意义。我们知道，在实际应用中，微分方程往往描述某种物理过程。将一个物理过程化为微分方程的初值问题时，初值条件是通过测量确定的，而测量一般不能保证绝对准确。如果初值的微小误差引起对应的解有很大变动，那么所求得的初值问题的解的使用价值就会很小。有了定理 6.1，这种情形就不会发生。

![image-20251128130815600](C:\Users\浪涛依旧铭记\AppData\Roaming\Typora\typora-user-images\image-20251128130815600.png)

![image-20251128130827395](C:\Users\浪涛依旧铭记\AppData\Roaming\Typora\typora-user-images\image-20251128130827395.png)

![image-20251128130836559](C:\Users\浪涛依旧铭记\AppData\Roaming\Typora\typora-user-images\image-20251128130836559.png)

![image-20251128130845993](C:\Users\浪涛依旧铭记\AppData\Roaming\Typora\typora-user-images\image-20251128130845993.png)



### 推论 6.1

若方程组 $(E)$ 的解 $x = \varphi(t,\tau_0,\xi_0)$ 在有限闭区间 $[\alpha,\beta]$ 上有定义，$\tau_0 \in (\alpha, \beta)$，则当 $(\tau,\xi)$ 与 $(\tau_0, \xi_0)$ 充分靠近时，解 $x = \varphi(t, \tau, \xi)$ 在 $[\alpha,\beta]$ 上有定义，且对 $t \in [\alpha,\beta]$ 一致地有 
$$
\lim_\limits{(\tau,\xi)\rightarrow(\tau_0, \xi_0)} \varphi(t,\tau,\xi) = \varphi(t, \tau_0, \xi_0)
$$


> [!tip]
>
> 由 $\varphi(t,\tau,\xi)$ 是 $V$ 上的关于 $(t,\tau,\xi)$ 的连续函数，显然。





### 推论 6.2

方程组 $(E)$ 的解 $x = \varphi(t, \tau, \xi)$ 在由 $(6.1)$ 式表示的集合 $S$ 上连续。此外，$S$ 是 $(t,\tau,\xi)$ 空间上的开集。





---



下面考虑含参量 $\lambda$ 的方程组 
$$
\frac{dx}{dt} = f(t,x,\lambda),(E)_\lambda
$$


设 $G$ 为 $(t,x)$ 空间的域，$D$ 为 $\lambda$ 空间的域，假设 $f(t,x,\lambda)$ 在 $$G \times D = \{(t,x,\lambda)|(t,x) \in G, \lambda \in D\}$$ 内连续，且对 $(x,\lambda)$ 局部地满足利氏条件，则根据存在与唯一性定理，对任意 $\lambda \in D$ 和 $(\tau,\xi) \in G$，初值问题 $(E)_\lambda,x(\tau) = \xi$ 的饱和解存在且唯一，记为 $x = \varphi(t,\tau,\xi,\lambda)$。



### 定理 6.2
设 $f(t,x,\lambda)$ 于域 $G\times D$ 内连续，且对 $(x, \lambda)$ 局部地满足利氏条件。若 $x = \psi(t)$ 是方程组 $(E)_{\lambda_0},\lambda_0 \in D$ 的一个解，$[\alpha,\beta]$ 是其存在区间的任一有限闭子区间，则存在 $\delta > 0$，使得 $x = \varphi(t,\tau,\xi,\lambda)$ 于闭域 $$V = \{(t,\tau,\xi,\lambda)| t,\tau \in [\alpha,\beta],|\xi - \psi(\tau)| + |\lambda - \lambda_0| \leq \delta\}$$ 上有定义且连续。

![image-20251128130801307](C:\Users\浪涛依旧铭记\AppData\Roaming\Typora\typora-user-images\image-20251128130801307.png)

类似地有推论 6.3 和 推论 6.4


![image-20251128130736872](C:\Users\浪涛依旧铭记\AppData\Roaming\Typora\typora-user-images\image-20251128130736872.png)





## 解对初值和参数的可微性



### Bellman-Gronwall 不等式

设 $x(t)$ 和 $f(t)$ 是区间 $[t_1, t_2]$ 上非负连续的纯量函数。若存在非负常数 $k$ 和 $\tau \in (t_1， t_2)$，使得 
$$
x(t) \leq k + | \int_\tau^tf(s)x(s)ds|, \space t \in(t_1,t_2)
$$
，则 
$$
x(t) \leq k e^{|\int_\tau^tf(s)ds|}, \space t \in (t_1, t_2)
$$





### 定理 7.1 解对初值的可微性

若 $f(t, x)$ 及其对 $x$ 的各分量的偏微商于 $(t,x)$ 空间域 $G$ 内连续，则方程组 $(E)$ 的解 $x = \varphi(t, \tau, \xi)$ 在集合 $$S = \{(t, \tau, \xi) | t \in (a(\tau, \xi), b(\tau, \xi)), (\tau, \xi) \in G\}$$ 内连续可微，且 $y = \frac{\partial\varphi}{\partial\xi_i}(t, \tau, \xi)(i = 1, 2, \dots, n), y = \frac{\partial\varphi}{\partial\tau}(t, \tau, \xi)$ 分别是初值问题
$$
\begin{align}
&y^{'} = f_x(t, \varphi(t, \tau, \xi))y,\space y(\tau) = e_i,\space i = 1, 2, \dots, n \space \space(7.3) \\
&y^{'} = f_x(t, \varphi(t, \tau, \xi))y,\space y(\tau) = -f(\tau, \xi) \space (7.4)
\end{align}
$$

的解，其中 $f_x(t,x)$ 是 $f(t,x)$ 关于 $x$ 的雅可比（Jacobi）矩阵，$\xi_i$ 是 $\xi$ 的第 $i$ 个分量，$e_i$ 是第 $i$ 个 $n$ 维基本列向量。



#### 注 7.1

当 $n = 1$ 时，
$$
\begin{align}
\frac{\partial\varphi}{\partial \xi}(t, \tau, \xi) = exp \{ \int_\tau^t f_x(s, \varphi(s,\tau,\xi))ds \} \\
\frac{\partial\varphi}{\partial \tau} = - f(\tau, \xi)exp \{\int_\tau^t f_x(s, \varphi(s, \tau, \xi))ds\}
\end{align}
$$


#### 注 7.2

反复利用上述各式，可以进一步得到关于解对初值的高阶可微性定理。例如，若 $f(t,x)$ 对 $x$ 的直到 $r(r \geq 1)$ 阶微商都在域 $G$ 内连续，则 $\varphi(t, \tau, \xi)$ 对 $\xi$ 的直到 $r$ 阶微商都连续。





### 定理 7.2 解对参量的连续性

若 $f(t, x, \lambda)$ 及其对 $x$ 于 $\lambda$ 的各个分量的偏微商于域 $G \times D$ 内连续，则对任意 $(\tau, \xi, \lambda) \in G \times D$，方程组 $(E)_\lambda$ 的解 $x = \varphi(t, \tau, \xi, \lambda)$ 在
$$
S = \{(t, \tau, \xi, \lambda) | t \in (a(\tau, \xi, \lambda),b(\tau,\xi, \lambda)), (\tau, \xi, \lambda) \in G \times D\}
$$
内连续可微，且 
$$
y = \frac{\partial\varphi}{\partial\xi_i}(t, \tau, \xi, \lambda)(i = 1, 2, \dots, n), \space y = \frac{\partial\varphi}{\partial \tau}(t, \tau, \xi, \lambda), \space y = \frac{\partial\varphi}{\partial \lambda_j}(t, \tau, \xi, \lambda)(j = 1, 2, \dots, m)
$$
 分别是初值问题 
$$
\begin{align}
&y^{'} = f_x(t, \varphi(t, \tau, \xi, \lambda), \lambda)y, \space y(\tau) = e_i, \space i = 1, 2, \dots, n  \\
&y^{'} = f_x(t, \varphi(t, \tau, \xi, \lambda), \lambda)y, \space y(\tau) = -f(\tau, \xi, \lambda) \\
&y^{'} = f_x(t, \varphi(t, \tau, \xi, \lambda), \lambda)y + f_{\lambda_j}(t, \varphi(t, \tau, \xi, \lambda), \lambda), \space y(\tau) = 0, \space j = 1, 2, \dots, m
\end{align}
$$
的解，其中 $\lambda_j$ 是 $\lambda$ 的第 $j$ 个分量。





---



# 第五章：定性理论初步



## 解的稳定性

### 定义 1.1 李雅普诺夫稳定

设方程组 $(E)$ 的解 $x = \varphi(t, \tau, \xi_0)$ 在区间 $[\tau, +\infty)$ 有定义。若对任给的 $\epsilon > 0$，都存在 $\delta > 0$，使得当 $|\xi - \xi_0| < \delta$ 时，解 $x = \varphi(t, \tau, \xi)$ 在区间 $[\tau, +\infty)$ 有定义，且 $$|\varphi(t, \tau, \xi) - \varphi(t, \tau, \xi_0)| < \epsilon, \space t \in [\tau, +\infty)$$，则称 $x = \varphi(t, \tau, \xi)$ （在李雅普诺夫意义下）是 **稳定** 的。否则，称 $x = \varphi(t, \tau, \xi_0)$ 是 **不稳定** 的。






### 定义 1.2 渐近稳定和全局渐近稳定

若 $x = \varphi(t, \tau, \xi_0)$ 是稳定的，且存在 $\delta_0 > 0$，使得只要 $|\xi - \xi_0| < \delta_0$，就有 $$\lim\limits_{t \rightarrow +\infty}(\varphi(t, \tau, \xi) - \varphi(t, \tau, \xi_0)) = 0$$，则称 $x = \varphi(t, \tau, \xi_0)$ （在李雅普诺夫意义下）是 **渐近稳定** 的。若 $G = \mathbb{R}^n$，且渐近稳定定义中 $\delta_0$ 可取 $+\infty$，则称解 $x = \varphi(t, \tau, \xi_0)$ 是 **全局渐近稳定** 的。



讨论
$$
\frac{dx}{dt} = A(t)x, \space (1.3)
$$
零解的稳定性





### 定理 1.1

设 $\Phi(t)$ 是方程组 $(1.3)$ 的基本解矩阵，则方程组的零解
1. 是稳定的，当且仅当 $\Phi(t)$ 在区间 $[0, +\infty)$ 上有界。
2. 是渐近稳定的，当且仅当 $\lim\limits_{t \rightarrow +\infty}\Phi(t) = 0$






### 定理 1.2

当 $A(t)$ 是常矩阵 $A$ 时，方程组 $(1.3)$ 的零解
1. 是渐近稳定的（也是全局渐近稳定），当且仅当 $A$ 的全部特征值都有负实部。
2. 是稳定的，当且仅当 $A$ 的全部特征值的实部是非正的，并且实部为零的特征值对应的若尔当小块都是一阶的。
3. 是不稳定的，当且仅当 $A$ 的特征值中至少有一个实部为正，或者至少有一个实部为零，而它所对应的若尔当小块是高于一阶的。

方程
$$
\frac{dx}{dt} = A(t)x + R(t, x), \space (1.2)
$$
，$A(t)$ 在区间 $[\tau, +\infty)$ 上连续，$R(t,x)$ 于 $\Omega = \{(t, x) | t \in [\tau, +\infty), |x| < H\}$ 上连续，局部地满足利氏条件，$R(t, 0) = 0$，且对 $t \in [\tau, +\infty)$ 一致地有 
$$
\lim\limits_{|x| \rightarrow 0} \frac{R(t,x)}{|x|} = 0
$$






### 定理 1.3
设 $A(t)$ 是常矩阵 $A$，
1. 若 $A$ 的全部特征值都有负实部，则方程组 $(1.2)$ 的零解是渐近稳定的。
2. 若 $A$ 的特征值中至少有一个具有正实部，则方程组 $(1.2)$ 的零解是不稳定的。



## 李雅普诺夫第二方法

考虑 **自治方程组（注定系统）** 零解的稳定性
$$
\frac{dx}{dt} = f(x)
$$
李雅普诺夫函数 $V(x)$ ，
$$
\frac{dV}{dt}_{(E)_a} = \sum\limits_{i = 1}^n \frac{\partial V(x)}{\partial x_i}f_i(x)
$$
称为 $V(x)$ 沿着方程组 $(E)_a$ 的方向导数。



$V(x)$ 是零点附近的定正函数

1. 方向导数是常负函数，零解稳定
2. 方向导数是定负函数，零解渐近稳定
3. 方向导数是定正函数，零解不稳定



- 注意，取不同的李雅普诺夫函数 $V(x)$，得到的结果可能不一样，即可能得到稳定也可能得到渐近稳定。但是稳定和不稳定一定是对立的，即不可能有两个不同的李雅普诺夫函数分别得到稳定和不稳定的结果。



## 一般定性理论的概念

考虑自治方程组
$$
\frac{dx}{dt} = f(x)
$$
，假设 $f(x)$ 于 $\mathbb{R}^n$ 连续可微。

- 称 $x$ 取值的空间为 **相空间**

- 方程组过点 $(\tau, \xi) \in \mathbb{R} \times \mathbb{R}^n$ 的解曲线 $x = \varphi(t, \tau, \xi)$ 是通过相空间中点 $\xi$ 的与 **速度场** 相吻合的一条光滑曲线，称为 **轨线**

- 方程组所有 **轨线** 构成 **相图**

- $f(x_0) = 0$，则 $x = x_0$ 是方程组的一个定常解（与时间 $t$ 无关），速度向量是零向量，方向无法确定。称 $x_0$ 为 **奇点**

- 若存在正数 $\omega$，使得 $\varphi(\omega, \xi) = \xi$，则有 
  $$
  \varphi(t + \omega, \xi) = \varphi(t, \xi), \qquad t\in \mathbb{R}
  $$
  称 $x = \varphi(t, \xi)$ 是方程组的一个 $\omega$ - 周期解，不是定常解的周期解所对应的轨线称之为 **闭轨**

- **闭轨的稳定性** 类似李雅普诺夫稳定性，但是和李雅普诺夫稳定性不同，主要体现在 $\xi$ 的选取范围上





## 平面动力系统

考虑平面动力系统
$$
\frac{dx}{dt} = X(x,y), \space \frac{dy}{dt} = Y(x, y), \qquad (3.1)
$$
其中 $X(x,y)$ 和 $Y(x,y)$ 于 $\mathbb{R}^2$ 连续可微。





### 平面动力系统的奇点

设 $p = tr A, q = det A$，分类原点作为奇点时的类型

1. 当 $p^2 = 4q$ 时，有两个相同实特征值，如果可对角化（Jordan 块是一阶的），星形节点；如果不可对角化（Jordan 块是二阶的），单向结点
   - 判断是否是单向结点很简单，随便取一条过原点的直线，如果它不给出特殊方向，那就一定是单向结点
   - 设 $k$ 解出单向结点特殊方向
   - 再随便取几个特殊点逼近一下
   - 星形结点只需要判断方向即可，很好画
2. 当 $p^2 > 4q > 0$ 时，有两个同号的实特征值，双向节点
   - 作图时要考虑两条特殊方向，以及其他轨线与哪条特殊方向代表的直线相切
   - 特殊方向直接设 $k$ 解方程
   - 相切情况看两条特殊直线中间直线上方向向量
3. 当 $q < 0$ 时，有两个异号的实特征值，鞍点
   - 作图时也要考虑两条特殊方向，求法同双向结点，其他轨线靠近哪条特殊直线时方向就和它靠近的特殊直线方向相同
4. 当 $0 < p^2 < 4q$ 时，有两个共轭复特征值，为焦点
5. 当 $q > 0, p = 0$ 时，有两个纯虚数特征值，为中心点

此外，在情形 1，2，4 中，奇点 $(0, 0)$ 的稳定性由 $p$ 的符号决定：当 $p < 0$ 时稳定，当 $p > 0$ 时不稳定（因为 $p$ 反应了特征值的实部，矩阵的迹就是所有特征值的和） 





### 平面动力系统的极限环

极限环：孤立闭轨，存在闭轨的一个邻域，在这个邻域内系统无其他闭轨。





### 庞加莱-本迪克松定理

设 $D$ 是由两条简单闭曲线 $\Gamma_1$ 和 $\Gamma_2$ 所围成的环域，且在 $\overline D = \Gamma_1 \cup D \cup \Gamma_2$ 上，系统

无奇点。如果从 $\Gamma_1$ 和 $\Gamma_2$ 上出发的轨线都不离开（或都不进入）$\overline D$，而 $\Gamma_1$ 和 $\Gamma_2$ 都不是系统 (3.1) 的闭轨，则系统在 $D$ 内至少有一条闭轨 $\Gamma$

- 解题方法论~~（背马原背上头了）~~：验证内部无奇点，分析边界速度场。





### 本迪克松准则

设 $X(x,y), Y(x,y)$ 在单连通区域 $D$ 上连续可微，若散度 
$$
div(X,Y) = \frac{\partial X}{\partial x} + \frac{\partial Y}{\partial y}
$$
在 $D$ 的任何子区域中不恒为零，且在 $D$ 中保持定号，则方程组 (3.1) 在 $D$ 中无闭轨。

