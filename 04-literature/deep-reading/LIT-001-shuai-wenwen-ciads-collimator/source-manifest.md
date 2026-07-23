# LIT-001 原始资料清单

## 1. 原始论文

| 项目 | 内容 |
|---|---|
| 文件名 | `帅文文+学位会审核版论文.pdf` |
| 题目 | 《CiADS缪子源靶后高功率准直器设计》 |
| 文件大小 | 6,913,966 bytes |
| SHA256 | `5694f46f9b1455af73bc449973db4ec31b4053827452c1bbcfec28e5211ad8df` |
| 证据地位 | 原始PDF为论文事实、页码、图表和数值的最终证据源 |

## 2. 人工精读资料

用户从 Zotero 导出7份Markdown精读记录，覆盖：

1. 摘要与研究主线；
2. 第3章3.1—3.2材料和结构；
3. 第3章3.3—3.5多级准直与CMA-ES；
4. 第3章3.6—3.7辐射屏蔽；
5. 第4章4.1—4.2初始热设计与结构优化；
6. 第4章4.3真实热源和热工水力；
7. 第4章4.4—4.6偏移工况与机器保护。

原始导出中包含Zotero内部链接、HTML高亮、阶段性回答和导师修订。正式知识层不逐字复制原始导出，而是保留：

- 论文事实；
- 页码、图号和表号；
- 经过修订的工程理解；
- 仍需计算文件确认的问题。

## 3. 已关联的工程资产

| 资产 | 仓库位置 | 当前用途 |
|---|---|---|
| FLUKA `.29` 数据 | `fluka_to_c_translation/input/` | 热沉积原始数据 |
| Python转换程序 | `fluka_to_c_translation/fluka_to_c_array_converter.py` | `.29`转C三维数组 |
| 数组 `.c/.h` | `fluka_to_c_translation/output/` | Fluent UDF数据层 |
| 独立一致性验证 | `fluka_to_c_translation/verify_heat_deposition_conversion.py` | 验证数据数量、顺序和数值 |
| 验证报告 | `fluka_to_c_translation/verification/beam_1mrad_offset_2mm_verification.md` | 保存PASS结果和功率修正 |
| Fluent覆盖率诊断UDF | `fluka_to_c_translation/udf/beam_1mrad_offset_2mm_coverage_diagnostic.c` | 检查voxel—cell体积覆盖与功率恢复 |
| Ansys接手记录 | `06-cases/ansys-cases/package-run-record.md` | Fluent/Mechanical模型、边界和结果记录 |
| 近期日志 | `01-daily-log/2026-07-20.md`至`2026-07-22.md`，以及根目录`2026-7.23.md` | 工程继承过程证据 |

## 4. 证据使用规则

- 论文数值引用回到原始PDF；
- 程序行为引用代码和自动验证结果；
- Fluent运行状态引用日志、case/data检查点和诊断输出；
- 尚未提交到仓库的本地主程序或结果文件，不标记为“仓库已有”；
- 论文叙述、当前代码实现和现场模型结果出现差异时，三者分别记录，不强行合并。
