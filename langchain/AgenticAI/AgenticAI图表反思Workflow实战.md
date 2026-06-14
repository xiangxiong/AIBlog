# 从 0 到 1 实现 Agentic AI 反思模式：让 LLM 自动画图并自我改进

> 本文基于 DeepLearning AI M2 实验，在本地用 **智谱 GLM** 跑通「生成图表 → 执行 → 反思 → 改进」完整 workflow，并整理为可独立运行的 Python 脚本。  
> 代码仓库：[AIBlog/langchain/AgenticAI](https://github.com/xiangxiong/AIBlog/tree/main/langchain/AgenticAI)

---

## 写在前面

很多人第一次用 LLM 做数据分析，流程是这样的：

> 问 ChatGPT → 复制代码 → 运行 → 图不对 → 再问一遍 → 再复制……

这其实是 **单次问答**，不是 **Agent**。

Agentic AI 里有一个非常经典的设计模式叫 **Reflection（反思）**：

1. 先让 LLM 生成一版结果（V1）
2. 再让 LLM **审查** 这版结果哪里不好
3. 基于审查意见生成改进版（V2）

这篇文章会用「咖啡销售数据可视化」这个例子，带你理解并跑通整个流程。

---

## 一、我们要解决什么问题？

**任务：** 用自然语言描述需求，自动生成 matplotlib 图表。

**示例需求：**

> Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv.

**期望输出：**

- 第一版图表 `chart_v1.png`
- LLM 对 V1 的文字点评（feedback）
- 改进版图表 `chart_v2.png`

**核心难点不在「会不会画图」，而在：**

- LLM 输出的是**文本**，怎么变成**可执行代码**？
- 代码执行后产生**图片**，怎么让 LLM **看见**并改进？
- 如何把以上步骤串成**自动化 pipeline**？

---

## 二、整体架构：四步 Workflow

```text
用户 instruction（文字）
        ↓
┌───────────────────────────────────────┐
│ Step 1  generate_chart_code           │  文本 LLM 写 matplotlib 代码
└───────────────────────────────────────┘
        ↓ code_v1（含 <execute_python> 标签）
┌───────────────────────────────────────┐
│ Step 2  extract_and_exec              │  正则提取 + exec 执行
└───────────────────────────────────────┘
        ↓ chart_v1.png
┌───────────────────────────────────────┐
│ Step 3  reflect_on_image_and_regenerate│  视觉 LLM 看图 + 写 V2 代码
└───────────────────────────────────────┘
        ↓ feedback + code_v2
┌───────────────────────────────────────┐
│ Step 4  extract_and_exec              │  再执行一次
└───────────────────────────────────────┘
        ↓ chart_v2.png
```

用三个角色来理解：

| 角色 | 做什么 | 对应函数 |
|------|--------|----------|
| 程序员 | 写 Python 绘图代码 | `generate_chart_code` |
| 运行环境 | 执行代码、保存 png | `extract_and_exec` |
| 审查员 | 看图挑毛病、写改进代码 | `reflect_on_image_and_regenerate` |
| 调度员 | 串联全流程 | `run_workflow` |

这就是 **Reflection Pattern**：不是一次生成完事，而是 **Generate → Execute → Reflect → Refine**。

---

## 三、三个关键机制

### 1. Prompt：真正驱动 LLM 行为的是提示词

Step 1 并不直接画图，而是构造一段 prompt 发给 LLM：

```python
def generate_chart_code(instruction: str, model: str, out_path_v1: str) -> str:
    prompt = f"""
    You are a data visualization expert.
    ...
    User instruction: {instruction}
    ...
    Return ONLY the code wrapped in <execute_python> tags.
    """
    return utils.get_response(model, prompt)
```

Prompt 里固定了：

- 数据 schema（`df` 有哪些列）
- 必须用 matplotlib
- 保存路径、dpi、`plt.close()` 等约束
- 输出格式必须用 `<execute_python>` 包裹

**改 prompt = 改 Agent 行为**，这是 Agent 开发里最重要的杠杆之一。

### 2. `<execute_python>` 标签：从 LLM 文本里抠出可执行代码

LLM 返回的往往是「解释 + 代码 + markdown」，程序很难直接运行。

所以约定：代码必须写在标签里：

```text
<execute_python>
import matplotlib.pyplot as plt
...
plt.savefig('chart_v1.png')
plt.close()
</execute_python>
```

提取并执行：

```python
def extract_and_exec(code_with_tags: str, df) -> None:
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", code_with_tags)
    if not match:
        raise RuntimeError("未找到 <execute_python> 代码块")
    exec(match.group(1).strip(), {"df": df})
```

- `re.search`：正则提取标签内 Python
- `exec(..., {"df": df})`：在只有 `df` 的环境里动态执行

这就是 Agent 的 **Code Execution Tool（代码执行工具）**。

### 3. 视觉反思：把图片发给 LLM「看」

Step 3 和 Step 1 最大的区别：**输入里多了图片**。

```python
feedback, code_v2 = reflect_on_image_and_regenerate(
    chart_path=out_v1,           # V1 图片路径
    instruction=user_instructions,
    model_name=reflection_model, # 视觉模型，如 glm-4v-plus
    out_path_v2=out_v2,
    code_v1=code_v1,             # 原始代码，供对照
)
```

内部流程：

1. 把 `chart_v1.png` 转成 base64
2. prompt + 图片一起发给视觉模型
3. 解析返回：第一行 JSON（feedback）+ 改进代码（`<execute_python>`）

模型返回示例：

```text
{"feedback": "The legend is unclear and the axis labels overlap."}

<execute_python>
...
</execute_python>
```

我本地跑的一次真实 feedback：

> The original code does not include a legend for the bars, making it unclear which color represents which year.

V2 代码 accordingly 加了明确的颜色和 legend——这就是反思的价值。

---

## 四、和普通 ChatGPT 问一句的区别

| 普通问答 | 本 Workflow |
|----------|-------------|
| 你问 → AI 答 → 结束 | 多步 pipeline，有中间产物 |
| 输出是文字 | 输出是可执行代码 + 图片文件 |
| 没有自我检查 | 有 Reflection 循环 |
| 你手动复制代码运行 | 程序自动 `exec` |
| 通常一个模型 | 可拆分：文本模型写代码 + 视觉模型反思 |

**Agentic AI 的本质**：LLM 不只是一个「聊天框」，而是 workflow 里的一个**可编排节点**。

---

## 五、本地跑通：智谱 GLM 配置

课程原版用 OpenAI，国内直连 often 超时。我用 **智谱 OpenAI 兼容接口** 跑通，模型分工：

| 步骤 | 模型 | 原因 |
|------|------|------|
| 生成 V1 代码 | `glm-4-flash` | 快、便宜、写代码够用 |
| 看图反思 V2 | `glm-4v-plus` | 支持视觉输入 |

### 1. 环境准备

```bash
cd langchain/AgenticAI
python -m venv .venv
source .venv/bin/activate
pip install pandas matplotlib python-dotenv openai jupyter
```

### 2. 配置 `.env`

```bash
ZHIPU_API_KEY=你的智谱Key
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
GLM_GENERATION_MODEL=glm-4-flash
GLM_REFLECTION_MODEL=glm-4v-plus
```

Key 在 [智谱开放平台](https://open.bigmodel.cn) 申请。`.env` 不要提交 Git。

### 3. 方式 A：Jupyter Notebook

```bash
jupyter notebook M2_UGL_1.ipynb
```

按 cell 顺序运行，适合学习和调试。

### 4. 方式 B：独立 Python 脚本（推荐日常使用）

```bash
python run_chart_workflow.py
```

自定义需求：

```bash
python run_chart_workflow.py \
  --instruction "Create a bar chart of total Q1 sales by coffee_name for 2024 vs 2025" \
  --basename my_chart
```

成功后会生成 `my_chart_v1.png` 和 `my_chart_v2.png`，终端打印每步日志和 feedback。

---

## 六、项目文件说明

```text
langchain/AgenticAI/
├── M2_UGL_1.ipynb          # 课程 notebook（已翻译中文说明）
├── run_chart_workflow.py   # 独立脚本，终端一键跑 workflow
├── utils.py                # 数据加载、LLM 调用、图片编码
├── coffee_sales.csv        # 示例数据集
└── .env                    # API Key（本地，不入库）
```

`run_workflow` 核心逻辑（简化）：

```python
def run_workflow(...):
    df = utils.load_and_prepare_data(dataset_path)

    code_v1 = generate_chart_code(user_instructions, generation_model, out_v1)
    extract_and_exec(code_v1, df)

    feedback, code_v2 = reflect_on_image_and_regenerate(
        chart_path=out_v1,
        instruction=user_instructions,
        model_name=reflection_model,
        out_path_v2=out_v2,
        code_v1=code_v1,
    )
    extract_and_exec(code_v2, df)

    return {"code_v1", "chart_v1", "feedback", "code_v2", "chart_v2"}
```

---

## 七、我踩过的坑

**1. OpenAI API 连不上**

表现：`APITimeoutError: Request timed out`  
解决：换智谱，或配置可用的 API 中转。

**2. Key 写错环境变量名**

智谱 Key 写在 `OPENAI_API_KEY` 下，`utils.py` 读不到 `ZHIPU_API_KEY` 会走错客户端。  
解决：`.env` 里用 `ZHIPU_API_KEY=...`。

**3. 反思步骤用了非视觉模型**

纯文本模型无法「看图」，feedback 质量会很差。  
解决：Step 3 必须用 `glm-4v-plus` 这类视觉模型。

**4. `exec` 的安全问题**

`exec` 会运行 LLM 生成的任意 Python。实验环境可以接受；生产环境需要沙箱或白名单 API。

---

## 八、可以怎么扩展？

1. **换数据集**：改 `--dataset`，prompt 里同步 schema  
2. **多轮反思**：V2 不满意 → 再 reflect 出 V3（循环 Reflection）  
3. **接入 LangGraph**：把四步变成状态机节点，更易观测和分支  
4. **换模型**：DeepSeek 写代码 + 通义千问 VL 反思（混合方案）  
5. **去掉 exec**：改为 Jupyter kernel 或 Docker 沙箱执行

---

## 九、总结

| 概念 | 一句话 |
|------|--------|
| Reflection Pattern | 生成 → 检查 → 改进，而不是一次出结果 |
| `<execute_python>` | 让程序从 LLM 文本里可靠提取代码 |
| `exec` | Agent 的代码执行能力 |
| 双模型 | 文本模型写代码，视觉模型看图反思 |
| Workflow | 多步 pipeline，每步有明确输入输出 |

如果你刚接触 Agentic AI，建议学习路径：

1. 先跑通 `python run_chart_workflow.py`，对比 v1 / v2 两张图  
2. 对照终端 feedback，理解 Step 3 改了什么  
3. 读 `generate_chart_code` 的 prompt，试改一条约束看输出变化  
4. 再打开 notebook，逐步单 cell 调试  


**如果这篇文章对你有帮助，欢迎 Star 仓库或在 Issue 里交流。** 下一篇可以写：如何把这套 workflow 用 LangGraph 重构，或 Reflection 与 Tool Calling 怎么配合使用。
