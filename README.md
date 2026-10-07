# Agent workflows that end in evidence

把“Agent 说完成了”变成“使用者可以核对的交付”。

这是一组从个人产品迭代、Windows 工具、本地语音、文档与内容制作中提炼的 **8 个 Agent Skills**。重点是接管真实项目、定位执行差异、保护私人资料、验收最后的成品。不是提示词大礼包，也不是承诺自动完成所有任务的软件。

## Skills

| Skill | 适用场景 | 应交付什么 |
|---|---|---|
| [project-handoff-evidence](skills/project-handoff-evidence/SKILL.md) | 旧 Agent 交接、脏工作树、发布与远端确认 | 证据表、准确主源码、已验与待验分离 |
| [windows-desktop-layout](skills/windows-desktop-layout/SKILL.md) | 桌面图标四角排布、预览正确却落位失败 | 基于 Shell 标识的计划、快照、延迟回读 |
| [chinese-mobile-pdf-qa](skills/chinese-mobile-pdf-qa/SKILL.md) | 手机阅读的中文 PDF、截图文字重排 | 正确语义顺序、字体检查、实际渲染证据 |
| [local-tts-video-workflow](skills/local-tts-video-workflow/SKILL.md) | 本地配音导入剪辑、音色与语言错配 | 音色核对、试听、字幕、可播放成品 |
| [windows-gpu-runtime-audit](skills/windows-gpu-runtime-audit/SKILL.md) | 有显卡但应用跑 CPU、环境不支持 CUDA | 硬件/驱动/运行时/实际执行四层结论 |
| [fiction-continuity-audit](skills/fiction-continuity-audit/SKILL.md) | 小说时间线、视角、人物知识冲突 | 带原文锚点的发现，保留作者决策权 |
| [product-demo-proof](skills/product-demo-proof/SKILL.md) | 软件宣传视频、界面图与真实产品混淆 | 真实操作素材、事实边界、最终导出检查 |
| [private-knowledge-vault](skills/private-knowledge-vault/SKILL.md) | 聊天和工程资料整理为 Obsidian 知识库 | 私有可检索档案、覆盖清单、事实归属 |

## 使用

将需要的整个 skill 文件夹放入你的 Agent 支持的 Skills 目录，例如 Codex 的用户目录：

```text
~/.codex/skills/project-handoff-evidence/
  SKILL.md
  agents/openai.yaml
```

有脚本的 Skill 请保留其 `scripts/` 子目录。路径与导入方式以所用 Agent 的当前文档为准；此处不自动改配置、不安装依赖、不创建任务。

示例：

```text
用 $project-handoff-evidence 检查这个项目的接管信息；先只读，告诉我哪些完成声明有实际证据。
用 $windows-gpu-runtime-audit 检查应用为什么使用 CPU，不要升级驱动或改全局环境。
用 $chinese-mobile-pdf-qa 检查这个 PDF 的手机阅读体验和中文文字可提取性。
```

Skills 是给 Agent 的任务指导，仍依赖实际工具、环境和权限。不能代替用户授权，也不能保证模型一定正确。

## 小型检查工具

- `windows-gpu-runtime-audit/scripts/audit_gpu.ps1`：PowerShell 7，只读检查 Windows 设备、驱动与指定 Python 环境。不会下载模型、修改驱动、枚举凭证或配置接口。实际推理是否使用 GPU仍需观察应用。
- `chinese-mobile-pdf-qa/scripts/check_pdf.py`：依赖 `pypdf`，检查页数、提取文本、字体嵌入与 ToUnicode 的线索。会报告结构警告，**不能替代渲染和视觉检查**。

```text
pwsh -NoProfile -File skills/windows-gpu-runtime-audit/scripts/audit_gpu.ps1 -PythonPath <实际解释器路径>
python skills/chinese-mobile-pdf-qa/scripts/check_pdf.py <文件.pdf>
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

仓库自检仅用 Python 标准库；PDF 工具需要在你选择的环境安装 `pypdf`。不存在的环境或无显卡输出不被猜测成成功。

## 设计与验证

每个 Skill 包含触发条件、最短流程、停止条件和可观察的验收结果。仓库检查覆盖结构、界面元数据、相对资源、明显秘密模式与路径泄漏；单元测试覆盖 PDF 检查器的结构分支和技能完整性。

这些检查不等于跨模型实战评测。未宣称在所有 Agent、Windows 版本或文档类型下均已验证。

已运行检查及其局限见 [验证记录](TESTING.md)。

本仓库只发布原创通用工作方法和辅助检查代码。不包含个人聊天、客户材料、声纹、API 凭证、交易配置或私有项目源码。

## 参考

目录形式参考 [Agent Skills specification](https://agentskills.io/specification) 与 [官方示例](https://github.com/anthropics/skills)。Windows 定位方法依据 [微软桌面图标示例](https://devblogs.microsoft.com/oldnewthing/20130318-00/?p=4933) 与 [新版 Shell 图标管理说明](https://devblogs.microsoft.com/oldnewthing/20211122-00/?p=105948)。方法重新撰写，未复制第三方 Skills 或插件实现。

原创部分采用 [MIT License](LICENSE)。第三方依赖遵循各自许可证。
