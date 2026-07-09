# 阶段交接：Ansys 复现通过后转入热工设计

日期：2026-07-09

## 1. 当前阶段状态

本阶段任务已通过老师验收。

阶段成果可以概括为：

```text
已基本掌握 Ansys Workbench / Fluent / Mechanical 文件包的读取、设置识别、已有结果核对，以及 UDF 热源修复后的短迭代复现流程。
```

后续工作不再继续沿当前师姐算例长时间迭代，而是转入老师新安排的热工设计、文献阅读和热应力计算任务。

## 2. 已完成的关键工作

### 2.1 Workbench / Mechanical 链路识别

- 成功打开师姐 Ansys Workbench 文件包。
- 识别到项目包含：
  - A: Fluid Flow (Fluent)
  - B: Static Structural
  - C: Static Structural 或其他结构分支
- B 系统 Mechanical 接收 A 系统 Fluent 的温度场，形成热结构计算链路。
- Mechanical 中确认结构结果：
  - 最大等效应力：126.82 MPa
  - 最大总变形：0.17117 mm

### 2.2 Fluent 设置识别

确认 Fluent 主要设置：

| 项目 | 内容 |
|---|---|
| Solver | Pressure-Based |
| Time | Steady |
| Energy | On |
| Turbulence | Realizable k-epsilon，Scalable Wall Function |
| Multiphase | Off |
| Radiation | Off |
| Fluid | water-liquid |
| Inlet | 9 m/s，20 ℃ |
| Outlet | outflow |
| Heat source zone | `source`，solid，copper，UDF 体积热源 |

### 2.3 原始结果核对

读取已有 case/data 后，核对结果：

| 项目 | 数值 |
|---|---:|
| source 最大温度 | 131.02633 ℃ |
| source 最低温度 | 35.76516 ℃ |
| source 平均温度 | 61.03741 ℃ |
| source 体积 | 0.006997188 m³ |
| fluid 最高温度 | 23.93453 ℃ |
| fluid 平均温度 | 20.57065 ℃ |
| 入口质量流量 | 7.966878 kg/s |
| 出口质量流量 | -7.966878 kg/s |
| 入口温度 | 19.99999 ℃ |
| 出口温度 | 20.97516 ℃ |
| 冷却水温升 | 0.97517 ℃ |
| 冷却水带走热量 | 约 32.48 kW |
| 压降 | 约 83.79 kPa |

该结果与 32 kW、9 m/s 正常工况高度吻合。

### 2.4 UDF 问题定位与修复

曾出现：

```text
Error: chip-exec: function "ENERGY_PIAN::libudf1" not found.
```

控制台提示原始 UDF 路径可能为：

```text
/LustreData5/home/shuaiwenwen/sww/heat_source_matrix_32.c
```

师姐补充文件：

```text
heat_source_matrix_0_1e6.c
pro.inp
```

将文件放入 Fluent 工作目录并启用 UDF 编译环境后，Fluent 成功加载：

```text
Found "libudf1" library
Opening library ...
ENERGY_PIAN
Done.
```

补齐后进行 10 步短迭代，控制台无 UDF 报错，`source` 最大温度为：

```text
132.40909 ℃
```

说明当前本机已能继续运行该 Fluent 算例。

## 3. 阶段性结论

可对外表述为：

```text
已完成师姐 Fluent-Mechanical 文件包的读取、关键参数识别、已有结果核对，并在补齐 UDF 源码/输入文件后完成短迭代复现。
```

不建议表述为：

```text
已经完整复现全部论文数据。
```

原因：完整复现还应包括长步数收敛、重新导入 Mechanical 并复核应力/变形、不同工况结果对比等。但本阶段老师要求的“学会使用 Ansys 并跑通师姐内容”的目标已经达到。

## 4. 老师后续新要求

老师后续安排已经转向更明确的设计任务：

> 做缪子束流踢坏区 / 高功率准直吸收结构的热工设计。

物理背景：

- 打靶后会产生部分不干净或偏离要求的缪子束流。
- 这些坏区束流需要通过人工校正和准直/吸收结构剔除。
- 该结构吸收坏掉的缪子束流时，因能量沉积、动量变化等原因形成热源。
- 当前主要任务是对这个吸收/准直板块进行热工设计。

设计约束：

| 约束 | 内容 |
|---|---|
| 功能约束 | 满足剔除坏区束流要求 |
| 材料 | 铜为主 |
| 温度限制 | 老师明确要求铜结构温度不能超过 300 ℃ |
| 结构限制 | 热应力和热变形需要控制在合理范围内 |
| 设计目标 | 探索更优散热结构 |

## 5. 新阶段建议路线

### 5.1 第一阶段：知识补课与文献阅读

优先阅读：

- 高功率准直器 / beam collimator cooling design
- muon target / beam dump / absorber thermal design
- 铜结构水冷设计
- 热沉积到体热源的转换方法
- 稳态热应力与热膨胀约束分析

### 5.2 第二阶段：热工基础计算

重点掌握：

- 导热方程
- 对流换热边界
- 水冷通道换热
- 热阻网络
- 最高温度估算
- `Q = m_dot * cp * ΔT` 水侧能量闭合

### 5.3 第三阶段：热应力计算

重点掌握：

- 温度场到热应力的来源
- 线膨胀系数
- 固定约束与热膨胀受限
- Von-Mises 应力
- 铜材料屈服强度与安全裕量

### 5.4 第四阶段：结构方案比较

可比较方向：

- 冷却水入口速度
- 冷却通道直径 / 数量 / 布置
- 铜块厚度和受热区形状
- 是否分段
- 是否开膨胀缝
- 是否采用外套管/蛇形管冷却
- 流阻、温升、最高温度、最大应力的综合权衡

## 6. 后续对话启动提示词

新对话可以从以下提示开始：

```text
我们已经完成师姐 Ansys Fluent-Mechanical 文件包的阶段性复现。当前新任务是围绕缪子束流踢坏区 / 高功率准直吸收结构做热工设计：铜材料温度不能超过 300 ℃，需要满足剔除坏区束流要求，同时控制热应力和热变形。请按文献阅读、热工基础、热应力计算和结构方案优化四条线，带我开始下一阶段学习和调研。
```

## 7. 仓库记录位置

相关记录主要位于：

```text
00-admin/current-task.md
00-admin/stage-handoff-2026-07-09.md
06-cases/ansys-cases/fluent-2026-07-09-settings.md
06-cases/ansys-cases/package-run-record.md
01-daily-log/2026-07-09.md
```
