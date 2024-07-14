from db_config import app
from flask import request, render_template


#user
from routes.user import user
from routes.classify import image_bp

app.config['UPLOAD_FOLDER'] = 'uploads/'

app.register_blueprint(user,url_prefix="/user")
app.register_blueprint(image_bp,url_prefix="/classify")
app.secret_key = 'doxjjarjeh3die'
#mushroom1

#...

@app.route('/')
def home():
    # 获取闪现消息
    message = request.args.get('message')
    return render_template('login.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
