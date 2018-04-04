import datetime
__author__ = 'bnk'

# 出现了未知bug
from apps import db


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/movie"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# db = SQLAlchemy(app)

# 会员
class user(db.Model):
    '''
    会员信息
    '''
    __tablename__ = 'user'
    # 用户id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名/昵称
    name = db.Column(db.String(100), unique=True)
    # 密码
    pwd = db.Column(db.String(200))
    # 邮箱
    email = db.Column(db.String(100), unique=True)
    # 手机号码
    phone = db.Column(db.String(11), unique=True)
    # 个性简介
    info = db.Column(db.Text)
    # 头像
    face = db.Column(db.String(255), unique=True)
    # 唯一标识
    uuid = db.Column(db.String(255), unique=True)
    # 添加时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    # 外键关系关联
    # 会员日志管理
    userlogs = db.relationship('UserLog', backref = 'user')
    # 用户评论
    comments = db.relationship('Comment', backref='user')
    # 收藏
    moviecol = db.relationship('Moviecol', backref='user')


    # 查询时返回的值, 自己去拼接
    def __repr__(self):
        return "<User %r>"%self.name

# 会员登陆日志
class UserLog(db.Model):
    '''
    会员登陆日志信息
    '''
    __tablename__ = 'userlog'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # user_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 登陆ip
    ip = db.Column(db.String(50))
    # 登陆时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)


    # 查询返回值
    def __repr__(self):
        return "<UserLog %r>"%self.ip


# 标签
class Tag(db.Model):
    '''
    电影所属标签
    '''
    __tablename__ = 'tag'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 标签名称
    name = db.Column(db.String(50), unique=True)
    # 添加时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    # 外键关系关联
    # 电影
    movies = db.relationship('Movie', backref='tag')

    def __repr__(self):
        return "<Tag %r>"%self.name


# 电影
class Movie(db.Model):
    '''
    电影基本信息
    '''
    __tablename__ = 'movie'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(255), unique=True)
    # 地址
    url = db.Column(db.String(255), unique=True)
    # 简介
    info = db.Column(db.Text)
    # 封面
    logo = db.Column(db.String(255))
    # 星级
    star = db.Column(db.SmallInteger)
    # 播放量
    play_num = db.Column(db.Integer)
    # 评论数
    comment_num = db.Column(db.BigInteger)
    # 所属标签id
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    # 上映地区
    area = db.Column(db.String(100))
    # 上映时间
    release_time = db.Column(db.Date)
    # 播放时长
    length = db.Column(db.String(100))
    # 添加时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    # 外键关系关联
    # 电影
    comments = db.relationship('Comment', backref='movie')
    # 收藏
    moviecol = db.relationship('Moviecol', backref='movie')


    def __repr__(self):
        return "<Movie %r>"%self.title


# 上映预告
class Preview(db.Model):
    '''
    电影预告
    '''
    __tablename__ = 'preview'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(255), unique=True)
    # 封面
    logo = db.Column(db.String(255))
    # 添加时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论
class Comment(db.Model):
    '''
    用户评论
    '''
    __tablename__ = 'comment'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 内容
    content = db.Column(db.Text)
    # 电影id
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    # 用户id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 添加时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Comment %r>" % self.id


# 电影收藏
class Moviecol(db.Model):
    '''
    用户收藏
    '''
    __tablename__ = 'moviecol'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 电影id
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    # 用户id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 添加时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Comment %r>" % self.id


# 权限
class Auth(db.Model):
    '''
    用户权限
    '''
    __tablename__ = 'auth'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 权限名称
    name = db.Column(db.String(100), unique=True)
    # 权限地址
    url = db.Column(db.String(255), unique=True)
    # 添加时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    '''
    角色
    '''
    # id
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    # 角色名称
    name = db.Column(db.String(100), unique=True)
    # 权限列表
    auths = db.Column(db.String(600))
    # 添加时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    # 外键关系关联
    # 管理员
    admin = db.relationship('Admin', backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    '''
    管理员
    '''
    # id
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    # 管理员账号
    name = db.Column(db.String(100), unique=True)
    # 密码
    pwd = db.Column(db.String(200))
    # 是否为超级管理员
    is_super = db.Column(db.SmallInteger)
    # 所属角色
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    # 添加时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    # 外键关系关联
    # 管理员登陆日志
    adminlogs = db.relationship('AdminLog', backref='admin')
    # 操作日志
    oplogs = db.relationship('Oplog', backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.name

    # 密码验证
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登陆日志
class AdminLog(db.Model):
    '''
    管理员登陆日志信息
    '''
    __tablename__ = 'adminlog'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # user_id
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    # 登陆ip
    ip = db.Column(db.String(50))
    # 登陆时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)


    # 查询返回值
    def __repr__(self):
        return "<AdminLog %r>"%self.i


# 操作日志
class Oplog(db.Model):
    '''
    管理员登陆日志信息
    '''
    __tablename__ = 'oplog'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # user_id
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    # 登陆ip
    ip = db.Column(db.String(50))
    # 操作原因
    reason = db.Column(db.String(600))
    # 登陆时间
    add_time = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)


    # 查询返回值
    def __repr__(self):
        return "<Oplog %r>"%self.id


# 本地测试
'''
if __name__ == "__main__":
    # 创建数据库
    # db.create_all()
    role = Role(
        name = '超级管理员',
        auths = ''
    )
    db.session.add(role)
    db.session.commit()
    from werkzeug.security import generate_password_hash

    admin = Admin(
        name = 'bnk',
        pwd = generate_password_hash('python123'),
        is_super = 0,
        role_id = 1
    )
    db.session.add(admin)
    db.session.commit()

'''
