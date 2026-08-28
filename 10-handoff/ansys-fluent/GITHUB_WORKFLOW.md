# GitHub 与工程资产管理

## 1. 仓库角色

GitHub 用来保存**可追溯的知识和代码**，不是用来无脑塞大型 ANSYS 二进制文件。

推荐流程：

```text
聊天 / 现场操作
→ 得到证据
→ 形成判断
→ 写日志或验证记录
→ GitHub 提交
→ 下一次从仓库恢复上下文
```

## 2. 适合进入 GitHub

- `.py / .c / .h / .md`
- 小型原始输入和验证数据
- TUI 命令与参数基线
- 错误证据与判断
- 验证报告
- 交接手册与资产清单

## 3. 大型 ANSYS 文件

`.cas / .dat / .msh / .wbpj / .scdoc / .x_t` 等大型文件建议保存到单位共享盘或本地工程盘。

GitHub 只保存 manifest，至少记录：

- 文件名
- 日期
- 来源
- 用途
- 状态（正式 / 诊断 / 废弃）
- 对应几何版本
- 可选 SHA256

## 4. 命名

推荐：

```text
collimator_geom_20260827_diagnostic_no_bad_pipe.x_t
collimator_geom_YYYYMMDD_<status>.x_t
beam1mrad_2mm_<geometry-version>_iterXXXX.cas.h5
```

避免：

```text
1111
new
final2
最终版2
真的最终
```

## 5. 记录状态

任何技术结论尽量标明：

- 已阅读
- 已运行
- 已验证
- 当前判断
- 待核实

不要把 AI 推测直接写成“已验证事实”。
