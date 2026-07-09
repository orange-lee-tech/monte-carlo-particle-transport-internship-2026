# 计算文件包运行记录

更新时间：2026-07-09

## 1. 文件包定位

该计算文件包由课题组/师姐提供，用于延续已有 Ansys 热工流体与热结构计算工作。

当前目标不是立即修改模型，而是：

```text
先打开 → 看懂项目结构 → 跑通/读取已有结果 → 记录设置 → 再考虑修改参数
```

## 2. 文件包基本信息

| 项目 | 内容 |
|---|---|
| 文件包名称 | 初步识别为 `32kw_files` / `dssmx_files` 相关 Workbench 文件包 |
| 来源 | 课题组/师姐提供 |
| 软件平台 | Ansys Workbench 2021 / Fluent 2021 |
| 重点模块 | Fluent + Mechanical |
| 可能涉及模块 | Meshing / Geometry / Static Structural / Fluent |
| 当前状态 | 已打开 Workbench；B 系统 Mechanical 结果可读；A 系统 Fluent case/data 主体可读 |
| 当前目标 | 先识别 Fluent—Mechanical 数据传递关系，再追溯 Fluent 设置与论文工况 |

## 3. 首次打开检查清单

- [x] 文件包能否正常解压或打开。
- [x] Workbench 项目能否加载。
- [x] 是否缺失路径、几何文件、网格文件或结果文件：已发现旧路径引用问题，但 case/data 文件本体存在。
- [x] 是否提示版本不兼容或 journal 读取异常：Fluent 读取时出现 `/Report/RunInformationSettings` 相关 journal 警告。
- [x] 是否包含 Fluent 模块。
- [x] 是否包含 Mechanical 模块。
- [x] 是否包含网格模块。
- [x] 是否已有计算结果。
- [ ] 是否需要重新计算。

说明：截至 2026-07-09 上午，B 系统 `Static Structural` 的结果可以正常打开；C 系统存在问号 / 闪电状态，暂未作为优先检查对象。A 系统 Fluent 可展开主要设置树，journal 报错暂判断为报告/运行信息恢复失败，不是 case/data 主体读取失败。

## 4. Workbench 项目结构记录

| 模块 / 系统 | 是否存在 | 作用判断 | 备注 |
|---|---|---|---|
| A: Fluid Flow (Fluent) | 是 | 流体与换热计算源头 | 已进入 Fluent 检查基础设置 |
| B: Static Structural | 是 | 热结构分析 | 已读取结果；接收 A3 导入温度载荷 |
| C: Static Structural | 是 | 可能为另一结构分支或待更新工况 | 存在问号 / 闪电，暂不优先处理 |
| Geometry | 是 | 几何建模或导入 | B 系统可正常显示几何 |
| Mesh / Meshing | 是 | 网格划分 | B 系统含 Body Sizing、Face Sizing 等局部网格控制 |
| Results | 是 | 后处理结果 | B 系统已有等效应力和总变形结果 |

## 5. Mechanical 设置与结果记录

### 5.1 B: Static Structural 树结构

```text
Model (B4)
- Geometry
- Materials
  - Structural Steel
- Coordinate Systems
  - Global Coordinate System
- Connections
  - Contacts
- Mesh
  - Body Sizing
  - Body Sizing 2
  - Face Sizing
  - Body Sizing 3
- Static Structural (B5)
  - Analysis Settings
  - Standard Earth Gravity
  - Fixed Support
  - Imported Load (A3)
    - Imported Body Temperature
    - Imported Body Temperature 2
    - Imported Body Temperature 3
  - Solution (B6)
    - Solution Information
    - Equivalent Stress
    - Total Deformation
```

### 5.2 结构结果

| 结果项 | 类型 | 单位 | 时间 | 最大值 | 最小值 | 备注 |
|---|---|---:|---:|---:|---:|---|
| Equivalent Stress | 等效 / Von-Mises 应力 | MPa | 1 s | 126.82 | 0.0016847 | 高应力主要集中在前端外缘或局部结构过渡区域附近 |
| Total Deformation | 总变形 | mm | 1 s | 0.17117 | 0 | 最大变形出现在前端局部区域，约束附近变形较小 |

## 6. Imported Load 温度载荷记录

B 系统中的 `Imported Load (A3)` 已确认包含 3 个导入体温度载荷，来源为 Fluent 计算结果文件：

```text
D:\zzq\32kw_files\dp0\FFF-2\Fluent\SYS-1.1 (1).dat
```

### 6.1 Imported Body Temperature

| 项目 | 数值 |
|---|---:|
| CFD 平均温度 | 54.578 ℃ |
| CFD 最高温度 | 73.146 ℃ |
| CFD 最低温度 | 42.611 ℃ |
| Mechanical 映射后平均温度 | 54.575 ℃ |
| 节点映射比例 | 100% |

### 6.2 Imported Body Temperature 2

| 项目 | 数值 |
|---|---:|
| CFD 平均温度 | 26.95 ℃ |
| CFD 最高温度 | 53.95 ℃ |
| CFD 最低温度 | 20.009 ℃ |
| Mechanical 映射后平均温度 | 26.913 ℃ |
| 节点映射比例 | 100% |
| 云图色标范围 | 20.009 ℃ 至 53.355 ℃ |

### 6.3 Imported Body Temperature 3

| 项目 | 数值 |
|---|---:|
| CFD 平均温度 | 51.824 ℃ |
| CFD 最高温度 | 131.01 ℃ |
| CFD 最低温度 | 35.807 ℃ |
| Mechanical 映射后平均温度 | 59.124 ℃ |
| 节点映射比例 | 99.9949% |
| 未映射节点处理 | 剩余节点被设置为平均温度 |
| 云图色标范围 | 约 35.86 ℃ 至 130.99 ℃ |

### 6.4 当前判断

- B 系统结构分析接收的是温度载荷，不是目前已观察到的压力载荷。
- `Imported Body Temperature 3` 的最高温度约为 131 ℃，明显高于另外两个温度载荷，后续应优先判断其是否对应论文中的束流热沉积主工况或高温区域。
- `Imported Body Temperature 2` 最高温度约 54 ℃，最低接近 20 ℃，可能与冷却水或低温区域有关，但需结合 Fluent 边界条件确认。
- 3 个导入体温度载荷可能对应不同部件、不同区域或不同数据映射对象，暂不能直接等同于 3 个工况。

## 7. Fluent 设置记录

### 7.1 文件读取情况

尝试从 Workbench / Fluent 读取已有 `case/data` 时，曾出现如下 journal 警告：

```text
Warning: An error or interrupt occurred while reading the journal file.
Some commands may not have been completed.

Error: state/object/set-state:Rules not found for object type path: /Report/RunInformationSettings
Error Object: ()
```

当前判断：该问题更像是 Fluent 恢复报告/运行信息设置时的 journal 兼容或旧环境残留问题；由于 Fluent 设置树、边界条件、材料、cell zone 和结果项可以展开，暂不认为其阻断 case/data 主体读取。

### 7.2 General / Models

| 项目 | 内容 |
|---|---|
| 求解器类型 | Pressure-Based |
| 速度形式 | Absolute |
| 时间类型 | Steady |
| 重力 | On；X=0，Y=-9.81 m/s²，Z=0 |
| 多相模型 | Off |
| 能量方程 | On |
| 湍流模型 | Realizable k-epsilon，Scalable Wall Function |
| 辐射模型 | Off |
| Heat Exchanger | Off |
| Species | Off |
| Discrete Phase | Off |
| Solidification & Melting | Off |

当前判断：该 Fluent 案例不是 VOF 两相瞬态模型，而是单相流动换热 + 固体导热 + 流固界面传热的稳态热工计算。

### 7.3 Materials

| 类型 | 材料 |
|---|---|
| Fluid | `air`、`water-liquid` |
| Solid | `aluminum`、`copper`、`steel` |

### 7.4 Boundary Conditions

| 边界 | 类型 | 关键设置 |
|---|---|---|
| inlet | velocity-inlet | 速度 9 m/s；入口温度 20 ℃；湍流强度 3.76%；水力直径 12 mm；初始表压 0 Pa |
| outlet | outflow | Flow Rate Weighting = 1 |
| interface | 多个 interface / mesh interface | 用于不同区域之间数据传递或流固/固固接触换热 |
| wall | 存在 | 详细壁面设置待继续检查 |

该入口设置与论文第 4 章中“冷却水流速 9 m/s、入口温度 20 ℃”的边界条件相对应，当前文件很可能对应论文流速为 9 m/s 的热分析工况。

### 7.5 Cell Zone Conditions

| Zone | Type | Material | Source Terms | 当前判断 |
|---|---|---|---|---|
| fluid | fluid | 待细查，预计为 water-liquid | 待确认 | 冷却水流体区域 |
| solid | solid | steel | 未勾选 | 结构/冷却管或支撑相关固体区域 |
| source | solid | copper | 已勾选 | 铜准直器主体或主要受热区 |
| pbk | solid | aluminum | 未勾选 | 可能为屏蔽块/辅助结构，需结合几何命名确认 |

### 7.6 热源项记录

`source` 区域中已确认存在一个能量源项：

| 项目 | 内容 |
|---|---|
| Cell Zone | `source` |
| Type | solid |
| Material | copper |
| Number of Energy sources | 1 |
| 能量源项单位 | W/m³ |
| Energy source | `udf ENERGY_FLUH::libudf1` |

当前判断：该热源不是简单常数，而是通过 UDF 加载的体积热源，命名为 `ENERGY_FLUH`，库名为 `libudf1`。这与论文中“FLUKA 模拟得到接近实际工况的功率密度分布作为热源，通过 UDF 编译后导入 ANSYS / Fluent 计算温度及热应力”的方法链条高度对应。

## 8. 第一次运行记录

| 项目 | 内容 |
|---|---|
| 运行日期 | 待填写 |
| 是否成功运行 | 待填写 |
| 运行耗时 | 待填写 |
| 是否收敛 | 待填写 |
| 报错信息 | 读取已有 case/data 时出现 `/Report/RunInformationSettings` journal 警告；暂未重新计算 |
| 解决方法 | 不立即重算；先读取已有设置和结果；必要时单独用 Fluent 先读 case 再读 data |
| 输出结果位置 | 待填写 |

说明：2026-07-09 当前操作为读取已有结果和检查项目结构，尚未重新计算。

## 9. 结果记录

| 结果项 | 数值/现象 | 备注 |
|---|---|---|
| 最高温度 | 131.01 ℃ | 来自 `Imported Body Temperature 3` 的 CFD 结果摘要 |
| 最低温度 | 20.009 ℃ | 来自 `Imported Body Temperature 2` 的 CFD 结果摘要 |
| 最大等效应力 | 126.82 MPa | B: Static Structural / Equivalent Stress |
| 最大总变形 | 0.17117 mm | B: Static Structural / Total Deformation |
| 入口速度 | 9 m/s | Fluent `velocity-inlet` |
| 入口温度 | 20 ℃ | Fluent `velocity-inlet` Thermal |
| 热源类型 | UDF 体积热源，`udf ENERGY_FLUH::libudf1` | Fluent `source` cell zone |
| 最大速度 | 待填写 | 需进入 Fluent 后处理查看 |
| 最大压力 | 待填写 | 需进入 Fluent 后处理查看 |
| 压降 | 待填写 | 需进入 Fluent 查看入口 / 出口数据 |
| 关键壁面热流 | 待填写 | 需进入 Fluent 查看壁面条件或后处理 |
| 残差变化 | 待填写 | 需进入 Fluent 查看计算监视器 |

## 10. 后续问题清单

- 这个文件包对应论文中的哪个模型或工况？当前优先判断为 9 m/s 冷却水热分析工况。
- 3 个 `Imported Body Temperature` 分别对应哪些结构区域、部件或载荷对象？
- UDF `ENERGY_FLUH` 的源码、输入数据或 FLUKA 功率密度文件位于何处？
- 冷却水出口温度、入口/出口压力以及压降分别是多少？
- Fluent 中壁面和 interface 是否全部设置为合理的 coupled / interface 换热关系？
- Fluent 到 Mechanical 的温度映射是否需要检查插值误差或未映射节点？
- 是否需要做不同流速对比？
- 当前计算目标是复现、验证，还是在已有模型上改工况？
