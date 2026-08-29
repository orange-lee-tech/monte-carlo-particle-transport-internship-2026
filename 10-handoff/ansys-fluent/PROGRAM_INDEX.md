# 程序与数据索引：先区分旧回归链与新正式链

## 1. 新正式 A 线（当前项目主线）

```text
target_4collimator001_fort.30
→ Fortran sequential binary parser
→ 300×300×384 float32
→ UDF static memory
→ 5 mA
→ RAW30_ENERGY_SOURCE
→ A4 CAD/FLUKA 坐标映射
```

已验证硬指标：

- 34,560,000 values；
- 1 mm × 1 mm × 1 mm voxel；
- 5 mA 全域功率 31.035322255 kW；
- 峰值源项 3.584363867049e+07 W/m³；
- 峰值 voxel center = (-1.85,+0.95,26.25) cm。

**这才是新正式模型应恢复的热源路线。**

### 仓库资产状态

这条路线的**验证事实**已由日志和交接文档保存，但当前 GitHub 树中：

- 没有 `target_4collimator001_fort.30`；
- 没有找到实现 `RAW30_ENERGY_SOURCE` 的正式 C 源码；
- 也没有当前可继续的 Workbench / Fluent Meshing 大型工程文件。

因此，A4 前必须先从原工作机/工程存储恢复上述资产。尤其是 RAW30 UDF 源码，应优先找回原实现，而不是根据文档重新猜写。

## 2. 仓库内的旧回归链（方法基线）

### `programs/validated/fluka_to_c_array_converter.py`

旧 `.29` 数据转 C 数组。用于验证数据重排方法，不是新 300×300×384 正式输入。

### `programs/validated/verify_heat_deposition_conversion.py`

独立验证旧 `.29 → C` 数值、顺序和数量。

### `data/beam_1mrad_offset_2mm.29`

旧 20×20×28、1 cm voxel 基准数据。

### `data/beam_1mrad_offset_2mm_heat_deposition.c/.h`

旧模型热沉积数组。

### `programs/diagnostic/beam_1mrad_offset_2mm_coverage_diagnostic.c`

旧模型 coverage / voxel-cell 映射诊断参考。

## 3. 不要混淆两个 DEFINE_SOURCE

```text
旧模型：ENERGY_PLAN
新 A 线：RAW30_ENERGY_SOURCE
```

旧 `ENERGY_PLAN` 用于证明 Fluent UDF / source / Solver 链能够工作；新正式几何完成 Volume Mesh 后，应恢复 `RAW30_ENERGY_SOURCE` 的 A4 坐标标定与挂接。
