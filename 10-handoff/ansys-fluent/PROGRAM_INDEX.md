# 程序与数据索引

本目录复制与 ANSYS 交接最直接相关的代码和 1 mrad + 2 mm 基准数据。原仓库仍是唯一版本源；这里的副本用于新人快速进入状态。

## 已验证程序

### `programs/validated/fluka_to_c_array_converter.py`

用途：

- 读取 FLUKA `.29` 数据区；
- 严格校验数据数量；
- 按 `array[ix][iy][iz]` 生成 C 数组；
- 不负责束流电流换算。

### `programs/validated/verify_heat_deposition_conversion.py`

用途：

- 独立重新解析 `.29` 与生成的 C 数组；
- 逐项比较；
- 检查数据数量、sum、max、min、索引顺序；
- 1 mrad + 2 mm 已得到 mismatch=0、最大误差=0。

## 历史诊断程序

### `programs/diagnostic/beam_1mrad_offset_2mm_coverage_diagnostic.c`

用途：

- Fluent 中进行热源覆盖率/映射诊断；
- 用于解释功率映射差异。

注意：使用诊断程序时，必须重新确认当前 Cell Zone 身份与并行环境，不要照搬旧 Zone ID。

## 基准数据

### `data/beam_1mrad_offset_2mm.29`

- FLUKA 计分数据。
- 网格：20 × 20 × 28。
- X/Y/Z 范围：±10 cm / ±10 cm / ±14 cm。

### `data/beam_1mrad_offset_2mm_heat_deposition.c/.h`

由转换程序生成的 1 mrad + 2 mm C 数组。

### `evidence/beam_1mrad_offset_2mm_verification.md`

`.29 → C` 独立验证报告。
