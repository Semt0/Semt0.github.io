---
title: 网络层：Concepts and Algorithm
description: 网络层服务模型、路由器结构，以及 DV、LS 与 BGP 的路由机制。
publishDate: 2026-10-24
tags:
  - 计算机
  - 计算机网络
draft: false
language: 中文
course: 计算机网络
order: 2
---

网络层要把包送过许多相互连接、又各有差异的网络。除了规定包的格式，还得回答两个问题：**网络向主机提供什么服务？路由器凭什么决定包往哪里走？**

## 一、网络层与服务模型

### 1. 为什么不能只靠扩大一个局域网？

链路层解决同一链路或二层网络内的帧交付。网络层把这些网络连接起来，让主机跨越多段链路通信。例如，一个包可以先走家里的 Wi-Fi，再经过运营商网络，最后进入服务器所在的以太网。

把所有设备都放进一个巨大的二层网络，会带来 MAC 表、广播范围和故障范围的扩张，也不方便表达不同组织之间的路径策略。这里并不是说交换机只能连接一种物理介质，而是说：**二层交换本身不能代替跨网络的层次寻址、IP 路由和管理边界。**

IP 在不同链路之上提供共同的数据报接口。路由器从入站帧中取出 IP 包，选择下一跳，再按出口链路的格式重新封装。各段链路可以不同，网络层仍然可以把它们串起来。

### 2. Routing 与 Forwarding

两者经常一起出现，但发生在不同的环节：

| 操作 | 在做什么 |
| --- | --- |
| Routing，路由 | 获得可达性和路径信息，选择路由，产生或更新转发表所需的信息 |
| Forwarding，转发 | 一个包到达后，查已有的表，决定出口与下一跳并执行转发 |

假设路由器 R 原先认为某个目的网络应经 B 到达。链路故障后，路由协议交换信息，重新选择经 C 的路径，并安装新的表项。这是控制平面的工作。随后到来的包按新表交给 C，这是数据平面的工作。

路由协议的消息本身也需要经过网络传输。“控制平面”描述的是功能，不表示它必然使用一套与业务链路完全分离的设施。

### 3. 数据报网络：每个包带目的地址

在 Datagram Model 中，网络层发送前通常不需要先建立一条电路。包携带目的地址，各台路由器独立查表，连续的下一跳选择形成整条路径。

同一对端点的多个包可以共用相同路径；如果路由表或转发选择改变，也可能经过不同路径。“每包查表”不等于每个包都重新运行一次路由算法。

IP 采用数据报模型，基本服务是尽力而为：不保证必达、有序、无重复，也不承诺确定的时延和带宽。可靠性可以由端系统中的 TCP 等协议继续提供。

### 4. 虚电路：先安装沿途状态

Virtual Circuit（VC，虚电路）通常有三个阶段：

1. **建立。** 选择路径，在沿途设备安装电路或标签状态。
2. **传输。** 包带较短的电路标识，设备按状态表转发，并可能替换标识。
3. **拆除。** 通信结束或电路失效后，删除相应状态。

电路标识通常只有链路或设备上的局部意义，不要求沿途都使用同一个数字。例如：

```text
R1：入端口 1、标签 12 → 出端口 2、标签 31
R2：入端口 3、标签 31 → 出端口 1、标签 8
```

这两台设备不是每次重新解读完整目的地址，而是依据已经安装的状态完成标签转发。

| 比较项 | 数据报 | 虚电路 |
| --- | --- | --- |
| 发送前建立 | 通常不需要 | 通常需要 |
| 包内主要标识 | 目的地址 | 电路标识或标签 |
| 主要转发状态 | 目的前缀到下一跳 | 电路或标签到出口、新标签 |
| 路径变化 | 转发表变化可改变后续包的路径 | 通常需修复或重建相关电路状态 |
| 资源协调 | 需要额外机制 | 可以在建立时协调，但不自动保证 QoS |

虚电路仍然可以让多个电路共享同一条物理链路，使用分组传输和排队。它不是“给一对主机单独拉一根线”，也不必然预约独占带宽。

:::study-note[TCP 连接与网络层虚电路]{kind="note"}

TCP 在端系统中维护连接状态，不要求每台 IP 路由器为这条 TCP 连接安装虚电路表项。传输层是否有连接，与网络层采用数据报还是虚电路，是两个不同的问题。

:::

### 5. MPLS 为什么像虚电路？

MPLS（Multiprotocol Label Switching）在入口为包添加标签，中间设备按标签选择出口、替换标签，出口再移除标签。标签交换路径称为 LSP（Label-Switched Path）。

一条 LSP 可以承载许多业务流，不是每条 TCP 连接都独享一条 MPLS 路径。MPLS 提供的是标签转发机制，带宽保证、保护切换和路径控制仍需相应的配置与协议支持。体系结构见 [RFC 3031](https://www.rfc-editor.org/rfc/rfc3031.html)。

后文的 Link-State Packet 也缩写为 LSP。一个指标签交换路径，一个指链路状态报文，阅读时要按上下文区分。

### 6. Quiz 3.1 — Service models

Does a TCP connection imply that every IP router stores a virtual-circuit entry for that connection? Does a virtual circuit necessarily reserve a dedicated physical link?

:::study-proof[Reference answer: Service models]{kind="example"}

No. TCP connection state is maintained by the endpoints; ordinary IP forwarding does not require a per-TCP-connection virtual-circuit entry in every router.

A virtual circuit also need not reserve a dedicated physical link. It can share packet-switched links with other circuits. Resource reservation and QoS guarantees require additional mechanisms.

:::

## 二、路由器内部：包为什么会排队？

### 1. 输入端、交换结构与输出端

存储转发（store-and-forward）模型：路由器收下完整的包，必要时暂存，然后继续发送。

```text
输入链路
  ↓
物理层接收、链路层处理
  ↓
查转发表、输入队列
  ↓
交换结构（switching fabric）
  ↓
输出队列、调度、链路层封装
  ↓
输出链路
```

Routing Processor 负责路由协议和管理等控制工作，并更新转发所用的信息。实际设备可以把查表等操作放在输入端硬件中，以便跟上线路速率。

交换结构把包从输入端搬到相应输出端。课件列出三种典型组织：

| 结构 | 包怎样通过设备内部 |
| --- | --- |
| Memory | 经共享内存等存储路径完成搬运 |
| Bus | 经共享总线传输，多路输入竞争总线带宽 |
| Interconnection Network | 通过交叉开关等互连结构连接输入与输出 |

若有 $N$ 个输入，每个输入速率为 $R$，总输入速率可达 $NR$。这是设计交换能力时的参考，但不意味着交换结构达到 $NR$ 后，所有拥塞都会消失。

### 2. 输入排队与输出排队

**输入排队**发生在输入侧的包不能及时进入交换结构时，例如交换结构吞吐不足，或多个输入争用输出。

**输出排队**发生在交换结构送往某个输出的总速率超过该输出的发送速率时。假设三个输入各以 1 Gbit/s 向同一个 1 Gbit/s 输出发送，即使内部可以同时搬运这些包，输出也只能每秒发走 1 Gbit。持续到达率为 3 Gbit/s 时，积压会按约 2 Gbit/s 增长，有限缓存最终会装满。

缓存可以吸收短时突发，却不能让长期超载的链路凭空增加发送能力。包在队列中等待会增加时延，缓存溢出则会造成丢包。

### 3. HOL blocking：空闲输出也可能用不上

考虑某个输入只维护一条 FIFO 队列，队首包要去输出 1，后面的包要去输出 2：

```text
队首 → [去输出 1] [去输出 2] → 队尾
          等待       被挡住
```

如果输出 1 暂时忙，而输出 2 空闲，队首包仍可能阻止后面的包进入交换结构。这就是 Head-of-Line Blocking（HOL，队头阻塞）。

它的关键不只是“输出 1 忙”，而是队列组织让本可使用输出 2 的包也无法前进。按输出分别组织输入队列，即 Virtual Output Queues（VOQ），可以缓解这类阻塞；它仍不能消除多个输入竞争同一个输出的容量限制，交换调度也仍然需要解决。

### 4. 调度与丢弃是两项决定

调度（scheduling）决定接下来发送哪个包；丢弃策略（drop policy）决定缓存不足等情况下丢哪个包。

优先级调度可以缩短某类流量的等待时间，但其他流量可能等得更久，严格优先级还可能造成低优先级流量饥饿。

### 5. Quiz 3.2 — HOL blocking

An input FIFO contains a packet for busy output 1 followed by a packet for idle output 2. Explain HOL blocking. Would a faster switching fabric eliminate all output congestion?

:::study-proof[Reference answer: HOL blocking]{kind="example"}

The head packet cannot advance because output 1 is busy. Under the FIFO queue organization, it blocks the following packet even though output 2 is available.

A faster fabric does not eliminate output congestion. If the aggregate arrival rate to one output exceeds that output's transmission rate, its queue can still grow and overflow.

:::

## 三、把路由问题写成图

### 1. “好路径”取决于选择的指标

把网络表示成图 $G=(V,E)$：节点为路由器，边为链路，$c(u,v)$ 为链路代价。本篇的最短路计算假设边权非负，且计算期间拓扑和边权保持不变。

路径 $P=(v_0,v_1,\ldots,v_k)$ 的代价是：

$$
C(P)=\sum_{i=0}^{k-1}c(v_i,v_{i+1})
$$

如果每条边的代价都是 1，最短路就是跳数最少的路径。如果代价来自配置权重，求出的就是配置权重之和最小的路径。除非指标本来就对应时延，否则不能把代价 8 直接读成 RTT=8 ms。

最短路也不自动等于最公平、最不拥塞的路径。很多源同时选择同一条“便宜”链路，仍可能使它过载。动态地把拥塞写进代价还会引入反馈：路由改变流量，流量又改变代价，需要额外处理稳定性。

### 2. 两条不同的分类轴

| 分类轴 | 两端分别表示什么 |
| --- | --- |
| Static / Dynamic | 路径更新方式及对变化的适应：较少改变，或定期、按事件更新 |
| Global / Decentralized Information | 计算时拥有本范围的拓扑，或主要通过邻居信息迭代 |

Link-State 常先收集拓扑，再本地计算；Distance Vector 则与邻居交换距离估计。两者都可以动态适应变化。

“使用全局信息”不等于“所有路由由一台中央服务器计算”。后面会看到，LS 的拓扑信息可以通过分布式泛洪收集，每台路由器分别运行算法。

## 四、Distance Vector：根据邻居的报告更新距离

### 1. Bellman–Ford 关系从哪里来？

记 $D_x(y)$ 为节点 $x$ 当前估计到目的 $y$ 的代价，$N(x)$ 为 $x$ 的邻居集合。只要 $x\ne y$，一条从 $x$ 出发的路径首先要经过某个邻居 $v$：先支付直连链路的代价，再支付从 $v$ 到 $y$ 的剩余代价。

$$
\boxed{D_x(y)=\min_{v\in N(x)}\{c(x,v)+D_v(y)\}}
$$

相应的下一跳为使右侧取最小值的邻居；如果有多个相同最小值，可以按规则选一个，或在协议支持时保留等价路径。

在最短路方程中，$D_v(y)$ 是正确的剩余距离；在实际 DV 协议中，它是**邻居最近报告的估计值**。这个区别解释了为什么拓扑变化和旧消息会造成问题。

### 2. 路由器保存什么，收到消息后做什么？

节点通常需要知道与直接邻居的链路代价，并维护到各目的地的距离和下一跳，还要保存更新所需的邻居报告。

- 到自己的距离设为 0，下一跳为本机。
- 不知道如何到达的目的地设为 $\infty$。
- 直连邻居的代价可以直接初始化，也可以通过第一轮交换学到。
- 收到邻居的新向量或发现链路变化后，重新比较各个邻居提供的候选路径。
- 本地估计变化后，按协议向邻居发布更新；协议还可能安排周期更新。

DV 的一个节点不需要先得到完整拓扑。它相信邻居报告的剩余距离，再加上自己到邻居的代价，逐步拼出更远的可达性。

### 3. 例题：课件 p.21 的四节点网络

![四节点无向加权图：AB=3、AD=7、BD=3、BC=6、DC=2](/media/compnet/routing-four-nodes.svg)

边权表示题设代价，所有链路在本例中均为双向。

先采用“已经知道直连邻居”的初始化。A 知道到 B 为 3，到 D 为 7，到 C 暂时不可达。

**第一次交换：利用邻居的直连距离。** B 报告到 C 为 6，D 报告到 C 为 2，所以 A 得到：

$$
D_A(C)=\min\{3+6,\;7+2\}=9
$$

到 D 则发现经 B 更便宜：

$$
D_A(D)=\min\{7,\;3+3\}=6
$$

与此同时，B 也会发现到 C 可以经 D：

$$
D_B(C)=\min\{6,\;3+2\}=5
$$

**第二次交换：A 收到 B 的新报告。** 于是：

$$
D_A(C)=\min\{3+5,\;7+2\}=8
$$

最终路径为 $A\rightarrow B\rightarrow D\rightarrow C$，下一跳是 B。

| A 所处阶段 | 到 B | 到 D | 到 C |
| --- | --- | --- | --- |
| 已知直连 | 3 | 7 | $\infty$ |
| 第一次交换后 | 3 | 6 | 9 |
| 第二次交换后 | 3 | 6 | 8 |

这是同步交换的教学示意：同一轮统一使用上一轮的报告。异步协议中消息到达顺序不同，不能把“第几轮得到结果”当作实现的固定时限。若从“除本机外全为无穷”开始计数，还要把发现直连邻居的过程另算一轮。

:::study-note[直连链路代价与最短距离]{kind="warning"}

A 到 D 的最短距离变成 6，并没有让直连边 $c(A,D)=7$ 变成 6。Bellman–Ford 在比较第一跳 D 时，仍应使用这条直连边的代价 7。代价为 6 的路径实际上先经过 B，不能据此把下一跳记成 D。

:::

### 4. Quiz 3.3 — Bellman–Ford update

A has neighbors B and D with link costs 3 and 7. B advertises distance 5 to C, and D advertises distance 2 to C. What distance and next hop should A choose?

:::study-proof[Reference answer: Bellman–Ford update]{kind="example"}

The candidate through B costs $3+5=8$, and the candidate through D costs $7+2=9$. A chooses distance 8 and next hop B. The first-hop cost is the direct link cost to the neighbor, not A's independently computed shortest distance to that neighbor.

:::

## 五、Count to Infinity：故障后的旧信息为什么会互相加强？

### 1. 一条三节点线路就足以出问题

考虑下面的网络，每条链路代价均为 1，没有其他到 A 的路径：

```text
A ──1── B ──1── C
```

稳定时，B 到 A 为 1；C 经 B 到 A，为 2。现在 A—B 断开，B 本应把 A 判为不可达。但 C 还没收到变化，继续报告旧消息：“我到 A 的代价是 2。”

如果 B 不知道 C 的路径原本就经过自己，便可能认为还有另一条路，把距离更新成 $1+2=3$，下一跳设为 C。随后 C 又相信 B 的新报告，把距离改成 $1+3=4$。接下来是 5、6、7……

| 更新事件 | 新的距离估计 |
| --- | --- |
| B 相信 C 的旧报告 2 | B 到 A 变成 3，经 C |
| C 相信 B 的报告 3 | C 到 A 变成 4，经 B |
| B 再相信 C 的报告 4 | B 到 A 变成 5，经 C |

没有任何新路径出现，两个节点却互相引用对方，形成转发环路和持续上升的估计。

### 2. 问题不在加法，而在隐藏的依赖

一个距离数字“2”没有说明这条路径是否依赖接收者。B 看到了 C 的距离，却看不到路径里原来就有 B。

因此，稳定拓扑下的最短路公式没有算错；出问题的是故障后的过时信息和分布式更新。所谓“坏消息传播慢”，不是故障消息完全不传播，而是有时要通过不断抬高估计，才能最终到达不可达状态。

### 3. Split horizon 与 poison reverse

| 机制 | 对学自邻居 B 的路由，怎样向 B 处理 |
| --- | --- |
| Split Horizon，水平分割 | 不把这条路由重新通告给 B |
| Poison Reverse，毒性逆转 | 明确向 B 通告此目的代价为 $\infty$ |

在刚才的例子中，C 到 A 是经 B 学到的。采用 poison reverse 时，C 向 B 报告的应是“到 A 不可达”，而不是 2，B 因而不会把 C 当成备选出口。

这些机制可以处理典型的双节点反向依赖，但不能保证消除所有更长的环路。限制最大可达距离也能让无穷计数在有限值停止，代价是网络可表达的路径长度受到限制。

### 4. RIP 如何落地？

RIP 使用跳数作为度量，把 16 定义为不可达，因此可达路径最多为 15 跳。课件 p.24 列出的典型定时参数是约 30 s 周期更新、180 s 超时，协议使用 UDP。

这些参数属于 RIP，不是所有 DV 协议都使用的通用常数。RIP 还具有触发更新等机制，不能把它理解成只有固定周期到了才允许报告变化。算法与不稳定性处理见 [RFC 2453](https://www.rfc-editor.org/rfc/rfc2453.html)。

### 5. Quiz 3.4 — Bad news and poison reverse

After link A–B fails in a line A–B–C, why might B believe C still has a route to A? How would poison reverse help in this two-router dependency?

:::study-proof[Reference answer: Bad news and poison reverse]{kind="example"}

C may advertise an old distance to A that was itself learned through B. A distance value alone does not reveal that dependency, so B may mistakenly select C as its next hop.

With poison reverse, C advertises an infinite distance to A back to B while C's route uses B. That prevents B from treating C as an alternative in this two-router dependency. It does not guarantee the absence of every longer routing loop.

:::


## 六、Flooding：把一份拓扑消息传给所有相关节点

### 1. 为什么要记来源和序号？

LS 路由希望各节点取得拓扑，但一个节点起初只知道邻居。Flooding（泛洪）让节点把收到的新通告复制给其他邻居，消息便能沿网络逐步扩散。

有环路的网络会产生重复副本。假设 A 的通告同时到达 B、C，B 又转给 C，C 就可能收到同一通告的两份副本。因此需要用**来源标识与序号**区分消息：

```text
(A, 6)：A 发布的第 6 个版本
(A, 7)：A 发布的第 7 个版本
```

第一次收到 `(A, 6)` 时处理并向其他邻居传播，再次收到它则不继续泛洪。之后 `(A, 7)` 到达时，它是新版本，仍应被接受和传播。若只记“以前听过 A”，就会把 A 之后的所有更新都错误地丢掉。

这里泛洪的是路由控制消息，不是要求把每个普通用户 IP 包都复制到所有端口。

### 2. 去重之外，还需要可靠性和过期规则

去重能限制重复传播，却不能保证每个节点都成功收到消息。需要可靠传播时，可以在邻居之间使用确认与重传。

旧消息也不能永久保留。Age 或寿命机制让不再刷新的通告过期，以免重启、分区等情况留下的旧信息一直占据数据库。序号回绕、节点重启后序号丢失、分区恢复后的新旧版本比较，都需要协议规定处理方式。

所以，“向其他邻居转发一次”只是泛洪的骨架。真实协议还必须判断什么是新消息、怎样补发，以及什么时候删除旧消息。

## 七、Link-State：先收集拓扑，再各自计算

### 1. 从本地链路到 LSDB

Link-State（LS，链路状态）路由分成两个阶段：

1. **传播拓扑。** 各节点发布自己的邻接与链路代价，在规定范围内泛洪。
2. **计算路径。** 各节点维护拓扑数据库，以自己为源运行最短路算法，生成下一跳信息。

Link-State Packet / Advertisement 是某个来源发布的一份链路状态；Link-State Database（LSDB）则是本节点收集、维护的状态集合。

这与 DV 的区别是：DV 主要告诉邻居“我认为到目的地还要花多少”；LS 则告诉其他节点“我连接哪些邻居，这些链路的代价是多少”。收到各节点的局部事实后，路由器可以拼出所在范围的拓扑。

### 2. Global 不等于中央部署

Dijkstra 的输入：集中、完整的拓扑信息。这里应把“计算时拥有拓扑”与“拓扑从哪里来”分开理解。

LS 实现：本地发现邻接，分布式泛洪，每台路由器独立计算。它不要求先有一台中央服务器向所有节点广播整张图。

在拓扑稳定、通告充分传播后，同一范围内的节点应逐步取得一致视图；它们仍以不同节点为根计算各自的最短路径树。真实 OSPF、IS-IS 还会使用区域等分层机制，因此“全局”应理解为算法所需的相应范围，并非每台路由器都完整保存整个互联网的每条链路。

### 3. Dijkstra 维护什么？

设源节点为 $s$，维护：

- 已确定集合 $S$：其中节点的最短距离已确定。
- 暂定距离 $d(v)$：当前发现的从 $s$ 到 $v$ 的最小代价。
- 前驱 $\operatorname{pred}(v)$：当前最好路径上，位于 $v$ 之前的节点。

先令 $d(s)=0$，其他距离为 $\infty$。每轮取尚未确定且暂定距离最小的节点 $u$，加入 $S$，再对其邻居做松弛：

$$
d(v)\leftarrow\min\{d(v),\;d(u)+c(u,v)\}
$$

如果经 $u$ 得到了更小的距离，还要把 $\operatorname{pred}(v)$ 更新成 $u$。

“暂定”表示之后仍可能被改小。只有当节点成为当前最小者并被确定时，Dijkstra 才承诺它的距离已是最终最短距离。

### 4. 为什么可以确定当前最小者？

直观上，如果还想从未确定区域绕一条更便宜的路到 $u$，就必须先进入某个尚未确定的节点。这个节点的暂定距离不会小于当前最小的 $d(u)$；后续边权又非负，继续走不可能把总代价降到 $d(u)$ 以下。

这也是非负边权条件的重要性：若允许负边，后来走一条负边可能使距离下降，原先“确定”的结论便不再可靠。Bellman–Ford 可以处理更一般的图，但本章网络例题都使用非负代价。

### 5. 用四节点图从 A 算一遍

仍使用前面的图，先把 A 加入 $S$，用 A 的直连边初始化：

| 已确定的节点 | $d(B)$ | $d(D)$ | $d(C)$ |
| --- | --- | --- | --- |
| A | 3 | 7 | $\infty$ |
| A、B | 3 | 6 | 9 |
| A、B、D | 3 | 6 | 8 |
| A、B、D、C | 3 | 6 | 8 |

先选 B，因为暂定距离 3 最小。通过 B，把到 D 的距离从 7 降为 $3+3=6$，把到 C 的距离改为 $3+6=9$。

接着选 D，距离为 6。通过 D，把到 C 的距离从 9 降为 $6+2=8$。最后确定 C。

结果与 DV 收敛后的最短距离一致，但计算所用的信息不同：这次 A 已经知道整张图，可以直接在本地逐步松弛，不必等邻居逐轮报告剩余距离。

### 6. 前驱不一定是下一跳

到 C 的前驱是 D。沿前驱倒着回溯：

$$
C\leftarrow D\leftarrow B\leftarrow A
$$

恢复的正向路径为 $A\rightarrow B\rightarrow D\rightarrow C$。A 真正要交付的第一跳是 B，所以 A 的转发表应写 B，不能把目的 C 的前驱 D 直接当作下一跳。

D 在本例中虽然也是 A 的直连邻居，但直接先去 D 会花费 7，再去 C 花费 2，总计 9，并不是算出的最短路径 8。

### 7. Quiz 3.5 — Dijkstra and next hops

In an undirected graph, AB=3, AD=7, BD=3, BC=6, and DC=2. Run Dijkstra from A. Give the distances to B, D, and C, and the next hop from A to C.

:::study-proof[Reference answer: Dijkstra and next hops]{kind="example"}

After A, settle B at distance 3. Relaxing through B gives D=6 and C=9. Then settle D at distance 6 and improve C to 8. Finally settle C.

The final distances are B=3, D=6, and C=8. The path to C is A → B → D → C, so A's next hop is B. D is C's predecessor on that path, not A's next hop.

:::

## 八、从最短路径树生成转发表

### 1. E 发布的是什么信息？

![八节点加权网络，E 的直连邻居为 A、B、C、D、F](/media/compnet/routing-eight-nodes.svg)

图按原页上方拓扑重绘。E 的本地邻接信息为：

```text
E 的邻居及链路代价
A: 10    B: 4    C: 1    D: 2    F: 2
```

E 可以把这些事实放入自己的链路状态通告。其他节点也发布各自的邻接，收集后便能形成运行 Dijkstra 所需的拓扑。

原页表格顶部的“Seq. #”容易引起误解：表中 A 后面的 10、B 后面的 4 等，对应右侧图上的**链路代价**。一条真实通告还需要自己的来源、序号和寿命等管理信息，不能把这几个邻居代价当成各自的通告序号。

### 2. 以 E 为根逐步确定节点

先确定 E，暂定距离为 A=10、B=4、C=1、D=2、F=2，G、H 为 $\infty$。

**先处理 C。** 它距离为 1，可以把到 B 的距离改成 $1+2=3$，把到 H 的距离改成 $1+3=4$；经 C 到 D 要花 $1+2=3$，比直连的 2 更差，所以 D 不变。

**再处理 D、F。** 两者距离同为 2，可以任选先后顺序。D 不产生更短路径；经 F 到 G 得到 $2+4=6$。

**接着处理 B。** B 的距离为 3，经 B 到 A 为 $3+4=7$，优于直连的 10。经 B 到 G 则为 $3+3=6$，与经 F 的候选相同。

最后按暂定距离处理 H=4、G=6、A=7，不再产生更小的距离。

### 3. 一棵可选的最短路径树

下面括号里是从 E 出发的累计代价：

```text
E (0)
├─ C (1)
│  ├─ B (3)
│  │  └─ A (7)
│  └─ H (4)
├─ D (2)
└─ F (2)
   └─ G (6)
```

到 G 有两条等价最短路径：$E\rightarrow F\rightarrow G$ 和 $E\rightarrow C\rightarrow B\rightarrow G$，总代价都是 6。这里按课件选择前一条，并不表示后一条不是最短路。若保留等价多路径，实际转发还需要相应的选择机制。

### 4. 转发表只取路径的第一跳

| 目的节点 | 最短代价 | 下一跳 |
| --- | --- | --- |
| A | 7 | C |
| B | 3 | C |
| C | 1 | C |
| D | 2 | D |
| E | 0 | 本机 |
| F | 2 | F |
| G | 6 | F（本例选择） |
| H | 4 | C |

例如到 A 的路径为 $E\rightarrow C\rightarrow B\rightarrow A$，E 的表里只需提取下一跳 C。真实 IP 转发表通常对应目的网络前缀、下一跳地址与出接口；字母节点是算法教学的简化表示。

Dijkstra 找到的是以一个源为根的最短路径树，不是整张图的最小生成树。后者最小化连接所有节点的树边总和，并不保证从某个源到每个目的的路径都最短。

### 5. 计算开销与变化处理

朴素实现每轮扫描尚未确定的节点，可做到 $O(\lvert V\rvert^2)$；使用邻接表和二叉堆时，常见复杂度为：

$$
O\big((\lvert V\rvert+\lvert E\rvert)\log\lvert V\rvert\big)
$$

LS 的整体开销还包括邻居发现、通告泛洪、LSDB 同步与存储，不只是一次 Dijkstra 运算。

链路断开时，仍在运行的相邻节点发布更新，其他路由器收到后更新拓扑并重新计算。如果 G 整台设备失效，不能指望 G 自己发送撤销；B、F 等邻居发现相邻链路消失，发布变化，旧状态再按协议规则处理。

各节点发现故障、收到通告、完成计算和安装转发表的时刻并不相同，因此 LS 收敛期间仍可能存在暂时环路。拥有正确的最短路算法，不等于运行中的网络永远瞬时一致。

## 九、DV 与 LS 怎样比较？

| 比较项 | DV | LS |
| --- | --- | --- |
| 交换内容 | 到目的地的距离估计 | 本地邻接与代价 |
| 信息传播 | 邻居之间迭代 | 在范围内泛洪 |
| 本地计算 | Bellman–Ford 更新 | 基于拓扑运行 Dijkstra |
| 主要状态 | 目的距离、下一跳及邻居报告等 | LSDB、路径与下一跳等 |
| 典型困难 | 旧信息循环依赖、无穷计数 | 消息版本、数据库同步、计算与安装时序 |
| 代表协议 | RIP | OSPF、IS-IS |

DV 的向量、邻居状态和更新量也会随规模增长；LS 的泛洪与拓扑存储可以通过区域等机制控制范围。不能据此得出“DV 总是更可扩展”或“LS 永远没有环路”。

OSPF（Open Shortest Path First）和 IS-IS（Intermediate System to Intermediate System）是实际的链路状态协议，除最短路计算外，还需要邻接管理、可靠传播、区域划分等机制。OSPFv2 的基础定义见 [RFC 2328](https://www.rfc-editor.org/rfc/rfc2328.html)。

### Quiz 3.6 — Global information

Is link-state routing necessarily implemented by a centralized routing server? What information does each router need before running Dijkstra?

:::study-proof[Reference answer: Global information]{kind="example"}

No. Routers can discover local adjacencies and flood link-state advertisements in a distributed way. Each router then runs its own computation.

Dijkstra needs a topology and link-cost view for the relevant scope. A router's immediate-neighbor costs alone are not enough to compute all shortest paths locally; the LSDB provides the additional topology information. During convergence, different routers may temporarily hold different views.

:::


## 十、分层路由与自治系统

### 1. 为什么需要管理边界？

前面的最短路例题假设所有节点使用一套图和一致的代价。互联网却由许多独立管理的网络组成：各方有自己的设备、内部结构、成本和对外政策，不可能要求所有路由器都掌握并优化同一张精细图。

AS（Autonomous System，自治系统）把共同管理和对外路由策略下的网络作为一个路由单位，以 ASN 标识。课件 p.38 的“Anonymous System”是误写，正确名称是 Autonomous System；AS 也不只是任意一组主机。定义与 BGP 的关系见 [RFC 4271](https://datatracker.ietf.org/doc/html/rfc4271)。

域内的 IGP（Interior Gateway Protocol），如 OSPF、IS-IS，处理域内路径。BGP 则交换跨 AS 的可达性与策略信息。划分边界后，外部可以不必知道内部每台路由器和每条链路。

### 2. 分层与前缀聚合怎样减少细节？

用文档地址举例，一个网络内部使用两个地址块：

```text
203.0.113.0/25
203.0.113.128/25
```

当可达性和策略允许时，对外可以用聚合前缀 `203.0.113.0/24` 表达它们的共同去向。包进入这个网络后，内部再按更具体的路由继续转发。

这不是在 IP 首部里先写一个“区域目的地”，到了区域再改成“主机目的地”。正常 IP 转发仍按目的 IP 查表，层次结构主要通过地址分配、前缀与路由信息表达。

一个 AS 可以通告多个前缀，也可以有多个外部出口。聚合需要满足地址范围、对齐和实际可达性等条件，不能把任意一组前缀都压成一条。课件 p.35 的“区域外只有一条路由”是简化模型，不是所有 AS 的固定结构。

### 3. Hot-potato routing 与非对称路径

同一个目的地可能有多个出口。其他偏好条件可比时，一个 AS 可以倾向于让流量尽快从内部代价较低的出口离开，减少自己承担的内部传输成本。这称为 Hot-Potato Routing。

在课件 p.36 的图中，A2 发往 B1 可以先从靠近 A2 的边界离开，再在 ISP B 内到达 B1；B1 发回 A2 时，ISP B 又倾向从靠近 B1 的边界离开，经 A1 再到 A2。去程与回程因此可以不同，也可能长于端到端共同优化得到的路径。

原页写了“symmetric”，但按图中的两条蓝色路径，应理解为**非对称**。造成这一现象的是双方各自的目标与出口决策，不是“只要分层，路径就必然不对称”。

实际 BGP 也不是总把最近出口放在第一位。进口策略、本地偏好等条件可能先排除或优先选择某些路由，IGP 的出口代价再在后续比较中发挥作用。

## 十一、Transit、Peering 与路由出口策略

### 1. 两种关系分别约定什么？

**Customer–Provider / Transit。** 客户向上游购买转接服务。Provider 按约定帮助客户访问更广的互联网，也承载外部发往客户的流量。

**Peering。** 对等方主要交换自身和各自客户的可达性。在课件采用的典型模型中，双方不会顺便替对方通往自己的其他 peer 或 provider 提供转接。

课件 p.37 使用 settlement-free peering，即双方不互付结算费。现实也有 paid peering，所以“互不付费”是该例的条件，不是所有 peering 的定义。

### 2. 为什么不能把学到的所有路由都告诉所有邻居？

假设 AS X 从自己的 Provider 学到前缀 P。如果 X 又把这条路由通告给一个无关 Peer，就相当于说“去 P 可以经过我”。Peer 随后可能把数据交给 X，X 再使用自己付费购买的上游服务转发。

这样，X 就可能在两个非客户之间提供未经约定的转接。BGP 的出口策略正是在决定：哪些可达性愿意提供给哪些邻居。

常见商业模型中的规则可概括为：

| 路由从哪里学来 | 向哪些方向通告 |
| --- | --- |
| 自身或客户 | 可向客户、peer、provider 通告 |
| Peer | 通常只向客户通告 |
| Provider | 通常只向客户通告 |

这是典型策略模型，具体合同和配置可以不同。错误地把路由传播到不应传播的关系，可能形成 route leak；相关分类见 [RFC 7908](https://www.rfc-editor.org/rfc/rfc7908.html)。

### 3. 补充：valley-free 路径

按上述规则观察数据路径，常见形式是：先沿 customer → provider 方向上行零次或多次，可选地经过一条 peer 链路，再沿 provider → customer 方向下行零次或多次。

```text
若干次上行 → 可选的一次对等互联 → 若干次下行
```

不能任意先下行到一个客户，再借它的另一个上游继续上行；否则这个客户就在替两个非客户提供中转。同样，连续穿过两个 peer 关系，通常也意味着中间一方提供了不愿承担的 transit。

这个模型解释了为什么“图上连着”不等于“这条路径会被通告并允许使用”。

### 4. Quiz 3.7 — Transit policy

AS X learns a route from its provider. Under the usual customer–provider and settlement-free peer model, should X export that route to an unrelated peer? Explain the economic reason.

:::study-proof[Reference answer: Transit policy]{kind="example"}

Normally, no. Exporting the provider-learned route to a peer would offer the peer a path through X and X's upstream provider. X would then provide transit between two non-customers and could pay upstream costs for the peer's traffic. Under the stated model, X normally exports that route only to its customers.

:::

## 十二、BGP：通告路径，按策略选择出口

### 1. Path vector 比距离数字多了什么？

BGP（Border Gateway Protocol）交换目的前缀的可达性。理解一条路由时，至少要看：

| 信息 | 含义 |
| --- | --- |
| Prefix | 通往哪个目的地址块 |
| AS_PATH | 这条通告经过的 AS 路径信息 |
| NEXT_HOP | 使用此路由时需要到达的 BGP 下一跳 |
| Policy attributes | 如 LOCAL_PREF 等参与本地选择的属性 |

与只交换一个距离数字相比，AS_PATH 提供了 AS 级路径信息。对于普通 AS_SEQUENCE 路径，收到包含自身 ASN 的路由时，可以拒绝它，以避免形成 AS 级循环。向外部邻居传播路由时，通告通常会加入本 AS 的 ASN。

AS_PATH 不列出 AS 内的每台路由器，也不是 RTT 或物理距离。AS 跳数少的路径，内部可能仍经过很多设备和很长链路。

### 2. 为什么更长的 AS_PATH 也可能被选中？

选路先受路由是否可用、进口策略和本地偏好等条件影响，不是把所有通告的 AS 数一数就结束。LOCAL_PREF 可以表达同一 AS 内对出口路由的偏好。

自编例：到同一前缀有两条候选，下一跳都可达、路由都被接受：

| 路由 | 本地设置 |
| --- | --- |
| 客户路由，AS_PATH 长度 3 | LOCAL_PREF=200 |
| Provider 路由，AS_PATH 长度 2 | LOCAL_PREF=100 |

在这种设置下，可以选择前者，即使其 AS_PATH 更长。本例中的偏好值是人为设定，用来说明策略作用，不是 BGP 给所有 customer/provider 路由规定的常数。

不同实现的完整比较过程还涉及其他属性与条件。本章需要掌握的是：**BGP 先在策略与可达性的约束下选路，不能背成“必选 AS 数最少”。**

### 3. eBGP、iBGP 与 IGP 各做哪一段工作？

| 机制 | 连接或作用范围 | 主要任务 |
| --- | --- | --- |
| eBGP | 不同 AS 的 BGP speakers | 交换跨域路由 |
| iBGP | 同一 AS 的 BGP speakers | 在域内传播 BGP 路由和相关属性 |
| IGP | 域内路由系统 | 提供内部路径以及到出口或 BGP 下一跳的可达性 |

例如边界路由器 R2 通过 eBGP 学到一个外部前缀，再通过 iBGP 把路由传给内部的 R0。R0 知道“外部有这条路”以后，还必须能够到达所选的 BGP NEXT_HOP；这通常依赖 IGP 或其他内部可达性机制进行解析。

所以 iBGP 不是 IGP 的别名。一个传播外部路由，一个处理内部路径，两者需要协同。BGP 会话使用 TCP；图中的逻辑 iBGP 连接可以经过多跳，不表示两端之间各有一根直连网线。

普通 iBGP 对从 iBGP 学来的路由有再通告限制，不能当成任意泛洪。传统 full mesh 要让相关 BGP speakers 两两建立逻辑会话；有 $n$ 个 speakers 时，会话数为 $n(n-1)/2$。Route Reflector 可以缓解全连接的规模问题，见 [RFC 4456](https://www.rfc-editor.org/rfc/rfc4456.html)。这里的 speakers 不是要求 AS 内每一台设备都运行 BGP。

### 4. BGP 选路与最长前缀匹配仍是两步

BGP 可以为一个目的前缀在多个候选路由中选择路径。安装到转发系统后，实际到来的包再根据目的 IP，在可用的不同前缀间进行最长前缀匹配。

例如，对某个 `/24` 的策略选路，不会把一个并不属于它的目的地址也吸进来。前缀选择的范围，与同一前缀内的候选路径选择，不能混成一个优先规则。

### 5. Quiz 3.8 — BGP versus shortest paths

A router receives a three-AS customer route and a two-AS provider route to the same prefix. Can policy make it choose the longer AS_PATH? What role can an IGP still play after the BGP exit is selected?

:::study-proof[Reference answer: BGP versus shortest paths]{kind="example"}

Yes. If both routes are usable and accepted, a policy giving the customer route a higher LOCAL_PREF can make it win despite its longer AS_PATH.

An IGP can still provide the internal path toward the chosen exit or resolve reachability to the BGP NEXT_HOP. Choosing an external route does not remove the need for internal forwarding. The exact route-selection process involves more conditions than AS_PATH length alone.

:::

## 十三、为什么 AS2 到 B 有两条路，到 C 只有一条？

### 1. 先看关系，再看路径

课件中，AS2、AS3、AS4 是 AS1 的客户；AS2 与 AS3 对等互联，AS3 与 AS4 也对等互联。A、B、C 分别是 AS2、AS3、AS4 所在一侧的目的前缀代号。

这里的 AS1 等是图中的网络代号，A、B、C 则是目的前缀，不是路由器端口或协议名称。

### 2. AS1 向客户 AS2 提供哪些路由？

AS2 向 AS1 通告自己的 A，AS_PATH 为 `[AS2]`。AS1 可以按服务关系向客户 AS2 提供其他网络的可达性，例如：

```text
目的 B：AS_PATH = [AS1, AS3]
目的 C：AS_PATH = [AS1, AS4]
```

这些通告告诉 AS2，可以先把相应流量交给 AS1，再分别经过 AS3、AS4 到达目的前缀。

### 3. Peer AS3 又给 AS2 带来什么？

AS2 与 AS3 可以互相通告自身的前缀。AS3 向 AS2 通告 B，AS_PATH 为 `[AS3]`。于是 AS2 到 B 有两个候选：

- 经 Provider：AS2 → AS1 → AS3 → B。
- 经 Peer：AS2 → AS3 → B。

课件选择 AS3。这条路既符合常见的 peer 经济偏好，又有更短的 AS_PATH；因此，单凭这个例子不能证明所有 BGP 决策都只比较路径长度。

### 4. 为什么 AS3 不再把 C 告诉 AS2？

AS3 确实与 AS4 对等互联，也可能从 AS4 学到 C。但按本例的出口策略，AS3 不会把从一个 peer 学来的路由，再通告给另一个 peer AS2。

否则，AS2 发往 C 的流量就可能走 AS2 → AS3 → AS4，让 AS3 在两个 peer 之间提供第三方中转。这不是本例 peering 提供的服务。

所以图上存在两条相连的 peer 链路，并不意味着 AS2 能学到经 AS3 到 C 的路由。在给定通告和策略下，AS2 到 C 只有经 AS1 的已知路由。

同理，AS2 也不会把从 Provider AS1 学到的 C，随意转告给 Peer AS3。

### 5. 通告方向与数据方向

课件用虚线画路由通告，用实线画业务包，它们不能当成同一种箭头：

```text
路由通告：AS2 → AS1
含义：经过 AS2 可以到达 A

发往 A 的数据：AS1 → AS2 → A
```

通告的来源在告诉邻居“可以经我到达这个目的地”，邻居随后发往该目的的数据便可能向通告来源转发。路由消息仍通过真实链路传输，但其语义与业务包的目的不同。

## 十四、把算法和实际转发接起来

一台路由器最终需要的是能执行的下一跳和出口信息，但这些信息可以来自不同机制：

1. **域内先形成路径。** DV 通过邻居迭代，或 LS 收集拓扑后计算，得到内部可达性。
2. **BGP 学习外部前缀。** 接受与出口策略决定愿意学习、使用和继续提供哪些路由。
3. **解析下一跳。** 通过内部路径到达所选出口或 BGP NEXT_HOP，把候选路由转成可安装的转发信息。
4. **逐包执行。** 包到来后查转发表，再处理 TTL、链路交付等动作，细节见 IP 协议实现篇。

任何一步都可能随故障或策略变化更新。最短路算法的正确性、路由协议的收敛，以及某一时刻业务包是否顺利抵达，是相关但不同的问题。

复习时可以用下面这些任务检查理解：

| 内容 | 应该能独立完成的任务 |
| --- | --- |
| 服务模型 | 区分 TCP 连接、IP 数据报与网络层虚电路 |
| 路由器结构 | 解释输入/输出排队、HOL 与输出容量限制 |
| DV | 用邻居报告算一次更新，并写出下一跳 |
| 故障 | 用三节点例子解释无穷计数与 poison reverse 的边界 |
| Flooding | 说明来源、序号、确认重传和 age 各解决什么问题 |
| LS / Dijkstra | 按轮确定节点，从前驱恢复路径，再提取第一跳 |
| 分层与 AS | 区分管理域、前缀聚合、IGP 与 BGP |
| BGP 策略 | 判断某条路由能否向 peer/provider 继续通告 |
| 域内外协作 | 说明为什么学到 BGP 路由后仍需要内部可达性 |

## 资料与校对说明

主要资料为 `lec4-mod3net_agent_networks.pdf`：pp.2–15 对应服务模型与路由器，pp.17–25 对应 DV 与泛洪，pp.26–33 对应 LS，pp.35–41 对应分层路由与 BGP。分享对话用于展开解释，例题数值按原图重新计算。

正文已在相关段落说明课件的几处简化或笔误：p.26 的全局拓扑输入不意味着 LS 必须中央部署；p.29 邻居表中的数字是链路代价；p.36 的图展示了非对称路径；p.38 的 AS 应展开为 Autonomous System。

| 协议资料 | 用于核对的内容 |
| --- | --- |
| [RFC 3031](https://www.rfc-editor.org/rfc/rfc3031.html) | MPLS 标签与标签交换路径 |
| [RFC 2453](https://www.rfc-editor.org/rfc/rfc2453.html) | RIP、距离向量与不稳定性处理 |
| [RFC 2328](https://www.rfc-editor.org/rfc/rfc2328.html) | OSPF、链路状态与区域 |
| [RFC 4271](https://datatracker.ietf.org/doc/html/rfc4271) | AS、BGP 路径属性与域内外会话 |
| [RFC 4456](https://www.rfc-editor.org/rfc/rfc4456.html) | iBGP route reflection |
| [RFC 7908](https://www.rfc-editor.org/rfc/rfc7908.html) | BGP 路由泄漏与出口关系 |
