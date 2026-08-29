# 自主实习工程管理仓库

本仓库记录 2026 年暑期在中国科学院近代物理研究所高功率束流室开展的生产实习，包括工程继承、热工仿真、数据验证、实验记录、文献材料与最终交付。

> **状态：2026-08-29，现场实习已结束，仓库进入成果整理与工程交接状态。**

## 项目主线与职责边界

本项目属于协作型科研工程。上游 FLUKA 粒子输运计算由团队其他成员负责，本人在其结果基础上重点承担数据接口、Fluent 热工链继承与验证、CAD / Fluent Meshing 排障，以及部分热物性实验。

```text
论文与既有工程基线
→ 上游 FLUKA 能量沉积结果
→ 数据完整性 / 单位 / 坐标 / 功率验证
→ Fluent UDF 热源加载
→ CAD / SpaceClaim / Fluent Meshing
→ Capping / Region / Volume Mesh
→ Solver 温度场
→ Mechanical 热应力
```

实习结束时，最后四个下游节点尚未全部闭环；对应执行状态已写入 `10-handoff/ansys-fluent/`。

## 已形成的关键成果

- 完成旧 `.29 → Python/C → UDF → Fluent` 热源链恢复；
- 将旧模型 **18.422%** 功率缺口分解到几何覆盖差异与 cell-centroid 映射欠/过填充，而非简单“漏网格”；
- 确认新 `.30.lis` 仅含 **14,786,930 / 34,560,000 = 42.786%** 数据，并改由原始 `fort.30` 完成完整二进制读取；
- Python 与 Fluent UDF 对 34.56M 数据、峰值与总量完成独立交叉验证，5 mA 全域积分功率约 **31.035 kW**；
- 将长期 Share Topology 故障从“继续加密网格”追溯到局部冷却管—主体 CAD 拓扑，并通过健康对照与删除问题管 A/B 试验获得强证据；
- DRPL-V 实验完成重复性与环境边界的阶段性评价；短期重复性总体较好，绝对准确度、凝露影响和厚度读数漂移仍未闭环；
- 形成每日事实日志、周报、最终报告、PPT 信息架构及 ANSYS / Fluent 正式交接包；运行资产并非全部进入 GitHub，外部资产与缺失 RAW30 UDF 源码已在交接清单中显式标记。

## 当前仓库结构

```text
monte-carlo-particle-transport-internship-2026/
├── 00-admin/                 # 原始任务、计划、当前状态与规则
├── 01-daily-log/             # 终版日志与周报
├── 02-meetings/              # 实际组会记录
├── 04-literature/            # 文献证据、精读、结构化笔记与专题综合
├── 05-software/              # 软件学习记录；正式续接入口不在这里
├── 06-cases/                 # Ansys / Fluent 算例与运行记录
├── 07-reports/               # 技术总盘点与最终实习报告
├── 08-presentation/          # 最终答辩 PPT 信息架构与历史组会材料
├── 09-archive/               # 已退出现役区但仍有参考价值的历史材料
├── 10-handoff/               # 正式工程交接包
└── fluka_to_c_translation/   # 旧 .29 回归链的代码与数据基线
```

`03-notes/` 原先只有通用占位 README，没有形成独立事实笔记，已在实习收尾清理；目录编号不重排，以避免大量历史链接失效。

## 推荐读取顺序

### 看实习成果

1. `07-reports/final-internship-report.md`
2. `07-reports/internship-content-review-by-technical-route.md`
3. `01-daily-log/weekly-review/`
4. 需要核对细节时再回到对应每日终版日志。

### 继续 ANSYS / Fluent 工程

1. `10-handoff/README.md`
2. `10-handoff/ansys-fluent/START_HERE.md`
3. `10-handoff/ansys-fluent/EXECUTION_RUNBOOK.md`
4. `10-handoff/ansys-fluent/NEXT_STEPS_CHECKLIST.md`

## 记录原则

- 区分“已运行、已验证、当前判断、待核实、未完成”；
- 关键结论必须能追溯到原始数据、代码、日志、实验或验证记录；
- 不把团队上游成果写成个人完成内容，也不因职责边界而放弃对输入的必要审查；
- AI 可用于解释、代码草拟、信息整理和假设生成，但不能替代守恒、对照、A/B 与人工责任；
- 未公开资料继续遵守保密和脱敏要求。