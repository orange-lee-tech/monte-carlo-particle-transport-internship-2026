# ANSYS / Fluent 交接资产清单

更新时间：2026-08-29

## 1. 已在 GitHub 中的交接资产

| 类别 | 文件 | 作用 |
|---|---|---|
| Word 快照 | `ANSYS_Fluent_工程交接手册_2026.docx` | 仓库审计前交接版；未含 8/29 新增资产预检 P0，当前状态以 Markdown 为准 |
| 快速入口 | `START_HERE.md` | 10 分钟定位当前状态 |
| 现场执行 | `EXECUTION_RUNBOOK.md` | 坐到工作机前直接照做 |
| 全量交接 | `ANSYS_HANDOFF.md` | 技术依据、历史证据、操作细节 |
| 当前清单 | `NEXT_STEPS_CHECKLIST.md` | 资产预检 → B5 → A4 → Solver |
| TUI 快查 | `TUI_QUICK_REFERENCE.md` | 命令、用途、风险 |
| 程序索引 | `PROGRAM_INDEX.md` | 区分新 fort.30 主线与旧 .29 回归链 |
| AI 协作 | `AI_COLLAB_GUIDE.md` | 提问模板和协作方式 |
| GitHub 管理 | `GITHUB_WORKFLOW.md` | 版本与工程资产管理 |

## 2. GitHub 中附带的旧回归快照

- `programs/validated/fluka_to_c_array_converter.py`
- `programs/validated/verify_heat_deposition_conversion.py`
- `programs/diagnostic/beam_1mrad_offset_2mm_coverage_diagnostic.c`
- `data/beam_1mrad_offset_2mm.29`
- `data/beam_1mrad_offset_2mm_heat_deposition.c/.h`
- `evidence/beam_1mrad_offset_2mm_verification.md`

这些文件与 `fluka_to_c_translation/` 中对应文件为**相同 SHA 的有意快照**：
- `fluka_to_c_translation/` 是旧 `.29` 回归链的规范代码位置；
- `10-handoff/ansys-fluent/` 保留一份快照，使交接包在旧链回归上可自包含；
- 不把这类重复当成需要清理的垃圾文件。

## 3. 运行新正式模型仍需的 GitHub 外资产

| 资产 | 当前仓库状态 | 原因 / 动作 |
|---|---|---|
| 当前 CAD / Workbench / Fluent Meshing 工程检查点 | 未入库 | 大型工程资产；应从工作机或单位工程存储恢复 |
| `target_4collimator001_fort.30` | 未入库 | 大型原始数据；应从上游/工作机恢复并核对文件身份 |
| 新 `fort.30` 解析 + `RAW30_ENERGY_SOURCE` UDF C 源码 | **未找到** | 小型代码本应适合版本管理；这是当前交接资产缺口，优先从原工作目录恢复并提交 |

## 4. 已验证但不能替代源文件的硬锚点

```text
300 × 300 × 384
34,560,000 float32
1 mm³ voxel
5 mA full-box power = 31.035322255 kW
peak source = 3.584363867049e+07 W/m³
peak voxel center = (-1.85,+0.95,26.25) cm
```

这些数值可以用于恢复后的回归验收，但**不能据此反向猜写缺失的正式 UDF 源码或重造 fort.30**。