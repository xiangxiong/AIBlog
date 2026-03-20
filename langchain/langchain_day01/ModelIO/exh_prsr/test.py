from datetime import datetime
from langchain_core.output_parsers import BaseOutputParser
from models import get_lc_model_client
from langchain.prompts import PromptTemplate
import datetime


client = get_lc_model_client()

# --- 自定义日期字符串解析器 ---
#  1.要求通过提示词，规范大模型的返回结果：字符串类型的结果
#  2.将大模型返回的字符串结果，进行解析，解析成指定的格式
class DateStringParser(BaseOutputParser[str]):
    # 定义模型应该输出的字符串格式，也是默认返回的格式
    target_format: str = "%Y-%m-%d"

    # 解析：将大模型返回结果，按照要求解析成想要的格式
    def parse(self, text: str) -> str:
        """
        接收模型的原始输出字符串，将其解析、验证并返回格式化后的字符串。
        """
        stripped_text = text.strip()

        try:
            # 使用 datetime.strptime 尝试解析字符串。
            # 如果字符串不符合 self.target_format，将抛出 ValueError
            print("尝试解析字符串:", stripped_text)

            dt_object = datetime.datetime.strptime(stripped_text, self.target_format)
            return dt_object.strftime(self.target_format)

        except ValueError as e:
            # 如果解析失败，抛出 LangChain 异常以便链可以处理错误
            from langchain_core.exceptions import OutputParserException
            raise OutputParserException(
                f"模型输出的日期格式不正确。期望格式为 '{self.target_format}'，但收到了: '{stripped_text}'. 错误: {e}"
            )

    # 规范大模型的输出的格式，返回的是提示词
    def get_format_instructions(self) -> str:
        """返回给 LLM 的指令，要求它输出特定的日期格式。"""
        # 使用当前日期作为示例，指导模型输出正确的格式
        example_date = datetime.datetime.now().strftime(self.target_format)
        print("当前期望格式:", self.target_format)
        return (
            f"请严格按照以下格式输出日期：'{self.target_format}'.\n"
            f"例如: {example_date}\n"
            f"只返回日期字符串，不要包含任何其他文本、空格或标点符号！"
        )


# --- 3. 组装 LCEL 链,测试自定义结果解析器效果 ---

# 实例化自定义解析器 可以在这里指定不同的日期格式
# date_parser = DateStringParser(target_format="%Y-%m-%d")
date_parser = DateStringParser(target_format="%m/%d/%Y %H:%M:%S")
# date_parser = DateStringParser(target_format="%d/%m/%Y")

# 定义模板
template = """
回答用户的问题：{question}

{format_instructions}  
"""

prompt = PromptTemplate.from_template(
    template,
    partial_variables={"format_instructions": date_parser.get_format_instructions()},
)

# 链式调用：使用自定义解析器作为最后一个组件
chain = prompt | client | date_parser

# --- 4. 执行并打印输出 ---
# question = "新中国是什么时候成立的？"
question = "北京夏季奥运会的开幕时间是？"

output = chain.invoke({"question": question})
print(output)

