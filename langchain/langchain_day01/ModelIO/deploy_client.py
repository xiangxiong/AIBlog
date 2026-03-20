#使用LangChain编写客户端访问我们基于LangServer的WEB服务
#对于其他编程语言来说，可以使用RESTful API来调用我们的服务
'''比如在postman或者apifox中访问http://localhost:8000/tslServer/invoke
在body中选择json，然后输入
{
    "input":
    {
        "language":"意大利文",
        "text":"为了部落！"
    }
}'''
from langserve import RemoteRunnable

if __name__ == "__main__":
    client = RemoteRunnable("http://localhost:8000/lanchainServer")
    print(client.invoke({'language': '意大利文', 'text': '我喜欢编程'}))