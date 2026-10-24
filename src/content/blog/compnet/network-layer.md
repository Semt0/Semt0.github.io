---
title: 网络层：An IP-flavored Network Layer Implementation
description: lab2 害人不浅。
publishDate: 2026-10-24
tags:
  - 计算机
  - 计算机网络
draft: false
language: 中文
course: 计算机网络
order: 1
---

本节围绕 **An IP-flavored Network Layer Implementation（以 IP 为核心的网络层实现）** 展开，回答一个问题：

> 互联网怎样让一个 IP 数据报经过多个不同的网络、路由器和物理链路，最终到达目的接口？

## 一、全章知识框架

前面学习路由算法时，重点是“怎样寻找路径”。这一章进一步讨论：**有了路径信息之后，一个数据报究竟怎样被逐跳送出去？**

| 主题 | 要解决的问题 | 需要抓住的机制 |
| --- | --- | --- |
| IP 数据报 | 路由器从哪里知道目的地、剩余跳数和载荷类型？ | IP 首部 |
| 地址与前缀 | 怎样表示接口地址和一整块目的地址？ | 子网掩码、CIDR |
| 转发 | 多条路由同时匹配时选哪一条？ | 最长前缀匹配 |
| 分片与 MTU | 下一条链路装不下这个包怎么办？ | 分片、DF、PMTUD |
| ICMP | 发送方怎样得知转发错误、探测网络？ | 不可达、超时、Echo |
| 与链路层协作 | 已知下一跳 IP，怎样在本地链路上找到它？ | ARP、帧封装 |
| Middleboxes | 途中设备为什么还会改地址、过滤或代理？ | NAT、防火墙、代理 |
| IPv6 | 地址扩大后，哪些机制保留，哪些机制改变？ | 128 位地址、扩展首部、邻居发现 |

### 1. IP 的“窄腰”结构

互联网里的应用和链路可以各不相同：上面有网页、视频、邮件等应用，下面可以是以太网、Wi-Fi 或其他链路。它们能够互通，是因为中间约定了共同的 IP 数据报格式和转发规则。

```text
        网页、视频、邮件等应用
             TCP、UDP 等
                 IP
        Ethernet、Wi-Fi、PPP 等
```

上、下两端有许多选择，中间收束到 IP，这就是“窄腰”（narrow waist）的意思。新增一种应用，不必为每种底层网络各写一套通信协议；采用一种新链路，也不必让所有应用随之改写，只要能承载 IP 数据报。

IP 统一的是网络层的接口，并不要求沿途帧格式相同。数据报从以太网进入另一种链路时，路由器会去掉原来的链路层封装，再按出口链路的要求重新封装。后面讨论的 MTU 和逐跳交付，都是这种异构网络互联需要处理的问题。

### 2. 路由与转发不是同一个动作

| 概念 | 解决的问题 | 典型机制 |
| --- | --- | --- |
| Addressing（寻址） | 怎样给接口分配地址，表达目的网络？ | IPv4、IPv6、网络前缀 |
| Routing（路由） | 怎样获得到达各个目的前缀的路径信息？ | 静态路由、OSPF、BGP |
| Forwarding（转发） | 这个已经到来的包，应该交给哪个下一跳、哪个出口？ | 转发表查找、最长前缀匹配 |
| Link delivery（链路交付） | 怎样把包交给同一链路上的下一跳？ | 以太网、ARP |

路由通常属于**控制平面**：根据拓扑、代价或策略，形成可达性与选路信息。转发通常属于**数据平面**：对每个到来的数据报查表并执行动作。BGP 的选路还受策略影响，不能把所有路由协议都理解成“计算物理距离最短的路”。

可以把全章串成：

$$
\boxed{\text{目的地址}\rightarrow\text{查转发表}\rightarrow\text{确定下一跳与出口}\rightarrow\text{链路交付}}
$$

:::study-note[路由器不必在每个包里拿到整条路径]{kind="tip"}

普通 IP 数据报携带目的 IP。每台路由器根据自己的转发表决定下一跳，多台设备连续执行这个局部动作，才构成整个端到端路径。普通主机也要查本机路由表，并非只有路由器才做下一跳选择。

:::

### 3. IP 提供什么服务？

IP 的基本服务模型是 **Best-Effort Delivery（尽力而为交付）**：尽力转发每个数据报，但不保证一定到达、按序到达、没有重复，也不承诺确定的时延或带宽。

“无连接”表示发送普通 IP 数据报前，不需要由 IP 在沿途建立一条连接。它不表示现实网络中的所有设备都没有状态：ARP 缓存、路由表、NAT 映射等都可以存在。

可靠、有序的字节流一般由 TCP 等端系统协议提供。IP 没有收到每个包的确认后自动重传的机制；ICMP 的错误报告也不会把 IP 变成可靠协议。

## 二、IP Datagram：数据报里到底装了什么？

### 1. 逐层封装与分用

以不含选项的 Ethernet + IPv4 + TCP 为例：

```text
应用层：  应用数据
传输层： [TCP 首部 | 应用数据]
网络层： [IPv4 首部 | TCP 首部 | 应用数据]
链路层： [Ethernet 首部 | IPv4 首部 | TCP 首部 | 应用数据 | FCS]
```

$$
\text{IP Datagram}=\text{IP Header}+\text{IP Payload}
$$

Payload 是相对于当前层而言的“载荷”，并不总等于应用数据：IP 的 Payload 可以是 TCP 报文段、UDP 数据报，也可以是 ICMP 消息。以太网帧的 Payload 则包含整个 IP 数据报。

无选项时，TCP 首部 20 B 加 IPv4 首部 20 B，共有 40 B 基本开销。这还没有计入以太网首部与 FCS，也不包括可能存在的 TLS、应用协议首部或 TCP/IP 选项。做长度题时，要先弄清题目算的是哪一层。

接收时，各层通过不同字段判断交给谁：

| 所在层 | 分用依据 | 例子 |
| --- | --- | --- |
| Ethernet | EtherType | `0x0800` 为 IPv4，`0x0806` 为 ARP，`0x86DD` 为 IPv6 |
| IPv4 | Protocol | `6` 为 TCP，`17` 为 UDP，`1` 为 ICMP |
| TCP / UDP | 端口以及连接上下文 | 把数据交给相应套接字 |

因此，**Protocol=6 只表示载荷交给 TCP，不表示一定是 HTTP**。应用属于哪个连接，还要继续看传输层信息。

### 2. IPv4 首部结构

下面每个横行共 32 bit；字段中的数字表示位数，文字宽度不按位数等比例绘制：

```text
| Version 4 | IHL 4 | DSCP 6 + ECN 2 | Total Length 16 |
| Identification 16 | Flags 3 | Fragment Offset 13    |
| TTL 8 | Protocol 8 | Header Checksum 16             |
| Source Address 32                                   |
| Destination Address 32                              |
| Options + Padding（若有，补齐到 32 bit 的整数倍）    |
```

| 字段 | 位数 | 用途与单位 |
| --- | --- | --- |
| Version | 4 | IP 版本；IPv4 的值为 4 |
| IHL | 4 | 首部长度，单位为 4 B；最小值为 5 |
| DSCP / ECN | 6 / 2 | 服务分类标记 / 显式拥塞通知 |
| Total Length | 16 | 整个 IPv4 数据报长度，单位为 B，包含首部 |
| Identification | 16 | 分片重组时用于区分所属的原始数据报 |
| Flags | 3 | 保留位、DF、MF |
| Fragment Offset | 13 | 本片数据在原始 IP Payload 中的起始位置，单位为 8 B |
| TTL | 8 | 转发时消耗的生存时间字段，通常作为跳数限制理解 |
| Protocol | 8 | 指明 IP Payload 的协议类型 |
| Header Checksum | 16 | 只校验 IPv4 首部，不校验 Payload |
| Source / Destination Address | 各 32 | 源接口地址 / 目的地址 |
| Options + Padding | 可变 | 可选信息和对齐填充 |

IHL 的单位与 Total Length 的单位不同。例如 `IHL=5` 表示首部为 $5\times4=20\,\mathrm{B}$，不是 5 B。IHL 最大为 15，因此 IPv4 首部最大为 60 B。

$$
L_{\text{header}}=4\times\mathrm{IHL},\qquad
L_{\text{payload}}=L_{\text{total}}-L_{\text{header}}
$$

Total Length 为 16 位，所以一个 IPv4 数据报的总长度最多是 $2^{16}-1=65535\,\mathrm{B}$。这只是协议字段能表达的上限，并不代表路径上的链路都能直接承载这么大的包。首部格式与字段定义见 [RFC 791，第 3.1 节](https://www.rfc-editor.org/rfc/rfc791.html#section-3.1)。

DSCP 与 ECN 也要结合网络的实际处理来理解。DSCP 可以供路由器选择不同的排队或转发待遇，但仅在包里填上某个值，并不会自动获得带宽或优先权；效果取决于网络的策略与资源配置。ECN 则让支持它的拥塞控制机制使用显式标记反馈拥塞，配合端系统作出响应，并不是每台路由器都会对每个包执行的固定步骤。两者分别见 [RFC 2474](https://www.rfc-editor.org/rfc/rfc2474.html) 和 [RFC 3168](https://www.rfc-editor.org/rfc/rfc3168.html)。

### 3. TTL 为什么必须逐跳减小？

假设错误路由造成：

$$
R_1\rightarrow R_2\rightarrow R_1\rightarrow R_2\rightarrow\cdots
$$

如果没有限制，一个包会持续占用链路和缓存。路由器转发 IPv4 数据报时，TTL 至少减少 1；通常按“每过一台路由器减 1”分析，例如 $64\rightarrow63\rightarrow62$。

**收到 TTL=1 的包时，路由器不能再把它转发到下一跳**，而是丢弃，通常向源端返回 ICMP Time Exceeded。普通二层交换机转发以太网帧不会因此减少 IP TTL。

TTL 的历史定义包含时间含义，在一般转发分析中把它当作跳数预算即可。目的主机接收交付到自己的包，与路由器继续转发不是一回事；不能把“到达目的主机”也机械算成一次转发。

TTL 只能限制一个包在环路里存活多久，不能消除路由表中的环路。要让后续数据报不再绕圈，仍需修正路由或等待路由协议收敛。

### 4. 首部校验和为什么要更新？

IPv4 Header Checksum 对首部中的 16 位字进行反码求和并取反，用来检测首部差错。TTL 属于首部，所以路由器修改 TTL 后，要相应更新校验和；可以增量更新，不必每次都完整重算。

它既不保护 IP Payload，也不是加密认证机制。以太网 FCS 和 TCP/UDP 校验和分别承担其他范围的差错检测，不能把这些字段混为一个“整个网络统一的校验和”。

### 5. 自测：首部与载荷的长度

An IPv4 packet has IHL=6 and Total Length=124 bytes. Find its header and payload lengths. Does the IPv4 header checksum cover that payload?

:::study-proof[Reference answer: IPv4 field units]{kind="example"}

The header length is $6\times4=24$ bytes. The payload length is $124-24=100$ bytes. IHL counts 32-bit words, whereas Total Length counts bytes and includes the header. The IPv4 header checksum covers the 24-byte header, not the 100-byte payload.

:::

## 三、IP Address、Prefix 与 Subnet：怎样表示一个网络？

### 1. IPv4 地址与接口

IPv4 地址采用 32 位表示，通常写成四段点分十进制，每段对应 8 位：

```text
192.168.1.10
11000000.10101000.00000001.00001010
```

每段范围为 0–255。这里的 32 位是 IPv4 的协议设计，并不是所有网络地址都必须为 32 位；IPv6 就使用 128 位。

更准确地说，IP 地址配置在**网络接口**上。一台主机可以同时有 Wi-Fi、以太网、VPN 等接口，一个接口也可以配置多个地址。路由器通常也有多个接口以及相应的 IP 地址。

### 2. `/24` 表示什么？

`192.168.1.10/24` 表示前 24 位为网络前缀，后 8 位是该前缀内的地址部分：

```text
11000000.10101000.00000001 | 00001010
<------ 网络前缀 24 bit --> | <- 8 bit ->
```

对应掩码为 `255.255.255.0`，网络前缀写作 `192.168.1.0/24`。要区分“一个接口地址带前缀长度”和“整个地址块的规范写法”。

一般地，前缀长度为 $p$ 时，后面还有 $32-p$ 位可以变化，因此地址块中的地址总数为：

$$
N_{\text{addresses}}=2^{32-p}
$$

这算的是地址总数，能否把其中某个地址配置给普通主机，还要看子网的使用方式。

$$
\boxed{\text{Network Address}=\text{IP Address}\mathbin{\&}\text{Subnet Mask}}
$$

掩码前面的连续 1 保留网络位，后面的 0 清除其余位。CIDR 中的掩码由连续的 1 再接连续的 0 构成。

### 3. 完整例题：`192.168.1.137/25` 属于哪里？

`/25` 的最后一个掩码字节是 `10000000`，即 128；137 的二进制为 `10001001`：

```text
IP 最后一字节：10001001  = 137
Mask：        10000000  = 128
按位与：      10000000  = 128
```

因此得到：

| 项目 | 结果 |
| --- | --- |
| 子网掩码 | `255.255.255.128` |
| 网络地址 | `192.168.1.128` |
| 地址块范围 | `192.168.1.128`–`192.168.1.255` |
| 定向广播地址 | `192.168.1.255` |
| 常规可分配接口地址 | `192.168.1.129`–`192.168.1.254` |
| 地址总数 | $2^{32-25}=128$ |
| 常规可分配地址数 | $128-2=126$ |

也可以用“块大小”快速计算：最后一字节每 $256-128=128$ 个地址为一块，所以边界为 0、128。

:::study-note[减 2 公式有适用条件]{kind="warning"}

普通 IPv4 广播子网常保留主机位全 0 的网络地址和全 1 的定向广播地址，因此可分配数常为 $2^{32-p}-2$。不能对所有前缀机械套用：`/31` 可用于点到点链路，`/32` 表示单个地址或主机路由。更不能按 IPv4 的这套规则计算 IPv6 的“广播地址”，因为 IPv6 没有广播。

:::

### 4. 前缀划分落在第三个字节时

`/24`、`/25` 的例子只需要看最后一个字节，但 CIDR 不要求网络位和点分十进制的分段对齐。以 `192.24.12.0/22` 为例：前两个字节已经占 16 位，第三个字节还要取前 6 位作为网络位。

```text
第三字节的掩码：11111100 = 252
第三字节的起点：00001100 = 12
可变化的后两位：      00、01、10、11
第三字节的范围：12、13、14、15
```

因此掩码为 `255.255.252.0`，第四个字节则可以完整地从 0 变到 255，整个地址块范围是 `192.24.12.0`–`192.24.15.255`，共有 $2^{10}=1024$ 个地址。

这里第三个字节的块大小为 $256-252=4$，所以块起点应是 0、4、8、12、16 等。`192.24.16.32` 已经进入下一块，不属于 `192.24.12.0/22`。这个判断在后面的路由查找例题中会用到。

### 5. 路由聚合为什么能缩小路由表？

如果为每个地址单独存一条路由，表项会非常庞大。前缀能用一条规则表示整个地址块的去向，例如 `10.0.0.0/8` 覆盖 $2^{24}$ 个地址，而 `10.1.2.0/24` 覆盖 256 个地址。

假设下面两个相邻地址块都应交给同一个下一跳：

```text
192.168.0.0/24  → R
192.168.1.0/24  → R
```

它们可以聚合为 `192.168.0.0/23 → R`，恰好覆盖从 `192.168.0.0` 到 `192.168.1.255`。聚合依赖**二进制前缀对齐**：不能因为两个网段的十进制数字相邻，就任意合成一个更短前缀；还要确保聚合后的转发行为符合实际可达性。

CIDR 与聚合的设计动机见 [RFC 4632](https://www.rfc-editor.org/rfc/rfc4632.html)。

### 6. 几类容易混淆的地址

| 地址或前缀 | 含义 |
| --- | --- |
| `10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16` | 私有 IPv4 地址范围，不作为全球公网可路由地址使用 |
| `127.0.0.0/8` | IPv4 环回地址范围，常见 `127.0.0.1` |
| `0.0.0.0` | 可表示尚未配置地址等情境下的未指定源地址 |
| `0.0.0.0/0` | 匹配所有 IPv4 目的地址的默认路由前缀 |
| `255.255.255.255` | IPv4 受限广播地址，不经路由器转发 |

地址 `0.0.0.0` 的含义与路由前缀 `0.0.0.0/0` 的含义不同；后者的关键是 `/0` 不限制目的地址中的任何一位。

私有地址中的 `172.16.0.0/12` 覆盖第二个字节为 16–31 的范围，并不是所有 `172.x.x.x` 都是私有地址。不同私网可以复用相同地址，但同一个网络里仍要协调分配，避免地址冲突；把两个地址范围重叠的私网连接起来，也可能遇到寻址问题。

私网访问外部服务时常用 NAT，也可以由代理或其他中继提供通信。NAT 是常见方案，不是私网与外部通信的唯一方式。

## 四、Longest Prefix Matching：路由器怎样查表？

### 1. 同时匹配多条路由时，选最具体的一条

假设转发表为：

| 目的前缀 | 下一跳或出口代号 |
| --- | --- |
| `10.0.0.0/8` | A |
| `10.1.0.0/16` | B |
| `10.1.2.0/24` | C |
| `0.0.0.0/0` | D |

目的地址 `10.1.2.37` 匹配这四条记录，默认路由也匹配，但 `/24` 最长，所以选择 C：

$$
\boxed{\text{在所有匹配项中，选择前缀位数最多的项}}
$$

对前缀 $P/p$，匹配条件可以写成：

$$
(D\mathbin{\&}M_p)=P
$$

其中 $D$ 是目的地址，$M_p$ 是前 $p$ 位为 1 的掩码，$P$ 是主机位清零的规范前缀地址。

“最长”指匹配的前缀位数最多，不是距离最短，也不是延迟最小。路由协议先形成可用的转发信息，最长前缀匹配再从中选择覆盖这个目的地址的最具体规则。多个候选路由具有相同前缀时，还可能涉及协议优先级、代价和等价多路径等规则，这不由“最长”二字单独决定。

### 2. 默认路由与找不到路由

`0.0.0.0/0 → 192.168.1.1` 的意思是：如果没有更具体的匹配，就把包交给这个网关。它并不表示“目的 IP 要改成网关 IP”。

如果连默认路由都没有，且没有任何匹配项，就不能凭空选择一个接口。主机可能向本地应用报告不可达；路由器通常丢弃，并在满足 ICMP 发送条件时向源端报告目的不可达。

高速转发可以使用前缀树、压缩查找结构或 TCAM 等硬件，不必逐条线性扫描。实现手段可以变化，最长前缀匹配的语义不变。

### 3. 例题：重叠的 `/19` 与 `/22`

再看课件 p.48 的两个表项。这次前缀边界不在整字节处，需要先算清范围：

```text
192.24.0.0/19  → D
192.24.12.0/22 → B
```

`/19` 在第三个字节保留前 3 位，剩余 5 位可变，因此第三个字节覆盖 0–31，整个范围为 `192.24.0.0`–`192.24.31.255`。`/22` 的范围刚刚算过，是 `192.24.12.0`–`192.24.15.255`。逐个检查可得：

- `192.24.6.0`：只匹配 `/19`，走 D。
- `192.24.13.32`：两条都匹配，选择更长的 `/22`，走 B。
- `192.24.16.32`：只匹配 `/19`，走 D。
- `192.24.54.0`：两条都不匹配，仅凭此表无法转发。

如果另外存在 `0.0.0.0/0 → G`，最后一个地址才会走 G。不能因为表中某个前缀“看起来比较接近”，就把无匹配的包交给它。

:::study-note[课件 p.48 的图与表不一致]{kind="warning"}

原页表格写的是 `192.24.0.0/19`，右侧图却标成 `/18`，范围画到了 `192.24.63.255`。页上的 `192.24.16.32 → B` 和 `192.24.54.0 → D` 也不符合表中两条前缀。这里按表格重算，并补入 `192.24.13.32`，用来说明两条路由同时匹配的情况。

:::

### 4. 自测：四个目的地址分别走哪里？

仍使用上表，判断 `10.1.2.37`、`10.1.8.20`、`10.3.4.5` 和 `8.8.8.8` 的去向。

:::study-proof[展开答案：最长前缀匹配]{kind="example"}

| 目的地址 | 最长匹配前缀 | 选择 |
| --- | --- | --- |
| `10.1.2.37` | `10.1.2.0/24` | C |
| `10.1.8.20` | `10.1.0.0/16` | B |
| `10.3.4.5` | `10.0.0.0/8` | A |
| `8.8.8.8` | `0.0.0.0/0` | D |

每次先确认匹配，再比较长度。不能只看到表中存在 `/24`，就把所有目的地址都交给 C。

:::

## 五、IP Fragmentation 与 Path MTU Discovery

### 1. MTU 限制的是哪部分长度？

MTU（Maximum Transmission Unit，最大传输单元）表示某条链路能够承载的最大网络层数据单元大小。普通以太网常见 MTU 为 1500 B，表示**整个 IP 数据报**最多为 1500 B，通常不计外层以太网首部和 FCS。

课件 p.51 用以太网约 1.5 KB、Wi-Fi 约 2.3 KB 说明链路承载能力可能不同。这里要区分链路帧的尺寸限制与接口实际配置的 IP MTU：不能据此认为所有 Wi-Fi 接口的 IP MTU 都是 2.3 KB。

没有 IPv4 选项时，首部为 20 B，留给 IP Payload 的空间是：

$$
1500-20=1480\,\mathrm{B}
$$

若里面还有 20 B 的 TCP 首部，则留给 TCP 数据的空间为：

$$
1500-20-20=1460\,\mathrm{B}
$$

这就是典型 IPv4 以太网环境中 MSS=1460 的来源。**MSS 指 TCP 数据长度，MTU 指 IP 数据报长度**；TCP 选项、IP 选项、隧道额外封装或更小的路径 MTU 都可能降低实际可发送的数据量。MSS 协商也不能替代沿途的 MTU 发现。

### 2. IPv4 的 DF、MF 与偏移量

如果一个 4000 B 的 IPv4 数据报遇到 MTU=1500 B 的出口：

- `DF=0`：允许分片，IPv4 路由器可以把它拆开。
- `DF=1`：Don't Fragment，不允许分片；路由器丢弃，通常发送 ICMP Fragmentation Needed。

Flags 中另一位 MF 是 More Fragments：`MF=1` 表示原始数据报后面还有分片，`MF=0` 表示本片是原始数据报的最后一片。一个未分片的数据报通常为 `MF=0` 且 `Offset=0`。

偏移量的基准是**原始 IP Payload 的起点**，单位为 8 B，不包含原始 IP 首部。

### 3. 完整计算：4000 B 数据报经过 MTU=1500 B 的链路

假设原始数据报和各分片均无 IPv4 选项，首部为 20 B，且允许分片：

$$
L_{\text{payload}}=4000-20=3980\,\mathrm{B}
$$

除原始数据报的最后一片外，每片数据长度必须是 8 B 的整数倍。因此一般计算式为：

$$
D_{\max}=8\left\lfloor\frac{\mathrm{MTU}-H}{8}\right\rfloor
$$

这里 $H$ 是分片首部长度。代入后得到 $D_{\max}=8\lfloor1480/8\rfloor=1480\,\mathrm{B}$。

| 分片 | 所承载的原始 Payload 字节范围（从 0 起算） | 数据长度 | IP 总长度 | Fragment Offset | MF |
| --- | --- | --- | --- | --- | --- |
| 1 | 0–1479 | 1480 B | 1500 B | 0 | 1 |
| 2 | 1480–2959 | 1480 B | 1500 B | 185 | 1 |
| 3 | 2960–3979 | 1020 B | 1040 B | 370 | 0 |

第二、三片的偏移分别为：

$$
\mathrm{Offset}_2=\frac{1480}{8}=185,\qquad
\mathrm{Offset}_3=\frac{2960}{8}=370
$$

检查结果时，至少验证三件事：数据长度之和 $1480+1480+1020=3980$；每片总长度不超过 1500；非最后一片的数据长度是 8 的整数倍。

```text
原始： [20 B 首部 |             3980 B 数据             ]
分片1：[20 B 首部 | 1480 B 数据]  Offset=0    MF=1
分片2：[20 B 首部 | 1480 B 数据]  Offset=185  MF=1
分片3：[20 B 首部 | 1020 B 数据]  Offset=370  MF=0
```

每片都带自己的 IP 首部，所以发送的 IP 总字节数变为 $1500+1500+1040=4040\,\mathrm{B}$，比原来的 4000 B 多 40 B。这里还没有计算三次链路层封装的额外开销。

:::study-note[IP 分片不会给每片重新添加 TCP 首部]{kind="warning"}

分片是把原始 IP Payload 切开。若 Payload 是一个 TCP 报文段，TCP 首部通常只位于第一片承载的起始部分；后续分片承载其后续字节。目的端先完成 IP 重组，再把完整的 TCP 报文段交给 TCP。这与 TCP 在发送前把字节流分成多个独立报文段不同。

:::

### 4. 谁重组？丢一片会怎样？

正常 IPv4 转发中，**目的主机负责重组，中间路由器不负责先收齐再重组**。分片使用共同的源地址、目的地址、Protocol 和 Identification 来关联原始数据报，Offset 决定放置位置，最后一片帮助确定数据总长度。

因此，收到 `MF=0` 的最后一片，只能确定原始数据在哪里结束，不能证明前面的字节已经收齐。上例中即使先收到了第三片，仍然必须等待覆盖字节 0–2959 的前两片到达。

分片可以乱序到达。如果某片一直未到，重组计时器到期后会丢弃未完成的数据报。IP 不会自行可靠地补发丢失分片；若上层为 TCP，恢复由 TCP 的重传机制完成。

已经产生的 IPv4 分片还可能在后续更小的 MTU 处继续分片；这时偏移仍相对最初的数据报计算，MF 也要反映最初的数据报后面是否仍有数据。上面的固定 20 B 首部假设用于简化计算；有 IPv4 选项时，还要考虑哪些选项复制到后续分片。

### 5. PMTUD：尽量从源头避免中途分片

一条给定路径的 Path MTU 是沿途各段 MTU 的最小值：

$$
\mathrm{PMTU}=\min(\mathrm{MTU}_1,\mathrm{MTU}_2,\ldots,\mathrm{MTU}_n)
$$

例如课件 p.53 的路径上，MTU 依次为 1400、1200、900 B，最终 PMTU 为 900 B。源端根据某一跳反馈把包缩到 1200 B 后，还可能在后面遇到 900 B 的瓶颈，需要继续调整。路由改变后 PMTU 可能改变；往返方向的路径不同，也可能有不同 PMTU。

经典 IPv4 PMTUD 的过程为：

1. 源主机发送 `DF=1` 的数据报。
2. 某路由器发现报文大于出口 MTU，丢弃它。
3. 路由器返回 ICMP Destination Unreachable，`Type=3, Code=4`，报告需要分片，并按相应规范携带下一跳 MTU。
4. 源端降低后续数据报大小；必要的数据恢复由传输层或应用负责，不是路由器把被丢的包自动缩小后补发。

如果必需的 ICMP 反馈被过滤，源端可能持续发送大包，形成 **PMTUD Black Hole（路径 MTU 发现黑洞）**：小包可能通过，大包却持续无响应。仅凭这个症状不能直接确定原因，还要核实 MTU、DF、丢包和 ICMP 反馈。

PLPMTUD 通过分组层的探测与成功交付反馈推断可用大小，减少对 ICMP 反馈的依赖；TCP 与数据报传输的相关机制分别见 [RFC 4821](https://www.rfc-editor.org/rfc/rfc4821.html) 和 [RFC 8899](https://www.rfc-editor.org/rfc/rfc8899.html)。经典 IPv4 PMTUD 见 [RFC 1191](https://www.rfc-editor.org/rfc/rfc1191.html)。

PMTUD 的目标是尽量避免沿途分片，不代表 IPv4 已经取消分片。课件 p.51 所说的“用路径发现代替分片”，应放在这个设计目标下理解。

### 6. 自测：DF 与过大的包

A DF-marked IPv4 packet is 1300 bytes, but a downstream link has MTU 1200 bytes. What should happen in classic PMTUD? Why can filtering the feedback cause a black hole?

:::study-proof[Reference answer: Path MTU discovery]{kind="example"}

The router drops the packet because it cannot forward it on that link and DF forbids fragmentation. It sends an ICMP Destination Unreachable message with Type 3, Code 4, subject to the ICMP error-generation rules. The feedback reports the next-hop MTU so that the sender can reduce later packet sizes.

If the feedback is filtered, a sender relying on classic PMTUD may keep sending packets that are too large. Small packets can still pass, while larger transfers stall. IP itself does not retransmit the dropped data.

:::

### 7. 自测：MTU 不是整齐的 1500 时怎么办？

一个总长 2520 B、首部 20 B 的 IPv4 数据报允许分片，出口 MTU 为 1000 B。求每片数据长度、总长度、Offset 和 MF。

:::study-proof[展开答案：先减首部，再按 8 B 向下取整]{kind="example"}

原始数据为 $2520-20=2500\,\mathrm{B}$。每片最多容纳 980 B，但非最后一片的数据长度必须按 8 B 对齐，所以取 $8\lfloor980/8\rfloor=976\,\mathrm{B}$。

| 分片 | 数据长度 | IP 总长度 | Offset | MF |
| --- | --- | --- | --- | --- |
| 1 | 976 B | 996 B | 0 | 1 |
| 2 | 976 B | 996 B | 122 | 1 |
| 3 | 548 B | 568 B | 244 | 0 |

不能为了把总长度凑到 1000 B，而让前两片各装 980 B 数据，因为 $980/8$ 不是整数。

:::


## 六、ICMP：错误反馈与网络诊断

### 1. ICMP 与 IP 的关系

IP 不保证交付，但发送方仍然需要知道部分错误，例如没有可用路由、TTL 耗尽、报文太大。ICMP（Internet Control Message Protocol）用于传递这类控制与诊断信息。

ICMP 在功能上属于网络层的控制机制。它借助 IP 承载，并不因为放在 IP Payload 里，就变成了基于 TCP/UDP 的应用层协议。

IPv4 中，ICMP 封装在 IP Payload 内，Protocol=1：

```text
[IPv4 首部，Protocol=1 | ICMP Type | Code | Checksum | 其余字段与数据]
```

Type 表示消息大类，Code 进一步区分具体原因。常见 IPv4 ICMP 类型如下；这些编号不能直接套用到 ICMPv6。

| Type | Code 示例 | 消息 | 用途 |
| --- | --- | --- | --- |
| 0 | 0 | Echo Reply | ping 回复 |
| 3 | 0 / 1 | Network / Host Unreachable | 网络或主机不可达 |
| 3 | 3 | Port Unreachable | 例如 UDP 目的端口无人接收 |
| 3 | 4 | Fragmentation Needed | IPv4 包太大且 DF=1 |
| 8 | 0 | Echo Request | ping 请求 |
| 11 | 0 | Time Exceeded in Transit | 转发途中 TTL 耗尽 |
| 11 | 1 | Fragment Reassembly Time Exceeded | 分片重组超时 |
| 12 | 依具体问题而定 | Parameter Problem | IP 首部参数存在问题 |

ICMP 错误会引用引发错误的原始报文。经典格式包含**原 IPv4 首部，加上原 IP Payload 开头的 8 B**；后续规范和实现可以引用更多。若载荷是 TCP/UDP，开头的字节含有端口等信息，有助于源端把错误关联到相应的发送或连接。

```text
[新 IP 首部 | ICMP 首部 | 原 IP 首部 | 原 IP Payload 的前 8 B 或更多]
```

课件 p.55 的“IP datagram 的前 8 bytes”省略了这个区别，不能理解成只带整个原 IP 包开头的 8 B。**错误报告通常发给原数据报的源端**，不是继续发往原目的端。基本消息格式见 [RFC 792](https://www.rfc-editor.org/rfc/rfc792.html)。

旧表中还可能出现 `Type=4, Code=0` 的 Source Quench。它曾用于请求源端减少发送，如今已被弃用，不能把它当作现代 IP 拥塞控制的常规办法；弃用说明见 [RFC 6633](https://www.rfc-editor.org/rfc/rfc6633.html)。

### 2. 为什么不能认为“丢包一定有 ICMP”？

错误报告本身也可能丢失、被过滤或受到限速。另外，为防止错误消息引发更多错误消息和广播风暴，协议对 ICMP 错误的产生有明确限制，例如通常不对另一条 ICMP 错误再生成 ICMP 错误，也不对非首片错误生成这类报告。这里说的是 **ICMP 错误消息**，并非禁止对 Echo Request 发送 Echo Reply。相关限制见 [RFC 1812，第 4.3.2.7 节](https://www.rfc-editor.org/rfc/rfc1812.html#section-4.3.2.7)。

因此，“没有收到 ICMP 错误”不能证明包已经送达；“收到了不可达”也不代表 IP 接下来会自动重传。

### 3. ping 测量什么？

ping 发送 Echo Request，目标若允许且能够响应，则发送 Echo Reply。发送端把请求与回复关联，计算：

$$
\mathrm{RTT}=t_{\text{reply}}-t_{\text{request}}
$$

这里测量的是 **ICMP 探测的往返时间**，不是单向延迟，也不一定等于某个 TCP 连接的 RTT。

| 观察 | 可以得出的结论 | 不能直接得出的结论 |
| --- | --- | --- |
| ping 有回复 | 此次探测往返成功，目标回应了 Echo | HTTP 服务一定正常、所有协议都可达 |
| ping 没回复 | 此次 Echo 探测没收到预期回复 | 目标一定关机或完全断网 |
| ping 出现丢包 | 部分探测未在等待时间内获得回复 | 应用流量一定具有相同丢包率 |

### 4. traceroute 为什么能发现路径？

设实际路径为：

```text
A → R1 → R2 → R3 → B
```

发送端逐步增加探测包的初始 TTL，利用不同位置产生的 Time Exceeded：

| 初始 TTL | 转发过程 | 典型反馈 |
| --- | --- | --- |
| 1 | R1 不能继续转发 | R1 返回 Time Exceeded |
| 2 | R1 将 TTL 减为 1，R2 不能继续转发 | R2 返回 Time Exceeded |
| 3 | R1、R2 各消耗一次 TTL，R3 不能继续转发 | R3 返回 Time Exceeded |
| 4 | 包通过三个中间路由器，到达 B | 依探测协议产生终点反馈 |

经典 UDP traceroute 向目标的高位 UDP 端口发送探测，到达目标后常以 ICMP Port Unreachable 作为终点反馈；ICMP Echo 探测则期待 Echo Reply，TCP 探测可能根据 SYN-ACK 或 RST 判断抵达。

理解输出时要注意：

- 每一行的 RTT 是**源端到该跳回复的往返时间**，不是该段链路的单独延迟。相邻行 RTT 相减，不能可靠地当作中间链路延迟。
- `* * *` 表示未收到预期回复，可能由限速、过滤、不响应或丢包造成；后续跳仍可能正常回复。
- 负载均衡和路由变化可能让不同探测包走不同路径；回复走的回程也可能不同。
- 输出的是探测观察到的回复地址，不能保证展示所有设备或精确复原每条业务流的路径。

## 七、Co-operating with Link Layer：找到下一跳后怎样送过去？

### 1. IP 地址与 MAC 地址各自负责什么？

IP 地址与前缀用于跨网络寻址和路由。以太网 MAC 地址用于当前二层网络上的帧交付。普通二层交换机主要按目的 MAC 转发帧，路由器则取出 IP 数据报，按目的 IP 选择下一跳。

下面用两个网段说明，假设中间无 NAT：

```text
  Host A                 Router R                   Host B
192.168.1.10/24     192.168.1.1 | 10.0.0.1        10.0.0.20/24
    MAC_A       ——     MAC_RL   |  MAC_RR     ——      MAC_B
                   左侧以太网     右侧以太网
```

`MAC_A` 等是地址代号；路由器两个以太网接口各有自己的 MAC，不能把整台路由器视作只有一个统一 MAC。

### 2. 先查路由，再决定 ARP 查询谁

Host A 的路由表简化为：

```text
192.168.1.0/24  → 直连，使用本地以太网接口
0.0.0.0/0      → 下一跳 192.168.1.1，使用同一接口
```

如果目的为 `192.168.1.20`，匹配直连路由，A 通常直接解析这个目的地址的 MAC。如果目的为 `10.0.0.20`，使用默认路由，A 应解析**网关 `192.168.1.1` 的 MAC**。

这就是两个不同问题：

$$
\text{目的 IP：最终要交给谁？}\qquad
\text{下一跳 IP：这一跳先交给谁？}
$$

“比较本机和目的的网络地址”是简单单接口场景下判断直连的一种方式；更一般的规则是查路由表，因为可能存在多接口、主机路由、VPN 或其他更具体的路由。

### 3. ARP 如何得到网关 MAC？

ARP（Address Resolution Protocol）在当前链路上建立 IPv4 地址到链路层地址的映射。典型流程为：

1. A 检查 ARP 缓存是否存在可用的 `192.168.1.1 → MAC_RL` 表项。
2. 若没有，广播 ARP Request：谁拥有 `192.168.1.1`？请告诉 `192.168.1.10`。
3. 网关通常向 A 单播 ARP Reply，给出自己的链路层地址。
4. A 缓存映射，再发送等待的 IP 数据报；若解析最终失败，则无法在这条链路上完成交付。

请求帧的目的 MAC 通常为 `ff:ff:ff:ff:ff:ff`。ARP 使用自己的以太网类型 `0x0806`，**不是封装在 IPv4 中的一条 IP 消息**。ARP 广播通常不会被路由器转发到另一个网段，所以 A 不能靠一次本地广播直接查到远端 B 的 MAC。协议见 [RFC 826](https://www.rfc-editor.org/rfc/rfc826.html)。

:::study-note[DNS、路由与 ARP 各查什么？]{kind="tip"}

DNS 解析域名对应的地址等记录；路由查找根据目的 IP 决定出口和下一跳；ARP 在当前 IPv4 链路上解析下一跳的链路层地址。它们的输入、作用范围和缓存都不同。知道远端服务器的 IP 后，仍可能需要先用 ARP 找到本地网关。

:::

### 4. 经过路由器后，哪些地址发生变化？

对于上面的 A → R → B：

| 字段 | A 到 R 的帧 | R 到 B 的帧 |
| --- | --- | --- |
| Ethernet Source MAC | `MAC_A` | `MAC_RR` |
| Ethernet Destination MAC | `MAC_RL` | `MAC_B` |
| IP Source | `192.168.1.10` | `192.168.1.10` |
| IP Destination | `10.0.0.20` | `10.0.0.20` |
| TTL | 假设为 64 | 正常转发后为 63 |
| IPv4 Header Checksum | 与 TTL=64 的首部对应 | 随首部变化更新 |

R 去掉入站帧封装，查自己的转发表，确定 B 在右侧直连链路上，解析 B 的 MAC，然后重新封装一个新帧。新的 Ethernet FCS 也按新帧计算。

所以普通路由转发中，**链路层封装随路由跳逐段更换，源和目的 IP 通常保持不变，TTL 会变化**。同一个以太网段内跨交换机转发时，并非每经过一台交换机都要改写源、目的 MAC。也不是所有链路都采用以太网 MAC，表格的结论以本例链路类型为前提。

### 5. 路由器处理数据报的概念流程

1. 接收入站帧，检查链路层差错等信息，识别承载的网络层协议。
2. 检查 IP 首部是否合法，例如 IPv4 长度、版本和首部校验和。
3. 判断是否交付给路由器自身；发给本机的包应进入本地协议处理，而不是一律转发。
4. 若需转发，检查 TTL、查转发表，确定出口与下一跳；无路由或 TTL 耗尽时进入相应错误处理。
5. 减少 TTL、处理出口 MTU，必要时分片或丢弃，并为修改后的首部更新校验和。
6. 获得下一跳的链路层地址；以太网上可使用 ARP 缓存或发起解析。
7. 排队、重新封装并发送；队列拥塞等因素仍可能造成丢包。

这是帮助理解的逻辑流程，实际设备可能把查表、校验、过滤、排队等工作流水化处理。路由器并不会为了每个数据报都重新运行一次 OSPF 或 BGP。

### 6. DHCP 为主机提供什么配置？

IP 前缀与所在网络有关。电脑从一个网络搬到另一个网络后，通常需要重新获得适合新网络的地址与路由配置，不能任意沿用原来的地址。DHCP 就是帮助主机取得这些配置的常用机制。

典型 IPv4 DHCP 可以为主机提供地址、子网掩码、租期，以及默认网关、DNS 服务器等选项。常见的首次分配过程简称 DORA：

```text
Discover → Offer → Request → ACK
发现服务器   提供配置   请求配置   确认租约
```

初次加入时，客户端可能还没有可用地址，可以用 `0.0.0.0` 作为源地址，通过广播寻找服务器。Offer 表示服务器提出一份配置；客户端用 Request 表达选择、请求租约，服务器再用 ACK 确认。**收到 Offer 还不等于已经完成地址分配。**

Lease（租约）是有期限的使用许可。主机需要按协议续租；如果续租失败且租约已经到期，就不能无限期继续占用这个地址。续租或复用已有地址的流程可能不经过完整 DORA，因此“四步过程”是典型首次分配流程，不是每次 DHCP 交互都固定走四步。

存在 DHCP Relay 时，服务器也可以位于其他网段，不必与客户端处在同一条二层链路。DHCP 典型使用 UDP，服务器端口为 67，客户端端口为 68；它属于应用层协议，作用是提供网络配置，并不代替 IP 转发或 ARP。拿到配置也不能单独证明网关、DNS 或外部网络都工作正常。机制见 [RFC 2131](https://www.rfc-editor.org/rfc/rfc2131.html)。

### 7. 服务发现与 ARP 的区别

取得地址、能够发包以后，主机还可能需要知道“这个网络里有哪些打印机或其他服务”。Bonjour、zeroconf 一类机制处理的是这类自动配置与发现需求，其中的服务发现常结合 mDNS 和 DNS-SD；它们不是 ARP 的另一种叫法，也不都使用广播。

| 当前想知道什么 | 对应机制 |
| --- | --- |
| 我应该使用什么地址、掩码和网关？ | DHCP 等配置机制 |
| 这个本地下一跳 IP 对应哪个链路层地址？ | ARP |
| 哪里提供某种服务，应该连接哪个实例和端口？ | DNS-SD 等服务发现机制 |

mDNS 可以在本地链路上通过多播进行类似 DNS 的查询，DNS-SD 则规定如何用 DNS 记录描述和查找服务实例。发现到一台打印机，只说明找到了服务信息；能否使用它，仍由服务本身的身份验证与访问控制决定。协议分别见 [RFC 6762](https://www.rfc-editor.org/rfc/rfc6762.html) 和 [RFC 6763](https://www.rfc-editor.org/rfc/rfc6763.html)。

## 八、Middleboxes：途中设备还能做什么？

Middlebox 指在数据路径上承担普通 IP 转发之外功能的设备或功能。例如，负载均衡器可以把请求分给不同后端，缓存可以减少重复传输，NAT 和防火墙则分别处理地址转换与访问控制。这些功能可以集成在同一台设备里，也可能引入额外状态和兼容性问题。

### 1. NAT / NAPT 怎样让多台设备共享一个公网地址？

私有 IPv4 地址可在不同内部网络重复使用，不能直接作为全球公网的可路由地址。家庭网络常使用 NAPT（Network Address Port Translation，也常称 PAT），把内部地址和端口映射为外部地址和端口。

设两台内部主机都访问示例服务器 `198.51.100.80:443`，网关外部地址为示例 `203.0.113.5`：

| 协议 | 内部源地址与端口 | 转换后的外部源地址与端口 | 远端 |
| --- | --- | --- | --- |
| TCP | `192.168.1.10:50000` | `203.0.113.5:62001` | `198.51.100.80:443` |
| TCP | `192.168.1.11:50000` | `203.0.113.5:62002` | `198.51.100.80:443` |

第一条连接出站时：

```text
转换前：192.168.1.10:50000 → 198.51.100.80:443
转换后：203.0.113.5:62001  → 198.51.100.80:443
```

回复到达网关时：

```text
到达外侧：198.51.100.80:443 → 203.0.113.5:62001
送入内侧：198.51.100.80:443 → 192.168.1.10:50000
```

即使两台内部主机使用相同源端口，也可以借助不同外部端口区分。真实映射和过滤规则还可能参考协议、远端地址和端口，不能把这个示意表当成所有 NAT 的完整状态模型。

外部端口只是映射的一部分，映射结束或过期后可能被重新使用，并不是某台设备永久的身份。TCP/UDP 的端口字段只有 16 位，网关的状态表和资源也有限，因此共享一个公网地址不等于能够建立无限多条映射；实际容量还取决于 NAT 的映射方式与实现。

改写 IPv4 地址时要更新 IPv4 首部校验和；改写地址或 TCP/UDP 端口时，还需按协议规则处理传输层校验和，因为 TCP/UDP 校验的伪首部也包含 IP 地址。基本 NAT、NAPT 和相关限制见 [RFC 3022](https://www.rfc-editor.org/rfc/rfc3022.html)。

UDP 没有 TCP 那样的握手，NAT 仍然可以在看到出站 UDP 报文后建立映射，并用它处理返回报文。映射空闲一段时间后可能超时，应用需要处理映射失效或按需维持它。因此，讨论 NAT 的“连接状态”时，不应据此认为它只支持 TCP、不支持 UDP。UDP 映射与超时的要求见 [RFC 4787](https://www.rfc-editor.org/rfc/rfc4787.html)。

**自测：NAT 与 UDP**

Two hosts both use internal TCP source port 1234 and share one public IP. How can a NAPT distinguish their return traffic? Can it also keep state for UDP without a connection handshake?

:::study-proof[Reference answer: NAT state]{kind="example"}

For example, the NAPT can map the two internal endpoints to different public source ports. It uses the stored mappings, including the transport protocol, to restore the internal destinations of return packets. Depending on the mapping behavior, remote addresses and ports may also matter.

Yes. A UDP mapping can be created when an outbound datagram is observed and maintained with a timeout. A TCP-style handshake is not required to create mapping state.

:::

### 2. NAT 对端到端通信有什么影响？

外部发送方仅知道共享的公网地址时，通常无法凭空确定应该访问内部哪一台设备；缺少匹配映射或允许规则时，新的入站通信往往无法建立。因此可能需要静态端口映射、穿透协商或中继。

如果应用把自身 IP 和端口写进应用数据，单纯改包头也可能不够。NAT 表项还具有生命周期，超时可能使后续包失去原映射。它缓解了地址不足，却增加了连接建立和状态维护的复杂度。

**NAT 本身不等于防火墙。** 地址转换描述如何改写和映射，防火墙描述哪些流量被允许；它们常在同一台家庭网关里实现，但概念和配置职责不同。地址转换本身也不提供加密或身份认证。

### 3. 防火墙与代理有什么不同？

| 功能 | 核心动作 | 例子 |
| --- | --- | --- |
| 普通 IP 转发 | 依据目的 IP 选择下一跳 | 把包交给出口邻居 |
| NAT / NAPT | 改写地址，可能改写端口，维护映射 | 多台主机共享一个外部 IPv4 地址 |
| 防火墙 | 根据规则允许或丢弃流量 | 按地址、端口、协议或连接状态过滤 |
| 应用代理 | 代表客户端与服务器交互，可能终止并新建连接 | HTTP 代理、缓存代理 |

状态防火墙可以跟踪连接：允许符合已建立状态的返回流量，限制未经允许的新连接。是否放行仍取决于实际规则，不是所有设备都默认采用同一策略。

代理可能形成 Client ↔ Proxy 与 Proxy ↔ Server 两段连接；缓存、内容检查能力取决于协议和配置，例如普通 HTTPS 隧道代理不能仅凭转发加密字节就直接读取 HTTP 内容。

Middleboxes 表明，现实互联网的中间设备可能检查传输层甚至应用层，也可能改变通信的地址、状态或连接边界。

## 九、IPv6：哪些设计改变了？

### 1. 地址长度与压缩规则

IPv4 理论地址空间为 $2^{32}\approx4.3\times10^9$，实际可作全球单播分配的空间更少。IPv6 将地址扩展到 128 位：

$$
2^{128}\approx3.4\times10^{38}
$$

地址由 8 组十六进制数构成，每组 16 位：

```text
完整：2001:0db8:0000:0000:0000:ff00:0042:8329
压缩：2001:db8::ff00:42:8329
```

每组的前导零可以省略；连续的全零组可以用 `::` 省略。**同一个地址最多使用一次 `::`**，否则无法唯一恢复省略的组数。`::` 是全零的未指定地址，`::1` 是 IPv6 环回地址；不要与默认路由 `::/0` 混淆。

### 2. 固定 40 B 的基本首部

| 字段 | 位数 | 含义 |
| --- | --- | --- |
| Version | 4 | 值为 6 |
| Traffic Class | 8 | 包括服务分类与拥塞相关标记 |
| Flow Label | 20 | 流标识 |
| Payload Length | 16 | 基本首部之后的长度，包含扩展首部和上层数据 |
| Next Header | 8 | 后面是哪个扩展首部或上层协议 |
| Hop Limit | 8 | 转发跳数限制 |
| Source Address | 128 | 源 IPv6 地址 |
| Destination Address | 128 | 目的 IPv6 地址 |

位数之和为 $320\,\mathrm{bit}=40\,\mathrm{B}$。普通情况下总长度为 $40+\text{Payload Length}$；特殊的超大载荷机制不在本节展开。

IPv4 的 Total Length 包含 IPv4 首部，IPv6 的 Payload Length 不包含 40 B 基本首部，做长度题时不能直接互换。

IPv6 的可选信息通常放在扩展首部里，通过 Next Header 串联，例如：

```text
IPv6 基本首部 → 扩展首部 → TCP 首部 → 应用数据
```

没有扩展首部时，Next Header 可以直接指向 TCP=6、UDP=17 或 ICMPv6=58。首部与分片规则见 [RFC 8200，第 3–5 节](https://www.rfc-editor.org/rfc/rfc8200.html#section-3)。

### 3. IPv4 与 IPv6 对照

| 特征 | IPv4 | IPv6 |
| --- | --- | --- |
| 地址长度 | 32 bit | 128 bit |
| 基本首部 | 通常 20 B，含选项时可变 | 固定 40 B，扩展首部另计 |
| 跳数限制 | TTL | Hop Limit |
| IP 首部校验和 | 有 | 无 |
| 长度字段 | Total Length，含首部 | Payload Length，不含基本首部 |
| 路由器分片 | DF=0 时可以 | 不允许 |
| 地址解析 | ARP | ICMPv6 Neighbor Discovery |
| 广播 | 有 | 无广播，使用多播等机制 |
| 前缀与查表 | CIDR、最长前缀匹配 | 仍使用前缀与最长前缀匹配 |

课件 p.71 的首部图使用了旧式的 `Pri / Priority` 标注；学习现行 IPv6 时，应以上表的 8 位 Traffic Class 和 20 位 Flow Label 为准。页上的“No options”也不是说 IPv6 失去了可选信息，而是基本首部里不再有 IPv4 那样的可变 Options 区，相关信息由扩展首部承载。

IPv6 去掉 IP 首部校验和，路由器改变 Hop Limit 后就不必更新这个字段；这不意味着网络不再需要差错检测，链路层与传输层仍承担相应职责。

### 4. IPv6 包太大时怎么办？

IPv6 路由器不能中途分片。若包超过出口 MTU，路由器丢弃并通常发送 **ICMPv6 Packet Too Big（Type=2, Code=0）**，源端据此调整大小。如需 IPv6 分片，由源节点添加 Fragment 扩展首部并执行，目的节点重组。

所以“IPv6 没有路由器分片”不等于“IPv6 完全没有分片”。IPv6 要求链路能提供至少 1280 B 的 MTU 能力；底层若无法直接承载，要在 IPv6 之下提供必要适配。

课件 p.71 将这一项简写为“No fragmentation/reassembly”，阅读时应结合处理节点区分：中间路由器不分片，源节点仍可分片，目的节点仍可重组。

### 5. Neighbor Discovery 与自动配置

IPv6 不使用 ARP。Neighbor Discovery（ND）基于 ICMPv6，承担邻居链路层地址解析、邻居可达性检测和路由器发现等任务：

| 消息 | 用途 |
| --- | --- |
| Neighbor Solicitation / Advertisement（NS / NA） | 邻居地址解析、可达性相关处理等 |
| Router Solicitation / Advertisement（RS / RA） | 请求与通告路由器、前缀等信息 |

地址解析请求通常利用目标相关的多播，不是照搬 IPv4 ARP 广播。主机可结合 RA 中的前缀信息与 SLAAC 生成地址，并进行重复地址检测；也可以根据网络配置使用 DHCPv6。

**IPv6 默认路由器通常通过 RA 发现，不由 DHCPv6 分配默认网关。** ND 和 SLAAC 相关机制分别见 [RFC 4861](https://www.rfc-editor.org/rfc/rfc4861.html) 与 [RFC 4862](https://www.rfc-editor.org/rfc/rfc4862.html)。

### 6. 核心转发思想仍然成立

例如转发表：

```text
2001:db8:1::/48    → A
2001:db8:1:2::/64  → B
::/0              → D
```

目的地址 `2001:db8:1:2::1234` 同时匹配三个前缀，选择最具体的 `/64`，交给 B。地址长度变了，但“目的地址 → 最长前缀匹配 → 下一跳 → 链路交付”的思路保留。

### 7. IPv4 与 IPv6 怎样共存？

| 方法 | 思路 |
| --- | --- |
| Dual Stack（双栈） | 同一设备同时支持 IPv4 与 IPv6，按目标与网络条件选择 |
| Tunneling（隧道） | 把一种网络层数据报放在另一种协议的载荷里跨越中间网络 |
| Translation（转换） | 在特定边界转换协议，例如 NAT64 连接部分 IPv6 与 IPv4 通信场景 |

NAT64 的具体能力与限制见 [RFC 6146](https://www.rfc-editor.org/rfc/rfc6146.html)。IPv6 地址空间扩大，并不自动提高应用速度或保证通信安全，也不保证访问不受防火墙限制；实际效果仍取决于路径、实现和策略。

课件 p.70 的采用率图标注日期为 2013 年 1 月 30 日，只能用于理解当时的部署背景，不能当作当前 IPv6 使用比例。

### 8. 隧道里的内层包与外层包

课件 pp.72–73 的例子是：两段支持 IPv6 的网络，中间隔着只按 IPv4 转发的网络。可以让入口 B 把一个完整的 IPv6 包装进 IPv4 包，交给中间网络；出口 E 收到后去掉外层 IPv4 封装，再继续处理里面的 IPv6 包。

```text
IPv6 段：A → B（隧道入口）
IPv4 段：B ⇒ … ⇒ E（隧道出口）
IPv6 段：E → F

外层 IPv4 包
├─ IPv4 首部：B → E
└─ 内层 IPv6 包
   ├─ IPv6 首部：A → F
   └─ 上层数据
```

这里的 A、F 表示内层通信端点，B、E 表示隧道端点，实际需要填写相应接口的地址。中间 IPv4 路由器按**外层目的 IPv4 地址**选择下一跳，不需要为内层 IPv6 目的地址提供原生 IPv6 路由；出口解封装后，才继续按内层目的地址转发。

这与 NAT64 的协议转换不同：隧道保留内层 IPv6 包，在外面再加一层承载；转换则改变网络层协议与地址表示。从 IPv6 的角度，整个隧道可以作为一条链路使用，背后却可能经过多台 IPv4 路由器。相关机制见 [RFC 4213](https://www.rfc-editor.org/rfc/rfc4213.html)。

多出来的首部会占用底层链路的 MTU。若底层路径 MTU 为 1500 B，隧道只增加 20 B 外层 IPv4 首部，则为避免外层分片，完整内层包最多为：

$$
L_{\text{inner,max}}=1500-20=1480\,\mathrm{B}
$$

**1480 B 包括内层 IPv6 首部，不是应用数据长度。** 若还存在其他封装，要继续扣除额外首部；若后续路径的 MTU 更小，也要相应下调。这就是为什么增加隧道后，原先能通过的大包可能需要重新调整大小。

**自测：隧道封装后的长度**

An IPv6-in-IPv4 tunnel adds only a 20-byte outer IPv4 header over a path with MTU 1500 bytes. What is the largest complete inner IPv6 packet that fits without outer fragmentation? If it contains only a 40-byte IPv6 header and a 20-byte TCP header, how much TCP data fits?

:::study-proof[Reference answer: Tunnel overhead]{kind="example"}

The complete inner IPv6 packet can be at most $1500-20=1480$ bytes. With no IPv6 extension headers or TCP options, the maximum TCP data length is $1480-40-20=1420$ bytes. The outer IP header, inner IP header, and transport header all consume space, but at different encapsulation levels.

:::

## 十、把整章串起来：访问服务器时发生了什么？

假设电脑配置为：

```text
接口：        192.168.1.10/24
默认网关：    192.168.1.1
网关外部地址：203.0.113.5（示例）
服务器地址：  198.51.100.80（示例）
```

下面以普通 TCP 应用为例。DNS 查询本身也要使用网络；这里从“应用已经得到服务器地址”之后开始追踪业务包。

1. **准备传输层报文。** TCP 为连接建立或数据传输构造报文段。应用写入的数据不一定一整块对应一个 IP 包，TCP 会按发送条件组织数据。
2. **选择源地址和路由。** 本机按服务器目的地址查表，发现没有更具体的匹配，使用默认网关，并据所用接口等条件选择源地址。
3. **生成 IPv4 数据报。** 源 IP 为 `192.168.1.10`，目的 IP 为 `198.51.100.80`，Protocol=6，填写 TTL、长度、校验和等信息，并遵守已知 MTU 限制。
4. **交付本地网关。** 查询或解析 `192.168.1.1` 的 MAC，封装以太网帧。帧的目的 MAC 属于网关，而 IP 的目的地址仍为服务器。
5. **网关转发并进行 NAPT。** 网关检查并查表，减少 TTL，可能将源地址与端口改写为 `203.0.113.5:62001` 等映射，再封装出口链路帧。
6. **经过后续路由器。** 每台路由器根据自己的转发表选择下一跳，消耗 TTL，处理出口 MTU，并完成相应链路交付。未遇到其他地址转换时，网关转换后的 IP 地址保持不变。
7. **处理可能的错误。** 无路由、TTL 耗尽或包太大等情况可能触发 ICMP；队列丢包和反馈丢失等情况也可能没有可见报告。
8. **服务器接收并分用。** 服务器确认数据报交给本机；若存在分片先重组，再按 Protocol 交给 TCP。TCP 继续处理连接状态、校验、顺序与应用交付。
9. **回复沿返回路径传输。** 服务器发给外部地址和映射端口；经过 NAT 网关时恢复内部目的地址与端口，再交给内部主机。返回路径不一定与去程完全相同。

DNS、ARP 和 NAT 映射都有缓存或状态生命周期，并不是每发一个包都要重新查询和建表。TCP 的连接建立也不是每个数据包都重复一次。

:::study-note[三个必须能说清的区别]{kind="abstract"}

**Routing 与 Forwarding：** 路由形成可达性和选路信息，转发按已有信息处理当前数据报。

**目的 IP 与下一跳 IP：** 目的 IP 标识最终网络层目的地；下一跳 IP 标识当前链路先交给谁。

**端到端 IP 交付与逐跳帧交付：** IP 提供跨网络寻址和数据报转发；每一段链路用相应的链路层机制完成实际交付。

:::

## 十一、复习清单与综合自测

### 1. 应该掌握到什么程度？

| 知识点 | 自己能完成的任务 |
| --- | --- |
| IPv4 首部 | 说明 IHL、Total Length、TTL、Protocol、Checksum 和分片字段的作用与单位 |
| CIDR 与子网 | 计算掩码、网络地址、广播地址、地址范围，并说明减 2 的条件 |
| 最长前缀匹配 | 找出全部匹配项，再选择最长者；识别默认路由和无路由情况 |
| 分片 | 先扣首部，再做 8 B 对齐，计算长度、Offset、MF 并复核 |
| PMTUD | 解释 DF、ICMP Type=3 Code=4、路径 MTU 和黑洞现象 |
| ICMP 诊断 | 说明 ping 与 traceroute 的机制和观察边界 |
| IP 与链路层 | 说清路由查找、ARP 对象、重封装和逐跳地址变化，区分 DHCP 配置与服务发现 |
| Middleboxes | 画出 NAPT 双向映射，解释 UDP 映射与超时，区分转换、过滤与代理 |
| IPv6 | 比较地址、长度字段、首部、分片、ND、RA 和最长前缀匹配，计算隧道开销 |

### 2. 题目 A：独立计算一个子网

给定 `192.168.10.77/26`，求掩码、网络地址、广播地址和常规可分配范围。`192.168.10.130` 是否在同一个 `/26` 子网？

:::study-proof[展开答案：子网计算]{kind="example"}

`/26` 掩码为 `255.255.255.192`，每块包含 $2^6=64$ 个地址，最后一字节的块起点为 0、64、128、192。

77 位于 64–127，因此网络地址是 `192.168.10.64`，广播地址是 `192.168.10.127`，常规可分配范围是 `192.168.10.65`–`192.168.10.126`，共 62 个地址。

130 位于 128–191，属于 `192.168.10.128/26`，与前者不同。不能只看前面三个十进制数相同，就断定处在同一子网。

:::

### 3. 题目 B：给远端发包，到底 ARP 谁？

A 为 `192.168.1.10/24`，默认网关为 `192.168.1.1`，没有其他相关路由；目的为 `10.0.0.20`。第一次发送时无可用 ARP 缓存。写出 ARP 查询对象、第一帧的目的 MAC、IP 首部中的目的地址。

:::study-proof[展开答案：先选下一跳]{kind="example"}

ARP 查询对象为网关 IP `192.168.1.1`；第一帧的目的 MAC 为网关在本链路上的 MAC；IP 首部中的目的地址仍为 `10.0.0.20`。

先执行路由选择，才知道 ARP 应该解析谁。A 既不把 IP 目的地址改成网关，也不在本地广播查询远端 B 的 MAC。

:::

### 4. 题目 C：最后一片的 Offset=0 吗？

某 IPv4 分片满足 `MF=0`、`Fragment Offset=370`。它是未分片报文吗？原始数据中它从哪个字节开始？

:::study-proof[展开答案：MF 与 Offset 要一起看]{kind="example"}

它是最后一个分片，不是一个完整的未分片数据报。它承载的数据从原始 IP Payload 的第 $370\times8=2960$ 个字节偏移处开始（从 0 起算）。

`MF=0` 只表示后面没有更多分片；只有再结合 Offset，才知道它是否从原始数据起点开始。

:::

### 5. 题目 D：TTL 与 traceroute

路径为 A → R1 → R2 → B，探测包初始 TTL=2。谁通常返回哪类 ICMP？输出中这一跳的 RTT 是否等于 R1→R2 的链路延迟？

:::study-proof[展开答案：第二台路由器耗尽预算]{kind="example"}

R1 将 TTL 从 2 减为 1，R2 无法继续转发，通常向 A 返回 ICMP Time Exceeded，Type=11、Code=0。

这一跳的 RTT 包含 A 到 R2 以及回复回 A 的传输、排队和处理时间，不能当成 R1→R2 的单独延迟。

:::

### 6. 题目 E：IPv6 是否完全取消了分片？

一个 IPv6 包大于下一段链路的 MTU，路由器会怎样处理？还能由谁分片？

:::study-proof[展开答案：路由器不分片，源节点可以分片]{kind="example"}

路由器丢弃过大的包，通常返回 ICMPv6 Packet Too Big。源端可以调整后续包大小；如果使用 IPv6 分片，应由源节点添加 Fragment 扩展首部执行，目的节点重组。

IPv6 取消的是中间路由器分片，不是所有分片能力。

:::

### 7. 题目 F：NAT 的返回方向

已存在 TCP 映射 `192.168.1.10:50000 ↔ 203.0.113.5:62001`。服务器回复的目的为 `203.0.113.5:62001`，通过网关后目的应变为什么？这是否证明 NAT 和防火墙是同一个功能？

:::study-proof[展开答案：反向恢复内部目的]{kind="example"}

在符合映射与放行条件时，网关把目的恢复为 `192.168.1.10:50000`。这个动作体现地址和端口转换；是否允许这个包通过由相关过滤规则决定，不能据此把 NAT 等同于防火墙。

:::

## 参考与阅读顺序

课程资料为 `lec4-mod3net_agent_networks.pdf` 的 IP 实现部分。正文中标明页码的地方对应原课件；计算推导、自测和协议细节另作补充。课件 p.48 的前缀例子、p.55 的 ICMP 引用格式、p.71 的 IPv6 简写已在对应章节说明，阅读时以重新计算的结果和协议定义为准。

首次学习可以顺着正文读，复习时先独立完成折叠题，再按需查对应协议原文。示例中的 `198.51.100.0/24`、`203.0.113.0/24` 与 `2001:db8::/32` 为文档地址，用于说明机制。

| 想核对的内容 | 原始资料 |
| --- | --- |
| IPv4 首部、分片与重组 | [RFC 791](https://www.rfc-editor.org/rfc/rfc791.html) |
| DSCP 与 ECN | [RFC 2474](https://www.rfc-editor.org/rfc/rfc2474.html)、[RFC 3168](https://www.rfc-editor.org/rfc/rfc3168.html) |
| IPv4 路由器转发与 ICMP 约束 | [RFC 1812](https://www.rfc-editor.org/rfc/rfc1812.html) |
| CIDR 与路由聚合 | [RFC 4632](https://www.rfc-editor.org/rfc/rfc4632.html) |
| ICMP 消息与经典 IPv4 PMTUD | [RFC 792](https://www.rfc-editor.org/rfc/rfc792.html)、[RFC 1191](https://www.rfc-editor.org/rfc/rfc1191.html) |
| Source Quench 的弃用 | [RFC 6633](https://www.rfc-editor.org/rfc/rfc6633.html) |
| PLPMTUD 与数据报传输的扩展 | [RFC 4821](https://www.rfc-editor.org/rfc/rfc4821.html)、[RFC 8899](https://www.rfc-editor.org/rfc/rfc8899.html) |
| ARP 与 DHCP | [RFC 826](https://www.rfc-editor.org/rfc/rfc826.html)、[RFC 2131](https://www.rfc-editor.org/rfc/rfc2131.html) |
| mDNS 与 DNS-SD | [RFC 6762](https://www.rfc-editor.org/rfc/rfc6762.html)、[RFC 6763](https://www.rfc-editor.org/rfc/rfc6763.html) |
| NAT / NAPT 与 UDP 映射 | [RFC 3022](https://www.rfc-editor.org/rfc/rfc3022.html)、[RFC 4787](https://www.rfc-editor.org/rfc/rfc4787.html) |
| IPv6 基本协议、ND 与 SLAAC | [RFC 8200](https://www.rfc-editor.org/rfc/rfc8200.html)、[RFC 4861](https://www.rfc-editor.org/rfc/rfc4861.html)、[RFC 4862](https://www.rfc-editor.org/rfc/rfc4862.html) |
| IPv6 与 IPv4 转换的一个例子 | [RFC 6146](https://www.rfc-editor.org/rfc/rfc6146.html) |
| 双栈与 IPv6-in-IPv4 隧道 | [RFC 4213](https://www.rfc-editor.org/rfc/rfc4213.html) |
