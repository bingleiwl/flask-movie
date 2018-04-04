import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:bnlflw@127.0.0.1:3306/movie-flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '0d9acfcb1d574b0985a2fc4955a97a8f'
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')
#
db = SQLAlchemy(app)

from apps.home import home as home_blueprint
from apps.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint,)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


# 404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html')
