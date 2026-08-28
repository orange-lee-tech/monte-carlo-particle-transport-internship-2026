# 下一步检查清单

## Phase 1 — 几何与流体域

- [ ] 用 `/boundary/manage/list` 获取当前 Face Zone。
- [ ] 单独显示疑似长管 zone，确认两根长细管连续存在。
- [ ] 确认入口/出口端面是否独立成 zone。
- [ ] 若端面未分开，重新 Surface Mesh 时启用 `Invoke Zone Separation by Angle? = yes`。
- [ ] 删除/重设旧 Capping 选择。
- [ ] 手工选择真实 inlet / outlet 端面。
- [ ] Create / Update Regions。
- [ ] 检查 fluid / solid / dead / void 身份。
- [ ] 生成 Volume Mesh。

## Phase 2 — 恢复热源

- [ ] 进入 Solver 后重新识别 copper Cell Zone。
- [ ] 不复用旧 zone 10。
- [ ] 编译并加载正式 `ENERGY_PLAN` UDF。
- [ ] 将热源只挂到新版铜质准直器 Cell Zone。
- [ ] 做热源功率积分。
- [ ] 检查热斑空间位置。

## Phase 3 — 正式求解

- [ ] 检查材料和边界条件。
- [ ] 检查入口/出口质量流量。
- [ ] 检查能量输入/输出。
- [ ] 运行至温度监控量平台。
- [ ] 保存可复现 case/data 检查点。

## 停止条件

出现以下情况时停止继续调 Fluent：

- `Mesh topology corrupted`
- `SIGSEGV`
- 大量 `non-manifold configuration`
- 某局部接口 inter-zone intersection 数万级

这些优先回 CAD 检查实体穿模、共面重合、三体交线或坏面。
