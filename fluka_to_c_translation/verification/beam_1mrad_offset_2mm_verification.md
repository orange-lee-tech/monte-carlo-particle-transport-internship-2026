# beam_1mrad_offset_2mm 数据一致性验证

日期：2026-07-23  
结论：**PASS**

## 1. 验证对象

```text
fluka_to_c_translation/input/beam_1mrad_offset_2mm.29
fluka_to_c_translation/output/beam_1mrad_offset_2mm_heat_deposition.c
fluka_to_c_translation/output/beam_1mrad_offset_2mm_heat_deposition.h
```

验证脚本：

```text
fluka_to_c_translation/verify_heat_deposition_conversion.py
```

## 2. 逐项验证结果

```text
网格尺寸：20 × 20 × 28
坐标范围：X[-10,10] cm，Y[-10,10] cm，Z[-14,14] cm
理论数据量：11200
FLUKA 数据量：11200
C 数组数据量：11200
逐项不一致数量：0
最大绝对误差：0
最大相对误差：0
```

全局统计：

```text
FLUKA sum = 0.0093599553423524
C array sum = 0.0093599553423524
sum difference = 0
minimum = 0
maximum = 9.1767e-05
maximum index = (10,10,3)
```

数组排列验证：

```text
FLUKA 一维数据流：x 索引变化最快，y 其次，z 最慢
C 数组语义：array[ix][iy][iz]
排列结论：PASS
```

## 3. 主力机编译文件身份核验

本机仓库文件 SHA256：

```text
beam_1mrad_offset_2mm_heat_deposition.c
FDA9F7F9D62CF28586FBFD4813057E32AC52BAB7865316657AFF1F7C8F9E7808

beam_1mrad_offset_2mm_heat_deposition.h
CC5F0D7E3036E176665CDC9BD47186959D9BA40681D56A36E565A9238E676984
```

主力机以下位置中的 `.c/.h` 文件哈希均与仓库完全一致：

```text
dssmx_files/dp0/FFF-2/Fluent/
libudf1/src/
libudf1/win64/3ddp_host/
libudf1/win64/3ddp_node/
```

由此确认，2026-07-22 Fluent 3D 双精度并行构建使用的热沉积数组，与仓库当前通过逐项验证的数组属于同一版本。

## 4. 修正后的参考功率

在暂定束流电流 `I = 5 mA`、换算系数 `5×10^12 W/m³` 下：

```text
完整 FLUKA 计分盒参考功率 = 46.7997767 kW
峰值体积热源 = 4.58835×10^8 W/m³
```

此前记录的：

```text
sum = 0.00807373012674354
max = 6.3796e-05
完整计分盒功率 = 40.36865 kW
```

不对应仓库当前两个 `.29` 工况，不能继续作为本工况基准。

若继续采用 2026-07-22 Fluent 功率积分结果：

```text
source 区 = 37.239738 kW
四区域合计 = 38.174891 kW
```

则相对于修正后的 46.7997767 kW：

```text
source 区恢复比例 = 79.57%
四区域合计恢复比例 = 81.57%
未恢复比例 = 18.43%
未恢复功率约 = 8.625 kW
```

该差异不能再表述为 5.43%，需在后续坐标映射、区域覆盖和体积守恒检查中重新分析。

## 5. 阶段结论

```text
数据转换完整性：PASS
数组排列顺序：PASS
主力机编译数组身份：PASS
单位与束流电流假设：待继续核实
Fluent 映射功率恢复率：待重新解释
```
