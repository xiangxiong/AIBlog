#少样本提示模版的使用
# from langchain.prompts import PromptTemplate
# from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

from models import get_lc_model_client

#获得访问大模型客户端
client = ChatTongyi()

# 创建示例
examples = [
    {"sinput": "2+2", "soutput": "4", "sdescription": "加法运算"},
    {"sinput": "5-2", "soutput": "3", "sdescription": "减法运算"},
]

# 配置一个提示模板，用来一个示例格式化
examples_prompt_tmplt_txt = "算式： {sinput} 值： {soutput} 类型： {sdescription} "

# 这是一个提示模板的实例，用于设置每个示例的格式
# prompt_sample = PromptTemplate.from_template(examples_prompt_tmplt_txt)
prompt_sample = PromptTemplate(template=examples_prompt_tmplt_txt)

# 创建少样本示例的对象
prompt = FewShotPromptTemplate(
    examples=examples, # 示例样本
    example_prompt=prompt_sample, # 示例的提示模板
    prefix="你是一个数学专家, 能够准确说出算式的类型，", #前缀
    suffix="现在给你算式: {input} ， 值: {output} ，告诉我类型：", #后缀
    input_variables=["input", "output"]
)
print(prompt.format(input="2*5", output="10"))  # 你是一个数学专家,算式: 2*5  值: 10

print('-' * 50)

result = client.invoke(prompt.format(input="2*5", output="10"))
print(result.content)  # 使用: 乘法运算
