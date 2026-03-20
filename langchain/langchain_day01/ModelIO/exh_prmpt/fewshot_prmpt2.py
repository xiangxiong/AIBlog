#少样本提示模版的使用
# from langchain.prompts import PromptTemplate
# from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

from models import get_lc_model_client

#获得访问大模型客户端
client = ChatTongyi()

# 创建示例，模型学习用户给的参照样本，安装样本进行回答
examples = [
    {"input": "如何重置密码？", "output": "密码重置可以通过绑定邮箱重置密码，也可以通过手机号重置密码"},
    {"input": "我的设备无法开机怎么办？", "output": "故障排除步骤：1.可能是遥控器电池没电，2.确认电源状态，3.确认设备是否被锁屏"},
    {"input": "这款产品是否有夜间模式？", "output": "这款不提供夜间模式，请选择xx款式的产品"},
]

# 配置一个提示模板，用来一个示例格式化
examples_prompt_tmplt_txt = "用户问题： {input} 对应回答： {output}"

# 这是一个提示模板的实例，用于设置每个示例的格式
prompt_sample = PromptTemplate.from_template(examples_prompt_tmplt_txt)

# 创建少样本示例的对象
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=prompt_sample,
    prefix="你是一个智能客服, 能够根据用户问题给出答案，",
    suffix="现在给你用户提问: {input} ，请告诉我对应的结果：",
    input_variables=["input"]
)
print(prompt.format(input="这款产品有防水模式？"))

print('-' * 50)

result = client.invoke(prompt.format(input="这款产品有防水模式？"))
print(result.content)
