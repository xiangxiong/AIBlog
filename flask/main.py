
# 导入flask
from flask import request
from flask import Flask
from flask import make_response
from flask import session
import datetime
import os;

app = Flask(__name__)

# 启用session
app.config["SECRET_KEY"] = os.urandom(24); # 生成一个随机的24位字节, 作为session的密钥

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

# 操作session

# 添加session
@app.route("/add_session")
def add_session():
    session['username'] = "h22ello"
    session['nickname'] = "zhangsan"
    session['password'] = "h22ello"
    return "<p>添加session成功</p>"

@app.route("/get_session")
def get_session():
    username = session.get('username')
    print(session)
    return "<p>获取session成功</p>"+ f"username: {username}"

@app.route("/del_session")
def del_session():
    session.pop('username')
    session.pop('nickname')
    session.pop('password')
    return "<p>删除session成功</p>"

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask;
# from controller.user import user;
# app.register_blueprint(user);
# app = Flask(__name__)
# if __name__ == '__main__':
#     app.run(debug=True)

