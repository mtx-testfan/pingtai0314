from flask import Flask, render_template

# 创建app
from automation import automation
from interface import interface
from variable import variable

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(interface)
app.register_blueprint(variable)
app.register_blueprint(automation)
# 路由---返回的资源  testfan
@app.route('/')
def index():
    return render_template('index.html',title='testfan测试平台')



if __name__ == '__main__':
    app.run(debug=True)