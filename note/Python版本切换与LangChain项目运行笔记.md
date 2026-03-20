# Python版本切换与LangChain项目运行笔记

## 1. Flask 项目如何运行

仓库中的 Flask 示例入口文件：

- `/Users/aishawn/code/AIBlog/flask/main.py`

最直接的运行方式：

```bash
cd /Users/aishawn/code/AIBlog/flask

python3 -m venv venv
source venv/bin/activate

pip install flask
python3 main.py
```

启动后访问：

```text
http://127.0.0.1:5000/
```

说明：

- `main.py` 中已经包含 `app.run(debug=True)`。
- 所以直接执行 `python3 main.py` 即可。
- `flask/requirements.txt` 很大，更像整机环境导出，不建议初次直接全装。

---

## 2. langchain 目录如何运行

`/Users/aishawn/code/AIBlog/langchain` 不是单一服务，而是一组示例脚本。

基础环境准备：

```bash
cd /Users/aishawn/code/AIBlog/langchain

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

常见运行方式：

### 2.1 本地 RAG 示例

```bash
cd /Users/aishawn/code/AIBlog/langchain/RAG
python3 VectoerRAG.py
python3 Search.py
```

说明：

- `VectoerRAG.py` 用于构建本地向量库。
- `Search.py` 会读取本地向量库并调用 DeepSeek 模型。
- 运行 `Search.py` 前通常需要：

```bash
export DEEPSEEK_API_KEY=你的key
```

### 2.2 Agent 与 Memory 示例

```bash
cd /Users/aishawn/code/AIBlog/langchain
python3 "Memory/带记忆的对话链.py"
python3 "Agent/Agent 调用计算器.py"
```

注意：

- `Agent 调用计算器.py` 中存在 `hub.pull(...)`，需要联网。
- `带记忆的对话链.py` 依赖 `ChatDeepSeek`，需要配置 API Key。

---

## 3. `langchain_classic==1.0.1` 安装失败的原因

报错：

```text
ERROR: Could not find a version that satisfies the requirement langchain_classic==1.0.1
ERROR: No matching distribution found for langchain_classic==1.0.1
```

原因不是包名写错，而是当前 Python 版本过低。

当时环境信息：

- Python 版本：`3.9.6`
- pip 版本：`21.2.4`

问题本质：

- `langchain-classic`、`langchain-community` 等新版本依赖要求 `Python >= 3.10`
- 当前环境是 `Python 3.9.6`
- 所以 `pip` 会直接过滤掉这些版本，最终提示找不到可安装版本

解决方式：

```bash
cd /Users/aishawn/code/AIBlog/langchain
rm -rf venv
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## 4. `python3.11` 找不到如何解决

报错：

```text
zsh: command not found: python3.11
```

实际检查结果：

- 系统自带 Python：`/usr/bin/python3`
- Homebrew 安装的 Python 3.11：`/opt/homebrew/bin/python3.11`

如果未安装 Python 3.11，可执行：

```bash
brew install python@3.11
```

检查版本：

```bash
/opt/homebrew/bin/python3.11 --version
```

如果想让当前 shell 优先使用 Homebrew 的 Python：

```bash
export PATH="/opt/homebrew/bin:$PATH"
hash -r
python3 --version
```

如果想永久生效，把下面一行写进 `~/.zshrc`：

```bash
export PATH="/opt/homebrew/bin:$PATH"
```

然后执行：

```bash
source ~/.zshrc
```

---

## 5. “是否创建虚拟环境” 提示是什么意思

提示大意：

> 你可能把 Python 包安装到了全局环境中，这可能导致版本冲突。是否创建虚拟环境来隔离依赖？

含义：

- 全局环境是多个项目共用的
- 不同项目之间容易产生包版本冲突
- 更推荐每个项目使用自己的虚拟环境

标准做法：

```bash
cd /Users/aishawn/code/AIBlog/langchain
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

激活成功后，命令行前面会出现 `(venv)`。

---

## 6. `ModuleNotFoundError: No module named 'openai'` 如何解决

报错示例：

```text
ModuleNotFoundError: No module named 'openai'
```

含义：

- 当前运行脚本所使用的 Python 环境中，没有安装 `openai`

解决方式：

```bash
cd /Users/aishawn/code/AIBlog/langchain
source venv/bin/activate
pip install openai
python "langchain_day01/ModelIO/helloworld.py"
```

---

## 7. `langchain_day01` 项目如何运行

目录：

- `/Users/aishawn/code/AIBlog/langchain/langchain_day01`

这个目录也不是单一应用，而是一组示例脚本。

### 7.1 基础依赖安装

先进入目录并激活虚拟环境：

```bash
cd /Users/aishawn/code/AIBlog/langchain/langchain_day01
source venv/bin/activate
python -m pip install --upgrade pip
```

最小依赖建议先安装：

```bash
pip install openai langchain-openai langchain-community
```

如果要运行 Web 服务，还需要：

```bash
pip install fastapi uvicorn langserve
```

### 7.2 配置环境变量

这个目录里的代码默认偏向阿里百炼和 DeepSeek。

阿里百炼：

```bash
export DASHSCOPE_API_KEY=你的key
```

DeepSeek：

```bash
export Deepseek_Key=你的key
```

### 7.3 运行单文件示例

`helloworld.py`：

```bash
cd /Users/aishawn/code/AIBlog/langchain/langchain_day01
source venv/bin/activate
python "ModelIO/helloworld.py"
```

说明：

- 该脚本使用了 `ChatTongyi()`。
- 没有配置 `DASHSCOPE_API_KEY` 时会报鉴权错误。

### 7.4 运行 Web 服务

入口文件：

- `/Users/aishawn/code/AIBlog/langchain/langchain_day01/ModelIO/deploy_service.py`

运行命令：

```bash
cd /Users/aishawn/code/AIBlog/langchain/langchain_day01
source venv/bin/activate
python "ModelIO/deploy_service.py"
```

启动后访问：

```text
http://localhost:8000
http://localhost:8000/lanchainServer
```

客户端脚本：

```bash
python "ModelIO/deploy_client.py"
```

---

## 8. 为什么上级 `langchain` 安装过包，`langchain_day01` 还会提示缺包

核心原因：

- Python 包不是按目录共享的
- Python 包是按“当前解释器 / 当前虚拟环境”隔离的

例如：

- 在 `/Users/aishawn/code/AIBlog/langchain/venv` 安装的包
- 不会自动给 `/Users/aishawn/code/AIBlog/langchain/langchain_day01/venv` 使用
- 也不会自动给系统 Python 使用

所以判断依据不是“父目录是否安装过”，而是“当前脚本到底用哪个 Python 在运行”。

检查当前 Python：

```bash
which python
python --version
python -c "import sys; print(sys.executable)"
```

如果想复用上级 `langchain` 的环境：

```bash
cd /Users/aishawn/code/AIBlog/langchain
source venv/bin/activate
python "langchain_day01/ModelIO/helloworld.py"
```

---

## 9. 如何切换到指定版本的 Python

这台机器上确认可用的 3.11 路径为：

```bash
/opt/homebrew/bin/python3.11
```

### 9.1 临时使用指定版本

```bash
/opt/homebrew/bin/python3.11 --version
/opt/homebrew/bin/python3.11 your_script.py
```

### 9.2 当前 shell 会话切换

```bash
export PATH="/opt/homebrew/bin:$PATH"
hash -r
python3 --version
```

### 9.3 项目内固定使用 3.11

```bash
cd /Users/aishawn/code/AIBlog/langchain
rm -rf venv
/opt/homebrew/bin/python3.11 -m venv venv
source venv/bin/activate
python --version
```

推荐做法：

- 不直接改系统 Python
- 每个项目使用对应 Python 版本单独创建 `venv`

---

## 10. 结论

这次对话的核心结论如下：

- Flask 示例可以直接运行 `python3 main.py`
- `langchain` 和 `langchain_day01` 都是脚本集合，不是统一服务
- LangChain 新版本依赖通常要求 `Python >= 3.10`
- 当前机器应优先使用 `/opt/homebrew/bin/python3.11`
- 包是否可用，取决于当前激活的虚拟环境，而不是目录层级
- 运行前通常需要先完成三件事：切换正确 Python、激活正确 venv、安装对应依赖

