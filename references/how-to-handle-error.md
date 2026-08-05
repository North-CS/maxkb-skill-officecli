# 常见问题及解决办法

## 1. 文件相关问题

### 操作完后的文件没有找到
- 确认是否用了 `ls` 工具读取 `/tmp` 或 `/tmp/officecli` 下的文件列表——`ls` 工具无法正确列出这些路径。
- 正确做法：用 execute 工具运行 `python -c "import os; print(os.listdir('/tmp/officecli'))"` 来查看文件。

### 用户收到的文档没有内容
- 确认交付文件前是否运行了 `close` 命令关闭并保存文档。
- 正确做法：`/skills/office-cli-skill/officecli close <文件名>`

### 下载用户文件后找不到文件
- 确认是否重命名了文件——脚本会保留原文件名，不会重命名为 `input.xxx`。
- 确认文件是否下载到了 `/tmp/officecli` 目录，而非 `/tmp` 根目录。

## 2. 运行及权限问题

### execute 命令执行错误：找不到命令
- execute 工具**只能运行 `python` 命令**。
- `cd`、`mkdir`、`ls`、`rm`、`echo` 等 shell 命令会提示找不到对应命令。
- 如果需要多条命令，用 python 脚本代替，例如：
  ```python
  python -c "import os; os.makedirs('/tmp/officecli', exist_ok=True)"
  ```

### 各种权限问题、执行错误
- AI 仅对 `/tmp` 下有读写权限，对 `/skills` 或其他目录只有读权限，无写权限。
- 遇到此类问题直接放弃任务并向用户报告。

## 3. 因未遵守 SKILL.md 规则导致的问题

### 读取了环境变量
- **禁止**通过 `read_file`、`edit_file`、`os.environ`、`os.getenv`、读取 `.env` 文件等方式读取或展示环境变量值。
- 环境变量仅由脚本内部使用，脚本会自动从 `.env` 加载，无需手动读取。

### 使用了相对路径
- 运行 scripts 下脚本和 officecli 必须使用**绝对路径**。
- ❌ `cd /tmp/officecli && officecli help`（`cd` 不可用，且 `officecli` 缺少绝对路径）
- ✅ `/skills/office-cli-skill/officecli help`

### 未初始化就开始操作
- 首次对话必须先运行 `python /skills/office-cli-skill/scripts/init.py` 清空残留文件，否则可能使用到上次遗留的旧文件。

### 未按 Workflow 顺序执行
- 必须严格按照 SKILL.md 中的 Workflow 步骤执行：初始化 → 完成任务 → 关闭保存 → 交付文件。
- 跳过"关闭并保存文档"步骤会导致用户收到空白文档。
- 跳过"初始化"步骤可能使用到残留的旧文件。
