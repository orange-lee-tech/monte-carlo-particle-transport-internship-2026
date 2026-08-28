# START HERE — ANSYS / Fluent 执行入口

> 目标：接手者 10 分钟知道“现在在哪、下一步点什么、什么时候停”。

## 1. 先看工程结构：A/B 两线，当前先推 B 线

```text
A线：FLUKA 数据导入
fort.30 → 34,560,000 float32 → UDF static memory → 5 mA → 31.035 kW
状态：A1–A3 完成，A4 坐标映射等待正式体网格

B线：模型导入
CAD → Surface Mesh → Share → Capping → Region → Volume Mesh
状态：Share 主阻塞已突破；当前停在 Capping / Region

汇合点：
Volume Mesh → 新 copper Cell Zone → A4 坐标标定 → RAW30_ENERGY_SOURCE → 功率积分 → Solver
```

**所以现在不要再研究 fort.30 文件格式，也不要先挂 UDF。先把 B 线推进到 Volume Mesh。**

## 2. 坐到工作机前，按这一串做

```text
1. 打开当前 Share 后 Fluent Meshing 状态
2. /boundary/manage/list
3. 逐个显示长管候选 Face Zone
4. 找到真实 inlet / outlet 开口端面
5. 重建 Capping（不要复用旧 Zone 选择）
6. Create / Update Regions
7. 确认 water region 连通、solid/dead/void 身份合理
8. Volume Mesh
9. 保存检查点
10. 进入 Solver 后重新识别 copper Cell Zone
11. 恢复 A4 坐标标定
12. 挂 RAW30_ENERGY_SOURCE
13. 功率积分 + 热斑位置验证
14. 通过后才正式迭代
```

## 3. 三条红线

- 新网格后 **Zone ID 必须重新识别**；旧 `zone 10 = source` 只属于旧模型。
- 出现 `Mesh topology corrupted / SIGSEGV`，立即恢复基线，不继续调参。
- 不再优先走 0.5 mm 强加密、0.25 mm、全局 Force Share、`.30.lis` 正式输入这些已否定路线。

## 4. 两个硬回归锚点

A 线新数据：

```text
300 × 300 × 384
1 mm³ voxel
34,560,000 float32
5 mA integrated power = 31.035322255 kW
peak source = 3.584363867049e+07 W/m³
peak FLUKA voxel center = (-1.85,+0.95,26.25) cm
```

B 线几何诊断：

```text
主体 ↔ wall.5 ≈ 79,829 inter-zone intersections
主体 ↔ wall.6 ≈ 69,515
主体 ↔ wall.7 = 0
self-intersection = 0
duplicate = 0
```

删除可疑管后 Share 能继续完成 Intersect / region computation，是当前最强 A/B 证据。

## 5. 继续工作时优先读

1. `EXECUTION_RUNBOOK.md` — 真正的“拿来就做”执行卡。
2. `ANSYS_HANDOFF.md` — 全量技术交接。
3. `NEXT_STEPS_CHECKLIST.md` — 当前关口验收表。
4. `TUI_QUICK_REFERENCE.md` — TUI 快查。
5. `01-daily-log/2026-08-17.md` — A/B 拆线与 A1–A3。
6. `01-daily-log/2026-08-27.md` — B 线 Share 突破与 Capping 停点。
