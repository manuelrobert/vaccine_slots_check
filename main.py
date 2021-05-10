from flask import Flask

app = Flask(__name__)

from home.routes import home
app.register_blueprint(home)

if __name__ == '__main__':
    app.run(debug=True)