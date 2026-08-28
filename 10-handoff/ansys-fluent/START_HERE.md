# START HERE — ANSYS / Fluent 交接入口

> 目标：让下一位接手者 **30 分钟知道项目在做什么，半天内知道下一步该做什么**。

## 1. 先记住一句话

不要从头重建模型，也不要先调 Fluent 参数。当前已经完成 FLUKA → C 数组 → Fluent UDF 数据链验证，以及大量 Surface Mesh / Share Topology 排障；真正的接续点是：

```text
修复 Capping / Face Zone
→ 正确创建 Fluid Region
→ Volume Mesh
→ 重新识别新版铜体 Cell Zone
→ 恢复 ENERGY_PLAN UDF
→ 重新做功率积分
→ Solver
```

## 2. 当前状态

- `.29 → C`：已严格验证，逐点误差为 0。
- UDF：旧模型中已经完成编译、加载、功率积分和求解。
- Surface Mesh：可正常生成。
- Share Topology：局部主导故障已通过 A/B 试验定位。
- 当前卡点：Capping 引用旧 Face Zone，长管入口/出口需要重新识别。
- Volume Mesh / 新版 Solver：尚未完成。

## 3. 第一天不要做什么

- 不要 `Update All`。
- 不要把网格一律加密到 0.5 mm。
- 不要把旧 `zone 10 = copper` 直接套到新模型。
- 不要用 Share Topology 替 CAD 修穿模。
- 不要看到“长管像被截断”就回 CAD 重画；先查 Face Zone。

## 4. 新人阅读顺序

1. `ANSYS_Fluent_工程交接手册_2026.docx`
2. `ANSYS_HANDOFF.md`
3. `NEXT_STEPS_CHECKLIST.md`
4. `TUI_QUICK_REFERENCE.md`
5. `PROGRAM_INDEX.md`
6. `AI_COLLAB_GUIDE.md`
7. `GITHUB_WORKFLOW.md`

## 5. 当前最小操作

在现有 Share 已完成的 Fluent Meshing 状态下：

```text
/boundary/manage/list
```

重新获取当前 Face Zone，定位两根长细管和真实入口/出口端面，再重建 Capping。

---

**交接原则：先接上已有链路，再优化；先验证几何，再调网格；先看证据，再改参数。**
