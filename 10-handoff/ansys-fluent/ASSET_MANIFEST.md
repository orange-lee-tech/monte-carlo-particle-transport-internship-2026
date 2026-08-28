# ANSYS 交接资产清单

| 类别 | 文件 | 作用 |
|---|---|---|
| 正式 Word | `ANSYS_Fluent_工程交接手册_2026.docx` | A/B 双线 + 执行卡 + 验收关口 |
| 快速入口 | `START_HERE.md` | 10 分钟定位当前状态 |
| 现场执行 | `EXECUTION_RUNBOOK.md` | 坐到工作机前直接照做 |
| 全量交接 | `ANSYS_HANDOFF.md` | 技术依据、历史证据、操作细节 |
| 当前清单 | `NEXT_STEPS_CHECKLIST.md` | B5 → A4 → Solver Gate |
| TUI 快查 | `TUI_QUICK_REFERENCE.md` | 命令、用途、风险 |
| 程序索引 | `PROGRAM_INDEX.md` | 区分新 fort.30 主线与旧 .29 回归链 |
| AI 协作 | `AI_COLLAB_GUIDE.md` | 提问模板和协作方式 |
| GitHub 管理 | `GITHUB_WORKFLOW.md` | 版本与工程资产管理 |

## 仓库内附带的旧回归资产

- `programs/validated/fluka_to_c_array_converter.py`
- `programs/validated/verify_heat_deposition_conversion.py`
- `programs/diagnostic/beam_1mrad_offset_2mm_coverage_diagnostic.c`
- `data/beam_1mrad_offset_2mm.29`
- `data/beam_1mrad_offset_2mm_heat_deposition.c/.h`
- `evidence/beam_1mrad_offset_2mm_verification.md`

这些用于旧模型方法回归。新正式 A 线以 `fort.30 → RAW30_ENERGY_SOURCE` 为主。
