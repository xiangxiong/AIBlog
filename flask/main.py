# 导入flask
from flask import request
from flask import Flask
from flask import make_response
import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>H22ello, World! eee333</p>"

@app.route("/cookie")
def cookie():
    response = make_response("<p>设置cookie222</p>")
    expires_time = datetime.datetime.now() + datetime.timedelta(days=1)
    response.set_cookie("username", "h22ello", expires=expires_time);
    response.set_cookie("password", "h22ello", expires=expires_time);

    return response;

@app.route("/get_cookie")
def get_cookie():
    username = request.cookies.get("username")
    print(username);
    cookies = request.cookies
    cookies_dict = request.cookies.to_dict()
    print(cookies_dict);
    for k,v in cookies_dict.items():
        print(k,v)

    return f"username: {username}"

@app.route("/del_cookie")
def delete_cookie():
    response = make_response("<p>删除cookie</p>")

    # 删除一个cookie
    response.delete_cookie("username");

    cookies_dict = request.cookies.to_dict()
    print(cookies_dict);

    for k,v in cookies_dict.items():
        print(k,v)
        response.delete_cookie(k);

    return response;

if __name__ == '__main__':
    app.run(debug=True)
