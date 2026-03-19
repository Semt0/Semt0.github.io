---
date: 2026-03-19
---

## LU 分解

### LU 分解的引入

Gauss 消去法（以及列主元消去法）背后都对应一种矩阵分解思想：把系数矩阵分解为下三角与上三角的乘积。

定义 **LU 分解** ：若矩阵 \(A\in\mathbb R^{n\times n}\) 可写为

\[
A = L U
\]

其中 \(L\) 为下三角矩阵，\(U\) 为上三角矩阵，则称 \(A\) 存在 LU 分解。

由于分解不唯一，通常约定 \(L\) 为 **单位下三角矩阵** （对角线全为 1），从而 LU 分解唯一（在满足存在性条件时）。

!!! tips "证明思路"

    这一段的关键点是： **LU 分解本质上就是把 Gauss 消去过程“矩阵化”** 。

    - 先假设消元过程中每一步主元 \(a_{kk}\neq 0\)，则存在一系列消元矩阵 \(M_1,\dots,M_{n-1}\) 使得

    \[
    U = M_{n-1}\cdots M_2 M_1 A
    \]

    其中 \(U\) 为上三角矩阵（也就是消元后的系数矩阵）。

    - 把两边左乘逆矩阵并令

    \[
    L = M_1^{-1} M_2^{-1} \cdots M_{n-1}^{-1}
    \]

    即得 \(A = L U\)。由于每个 \(M_k^{-1}\) 都是单位下三角形式的初等矩阵，所以 \(L\) 也是 **单位下三角矩阵** 。

    - 若不强制 \(L\) 的对角线为 1，则可把任意可逆对角矩阵 \(D\) 吸收进 \(L\) 或 \(U\)：\(A=(L D)(D^{-1}U)\)，因此分解不唯一；规定 \(L\) 为单位下三角后，分解被固定（在存在时唯一）。

若已得 \(A = L U\)，则线性方程组

\[
A x = b
\]

可改写为

\[
L U x = b
\]

令 \(y \equiv U x\)，则分两步求解：


- 先解 \(L y = b\)（前代）；
- 再解 \(U x = y\)（回代）。

### LU 矩阵的计算（系数比较 / 递推）

对 \(A = L U\)（其中 \(L\) 单位下三角，\(U\) 上三角）逐行逐列比较系数，可得到典型递推关系。

首先 \(U\) 的第一行直接等于 \(A\) 的第一行：

\[
u_{1j} = a_{1j},\quad j=1,2,\dots,n .
\]

随后由第一列比较得到 \(L\) 的第一列（除对角元外）：

\[
l_{i1} u_{11} = a_{i1}\;\Rightarrow\; l_{i1}=\frac{a_{i1}}{u_{11}},\quad i=2,3,\dots,n .
\]

再由第二行（及后续行）比较得到 \(U\) 的元素，例如

\[
l_{21} u_{2j} + u_{2j} = a_{2j}
\]

在课件中写成更一般的递推形式（见下方算法）。

### 算法与复杂度

#### 算法 3.1（显式存储 \(L,U\)）

输入：\(A\in\mathbb R^{n\times n}\)（存于 `a[i,j]`）  
输出：单位下三角矩阵 \(L\)（存于 `l[i,j]`）与上三角矩阵 \(U\)（存于 `u[i,j]`），使 \(A=L U\)

```text
l[i,j] = 0, l[i,i] = 1
u[i,j] = 0
for k = 1..n:
    for j = k..n:
        u[k,j] = a[k,j]
        for m = 1..k-1:
            u[k,j] = u[k,j] - l[k,m] * u[m,j]
    for i = k+1..n:
        l[i,k] = a[i,k]
        for m = 1..k-1:
            l[i,k] = l[i,k] - l[i,m] * u[m,k]
        l[i,k] = l[i,k] / u[k,k]
```

乘除法量级约为

\[
2\sum_{k=1}^{n-1}(n-k)k + n \approx \frac{n^3}{3} .
\]

=== "Python"

    ```python
    import numpy as np
    
    def lu_explicit(A):
        """
        LU 分解 - 显式存储 L 和 U
        
        参数:
            A: n×n 系数矩阵 (numpy array)
        返回:
            L: 单位下三角矩阵
            U: 上三角矩阵
        """
        n = A.shape[0]
        L = np.eye(n)  # L 初始化为单位矩阵
        U = np.zeros((n, n))
        
        for k in range(n):
            # 计算 U 的第 k 行
            for j in range(k, n):
                U[k, j] = A[k, j]
                for m in range(k):
                    U[k, j] -= L[k, m] * U[m, j]
            
            # 计算 L 的第 k 列（对角线以下）
            for i in range(k + 1, n):
                L[i, k] = A[i, k]
                for m in range(k):
                    L[i, k] -= L[i, m] * U[m, k]
                L[i, k] /= U[k, k]  # 除以主元
        
        return L, U
    ```

=== "C++"

    ```cpp
    #include <vector>
    #include <cmath>
    
    using Matrix = std::vector<std::vector<double>>;
    
    /**
     * LU 分解 - 显式存储 L 和 U
     * 
     * 参数:
     *   A: n×n 系数矩阵 (按值传递，不会被修改)
     *   L: 输出参数，单位下三角矩阵
     *   U: 输出参数，上三角矩阵
     * 返回:
     *   成功返回 true，若遇到零主元返回 false
     */
    bool luExplicit(const Matrix& A, Matrix& L, Matrix& U) {
        int n = A.size();
        L.assign(n, std::vector<double>(n, 0.0));
        U.assign(n, std::vector<double>(n, 0.0));
        
        // L 初始化为单位矩阵
        for (int i = 0; i < n; ++i) {
            L[i][i] = 1.0;
        }
        
        for (int k = 0; k < n; ++k) {
            // 计算 U 的第 k 行
            for (int j = k; j < n; ++j) {
                U[k][j] = A[k][j];
                for (int m = 0; m < k; ++m) {
                    U[k][j] -= L[k][m] * U[m][j];
                }
            }
            
            // 检查主元
            if (std::abs(U[k][k]) < 1e-15) {
                return false;  // 遇到奇异矩阵
            }
            
            // 计算 L 的第 k 列（对角线以下）
            for (int i = k + 1; i < n; ++i) {
                L[i][k] = A[i][k];
                for (int m = 0; m < k; ++m) {
                    L[i][k] -= L[i][m] * U[m][k];
                }
                L[i][k] /= U[k][k];
            }
        }
        
        return true;
    }
    ```

#### 原位存储（把 \(L\) 与 \(U\) 塞回 \(A\) 里）

由于 \(L\) 的对角线全为 1，可以不存；把

- \(U\) 放在 \(A\) 的上三角（含对角）位置；
- \(L\) 的严格下三角元素放在 \(A\) 的下三角位置；

即最终内存中的 \(A\) 形如

\[
\begin{bmatrix}
u_{11} & u_{12} & \cdots & u_{1n}\\
l_{21} & u_{22} & \cdots & u_{2n}\\
\vdots & \vdots & \ddots & \vdots\\
l_{n1} & l_{n2} & \cdots & u_{nn}
\end{bmatrix}.
\]

算法 3.2（原位存储）：

```text
for k = 1, 2, ..., n do
    // 计算 U 的第 k 行（已在上三角位置）
    for j = k, k+1, ..., n do
        for m = 1, 2, ..., k-1 do
            a[k,j] ← a[k,j] - a[k,m] * a[m,j]
    end for
    // 计算 L 的第 k 列（存储到下三角位置）
    for i = k+1, k+2, ..., n do
        for m = 1, 2, ..., k-1 do
            a[i,k] ← a[i,k] - a[i,m] * a[m,k]
        a[i,k] ← a[i,k] / a[k,k]
    end for
end for
```

=== "Python"

    ```python
    import numpy as np
    
    def lu_inplace(A):
        """
        LU 分解 - 原位存储（Doolittle 算法）
        
        参数:
            A: n×n 系数矩阵 (会被修改，存储 L 和 U)
        返回:
            A: 修改后的矩阵，其中:
               - 上三角部分（含对角线）存储 U
               - 严格下三角部分存储 L（对角线隐含为 1）
        """
        n = A.shape[0]
        
        for k in range(n):
            # 计算 U 的第 k 行（已在上三角位置）
            for j in range(k, n):
                for m in range(k):
                    A[k, j] -= A[k, m] * A[m, j]
            
            # 计算 L 的第 k 列（存储到下三角位置）
            for i in range(k + 1, n):
                for m in range(k):
                    A[i, k] -= A[i, m] * A[m, k]
                A[i, k] /= A[k, k]
        
        return A
    
    def solve_lu_inplace(A_lu, b):
        """
        利用原位存储的 LU 分解求解 Ax = b
        
        参数:
            A_lu: 经过 lu_inplace 处理后的矩阵
            b: 右端向量
        返回:
            x: 解向量
        """
        n = len(b)
        x = np.zeros(n)
        y = np.zeros(n)
        
        # 前代：解 Ly = b（L 对角线隐含为 1）
        for i in range(n):
            y[i] = b[i]
            for j in range(i):
                y[i] -= A_lu[i, j] * y[j]  # L[i,j] 存储在 A_lu 的下三角
        
        # 回代：解 Ux = y
        for i in range(n - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, n):
                x[i] -= A_lu[i, j] * x[j]  # U[i,j] 存储在 A_lu 的上三角
            x[i] /= A_lu[i, i]  # U[i,i] 在对角线上
        
        return x
    ```

=== "C++"

    ```cpp
    #include <vector>
    #include <cmath>
    
    using Matrix = std::vector<std::vector<double>>;
    
    /**
     * LU 分解 - 原位存储（Doolittle 算法）
     * 
     * 参数:
     *   A: n×n 矩阵，会被原地修改为:
     *      - 上三角部分（含对角线）存储 U
     *      - 严格下三角部分存储 L（对角线隐含为 1）
     * 返回:
     *   成功返回 true，若遇到零主元返回 false
     */
    bool luInPlace(Matrix& A) {
        int n = A.size();
        
        for (int k = 0; k < n; ++k) {
            // 计算 U 的第 k 行
            for (int j = k; j < n; ++j) {
                for (int m = 0; m < k; ++m) {
                    A[k][j] -= A[k][m] * A[m][j];
                }
            }
            
            // 检查主元
            if (std::abs(A[k][k]) < 1e-15) {
                return false;
            }
            
            // 计算 L 的第 k 列（存储到下三角）
            for (int i = k + 1; i < n; ++i) {
                for (int m = 0; m < k; ++m) {
                    A[i][k] -= A[i][m] * A[m][k];
                }
                A[i][k] /= A[k][k];
            }
        }
        
        return true;
    }
    
    /**
     * 利用原位存储的 LU 分解求解 Ax = b
     * 
     * 参数:
     *   A_lu: 经过 luInPlace 处理后的矩阵
     *   b: 右端向量
     * 返回:
     *   x: 解向量
     */
    std::vector<double> solveLuInPlace(const Matrix& A_lu, 
                                       const std::vector<double>& b) {
        int n = b.size();
        std::vector<double> x(n), y(n);
        
        // 前代：解 Ly = b（L 对角线隐含为 1）
        for (int i = 0; i < n; ++i) {
            y[i] = b[i];
            for (int j = 0; j < i; ++j) {
                y[i] -= A_lu[i][j] * y[j];  // L[i][j] 在下三角
            }
        }
        
        // 回代：解 Ux = y
        for (int i = n - 1; i >= 0; --i) {
            x[i] = y[i];
            for (int j = i + 1; j < n; ++j) {
                x[i] -= A_lu[i][j] * x[j];  // U[i][j] 在上三角
            }
            x[i] /= A_lu[i][i];  // U[i][i] 在对角线上
        }
        
        return x;
    }
    ```

#### 改进版本（向量化优化）

算法 3.3（改进原位，适合按行存储）：

```text
for k = 1, 2, ..., n-1 do
    // 计算 L 的第 k 列乘子
    for i = k+1, k+2, ..., n do
        a[i,k] ← a[i,k] / a[k,k]
    end for
    // 更新 Schur 补（右下角子矩阵）
    for i = k+1, k+2, ..., n do
        for j = k+1, k+2, ..., n do
            a[i,j] ← a[i,j] - a[i,k] * a[k,j]
        end for
    end for
end for
```

算法 3.4（向量化版本，适合按行存储）：

```text
for k = 1, 2, ..., n-1 do
    a[k+1:n,k] ← a[k+1:n,k] / a[k,k]           // 向量除法
    for i = k+1, k+2, ..., n do
        a[i,k+1:n] ← a[i,k+1:n] - a[i,k] * a[k,k+1:n]  // 向量减向量乘标量
    end for
end for
```

算法 3.5（向量化版本，适合按列存储）：

```text
for k = 1, 2, ..., n-1 do
    a[k+1:n,k] ← a[k+1:n,k] / a[k,k]           // 向量除法
    for j = k+1, k+2, ..., n do
        a[k+1:n,j] ← a[k+1:n,j] - a[k+1:n,k] * a[k,j]  // 向量减向量乘标量
    end for
end for
```

=== "Python（向量化版本）"

    ```python
    import numpy as np
    
    def lu_inplace_optimized(A):
        """
        LU 分解 - 改进原位算法（向量化优化）
        
        参数:
            A: n×n 系数矩阵 (numpy array, 会被修改)
        返回:
            A: 修改后的矩阵，存储 L 和 U
        """
        n = A.shape[0]
        
        for k in range(n - 1):
            # 计算 L 的第 k 列（向量化除法）
            A[k+1:n, k] /= A[k, k]
            
            # 更新 Schur 补（向量化操作）
            # A[i,j] = A[i,j] - A[i,k] * A[k,j]
            # 使用外积更新子矩阵
            A[k+1:n, k+1:n] -= np.outer(A[k+1:n, k], A[k, k+1:n])
        
        return A
    
    def lu_row_oriented(A):
        """
        按行存储优化的 LU 分解（算法 3.4）
        
        参数:
            A: n×n 系数矩阵 (numpy array)
        返回:
            A: 修改后的矩阵
        """
        n = A.shape[0]
        
        for k in range(n - 1):
            # 向量除法：计算乘子
            A[k+1:n, k] = A[k+1:n, k] / A[k, k]
            
            # 按行更新（适合行存储内存布局）
            for i in range(k + 1, n):
                # 向量减向量乘标量
                A[i, k+1:n] = A[i, k+1:n] - A[i, k] * A[k, k+1:n]
        
        return A
    
    def lu_col_oriented(A):
        """
        按列存储优化的 LU 分解（算法 3.5）
        
        参数:
            A: n×n 系数矩阵 (numpy array)
        返回:
            A: 修改后的矩阵
        """
        n = A.shape[0]
        
        for k in range(n - 1):
            # 向量除法：计算乘子
            A[k+1:n, k] = A[k+1:n, k] / A[k, k]
            
            # 按列更新（适合列存储内存布局，如 Fortran）
            for j in range(k + 1, n):
                # 向量减向量乘标量
                A[k+1:n, j] = A[k+1:n, j] - A[k+1:n, k] * A[k, j]
        
        return A
    ```

=== "C++（向量化版本）"

    ```cpp
    #include <vector>
    #include <cmath>
    
    using Matrix = std::vector<std::vector<double>>;
    
    /**
     * LU 分解 - 改进原位算法（算法 3.3）
     * 
     * 参数:
     *   A: n×n 矩阵，会被原地修改
     * 返回:
     *   成功返回 true
     */
    bool luInPlaceOptimized(Matrix& A) {
        int n = A.size();
        
        for (int k = 0; k < n - 1; ++k) {
            // 检查主元
            if (std::abs(A[k][k]) < 1e-15) {
                return false;
            }
            
            // 计算 L 的第 k 列乘子
            for (int i = k + 1; i < n; ++i) {
                A[i][k] /= A[k][k];
            }
            
            // 更新 Schur 补（右下角子矩阵）
            for (int i = k + 1; i < n; ++i) {
                for (int j = k + 1; j < n; ++j) {
                    A[i][j] -= A[i][k] * A[k][j];
                }
            }
        }
        
        return true;
    }
    
    /**
     * 按行存储优化的 LU 分解（算法 3.4）
     * 内存访问模式更适合 C/C++ 的行主序数组
     */
    bool luRowOriented(Matrix& A) {
        int n = A.size();
        
        for (int k = 0; k < n - 1; ++k) {
            if (std::abs(A[k][k]) < 1e-15) {
                return false;
            }
            
            // 计算乘子
            for (int i = k + 1; i < n; ++i) {
                A[i][k] /= A[k][k];
            }
            
            // 按行更新（内层循环访问连续内存）
            for (int i = k + 1; i < n; ++i) {
                double lik = A[i][k];
                for (int j = k + 1; j < n; ++j) {
                    A[i][j] -= lik * A[k][j];
                }
            }
        }
        
        return true;
    }
    
    /**
     * 按列存储优化的 LU 分解（算法 3.5）
     * 内存访问模式更适合 Fortran 的列主序数组
     */
    bool luColOriented(Matrix& A) {
        int n = A.size();
        
        for (int k = 0; k < n - 1; ++k) {
            if (std::abs(A[k][k]) < 1e-15) {
                return false;
            }
            
            // 计算乘子
            for (int i = k + 1; i < n; ++i) {
                A[i][k] /= A[k][k];
            }
            
            // 按列更新（内层循环访问连续内存）
            for (int j = k + 1; j < n; ++j) {
                double akj = A[k][j];
                for (int i = k + 1; i < n; ++i) {
                    A[i][j] -= A[i][k] * akj;
                }
            }
        }
        
        return true;
    }
    ```

#### LU 分解与 Gauss 消去的关系

从计算复杂度角度，LU 分解与 Gauss 消去同阶；但当需要对同一 \(A\) 解多个不同右端项 \(b\) 时，先做一次 LU 分解会更划算（后续只需重复前代 + 回代）。

### LU 分解的存在性

定理 **LU 存在唯一性条件** ：矩阵 \(A\in\mathbb R^{n\times n}\) 存在唯一（\(L\) 为单位下三角）的 LU 分解的充要条件是：对所有 \(k=1,2,\dots,n-1\)，其 \(k\) 阶顺序主子阵 \(A_k\) 的行列式不为 0。

!!! note "证明"

    **充分性（归纳构造）**

    对矩阵阶数 \(n\) 作数学归纳法。

    - \(n=1\) 时：\(A=[a_{11}]\)，取 \(L=[1],\;U=[a_{11}]\) 即可，分解显然存在且唯一。

    - 设对所有 \((n-1)\times(n-1)\) 阶矩阵，只要各顺序主子阵非奇异就存在唯一分解，现考察 \(n\) 阶情形。

    将 \(A\) 写成分块形式

    \[
    A=\begin{bmatrix}a_{11}&u^T\\l&B\end{bmatrix},
    \quad a_{11}\in\mathbb R,\;u,l\in\mathbb R^{n-1},\;B\in\mathbb R^{(n-1)\times(n-1)}.
    \]

    由条件，\(\det(A_1)=a_{11}\neq 0\)，故可唯一确定第一行第一列

    \[
    u_{1j}=a_{1j},\quad l_{i1}=\frac{a_{i1}}{a_{11}},\quad i,j=2,\dots,n.
    \]

    令 **Schur 补** 为（Schur 补相关知识回顾见本文尾部）

    \[
    \widehat B = B - \frac{l\,u^T}{a_{11}}.
    \]

    注意对任意 \(1\le k\le n-2\)，\(\widehat B\) 的第 \(k\) 阶顺序主子阵满足

    \[
    \det(\widehat B_k)=\frac{\det(A_{k+1})}{a_{11}}\neq 0,
    \]

    因此 \(\widehat B\) 满足归纳假设，存在唯一分解 \(\widehat B=L_{n-1}U_{n-1}\)。于是

    \[
    A=
    \underbrace{\begin{bmatrix}1&0\\l/a_{11}&L_{n-1}\end{bmatrix}}_{=L}
    \underbrace{\begin{bmatrix}a_{11}&u^T\\0&U_{n-1}\end{bmatrix}}_{=U},
    \]

    这给出了 \(A\) 的一个 LU 分解，且由归纳唯一性，该分解唯一。充分性得证。

    ---

    **必要性**

    设 \(A=LU\) 存在（\(L\) 单位下三角，\(U\) 上三角）。

    对任意 \(k=1,\dots,n-1\)，把 \(A\) 按前 \(k\) 行列分块

    \[
    A_k = L_k U_k,
    \]

    其中 \(L_k\) 是 \(L\) 的 \(k\) 阶主子阵（单位下三角），\(U_k\) 是 \(U\) 的 \(k\) 阶主子阵（上三角），于是

    \[
    \det(A_k)=\det(L_k)\det(U_k)=\det(U_k)=\prod_{j=1}^{k}u_{jj}.
    \]

    分两种情形：

    - **\(A\) 非奇异** ：\(L\) 可逆，故 \(U=L^{-1}A\) 也可逆，所有 \(u_{jj}\neq 0\)，从而 \(\det(A_k)\neq 0\)。

    - **\(A\) 奇异** ：若存在某 \(k<n\) 使 \(u_{kk}=0\)，则第 \(k\) 步消元中可对 \(l_{ik}\)（\(i>k\)）任意赋值（方程 \(l_{ik}\cdot 0=0\) 对任何 \(l_{ik}\) 都成立），分解不唯一，与"唯一"假设矛盾；故对 \(k=1,\dots,n-1\) 必须有 \(u_{kk}\neq 0\)，即 \(\det(A_k)\neq 0\)。

    必要性得证。\(\blacksquare\)

### LU 分解的再思考（分块 / 递归）

将

\[
A=
\begin{bmatrix}
a_{11} & u^T\\
l & B
\end{bmatrix}
\]

写成分块乘积，可把 \(n\times n\) 的 LU 分解问题递归地降为 \((n-1)\times(n-1)\) 的问题，关键中间量是 Schur 补：

\[
B - \frac{l u^T}{a_{11}} = B - \left(\frac{l}{a_{11}}\right)u^T .
\]

如果能得到 Schur 补的 $LU$ 分解形式， 

$$
B - \frac{lu^{T}}{a_{11}} = L_{n - 1} U_{n - 1}
$$

那么

$$
\begin{bmatrix}
1 & 0 \\\
\frac{l}{a_{11}}  &  I_{n - 1}
\end{bmatrix}
\begin{bmatrix}
1  & 0 \\\
0  &  B - \frac{lu^{T}}{a_{11}}
\end{bmatrix}
\begin{bmatrix}
a_{11} & u^{T}  \\\
0 & I_{n - 1}
\end{bmatrix}
=
\begin{bmatrix}
1 & 0 \\\
\frac{l}{a_{}} & L_{n - 1}
\end{bmatrix}
\begin{bmatrix}
a_{11} &  u^{T}  \\\
0 & U_{n -1}
\end{bmatrix}
\equiv LU
$$


这也解释了“先算乘子，再更新右下角子块”的改进原位算法（课件算法 3.3）。

### 带状矩阵的 LU 分解

定义 **带宽** ：对 \(A\in\mathbb R^{m\times n}\)，若对任何 \(i>j+p\) 有 \(a_{ij}=0\)，则称 \(A\) 具有下带宽 \(p\)；若对任何 \(j>i+q\) 有 \(a_{ij}=0\)，则称 \(A\) 具有上带宽 \(q\)。

常见结构的带宽（方阵 \(n\times n\)）：


- 对角矩阵：下带宽 \(0\)，上带宽 \(0\)
- 上三角：下带宽 \(0\)，上带宽 \(n-1\)
- 下三角：下带宽 \(n-1\)，上带宽 \(0\)
- 三对角：下带宽 \(1\)，上带宽 \(1\)

若 \(p,q\ll n\)，矩阵稀疏，可采用压缩存储（按列把非零带映射到 \((p+q+1)\times n\) 的存储阵）。

定理 **带宽在 LU 中保持** ：若 \(A=L U\)，且 \(A\) 上带宽为 \(q\)、下带宽为 \(p\)，则 \(U\) 的上带宽为 \(q\)，\(L\) 的下带宽为 \(p\)。

!!! note "证明（数学归纳法）"

    对矩阵阶数 \(n\) 作归纳。

    - **基础情形** （\(n=1\)）：\(A=[a_{11}]\)，\(L=[1]\)，\(U=[a_{11}]\)，带宽显然保持（\(p=q=0\) 或根据 \(a_{11}\) 位置确定）。

    - **归纳假设** ：假设对任意 \((n-1)\times(n-1)\) 阶矩阵，定理成立。

    - **归纳步骤** ：考察 \(n\) 阶矩阵 \(A\)。将 \(A\) 写成分块形式：

    \[
    A=\begin{bmatrix}a_{11}&u^T\\l&B\end{bmatrix},
    \]

      其中 \(a_{11}\in\mathbb R\)，\(l\in\mathbb R^{n-1}\)，\(B\in\mathbb R^{(n-1)\times(n-1)}\)。

      由于 \(A\) 的下带宽为 \(p\)，则 \(l\) 的非零元最多只有前 \(p\) 个（即 \(l_i=0\) 对 \(i>p+1\)）。同理，\(u^T\) 的非零元最多只有前 \(q\) 个。

      LU 分解的第一步给出：

    \[
    A=\begin{bmatrix}1&0\\l/a_{11}&I_{n-1}\end{bmatrix}
    \begin{bmatrix}a_{11}&u^T\\0&B-lu^T/a_{11}\end{bmatrix}.
    \]

      这里：

      - 乘子向量 \(l/a_{11}\) 的非零结构继承 \(l\) 的结构，最多前 \(p\) 个非零；
      - Schur 补 \(\widehat B=B-lu^T/a_{11}\) 的 \((i,j)\) 元为 \(b_{ij}-l_i u_j/a_{11}\)。当 \(i>j+p\) 或 \(j>i+q\) 时，原 \(b_{ij}=0\)，且 \(l_i u_j=0\)（因超出带宽），故 \(\widehat B\) 保持带宽 \((p,q)\)。

      对 \((n-1)\times(n-1)\) 的 \(\widehat B\) 应用归纳假设，其 LU 分解 \(\widehat B=L_{n-1}U_{n-1}\) 保持带宽。最终拼得的 \(L\) 与 \(U\) 也保持原带宽 \(p,q\)。\(\square\)

### 算法 3.6：带状矩阵 LU 分解（原位存储）

**输入** ：带状矩阵 \(A\in\mathbb R^{n\times n}\)，压缩存储于 `a[i,j]`，上带宽 \(q\)，下带宽 \(p\)  
**输出** ：单位下三角矩阵 \(L\)（存 `a[i,j], i>j`）与上三角矩阵 \(U\)（存 `a[i,j], i\le j`），使 \(A=LU\)

```text
for k = 1, 2, ..., n-1 do
    // 计算 L 的第 k 列（乘子），只计算带宽范围内的行
    for i = k+1, k+2, ..., min{k+p, n} do
        a[i,k] ← a[i,k] / a[k,k];
    end for
    // 更新 Schur 补，只更新带宽范围内的子矩阵
    for i = k+1, k+2, ..., min{k+q, n} do
        for j = k+1, k+2, ..., min{k+p, n} do
            a[i,j] ← a[i,j] - a[i,k] * a[k,j];
        end for
    end for
end for
```

**算法要点** ：


- 循环边界用 \(\min\{k+p,n\}\) 和 \(\min\{k+q,n\}\) 限制，只处理带宽内的元素；
- 当 \(n\gg p,q\) 时，内层循环长度由 \(O(n)\) 降为 \(O(p)\) 或 \(O(q)\)；
- 总运算量：乘除法与加减法各约 \(n p q\) 次，远小于满矩阵的 \(n^3/3\)。

=== "Python"

    ```python
    import numpy as np
    
    def lu_banded(A, p, q):
        """
        带状矩阵 LU 分解 - 原位存储
        
        参数:
            A: n×n 带状系数矩阵 (numpy array, 会被修改)
            p: 下带宽
            q: 上带宽
        返回:
            A: 修改后的矩阵，其中:
               - 上三角部分（含对角线）存储 U
               - 严格下三角部分存储 L
        注意:
            此实现假设 A 已经是完整矩阵，实际应用中应使用压缩存储
        """
        n = A.shape[0]
        
        for k in range(n - 1):
            # 计算 L 的第 k 列乘子（只计算带宽范围内的行）
            i_max = min(k + p + 1, n)  # 行索引范围 [k+1, min(k+p, n-1)]
            for i in range(k + 1, i_max):
                if abs(A[k, k]) < 1e-15:
                    raise ValueError("Zero pivot encountered")
                A[i, k] /= A[k, k]
            
            # 更新 Schur 补（只更新带宽范围内的子矩阵）
            i_max = min(k + q + 1, n)  # 行索引受上带宽限制
            j_max = min(k + p + 1, n)  # 列索引受下带宽限制
            for i in range(k + 1, i_max):
                for j in range(k + 1, j_max):
                    A[i, j] -= A[i, k] * A[k, j]
        
        return A
    
    def lu_banded_compressed(A_band, p, q, n):
        """
        带状矩阵 LU 分解 - 压缩存储版本
        
        参数:
            A_band: (p+q+1)×n 压缩存储矩阵
                   行 0 到 q: 上对角线
                   行 q: 主对角线
                   行 q+1 到 p+q: 下对角线
            p: 下带宽
            q: 上带宽
            n: 原矩阵阶数
        返回:
            A_band: 修改后的压缩存储矩阵，包含 L 和 U
        """
        # 压缩存储索引映射: A[i,j] -> A_band[q+i-j, j] (当 |i-j| <= max(p,q))
        for k in range(n - 1):
            # 计算乘子并存储到下对角线位置
            i_max = min(k + p, n - 1)
            for i in range(k + 1, i_max + 1):
                # 获取 A[k,k] 和 A[i,k]
                akk = A_band[q, k]
                aik = A_band[q + i - k, k] if (i - k) <= p else 0
                
                if abs(akk) < 1e-15:
                    raise ValueError("Zero pivot encountered")
                
                # 计算乘子 l_ik = a_ik / a_kk
                lik = aik / akk
                # 存储回下对角线位置
                A_band[q + i - k, k] = lik
            
            # 更新 Schur 补
            i_max = min(k + q, n - 1)
            for i in range(k + 1, i_max + 1):
                for j in range(k + 1, min(k + p, n - 1) + 1):
                    # 获取 A[i,j], A[i,k], A[k,j]
                    aij = A_band[q + i - j, j] if abs(i - j) <= p + q else 0
                    aik = A_band[q + i - k, k]  # 已存储的乘子
                    akj = A_band[q + k - j, j] if (j - k) <= q else 0
                    
                    # 更新: A[i,j] = A[i,j] - A[i,k] * A[k,j]
                    A_band[q + i - j, j] = aij - aik * akj
        
        return A_band
    ```

=== "C++"

    ```cpp
    #include <vector>
    #include <cmath>
    #include <algorithm>
    
    using Matrix = std::vector<std::vector<double>>;
    
    /**
     * 带状矩阵 LU 分解 - 原位存储
     * 
     * 参数:
     *   A: n×n 带状矩阵，会被原地修改
     *   p: 下带宽
     *   q: 上带宽
     * 返回:
     *   成功返回 true
     */
    bool luBanded(Matrix& A, int p, int q) {
        int n = A.size();
        
        for (int k = 0; k < n - 1; ++k) {
            // 检查主元
            if (std::abs(A[k][k]) < 1e-15) {
                return false;
            }
            
            // 计算 L 的第 k 列乘子（只计算带宽范围内的行）
            int i_max = std::min(k + p + 1, n);
            for (int i = k + 1; i < i_max; ++i) {
                A[i][k] /= A[k][k];
            }
            
            // 更新 Schur 补（只更新带宽范围内的子矩阵）
            i_max = std::min(k + q + 1, n);  // 行索引受上带宽限制
            int j_max = std::min(k + p + 1, n);  // 列索引受下带宽限制
            for (int i = k + 1; i < i_max; ++i) {
                for (int j = k + 1; j < j_max; ++j) {
                    A[i][j] -= A[i][k] * A[k][j];
                }
            }
        }
        
        return true;
    }
    
    /**
     * 带状矩阵 LU 分解 - 压缩存储版本
     * 
     * 压缩存储方案: A[i,j] 存储在 band[q + i - j][j] (0 <= q+i-j < p+q+1)
     * 其中 band[0..q-1] 存上对角线，band[q] 存主对角线，
     * band[q+1..p+q] 存下对角线
     * 
     * 参数:
     *   band: (p+q+1)×n 压缩存储矩阵
     *   p, q: 下、上带宽
     *   n: 原矩阵阶数
     */
    bool luBandedCompressed(std::vector<std::vector<double>>& band, 
                             int p, int q, int n) {
        int diag_row = q;  // 主对角线在压缩矩阵中的行索引
        
        for (int k = 0; k < n - 1; ++k) {
            double akk = band[diag_row][k];
            
            if (std::abs(akk) < 1e-15) {
                return false;
            }
            
            // 计算乘子（只计算下带宽范围内的行）
            int i_max = std::min(k + p + 1, n);
            for (int i = k + 1; i < i_max; ++i) {
                int row_idx = diag_row + i - k;  // 在压缩矩阵中的行索引
                band[row_idx][k] /= akk;  // 存储乘子 l_ik
            }
            
            // 更新 Schur 补
            i_max = std::min(k + q + 1, n);
            for (int i = k + 1; i < i_max; ++i) {
                int row_ik = diag_row + i - k;
                double lik = band[row_ik][k];
                
                for (int j = k + 1; j < std::min(k + p + 1, n); ++j) {
                    // 获取 A[i,j] 的压缩存储位置
                    int row_ij = diag_row + i - j;
                    int row_kj = diag_row + k - j;
                    
                    if (row_ij >= 0 && row_ij < p + q + 1 &&
                        row_kj >= 0 && row_kj < p + q + 1) {
                        band[row_ij][j] -= lik * band[row_kj][j];
                    }
                }
            }
        }
        
        return true;
    }
    ```

## 对称正定矩阵与 Cholesky / LDLT

### 对称正定矩阵的性质

定义 **对称正定矩阵** ：\(A\in\mathbb R^{n\times n}\) 满足

\[
A^T = A,\quad \forall x\neq 0,\; x^T A x > 0 .
\]

定理：若 \(A\) 对称正定，则其所有主子阵也对称正定；特别地，所有对角线元素均为正数。

### Cholesky 分解

定理 **Cholesky 分解** ：若 \(A\) 对称正定，则存在唯一的下三角矩阵 \(L\)，且对角元均为正，使得

\[
A = L L^T .
\]

解方程 \(A x=b\) 时可分两步：


- 先解 \(L y=b\)；
- 再解 \(L^T x=y\)。

通过比较系数可得到 \(L\) 的递推：

\[
l_{11}^2=a_{11}\Rightarrow l_{11}=\sqrt{a_{11}},
\]

\[
l_{i1}l_{11}=a_{i1}\Rightarrow l_{i1}=\frac{a_{i1}}{l_{11}},
\]

\[
l_{21}^2+l_{22}^2=a_{22}\Rightarrow l_{22}=\sqrt{a_{22}-l_{21}^2},
\]

以此类推。

#### 算法 3.7（Cholesky 伪代码）

```text
L[:,:] = 0
for k = 1..n:
    l[k,k] = a[k,k]
    for j = 1..k-1:
        l[k,k] = l[k,k] - l[k,j] * l[k,j]
    l[k,k] = sqrt(l[k,k])
    for j = k+1..n:
        l[j,k] = a[j,k]
        for i = 1..k-1:
            l[j,k] = l[j,k] - l[j,i] * l[k,i]
        l[j,k] = l[j,k] / l[k,k]
```

=== "Python"

    ```python
    import numpy as np
    
    def cholesky(A):
        """
        Cholesky 分解: A = L L^T
        
        参数:
            A: n×n 对称正定矩阵 (numpy array)
        返回:
            L: 下三角矩阵，满足 A = L @ L.T
        异常:
            ValueError: 若矩阵不是正定（遇到非正主元）
        """
        n = A.shape[0]
        L = np.zeros((n, n))
        
        for k in range(n):
            # 计算对角元 L[k,k]
            L[k, k] = A[k, k]
            for j in range(k):
                L[k, k] -= L[k, j] ** 2
            
            if L[k, k] <= 0:
                raise ValueError("Matrix is not positive definite")
            
            L[k, k] = np.sqrt(L[k, k])
            
            # 计算第 k 列的非对角元
            for j in range(k + 1, n):
                L[j, k] = A[j, k]
                for i in range(k):
                    L[j, k] -= L[j, i] * L[k, i]
                L[j, k] /= L[k, k]
        
        return L
    
    def cholesky_solve(L, b):
        """
        利用 Cholesky 分解求解 Ax = b
        
        参数:
            L: Cholesky 分解得到的下三角矩阵
            b: 右端向量
        返回:
            x: 解向量
        """
        n = len(b)
        
        # 前代：解 L y = b
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i]
            for j in range(i):
                y[i] -= L[i, j] * y[j]
            y[i] /= L[i, i]
        
        # 回代：解 L^T x = y
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, n):
                x[i] -= L[j, i] * x[j]  # 注意：L^T[i,j] = L[j,i]
            x[i] /= L[i, i]
        
        return x
    ```

=== "C++"

    ```cpp
    #include <vector>
    #include <cmath>
    #include <stdexcept>
    
    using Matrix = std::vector<std::vector<double>>;
    
    /**
     * Cholesky 分解: A = L L^T
     * 
     * 参数:
     *   A: n×n 对称正定矩阵
     *   L: 输出参数，下三角矩阵
     * 返回:
     *   成功返回 true，若遇到非正主元返回 false
     */
    bool cholesky(const Matrix& A, Matrix& L) {
        int n = A.size();
        L.assign(n, std::vector<double>(n, 0.0));
        
        for (int k = 0; k < n; ++k) {
            // 计算对角元 L[k,k]
            double sum = A[k][k];
            for (int j = 0; j < k; ++j) {
                sum -= L[k][j] * L[k][j];
            }
            
            if (sum <= 0) {
                return false;  // 矩阵不是正定
            }
            
            L[k][k] = std::sqrt(sum);
            
            // 计算第 k 列的非对角元
            for (int j = k + 1; j < n; ++j) {
                double s = A[j][k];
                for (int i = 0; i < k; ++i) {
                    s -= L[j][i] * L[k][i];
                }
                L[j][k] = s / L[k][k];
            }
        }
        
        return true;
    }
    
    /**
     * 利用 Cholesky 分解求解 Ax = b
     * 
     * 参数:
     *   L: Cholesky 分解得到的下三角矩阵
     *   b: 右端向量
     * 返回:
     *   x: 解向量
     */
    std::vector<double> choleskySolve(const Matrix& L, 
                                      const std::vector<double>& b) {
        int n = b.size();
        std::vector<double> y(n), x(n);
        
        // 前代：解 L y = b
        for (int i = 0; i < n; ++i) {
            y[i] = b[i];
            for (int j = 0; j < i; ++j) {
                y[i] -= L[i][j] * y[j];
            }
            y[i] /= L[i][i];
        }
        
        // 回代：解 L^T x = y
        for (int i = n - 1; i >= 0; --i) {
            x[i] = y[i];
            for (int j = i + 1; j < n; ++j) {
                x[i] -= L[j][i] * x[j];  // L^T[i][j] = L[j][i]
            }
            x[i] /= L[i][i];
        }
        
        return x;
    }
    ```

#### Cholesky 的再思考（分块 / 递归）

把对称正定矩阵写为

\[
A=
\begin{bmatrix}
a_{11} & l^T\\
l & B
\end{bmatrix},
\]

可证明 Schur 补

\[
B-\frac{l l^T}{a_{11}}
\]

仍为正定；若它可 Cholesky 分解，则可递归构造 \(A\) 的 Cholesky 分解。对应改进原位算法如下：

#### 算法 3.8：改进 Cholesky（原位存储）

```text
for k = 1, 2, ..., n do
    a[k,k] ← sqrt(a[k,k])           // 计算 L[k,k]
    for i = k+1, k+2, ..., n do
        a[i,k] ← a[i,k] / a[k,k]    // 计算 L[i,k]
    end for
    for i = k+1, k+2, ..., n do
        for j = i, i+1, ..., n do
            a[j,i] ← a[j,i] - a[i,k] * a[j,k]  // 更新 Schur 补
        end for
    end for
end for
```

=== "Python"

    ```python
    import numpy as np
    
    def cholesky_inplace(A):
        """
        Cholesky 分解 - 原位存储（改进算法）
        
        参数:
            A: n×n 对称正定矩阵 (numpy array, 会被修改)
        返回:
            A: 修改后的矩阵，下三角部分存储 L
        """
        n = A.shape[0]
        
        for k in range(n):
            # 检查并计算对角元
            if A[k, k] <= 0:
                raise ValueError("Matrix is not positive definite")
            A[k, k] = np.sqrt(A[k, k])
            
            # 计算第 k 列的非对角元（乘子）
            for i in range(k + 1, n):
                A[i, k] /= A[k, k]
            
            # 更新 Schur 补（右下角子矩阵）
            for i in range(k + 1, n):
                for j in range(i, n):  # 从 i 开始，利用对称性
                    A[j, i] -= A[i, k] * A[j, k]
        
        return A
    
    def cholesky_inplace_optimized(A):
        """
        Cholesky 分解 - 原位存储（向量化优化版本）
        
        利用 numpy 的向量化操作提高效率
        """
        n = A.shape[0]
        
        for k in range(n):
            # 计算对角元
            if A[k, k] <= 0:
                raise ValueError("Matrix is not positive definite")
            A[k, k] = np.sqrt(A[k, k])
            
            # 计算乘子（向量化）
            A[k+1:n, k] /= A[k, k]
            
            # 更新 Schur 补（向量化外积）
            if k + 1 < n:
                # A[k+1:n, k+1:n] -= np.outer(A[k+1:n, k], A[k+1:n, k])
                # 更高效的实现：只更新下三角部分
                for i in range(k + 1, n):
                    A[i:n, i] -= A[i, k] * A[i:n, k]
        
        return A
    ```

=== "C++"

    ```cpp
    #include <vector>
    #include <cmath>
    #include <stdexcept>
    
    using Matrix = std::vector<std::vector<double>>;
    
    /**
     * Cholesky 分解 - 原位存储（改进算法 3.8）
     * 
     * 参数:
     *   A: n×n 对称正定矩阵，会被原地修改
     *      下三角部分存储 L，上三角部分保持原值（未使用）
     * 返回:
     *   成功返回 true
     */
    bool choleskyInPlace(Matrix& A) {
        int n = A.size();
        
        for (int k = 0; k < n; ++k) {
            // 检查并计算对角元
            if (A[k][k] <= 0) {
                return false;
            }
            A[k][k] = std::sqrt(A[k][k]);
            
            // 计算第 k 列的非对角元（乘子）
            for (int i = k + 1; i < n; ++i) {
                A[i][k] /= A[k][k];
            }
            
            // 更新 Schur 补（只更新下三角部分）
            for (int i = k + 1; i < n; ++i) {
                for (int j = i; j < n; ++j) {
                    A[j][i] -= A[i][k] * A[j][k];
                }
            }
        }
        
        return true;
    }
    
    /**
     * Cholesky 分解 - 按行存储优化版本（算法 3.4 的 Cholesky 版本）
     * 
     * 内存访问模式更适合 C/C++ 的行主序数组
     */
    bool choleskyRowOriented(Matrix& A) {
        int n = A.size();
        
        for (int k = 0; k < n; ++k) {
            if (A[k][k] <= 0) {
                return false;
            }
            
            // 计算对角元
            double lkk = std::sqrt(A[k][k]);
            A[k][k] = lkk;
            
            // 计算乘子
            for (int i = k + 1; i < n; ++i) {
                A[i][k] /= lkk;
            }
            
            // 按行更新 Schur 补
            for (int i = k + 1; i < n; ++i) {
                double lik = A[i][k];
                for (int j = k + 1; j <= i; ++j) {  // 只更新下三角
                    A[i][j] -= lik * A[j][k];
                }
            }
        }
        
        return true;
    }
    ```

### \(L D L^T\) 分解（改进 Cholesky）

进一步可把对称正定矩阵分解为

\[
A = L D L^T ,
\]

其中 \(L\) 为单位下三角矩阵，\(D\) 为对角矩阵。

与 Cholesky 相比，它避免了约 \(n\) 次开方操作；乘除与加减的主导项仍为 \(n^3/6\) 量级，因此也常称为 **改进 Cholesky 法** 。

算法 3.9：LDLT 分解改进算法（原位存储）

```text
for k = 1, 2, ..., n do
    // 利用对称性，复制下三角到上三角
    for i = k+1, k+2, ..., n do
        a[k,i] ← a[i,k]
    end for
    // 计算 L 的第 k 列（乘子）
    for i = k+1, k+2, ..., n do
        a[i,k] ← a[i,k] / a[k,k]
    end for
    // 更新 Schur 补
    for i = k+1, k+2, ..., n do
        for j = i, i+1, ..., n do
            a[j,i] ← a[j,i] - a[i,k] * a[k,j]
        end for
    end for
end for
```

说明：


- 算法结束后，\(D\) 的对角元 \(d_{kk}\) 存储在 `a[k,k]`；
- \(L\) 的严格下三角元素 \(l_{ik}\)（\(i>k\)）存储在 `a[i,k]`；
- 对角线 \(l_{kk}=1\) 隐式存储，不占用空间。

=== "Python"

    ```python
    import numpy as np
    
    def ldlt_inplace(A):
        """
        LDL^T 分解 - 原位存储（改进算法）
        
        参数:
            A: n×n 对称正定矩阵 (numpy array, 会被修改)
        返回:
            A: 修改后的矩阵，其中:
               - 对角线 a[k,k] 存储 D[k,k]
               - 严格下三角 a[i,k] (i>k) 存储 L[i,k]
               - L 对角线隐式为 1
        注意:
            此实现不处理选主元，假设矩阵良好条件
        """
        n = A.shape[0]
        
        for k in range(n):
            # 检查主元（D[k,k] 必须为正）
            if A[k, k] <= 0:
                raise ValueError("Matrix is not positive definite")
            
            # 利用对称性，先把下三角复制到上三角（可选，取决于实现）
            for i in range(k + 1, n):
                A[k, i] = A[i, k]
            
            # 计算 L 的第 k 列乘子（严格下三角部分）
            for i in range(k + 1, n):
                A[i, k] /= A[k, k]
            
            # 更新 Schur 补（右下角子矩阵）
            for i in range(k + 1, n):
                for j in range(i, n):  # 从 i 开始，利用对称性只更新下三角
                    A[j, i] -= A[i, k] * A[k, j]
        
        return A
    
    def ldlt_solve_inplace(A_ldlt, b):
        """
        利用原位存储的 LDL^T 分解求解 Ax = b
        
        参数:
            A_ldlt: 经过 ldlt_inplace 处理后的矩阵
            b: 右端向量
        返回:
            x: 解向量
        """
        n = len(b)
        y = np.zeros(n)
        x = np.zeros(n)
        
        # 前代：解 L y = b（L 对角线隐式为 1）
        for i in range(n):
            y[i] = b[i]
            for j in range(i):
                y[i] -= A_ldlt[i, j] * y[j]  # L[i,j] 在下三角
        
        # 解 D z = y（对角方程）
        for i in range(n):
            y[i] /= A_ldlt[i, i]  # D[i,i] 在对角线上
        
        # 回代：解 L^T x = z（L^T 对角线隐式为 1）
        for i in range(n - 1, -1, -1):
            x[i] = y[i]
            for j in range(i + 1, n):
                x[i] -= A_ldlt[j, i] * x[j]  # L^T[i,j] = L[j,i]
        
        return x
    
    def ldlt_explicit(A):
        """
        LDL^T 分解 - 显式存储 L 和 D
        
        返回显式的单位下三角矩阵 L 和对角矩阵 D
        """
        n = A.shape[0]
        L = np.eye(n)  # 单位下三角
        D = np.zeros(n)
        
        for k in range(n):
            # D[k,k] = A[k,k] - sum(L[k,j]^2 * D[j,j])
            D[k] = A[k, k]
            for j in range(k):
                D[k] -= L[k, j] ** 2 * D[j]
            
            if D[k] <= 0:
                raise ValueError("Matrix is not positive definite")
            
            # L[i,k] = (A[i,k] - sum(L[i,j]*L[k,j]*D[j,j])) / D[k,k]
            for i in range(k + 1, n):
                L[i, k] = A[i, k]
                for j in range(k):
                    L[i, k] -= L[i, j] * L[k, j] * D[j]
                L[i, k] /= D[k]
        
        return L, np.diag(D)
    ```

=== "C++"

    ```cpp
    #include <vector>
    #include <cmath>
    #include <stdexcept>
    
    using Matrix = std::vector<std::vector<double>>;
    
    /**
     * LDL^T 分解 - 原位存储（改进算法 3.9）
     * 
     * 参数:
     *   A: n×n 对称正定矩阵，会被原地修改
     *      - 对角线 A[k,k] 存储 D[k,k]
     *      - 严格下三角 A[i,k] (i>k) 存储 L[i,k]
     *      - L 对角线隐式为 1
     * 返回:
     *   成功返回 true
     */
    bool ldltInPlace(Matrix& A) {
        int n = A.size();
        
        for (int k = 0; k < n; ++k) {
            // 检查主元
            if (A[k][k] <= 0) {
                return false;
            }
            
            // 计算 L 的第 k 列乘子
            for (int i = k + 1; i < n; ++i) {
                A[i][k] /= A[k][k];
            }
            
            // 更新 Schur 补（只更新下三角部分）
            for (int i = k + 1; i < n; ++i) {
                for (int j = i; j < n; ++j) {
                    A[j][i] -= A[i][k] * A[k][j];
                }
            }
        }
        
        return true;
    }
    
    /**
     * 利用原位存储的 LDL^T 分解求解 Ax = b
     * 
     * 参数:
     *   A_ldlt: 经过 ldltInPlace 处理后的矩阵
     *   b: 右端向量
     * 返回:
     *   x: 解向量
     */
    std::vector<double> ldltSolveInPlace(const Matrix& A_ldlt,
                                        const std::vector<double>& b) {
        int n = b.size();
        std::vector<double> y(n), x(n);
        
        // 前代：解 L y = b（L 对角线隐式为 1）
        for (int i = 0; i < n; ++i) {
            y[i] = b[i];
            for (int j = 0; j < i; ++j) {
                y[i] -= A_ldlt[i][j] * y[j];
            }
        }
        
        // 解 D z = y
        for (int i = 0; i < n; ++i) {
            y[i] /= A_ldlt[i][i];
        }
        
        // 回代：解 L^T x = z
        for (int i = n - 1; i >= 0; --i) {
            x[i] = y[i];
            for (int j = i + 1; j < n; ++j) {
                x[i] -= A_ldlt[j][i] * x[j];
            }
        }
        
        return x;
    }
    
    /**
     * LDL^T 分解 - 显式存储版本
     * 
     * 参数:
     *   A: 输入对称正定矩阵
     *   L: 输出单位下三角矩阵
     *   D: 输出对角矩阵（以一维向量形式返回对角元）
     */
    bool ldltExplicit(const Matrix& A, Matrix& L, std::vector<double>& D) {
        int n = A.size();
        L.assign(n, std::vector<double>(n, 0.0));
        D.assign(n, 0.0);
        
        // L 初始化为单位矩阵
        for (int i = 0; i < n; ++i) {
            L[i][i] = 1.0;
        }
        
        for (int k = 0; k < n; ++k) {
            // D[k] = A[k,k] - sum(L[k,j]^2 * D[j])
            D[k] = A[k][k];
            for (int j = 0; j < k; ++j) {
                D[k] -= L[k][j] * L[k][j] * D[j];
            }
            
            if (D[k] <= 0) {
                return false;
            }
            
            // L[i,k] = (A[i,k] - sum(L[i,j]*L[k,j]*D[j])) / D[k]
            for (int i = k + 1; i < n; ++i) {
                L[i][k] = A[i][k];
                for (int j = 0; j < k; ++j) {
                    L[i][k] -= L[i][j] * L[k][j] * D[j];
                }
                L[i][k] /= D[k];
            }
        }
        
        return true;
    }
    ```

## Schur 补回顾

给定分块矩阵

\[
M=
\begin{bmatrix}
A & B\\
C & D
\end{bmatrix},
\]

其中 \(A\in\mathbb R^{k\times k}\)、\(D\in\mathbb R^{m\times m}\)。

若 \(A\) 可逆，则称

\[
S_{/A}=D-C A^{-1} B
\]

为 \(A\) 在 \(M\) 中的 **Schur 补** ；若 \(D\) 可逆，则

\[
S_{/D}=A-B D^{-1} C
\]

为 \(D\) 在 \(M\) 中的 Schur 补。

### 1) 分解与行列式公式

当 \(A\) 可逆时，有分解

\[
\begin{bmatrix}
A & B\\
C & D
\end{bmatrix}
=
\begin{bmatrix}
I & 0\\
C A^{-1} & I
\end{bmatrix}
\begin{bmatrix}
A & B\\
0 & D-C A^{-1}B
\end{bmatrix},
\]

因此

\[
\det(M)=\det(A)\det(S_{/A}).
\]

同理（\(D\) 可逆）：

\[
\det(M)=\det(D)\det(S_{/D}).
\]

这也是前面 LU 存在性证明里出现

\[
\det(\widehat B_k)=\frac{\det(A_{k+1})}{\det(A_1)}
\]

这类关系的来源。

### 2) 与 LU / Cholesky 的关系

- **LU 递归** ：把 \(A\) 写成 \(\begin{bmatrix}a_{11}&u^T\\ l&B\end{bmatrix}\) 后，右下角更新

\[
\widehat B = B-\frac{l u^T}{a_{11}}
\]

  就是一步消元后的 Schur 补（也叫 trailing submatrix update）。

- **Cholesky 递归** ：对对称正定矩阵，分块后出现

\[
\widehat B = B-\frac{l l^T}{a_{11}}
\]

  ，它是对称 Schur 补，且仍保持正定。

### 3) 两个常用判定结论

- **可逆判定** ：若 \(A\) 可逆，则 \(M\) 可逆 \(\Leftrightarrow\) \(S_{/A}\) 可逆（对 \(D\) 的版本同理）。

- **正定判定（对称情形）** ：若

\[
M=\begin{bmatrix}A&B\\B^T&D\end{bmatrix}
\]

  且 \(A\succ 0\)，则

\[
M\succ 0 \;\Leftrightarrow\; D-B^T A^{-1} B \succ 0.
\]

  这就是 Cholesky 分块递归“每一步都合法”的理论基础。

## 小结


- **LU 分解** ：把 \(A\) 写成单位下三角 \(L\) 与上三角 \(U\) 的乘积，适合多右端项的快速求解。
- **存在性** ：顺序主子阵行列式均非零 \(\Leftrightarrow\) 唯一 LU（在 \(L\) 单位化约定下）。
- **带状矩阵** ：当带宽小，带状 LU 可把复杂度降到 \(O(n p q)\)。
- **对称正定** ：可用 **Cholesky** \(A=L L^T\) 或 **LDLT** \(A=L D L^T\) ，通常更高效且数值性质更好。
