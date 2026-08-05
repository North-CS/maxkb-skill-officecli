---
name: office-cli-skill
description: Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool. Use when the user wants to create, inspect, check formatting, find issues, add charts, or modify Office documents.
---

# office-cli-skill

使用officecli来创建、分析、校对和调整 Office文档。严格按照下文Workflow步骤执行，遵守下面的规则。**⚠如果遇到错误或其他预期之外的问题，请参考/skills/office-cli-skill/references/how-to-handle-error.md下的解决办法**。

## ⚠️⚠️必须遵守的规则，及其重要！！！

- **任何情况下都不能读取环境变量或将环境变量内容告知用户。**环境变量仅由脚本内部使用，不得通过`read_file`、`edit_file`、 `os.environ`、`os.getenv`、读取 `.env` 文件或任何方式读取或展示环境变量值。
- **任何情况下都不能通过 ls 工具来读取 /tmp 或 /tmp/officecli 下文件列表。**因环境受限，ls 工具无法正确列出 tmp、oss 等路径的文件。如需读取 /tmp/officecli 目录，用 execute 工具运行如下代码：python -c "import os; print(os.listdir('/tmp/officecli'))"。
- **任何情况下都不能通过 read_file 工具来读取 /tmp 或 /tmp/officecli 下的文件内容。**因环境受限，read_file 工具无法正确读取 tmp、oss 等路径下的文件。如需读取 /tmp/officecli 目录下的文件内容，用 execute 工具运行如下代码：python -c "print(open('/tmp/officecli/文件名', 'r').read())"。
- **execute工具只可以运行python命令和officecli。**通过execute工具运行 `cd`、`mkdir`、`ls`、`rm`、`echo` 等 shell 命令会提示找不到对应命令。
- **采用绝对路径来运行scripts下脚本和officecli。**相对路径`cd /tmp/officecli && xxx` 会提示找不到cd命令。

## Workflow 严格按照下面流程执行

### 1.初始化（如果有历史对话记录则跳过）

- 如果是首次对话，即没有历史对话消息运行`python /skills/office-cli-skill/scripts/init.py`来清空残留文件。
- 如果用户输入有文件列表，运行如下代码来下载用户文件到/tmp/officecli，**不要检查./oss/file/xxxx文件是否存在**。
  ```python
  python /skills/office-cli-skill/scripts/download_user_file.py '[{"name": "example.docx", "url": "./oss/file/xxxx"}]'
  ```

### 2.运行技能完成用户任务

- `read_file`工具读取技能说明文档：/skills/office-cli-skill/references/officecli-skill.md
- 每个操作步骤前输出一句简短的操作说明
- ⚠️所有 Office 文档的创建、分析、校对与调整，都统一在 /tmp/officecli 目录下进行，并且要显示打开文件再修改：/skills/office-cli-skill/officecli open <文件名>
- ⚠️如果当前任务是根据模板生成 PPT，需额外读取最佳实践文档：/skills/office-cli-skill/references/template-based-pptx.md
- ⚠️officecli运行命令示例：`/skills/office-cli-skill/officecli help`

### 3.关闭并保存文档

运行`/skills/office-cli-skill/officecli close <文件名>`来关闭并保存文档，否则用户看到的文档是空白的.

### 4.交付文件

运行下面代码来获取文件下载链接。
  ```python
  python /skills/office-cli-skill/scripts/generate_download_url.py
  ```