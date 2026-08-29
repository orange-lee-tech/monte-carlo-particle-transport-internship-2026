# 10-handoff：正式工程交接入口

本目录只保存仍需要后续人员继续执行的工程交接包。它与 `09-archive/` 的区别是：这里描述**当前有效状态和下一步操作**。

## 当前交接包

`ansys-fluent/`：准直器热工仿真工程续接。

推荐阅读顺序：

1. `ansys-fluent/START_HERE.md`
2. `ansys-fluent/EXECUTION_RUNBOOK.md`
3. `ansys-fluent/NEXT_STEPS_CHECKLIST.md`
4. `ansys-fluent/ANSYS_HANDOFF.md`
5. 需要代码/数据时查 `PROGRAM_INDEX.md` 与 `ASSET_MANIFEST.md`。

## 资产完整性说明

本仓库的交接在**状态、方法和旧回归证据**上完整，但不是全部运行资产的镜像。正式续接前必须在工作机或单位工程存储中确认：

- 当前可继续的 CAD / Workbench / Fluent Meshing 检查点；
- 原始 `target_4collimator001_fort.30`；
- 实现新 `fort.30` 解析与 `RAW30_ENERGY_SOURCE` 的正式 UDF 源码。

其中大型 CAD / Workbench / `fort.30` 不入 GitHub 是资产管理策略；**新 RAW30 UDF 源码当前也未在仓库找到，是交接包仍需补齐的代码资产缺口。**

## 当前一句话状态

**A 线的数据读取与 5 mA 功率结论已经验证，B 线 Share 主阻塞已突破；但真正续接前先完成外部资产预检，再从端面识别 → Capping → Region → Volume Mesh 继续。**