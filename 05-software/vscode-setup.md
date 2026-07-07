# VS Code 配置记录

更新时间：2026-07-07

## 1. 当前已安装扩展

用户当前 VS Code 已安装扩展：

- Chinese simplified；
- Remote SSH；
- Remote SSH Editing configuration files；
- Remote explorer。

## 2. 当前判断

现阶段主要任务是学习 Ansys Workbench 与 Fluent，并跑通已有计算文件包。VS Code 暂时不是主工具，不需要立刻安装大量扩展。

当前已有扩展已经能支撑基础远程连接与远程文件编辑需求。

## 3. 暂时不急需安装的内容

在没有遇到明确脚本任务前，暂时不需要主动安装复杂扩展。

不建议现在为了“可能会用到”提前安装大量扩展，避免干扰当前主线。

## 4. 后续可能需要的扩展

如果后续出现脚本编写、远程服务器文件编辑、Fluent UDF 或数据处理任务，可再按需安装：

| 扩展 | 触发条件 | 作用 |
|---|---|---|
| Python | 需要处理数据、批量脚本、绘图 | Python 脚本支持 |
| C/C++ | 需要编写 Fluent UDF | C 语言语法与调试支持 |
| Fortran | 需要阅读或修改旧科学计算代码 | Fortran 代码支持 |
| Jupyter | 需要交互式处理结果数据 | 笔记本式计算与绘图 |
| Markdown All in One | 需要更舒服地写 Markdown 日志和笔记 | Markdown 编辑增强 |

## 5. 当前建议

当前不急着扩展 VS Code。优先保持轻量配置：

```text
Ansys / Fluent 是主线
VS Code 是备用工具
遇到脚本需求后再安装对应扩展
```

## 6. 远程连接注意事项

已有 Remote SSH 相关扩展，后续如果需要连接超算中心或远程桌面相关服务器，可以用于远程编辑配置文件或脚本。

但 Fluent 图形界面计算目前优先通过远程桌面完成，不一定需要 VS Code 直接介入。
