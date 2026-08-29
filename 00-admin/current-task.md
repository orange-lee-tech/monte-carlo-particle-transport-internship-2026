# 当前任务说明

更新时间：2026-08-29

## 1. 当前阶段

现场生产实习已结束，仓库进入 **成果定稿 + 答辩准备 + 工程交接** 阶段。

当前分成两条后续路线：

```text
A. 实习成果线
最终报告 → PPT 素材整理 → 开学答辩

B. 工程续接线
10-handoff/ansys-fluent/
→ B5 Capping / Region / Volume Mesh
→ A4 CAD↔FLUKA 坐标标定
→ RAW30_ENERGY_SOURCE
→ 功率积分
→ Solver
```

## 2. 实习成果状态

- 每日终版日志：已收口至 `2026-08-27.md`；
- 周报体裁材料：7 篇日志型周报 + 1 篇特别周刊，共 8 篇；
- 技术路线总盘点：已完成；
- 最终实习报告 Markdown：已完成并进入微调；
- 最终答辩 PPT 信息架构：已建立，后续以多图少字方式制作；
- ANSYS / Fluent 工程交接包：已建立并可执行。

## 3. 技术闭环状态

| 模块 | 状态 |
|---|---|
| 旧 `.29 → C/UDF → Fluent` | 已闭环 |
| 旧模型功率 / voxel-cell 映射诊断 | 已闭环 |
| 新 `fort.30` 34.56M 数据读取 | 已闭环 |
| 5 mA 归一化与 31.035 kW 全域积分 | 已闭环 |
| 新 CAD 主故障定位 | 基本闭环 |
| Share Topology | 删除问题管 A/B 后可实质继续 |
| Capping / fluid Region / Volume Mesh | 未闭环 |
| 新 Cell Zone 正式热源挂接 | 未完成 |
| 新模型温度场 / Mechanical 热应力 | 未完成 |
| DRPL-V 短期重复性 | 已验证，总体较好 |
| DRPL-V 绝对准确度 / 凝露定量 / 厚度漂移解释 | 未闭环 |

## 4. 当前最重要的事实边界

- 本人基于团队上游 FLUKA 粒子输运结果开展下游接口和热工工作，不将上游计算写成个人完成；
- 新正式模型不能写成已经完成完整热—结构求解；
- `.30.lis` 不能作为新正式数据源；
- 新模型不得复用旧 `zone 10 = source`；
- DRPL-V 不能写成已经完成绝对准确度校准或凝露影响定量；
- 旧模型 46.800 / 38.178 / 37.243 kW 只作旧几何回归证据，不能直接套到新模型。

## 5. 仓库读取顺序

### 做最终报告 / 答辩

1. `07-reports/final-internship-report.md`
2. `07-reports/internship-content-review-by-technical-route.md`
3. `08-presentation/final-internship-ppt-outline.md`
4. 需要证据时回查周报和每日日志。

### 继续工程计算

1. `10-handoff/README.md`
2. `10-handoff/ansys-fluent/START_HERE.md`
3. `10-handoff/ansys-fluent/EXECUTION_RUNBOOK.md`
4. `10-handoff/ansys-fluent/NEXT_STEPS_CHECKLIST.md`

聊天用于即时协作，GitHub继续作为长期事实库。