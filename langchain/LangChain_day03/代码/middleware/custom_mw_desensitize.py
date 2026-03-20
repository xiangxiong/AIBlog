import os
from dotenv import load_dotenv
# 验证模型连接
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), model="qwen-max",base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# 创建自定义脱敏中间件
from langchain.agents.middleware import AgentMiddleware
from typing import Any, Dict
import re
# 自定义中间件，中间件实现脱敏的，去除电话号码和邮箱信息
class DesensitizeDataMiddleware(AgentMiddleware):
    """脱敏中间件"""

    def __init__(self, patterns: list = None):
        super().__init__()
        self.patterns = patterns or [
            (r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[EMAIL]'),
            (r'(\+86)?1[3-9]\d{9}', '[PHONE]')
        ]

    def _desensitize_text(self, text: str) -> str:
        # 如果内容为空或已经包含脱敏标记，则跳过处理
        if not text or '[EMAIL]' in text or '[PHONE]' in text:
            return text
        # 快速预检查：只有当可能包含敏感信息时才继续处理
        if '@' not in text and not re.search(r'1[3-9]\d{9}', text):
            return text
        print(f"脱敏前: {text}")
        original_text = text
        for pattern, replacement in self.patterns:
            text = re.sub(pattern, replacement, text)
        # 只有当内容发生变化时才打印
        if original_text != text:
            print(f"脱敏后: {text}")
        return text

    def before_model(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """在模型调用前处理"""
        print("中间件DesensitizeDataMiddleware - before_model 被调用")
        if 'messages' in state:
            messages = state['messages']
            processed_any = False
            for message in messages:
                if hasattr(message, 'content') and isinstance(message.content, str):
                    # 只处理非空内容且未被脱敏的内容
                    if message.content and '[EMAIL]' not in message.content and '[PHONE]' not in message.content:
                        # 快速预检查：只有当可能包含敏感信息时才继续处理
                        if '@' in message.content or re.search(r'1[3-9]\d{9}', message.content):
                            # 只有在真正需要处理时才打印日志
                            if not processed_any:
                                print("进行脱敏处理.....")
                            original_content = message.content
                            message.content = self._desensitize_text(message.content)
                            # 只有当内容发生变化时才打印
                            if original_content != message.content:
                                print(f"消息内容已从 '{original_content}' 修改为 '{message.content}'")
                                processed_any = True
            if processed_any:
                print("脱敏处理完成！")
        return state

    def after_model(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """在模型调用后处理"""
        # 只有在真正处理了内容时才打印
        # 这里可以添加后处理逻辑
        return state

# 创建修复后的中间件
desed_middleware = DesensitizeDataMiddleware()

# ===== 测试中间件功能 =====

print("\n" + "=" * 50)
print("开始测试中间件功能")
print("=" * 50)

try:
    # 导入必要的组件
    from langchain_community.agent_toolkits.load_tools import load_tools
    from langgraph.checkpoint.memory import InMemorySaver
    from langchain.agents import create_agent

    # 导入工具，load_tools支持的工具可以在load_tools.py中查看
    tools = load_tools(["arxiv"])

    # 创建短期记忆实例
    memory = InMemorySaver()

    # 系统提示词设计
    system_prompt = "你是一个专业的论文查询助手，使用arxiv工具为用户查询论文信息，回答需简洁准确，包含论文标题、作者、发表时间和核心摘要。"

    # 创建带中间件的Agent
    agent_with_middleware = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=memory,
        # 加入脱敏的中间件
        middleware=[desed_middleware]
    )

    # 测试---
    # 测试: 包含电子邮件的输入
    print("测试: 电子邮件脱敏")
    email_input = "我的邮箱是test.user@example.com，请帮我查询论文1605.08386"
    print(f"输入内容: {email_input}")

    result1 = agent_with_middleware.invoke(
        {"messages": [{"role": "user", "content": email_input}]},
        config={"configurable": {"thread_id": "middleware_test_1"}}
    )
    print("结果:", result1["messages"][-1].content)

except Exception as e:
    print(f"中间件版本仍然失败: {e}")