# Fluent 设置初查记录（2026-07-09）

## 1. 对象

师姐 Ansys Workbench 文件包中的 A 系统 `Fluid Flow (Fluent)`。

当前操作目标：读取已有 case/data，检查模型设置，不重新计算。

## 2. 读取情况

Fluent 读取已有文件时，出现过 journal 警告：

```text
Warning: An error or interrupt occurred while reading the journal file.
Some commands may not have been completed.

Error: state/object/set-state:Rules not found for object type path: /Report/RunInformationSettings
Error Object: ()
```

当前判断：该问题更像是 Fluent 恢复报告/运行信息设置时的 journal 兼容或旧环境残留问题。由于 Fluent 设置树、边界条件、材料、cell zone 和结果项均可展开，暂不认为其阻断 case/data 主体读取。

## 3. General / Models

| 项目 | 内容 |
|---|---|
| Solver Type | Pressure-Based |
| Velocity Formulation | Absolute |
| Time | Steady |
| Gravity | On；X=0，Y=-9.81 m/s²，Z=0 |
| Multiphase | Off |
| Energy | On |
| Viscous | Realizable k-epsilon，Scalable Wall Function |
| Radiation | Off |
| Heat Exchanger | Off |
| Species | Off |
| Discrete Phase | Off |
| Solidification & Melting | Off |

当前判断：该 Fluent 案例不是 VOF 两相瞬态模型，而是稳态单相冷却换热 + 固体导热 + 流固界面传热模型。

## 4. Materials

| 类型 | 材料 |
|---|---|
| Fluid | `air`、`water-liquid` |
| Solid | `aluminum`、`copper`、`steel` |

## 5. Boundary Conditions

| 边界 | 类型 | 关键设置 |
|---|---|---|
| inlet | velocity-inlet | 速度 9 m/s；入口温度 20 ℃；湍流强度 3.76%；水力直径 12 mm；初始表压 0 Pa |
| outlet | outflow | Flow Rate Weighting = 1 |
| interface | 多个 interface / mesh interface | 用于不同区域之间数据传递或流固/固固接触换热 |
| wall | 存在 | 详细壁面设置待继续检查 |

## 6. Cell Zone Conditions

| Zone | Type | Material | Source Terms | 当前判断 |
|---|---|---|---|---|
| fluid | fluid | water-liquid | 待确认是否存在其他附加设置 | 冷却水流体区域 |
| solid | solid | steel | 未勾选 | 结构/冷却管或支撑相关固体区域 |
| source | solid | copper | 已勾选 | 铜准直器主体或主要受热区 |
| pbk | solid | aluminum | 未勾选 | 可能为屏蔽块/辅助结构，需结合几何命名确认 |

## 7. source 区域能量源项

`source` 区域中已确认存在一个能量源项：

| 项目 | 内容 |
|---|---|
| Cell Zone | `source` |
| Type | solid |
| Material | copper |
| Number of Energy sources | 1 |
| 能量源项单位 | W/m³ |
| Energy source | `udf ENERGY_FLUH::libudf1` |

当前判断：该热源不是简单常数，而是通过 UDF 加载的体积热源，命名为 `ENERGY_FLUH`，库名为 `libudf1`。后续需要查找该 UDF 源码或相关输入数据。

## 8. 温度结果核对

使用 Fluent：

```text
Reports → Volume Integrals
```

对 `source` cell zone 计算 `Temperature → Static Temperature` 的最大值与最小值，得到：

| 区域 | 变量 | 最大值 | 最小值 | 备注 |
|---|---|---:|---:|---|
| source | Static Temperature | 131.0263 ℃ | 35.76516 ℃ | 通过 Volume Integrals 读取，不依赖失效 contour surface |

该结果与 Mechanical 中 `Imported Body Temperature 3` 的 CFD 载荷摘要高度一致：

| 来源 | 最大温度 | 最小温度 |
|---|---:|---:|
| Fluent source zone / Volume Integrals | 131.0263 ℃ | 35.76516 ℃ |
| Mechanical Imported Body Temperature 3 / CFD summary | 131.01 ℃ | 35.807 ℃ |

当前判断：`Imported Body Temperature 3` 基本可确认为 Fluent 中 `source` 铜热源区温度场映射到 Mechanical 后的温度载荷。

## 9. 冷却水温升

使用 Fluent：

```text
Reports → Surface Integrals
```

对入口与出口 surface 计算 `Temperature → Static Temperature` 的面积加权平均值，得到：

| Surface | Report Type | Variable | 数值 |
|---|---|---|---:|
| inlet | Area-Weighted Average | Static Temperature | 19.99999 ℃ |
| outlet | Area-Weighted Average | Static Temperature | 20.97516 ℃ |

冷却水温升：

```text
ΔT = 20.97516 - 19.99999 = 0.97517 ℃
```

当前判断：在 9 m/s 冷却水工况下，冷却水通过流道后的面积平均温升约为 `0.975 ℃`。

## 10. 冷却水压降

使用 Fluent：

```text
Reports → Surface Integrals
```

对入口与出口 surface 计算 `Pressure → Static Pressure` 的面积加权平均值，得到：

| Surface | Report Type | Variable | 数值 |
|---|---|---|---:|
| inlet | Area-Weighted Average | Static Pressure | 46258.35 Pa |
| outlet | Area-Weighted Average | Static Pressure | -37528.33 Pa |

压降按入口平均静压减出口平均静压计算：

```text
Δp = p_inlet - p_outlet
   = 46258.35 - (-37528.33)
   = 83786.68 Pa
   ≈ 83.79 kPa
```

注意：当前出口边界类型为 `outflow`，不是 `pressure-outlet`。因此该压降可作为当前已收敛流场中的入口/出口静压差记录，但后续若用于泵选型或论文严谨对比，应确认压力参考位置、边界类型和是否应使用总压/静压。

## 11. 后处理对象问题

尝试使用已有 `contour-1` / `contour-2` 时，Fluent 提示部分 surface id 已失效：

```text
Following surface ids no longer exists:
48,47,51,50
They must have been deactivated/deleted.
```

以及在选择部分 interface 时出现：

```text
zone-surface: cannot create surface from sliding interface zone.
Creating empty surface.
```

当前处理策略：不依赖旧 contour 对象；优先使用 Volume Integrals / Surface Integrals 获取数值结果，后续如需云图则重新选择有效 wall 或创建新的切面。

## 12. 与论文的初步对应

- 入口速度 `9 m/s` 与论文第 4 章边界条件中的冷却水流速一致。
- 入口温度 `20 ℃` 与论文第 4 章边界条件中的冷却水入口温度一致。
- `fluid` 区域材料为 `water-liquid`，对应冷却水流道。
- `source` 铜区域的 UDF 体积热源对应论文中能量沉积热源进入热分析模型的关键环节。
- `source` 区域最高温度约 `131 ℃`，与 Mechanical 导入温度载荷 3 对应。
- 出口面积平均温度约 `20.975 ℃`，冷却水温升约 `0.975 ℃`。
- 入口/出口面积平均静压差约 `83.79 kPa`。
- 当前文件优先判断为论文 9 m/s 冷却水热分析工况。

## 13. 后续检查

- 检查 wall / interface 是否为合理的流固耦合换热边界。
- 查找 UDF `ENERGY_FLUH` 的源码、编译库或相关输入数据。
- 查看 Reports / Surface Integrals，提取壁面热流。
- 若能获得质量流量，可用 `Q = m_dot * cp * ΔT` 估算冷却水带走热量，并与 UDF 总热源功率核对。
