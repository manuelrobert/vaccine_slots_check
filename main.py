from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '85cdefc0d154fc149d383740d629a92a'

from home.routes import home
app.register_blueprint(home)

if __name__ == '__main__':
    app.run(debug=True)