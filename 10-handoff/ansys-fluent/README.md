# ANSYS / Fluent 工程交接包

本目录是正式交接入口。交接方式已经从“知识说明”改为“**状态机 + 执行卡 + 验收关口**”。

## 先读什么

1. `ANSYS_Fluent_工程交接手册_2026.docx` — 正式 Word 执行版。
2. `START_HERE.md` — 10 分钟定位当前状态。
3. `EXECUTION_RUNBOOK.md` — **下一位接手者实际照着做的操作手册**。
4. `NEXT_STEPS_CHECKLIST.md` — B5 → A4 → Solver 三个 Gate。
5. `ANSYS_HANDOFF.md` — 全量技术依据与历史结论。
6. `TUI_QUICK_REFERENCE.md` — Fluent Meshing TUI 快查。
7. `PROGRAM_INDEX.md` — 代码/数据用途和旧/新路线区别。
8. `AI_COLLAB_GUIDE.md` — 与 AI 协作方式。
9. `GITHUB_WORKFLOW.md` — 仓库管理。

## 先看清 A/B 两条线

```text
A线：新 FLUKA 数据导入
fort.30 → 34.56M float32 → 5 mA → UDF
A1–A3 已完成；A4 坐标映射等待 B 线

B线：新模型导入
CAD → Surface Mesh → Share → Capping → Region → Volume Mesh
Share 主阻塞已突破；当前从 Capping / Region 继续

两线汇合：
Volume Mesh → 新 copper Cell Zone → A4 → RAW30_ENERGY_SOURCE → 功率积分 → Solver
```

## 当前一句话

**现在先完成 B5：重新识别长管端面 → Capping → Region → Volume Mesh；随后恢复 A4，而不是重新开发数据读取或继续 Share 参数试错。**
