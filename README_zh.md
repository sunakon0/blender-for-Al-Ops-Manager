# 🤖 AI-Ops Manager (智能资产管家) - Blender 插件

![Blender Version](https://img.shields.io/badge/Blender-3.6%20%7C%204.0+-orange?logo=blender)
![AI Powered](https://img.shields.io/badge/AI-DeepSeek_R1-blue)
![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)

**AI-Ops Manager** 是一款基于 **DeepSeek-Reasoner (R1)** 推理模型开发的 Blender 智能化插件。它不仅能将自然语言转化为可执行的 Blender Python 脚本，还首创了“场景防错注入”和“一键报错修复”工作流，并允许你将好用的 AI 脚本固化为个人的专属工具库。

## ✨ 核心功能

* 🧠 **自然语言转脚本**：直接输入需求（例如：“将场景中所有高度小于5米的网格物体移入 'Low_Poly' 集合”），AI 即时生成规范的 Python 代码。
* 🎯 **智能上下文预设 (分类选择)**：在生成前选择任务类型（模型处理、材质节点、大纲整理、动画批处理）。插件会在后台自动向 AI 注入专家级的 API 限制条件，极大地降低 AI 幻觉和基础语法报错率。
* 🛠️ **一键报错智能修复**：运行代码报错了？只需将控制台的 Traceback 报错信息粘贴到插件指定的文本块中，点击“修复”，大模型会像真实程序员一样分析报错原因并覆盖正确代码。
* 📚 **构建专属脚本库**：对于测试成功的优秀脚本，输入名称并点击保存，它将作为实体按钮永久保留在界面的“常用脚本库”栏目中，一键复用，支持多设备打包分享。

## 📦 安装说明

1. 将本项目下载为 `.zip` 压缩包。
2. 打开 Blender，进入 `编辑 (Edit) > 偏好设置 (Preferences) > 插件 (Add-ons)`。
3. 点击 **安装 (Install...)** 并选择刚才下载的 `.zip` 文件。
4. 勾选启用 **AI-Ops Manager**。
5. **重要配置**：展开插件偏好设置面板，在 `DeepSeek API Key` 处填入你的密钥（可在 [DeepSeek 开放平台](https://platform.deepseek.com/) 申请）。

## 🚀 使用指南

### 1. 生成与运行
* 在 3D 视图按 `N` 键打开侧边栏，找到 **AI-Ops** 面板。
* 从下拉菜单中选择一个 **任务类型**（这对于提高代码成功率至关重要）。
* 在输入框中用自然语言描述你的需求。
* 点击 **生成脚本**，等待 AI 思考完成后，点击 **立即运行**。

### 2. 报错与修复
* 如果运行失败并产生报错，在面板的“报错修复中心”点击 **+ 号** 创建 `Error_Log` 日志块。
* 切换到 Blender 的文本编辑器 (Text Editor)，将系统控制台的红字报错粘贴进 `Error_Log`。
* 点击面板上的 **提交报错并智能修复**，AI 会自动修改并覆盖原脚本。

### 3. 沉淀与复用
* 当脚本完美运行后，在面板底部的输入框给它起个名字（例如 `批量材质重命名`），点击 **保存**。
* 这个功能会自动变成面板顶部“常用脚本库”里的一个按键，以后只需点击即可直接运行！

## 🤝 参与贡献
欢迎提交 Issue 和 Pull Request，或者在社区分享你用此插件生成的优秀 Python 自动化脚本！

## 📄 许可证
本项目采用 **[Creative Commons Zero v1.0 Universal (CC0 1.0)](https://creativecommons.org/publicdomain/zero/1.0/)** 许可证。这意味着本项目已完全贡献至公有领域（Public Domain）。任何人都可以自由地复制、修改、分发甚至用于商业用途，无需署名或请求许可。
