
from langchain_community.chat_message_histories import RedisChatMessageHistory
from models import get_lc_model_client
# pip install redis
# session_id 识别用户   0.3版本中 redis_url 访问路径
# history = RedisChatMessageHistory(session_id="my_session_id", redis_url="redis://localhost:6379")
# langchain 1.0  url
history = RedisChatMessageHistory(session_id="my_session_id1", url="redis://localhost:6379")


# history.clear()  清空历史消息

client = get_lc_model_client()
# # 第一次对话
# history.add_user_message("你是谁？")
# aimessage = client.invoke(history.messages)
# history.add_ai_message(aimessage)
# print(aimessage)
# print("==================")
# 第二次对话
history.add_user_message("重复一次")
print(history.messages)
aimessage = client.invoke(history.messages)
history.add_ai_message(aimessage)
print(aimessage)




