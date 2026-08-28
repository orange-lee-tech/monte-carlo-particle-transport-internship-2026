# ANSYS / Fluent 工程交接包

本目录是 2026 年暑期实习 ANSYS / Fluent 工作的正式交接入口。

## 新人阅读顺序

1. `ANSYS_Fluent_工程交接手册_2026.docx` — 正式 Word 交接版，优先阅读。
2. `START_HERE.md` — 30 分钟进入状态。
3. `ANSYS_HANDOFF.md` — 完整技术手册。
4. `NEXT_STEPS_CHECKLIST.md` — 当前接续任务。
5. `TUI_QUICK_REFERENCE.md` — Fluent Meshing TUI 快查。
6. `PROGRAM_INDEX.md` — 精选程序与数据用途。
7. `AI_COLLAB_GUIDE.md` — 与 AI 协作方法。
8. `GITHUB_WORKFLOW.md` — 仓库与大型工程资产管理。
9. `ASSET_MANIFEST.md` — 本交接包资产总表。

## 当前一句话状态

正式几何的 Share Topology 主导故障已通过 TUI + A/B 试验定位到局部管—主体接口；当前下一技术节点是重新识别长管 Face Zone、修复 Capping / Fluid Region，完成 Volume Mesh 后在新版 copper Cell Zone 上恢复既有 FLUKA → Fluent UDF 热源链。

## 交接原则

- 先接上已有链路，再优化。
- 先验证几何，再调网格。
- 新网格必须重新识别 Zone，禁止照搬旧 ID。
- Share Topology 不能代替 CAD 修穿模。
- 一次只解决一个层级的问题。
