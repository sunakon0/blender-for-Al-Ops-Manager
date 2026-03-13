# blender-for-Al-Ops-Manager
 Generate automated Python scripts for different requirements using natural language
# 🤖 AI-Ops Manager for Blender

![Blender Version](https://img.shields.io/badge/Blender-3.6%20%7C%204.0+-orange?logo=blender)
![AI Powered](https://img.shields.io/badge/AI-DeepSeek_R1-blue)
![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)

**AI-Ops Manager** is an intelligent Blender add-on powered by the **DeepSeek-Reasoner (R1)** model. It transforms natural language into executable Blender Python (bpy) scripts, featuring smart context injection, one-click execution, automated error fixing, and a reusable local script library.

## ✨ Key Features

* 🧠 **Natural Language to Script**: Describe your needs (e.g., "Assign a red material to all selected cubes"), and the AI will generate standard, efficient Blender Python code.
* 🎯 **Smart Context Injection (Category Selection)**: Select the task context (Model, Material, Outliner, Animation) before generating. The add-on automatically injects expert-level constraints to prevent common API errors (e.g., forcing the AI to use `bmesh` for geometry or ensuring `use_nodes=True` for materials).
* 🛠️ **AI-Powered Bug Fixing**: Encountered a Python Traceback? Simply paste the error log into the built-in Text Editor, click "Fix," and the AI will analyze the traceback and rewrite the correct code for you.
* 📚 **Reusable Script Library**: Save successfully generated scripts as permanent buttons in your UI. Build your own studio's toolset without writing a single line of code manually.

## 📦 Installation

1. Download the repository as a `.zip` file.
2. Open Blender and go to `Edit > Preferences > Add-ons`.
3. Click **Install...** and select the `.zip` file.
4. Check the box to enable **AI-Ops Manager**.
5. **Crucial Step**: Expand the add-on preferences and enter your `DeepSeek API Key` (Get it from [DeepSeek Platform](https://platform.deepseek.com/)).

## 🚀 How to Use

### 1. Generate & Run
* Open the **3D Viewport Sidebar (N-Panel)** and find the **AI-Ops** tab.
* Select a **Task Category** (General, Model, Material, Outliner, Animation) from the dropdown. *This drastically improves AI accuracy!*
* Type your prompt in the text box.
* Click **Generate Script**, wait a few seconds, and then click **Run Script**.

### 2. Debug & Fix
* If the script throws an error, click the **+** icon in the "Error Fixer" section to create an `Error_Log` text block.
* Open Blender's Text Editor, paste the Traceback from the System Console into `Error_Log`.
* Click **Submit Error and Fix Script**. The AI will patch your code automatically.

### 3. Save as Tool
* Once a script works perfectly, type a name (e.g., `Clean_Empty_Collections`) in the bottom section and click **Save**.
* Your new tool will permanently appear in the **Script Library** section at the top!

## 🤝 Contributing
Issues and Pull Requests are welcome! Feel free to share the custom tools you generated using this add-on.

## 📄 License
This project is dedicated to the public domain under the **[Creative Commons Zero v1.0 Universal (CC0 1.0)](https://creativecommons.org/publicdomain/zero/1.0/)** License. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.
