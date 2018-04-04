import os, uuid, datetime

from flask import Flask, render_template, redirect, url_for, flash, session, request
from functools import wraps
# from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename

from . import admin
from apps.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm
from apps.models import Admin, Tag, Movie, Preview
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/movie"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# db = SQLAlchemy(app)
from apps import db, app


# 访问控制
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')


# 管理员登陆页
@admin.route('/login/', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        data = login_form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if admin == None:
            flash('账号不存在!')
            return redirect(url_for('admin.login'))

        if not admin.check_pwd(data['pwd']):
            flash('密码错误')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']
        print('wentichuxianzainale')
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=login_form)


# 退出页
@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


# 修改密码页
@admin.route('/pwd/')
@admin_login_req
def pwd():
    return render_template('admin/pwd.html')


# 添加标签
@admin.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_req
def tag_add():
    tag_form = TagForm()
    if tag_form.validate_on_submit():
        data = tag_form.data
        # sql查询
        tag = Tag.query.filter_by(name=data['name']).count()
        # print(tag, data['name'])
        if tag == 1:
            flash('名称已经存在！', 'err')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        db.session.rollback()

        flash('添加标签成功', 'ok')
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=tag_form)


# 标签展示管理页面
@admin.route('/tag/list/<int:page>/', methods=['GET'])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 标签删除
@admin.route('/tag/del/<int:id>/', methods=['GET'])
@admin_login_req
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功！', 'ok')
    return redirect(url_for('admin.tag_list', page=1))


# 修改标签
@admin.route('/tag/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id=None):
    tag_form = TagForm()
    tag = Tag.query.get_or_404(id)
    if tag_form.validate_on_submit():
        data = tag_form.data
        # sql查询
        tag_count = Tag.query.filter_by(name=data['name']).count()
        # print(tag, data['name'])

        if tag_count == 1:
            # 使用下列语句会出现同一名称多次编辑，都提示添加成功！
            # if tag.name != data['name'] and tag_count == 1:
            flash('名称已经存在！', 'err')
            return redirect(url_for('admin.tag_edit', id=id))

        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        db.session.rollback()

        flash('修改标签成功', 'ok')
        return redirect(url_for('admin.tag_edit', id=id))
    return render_template('admin/tag_edit.html', form=tag_form, tag=tag)


# 添加电影
@admin.route('/movie/add/', methods=['GET', 'POST'])
@admin_login_req
def movie_add():
    movie_form = MovieForm()
    if movie_form.validate_on_submit():
        data = movie_form.data
        movie_is = Movie.query.filter_by(title=data['title']).count()
        if movie_is == 1:
            flash('电影已经存在!', 'err')
            return redirect(url_for('admin.movie_add'))
        file_url = secure_filename(movie_form.url.data.filename)
        file_logo = secure_filename(movie_form.logo.data.filename)
        # 文件上传判断文件夹是否存在
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        movie_form.url.data.save(app.config['UP_DIR'] + url)
        movie_form.logo.data.save(app.config['UP_DIR'] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            logo=logo,
            info=data['info'],
            star=int(data['star']),
            play_num=0,
            comment_num=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功！', 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=movie_form)


# 电影管理页面
@admin.route('/movie/list/<int:page>')
@admin_login_req
def movie_list(page=None):
    if page==None:
        page =1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/movie_list.html',page_data=page_data)


# 电影删除
@admin.route('/movie/del/<int:id>')
@admin_login_req
def movie_del(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash('删除电影成功！', 'ok')
    return redirect(url_for('admin.movie_list', page=1))


# 修改电影
@admin.route('/movie/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def movie_edit(id=None):
    movie_form = MovieForm()
    movie_form.url.validators = []
    movie_form.logo.validators = []
    movie = Movie.query.get_or_404(int(id))
    if request.method == 'GET':
        movie_form.info.data = movie.info
        movie_form.tag_id.data = movie.tag_id
        movie_form.star.data = movie.star
        # movie_form.url.data = movie.url
    if movie_form.validate_on_submit():
        data = movie_form.data
        movie_count = Movie.query.filter_by(title=data['title']).count()
        if movie_form == 1 and movie.title != data['title']:
            flash('片名以存在','err')
            return redirect(url_for('admin.movie_edit',id=id))

        # 判断是否存在上传文件夹
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')

        # 需要提交的相关信息
        if movie_form.url.data.filename != '':
            file_url = secure_filename(movie_form.url.data.filename)
            movie.url = change_filename(file_url)
            movie_form.url.data.save(app.config['UP_DIR']+movie.url)

        if movie_form.logo.data.filename != '':
            file_logo = secure_filename(movie_form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            movie_form.logo.data.save(app.config['UP_DIR'] + movie.logo)

        movie.star = data['star']
        movie.tag_id = data['tag_id']
        movie.info = data['info']
        movie.title = data['title']
        movie.area = data['area']
        movie.length = data['length']
        movie.release_time = data['release_time']
        db.session.add(movie)
        db.session.commit()
        flash('修改电影成功！', 'ok')
        return redirect(url_for('admin.movie_edit',id=movie.id))
    return render_template('admin/movie_edit.html', form=movie_form, movie=movie)


# 添加预告
@admin.route('/preview/add/', methods=['GET','POST'])
@admin_login_req
def preview_add():
    preview_from = PreviewForm()
    if preview_from.validate_on_submit():
        data = preview_from.data
        preview_is = Preview.query.filter_by(title=data['title']).count()
        if preview_is == 1:
            flash('预告已经存在!', 'err')
            return redirect(url_for('admin.preview_add'))
        file_logo = secure_filename(preview_from.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        logo = change_filename(file_logo)
        preview_from.logo.data.save(app.config['UP_DIR']+logo)
        preview = Preview(
            title = data['title'],
            logo = logo
        )
        db.session.add(preview)
        db.session.commit()
        flash('添加预告成功!','ok')
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html',form = preview_from)


# 预告管理页面
@admin.route('/preview/list/<int:page>', methods=['GET','POST'])
@admin_login_req
def preview_list(page=None):
    if page == None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/preview_list.html', page_data=page_data)


# 预告del操作
@admin.route('/preview/del/<int:id>', methods=['GET','POST'])
@admin_login_req
def preview_del(id=None):
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    flash('删除预告成功!','ok')
    return redirect(url_for('admin.preview_list',page=1))


# 预告修改页面
@admin.route('/preview/edit/<int:id>', methods=['GET','POST'])
@admin_login_req
def preview_edit(id=None):
    preview_from = PreviewForm()
    preview_from.logo.validators = []
    preview = Preview.query.get_or_404(int(id))
    if preview_from.validate_on_submit():
        data = preview_from.data
        if request.method == 'GET':
            preview_from.title.data = preview.title
        if preview_from.validate_on_submit():
            data = preview_from.data
            if preview_from.logo.data.filename != '':
                file_logo = change_filename(preview_from.log.data.filename)
                preview.logo = change_filename(file_logo)
                preview_from.logo.data.save(app.config['UP_DIR']+preview.logo)
            preview.title = data['title']
            db.session.add(preview)
            db.session.commit()
            flash('修改预告成功!', 'ok')
            return redirect(url_for('admin.preview_edit',id = id))
    return render_template('admin/preview_edit.html', form=preview_from,preview=preview)

# 用户管理页面
@admin.route('/user_list/')
@admin_login_req
def user_list():
    return render_template('admin/user_list.html')


# 用户信息展示页面
@admin.route('/user_view/')
@admin_login_req
def user_view():
    return render_template('admin/user_view.html')


# 用户评论
@admin.route('/comment_list/')
@admin_login_req
def comment_list():
    return render_template('admin/comment_list.html')


# 操作日志
@admin.route('/movie_col_list/')
@admin_login_req
def movie_col_list():
    return render_template('admin/movie_col_list.html')


# 操作日志
@admin.route('/oplog_list/')
@admin_login_req
def oplog_list():
    return render_template('admin/oplog_list.html')


# 管理员登陆日志
@admin.route('/admin_login_log_list/')
@admin_login_req
def admin_login_log_list():
    return render_template('admin/admin_login_log_list.html')


# 用户登陆日志
@admin.route('/user_login_log_list/')
@admin_login_req
def user_login_log_list():
    return render_template('admin/user_login_log_list.html')


# 添加权限
@admin.route('/auth_add/')
@admin_login_req
def auth_add():
    return render_template('admin/auth_add.html')


# 权限列表
@admin.route('/auth_list/')
@admin_login_req
def auth_list():
    return render_template('admin/auth_list.html')


# 添加角色
@admin.route('/role_add/')
@admin_login_req
def role_add():
    return render_template('admin/role_add.html')


# 角色列表
@admin.route('/role_list/')
@admin_login_req
def role_list():
    return render_template('admin/role_list.html')


# 添加管理员
@admin.route('/admin_add/')
@admin_login_req
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admin.route('/admin_list/')
@admin_login_req
def admin_list():
    return render_template('admin/admin_list.html')
