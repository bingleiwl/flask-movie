
from flask import render_template, redirect, url_for
__author__ = 'bnk'

from . import  home


# 主页
@home.route('/')
def index():
    return render_template('/home/index.html')


# 登陆页
@home.route('/login/')
def login():
    return render_template('/home/login.html')


# 退出页
@home.route('/logout/')
def logout():
    return redirect(url_for('home.login'))


# 登陆页
@home.route('/register/')
def register():
    return render_template('/home/register.html')


# 用户中心
@home.route('/user/')
def user():
    return render_template('/home/user.html')


# 修改密码
@home.route('/pwd/')
def pwd():
    return render_template('/home/pwd.html')


# 用户评论
@home.route('/comments/')
def comments():
    return render_template('/home/comments.html')


# 用户登陆日志
@home.route('/loginlog/')
def loginlog():
    return render_template('/home/loginlog.html')


# 用户收藏
@home.route('/moviecol/')
def moviecol():
    return render_template('/home/moviecol.html')


# 动画- 轮播图
@home.route('/animation/')
def animation():
    return render_template('/home/animation.html')


# 搜索
@home.route('/search/')
def search():
    return render_template('/home/search.html')


# 播放页面
@home.route('/play/')
def play():
    return render_template('/home/play.html')