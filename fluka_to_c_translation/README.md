# FLUKA `.29` → C 数组回归基线

本目录保存实习中恢复并验证的**旧模型数据转换链**。它仍是可执行、可回归的代码资产，但不再代表新正式模型的数据路线。

## 旧链

```text
FLUKA .29
→ fluka_to_c_array_converter.py
→ heat_deposition.c / .h
→ Fluent UDF: ENERGY_PLAN
→ 旧模型功率 / voxel-cell 映射回归
```

旧计分网格：

- X：-10 ~ 10 cm，20 bins；
- Y：-10 ~ 10 cm，20 bins；
- Z：-14 ~ 14 cm，28 bins；
- 共 20×20×28 = 11,200 个数据。

## 当前正式数据路线

新模型已改为：

```text
fort.30 原始 Fortran sequential binary
→ 34,560,000 float32
→ UDF static memory
→ 5 mA 归一化
→ RAW30_ENERGY_SOURCE
```

该新路线的状态、硬回归锚点与下一步不在本目录维护，统一查看：

`10-handoff/ansys-fluent/PROGRAM_INDEX.md`

## 目录内容

- `input/`：两组旧 `.29` 输入；
- `output/`：对应生成的 C / H 数组；
- `udf/`：旧模型 coverage / 映射诊断代码及参考头文件；
- `verification/`：旧 `.29 → C` 验证记录；
- 根目录两个 Python 脚本：转换与独立验证。

已删除无效 `.bak` 备份文件，Git 历史本身承担版本回溯功能。

## 与交接包的关系

`10-handoff/ansys-fluent/` 中保留了一份相同 SHA 的旧回归资产快照，目的是让交接包可自包含；本目录仍是旧链的规范代码位置。