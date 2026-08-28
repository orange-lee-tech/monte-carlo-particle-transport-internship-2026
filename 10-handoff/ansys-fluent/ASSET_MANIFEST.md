# ANSYS 交接资产清单

| 类别 | 文件 | 状态 |
|---|---|---|
| 入口 | `START_HERE.md` | 新人入口 |
| 正式手册 | `ANSYS_Fluent_工程交接手册_2026.docx` | 已排版并视觉校验 |
| Markdown 手册 | `ANSYS_HANDOFF.md` | 全量技术交接 |
| 当前行动 | `NEXT_STEPS_CHECKLIST.md` | 活跃 |
| TUI | `TUI_QUICK_REFERENCE.md` | 活跃 |
| AI 协作 | `AI_COLLAB_GUIDE.md` | 活跃 |
| GitHub | `GITHUB_WORKFLOW.md` | 活跃 |
| 程序索引 | `PROGRAM_INDEX.md` | 活跃 |
| 转换程序 | `programs/validated/fluka_to_c_array_converter.py` | 已验证 |
| 验证程序 | `programs/validated/verify_heat_deposition_conversion.py` | 已验证 |
| Coverage 诊断 | `programs/diagnostic/beam_1mrad_offset_2mm_coverage_diagnostic.c` | 诊断资产 |
| FLUKA 数据 | `data/beam_1mrad_offset_2mm.29` | 基准输入 |
| C 数组 | `data/beam_1mrad_offset_2mm_heat_deposition.c/.h` | 已验证输出 |
| 验证报告 | `evidence/beam_1mrad_offset_2mm_verification.md` | 已验证 |

## 仓库中重要原始记录

- `01-daily-log/2026-07-22.md`：第一版 UDF / Fluent 闭环。
- `01-daily-log/2026-07-23 .md`：`.29 → C` 严格验证、功率修正。
- `01-daily-log/2026-07-27.md`：逐体素功率缺口与诊断记录。
- `01-daily-log/2026-08-20.md`：Share Topology 深度排障。
- `01-daily-log/2026-08-27.md`：正式几何故障定位与实习收尾。
- `06-cases/ansys-cases/package-run-record.md`：旧模型算例运行记录。
- `WORKING_RULES.md`：长期仓库与协作规则。
