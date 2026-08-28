# ANSYS / Fluent 交接入口（兼容旧路径）

本路径原先保存过一版说明型交接。为避免与当前执行状态重复、冲突，**正式交接已经统一迁移到：**

```text
10-handoff/ansys-fluent/
```

优先阅读：

```text
START_HERE.md
EXECUTION_RUNBOOK.md
ANSYS_Fluent_工程交接手册_2026.docx
ANSYS_HANDOFF.md
NEXT_STEPS_CHECKLIST.md
```

当前工程必须按 A/B 两线理解：

```text
A线：fort.30 → 34.56M float32 → 5 mA → UDF
     A1-A3 已闭环；A4 坐标映射等待正式体网格

B线：CAD → Surface → Share → Capping → Region → Volume Mesh
     Share 主阻塞已突破；当前从 Capping / Region 继续

汇合：Volume Mesh → 新 copper Cell Zone → A4 → RAW30_ENERGY_SOURCE → 功率积分 → Solver
```

不要从旧 `.29`、`.30.lis`、0.5 mm 网格加密或全局 Force Share 路线重新开始。
