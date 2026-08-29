# ANSYS / Fluent 工程交接包

本目录是正式交接入口。交接方式已经从“知识说明”改为“**状态机 + 执行卡 + 验收关口**”。

## 先读什么

1. `START_HERE.md` — 10 分钟定位当前状态与资产预检。
2. `EXECUTION_RUNBOOK.md` — **下一位接手者实际照着做的操作手册**。
3. `NEXT_STEPS_CHECKLIST.md` — P0 → B5 → A4 → Solver Gate。
4. `ANSYS_HANDOFF.md` — 全量技术依据与历史结论。
5. `TUI_QUICK_REFERENCE.md` — Fluent Meshing TUI 快查。
6. `PROGRAM_INDEX.md` / `ASSET_MANIFEST.md` — 程序、数据与缺失资产状态。
7. `AI_COLLAB_GUIDE.md` — 与 AI 协作方式。
8. `GITHUB_WORKFLOW.md` — 仓库管理。
9. `ANSYS_Fluent_工程交接手册_2026.docx` — 本次 2026-08-29 仓库审计前形成的 Word 交接快照；便于阅读，但**未包含 2026-08-29 仓库资产审计新增的 P0 预检信息**，当前状态以 Markdown 为准。

## 先做资产预检

GitHub 当前保存了交接文档和旧 `.29` 回归资产，但**没有完整保存新正式模型的运行资产**。开始操作前先确认工作机/共享工程盘中存在：

1. 当前 Share 后可继续的 CAD / Workbench / Fluent Meshing 工程；
2. `target_4collimator001_fort.30` 原始文件；
3. 新 `fort.30` 解析与 `RAW30_ENERGY_SOURCE` 的正式 UDF C 源码。

前两项属于大型工程资产，按仓库策略保存在 GitHub 外；第 3 项是当前仓库审计发现的**代码资产缺口**。如果找不到正式 UDF 源码，不应根据 Markdown 描述直接重写一份并当成原实现。

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
