__author__ = 'bnk'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField

from wtforms.validators import DataRequired, ValidationError

from apps.models import Admin, Tag

tags = Tag.query.all()


# 管理员登陆表单
class LoginForm(FlaskForm):
    '''
    管理员登陆表单
    '''
    account = StringField(
        label="账号",
        validators=[
            DataRequired('请输入账号!')
        ],
        description='账号',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入账号!',
            # 'required': 'required',

        }
    )
    pwd = StringField(
        label="密码",
        validators=[
            DataRequired('请输入密码!')
        ],
        description='密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码!',
            'type': 'password',
            # 'required': 'required',
        }
    )
    submit = SubmitField(
        '登陆',
        render_kw={
            'class': 'btn btn-primary btn-block btn-flat',
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == '0':
            raise ValidationError('账号不存在!')


# 标签逻辑相关表单
class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[
            DataRequired('请输入标签！')
        ],
        description='标签',
        render_kw={
            'class': 'form-control',
            'id': 'input_name',
            # 'name': 'name',
            'placeholder': '请输入标签名称！'
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            'class': 'btn btn-primary',
        }
    )


# 电影逻辑相关表单
class MovieForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[
            DataRequired('请输入片名！')
        ],
        description='片名',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入片名！'
        }
    )
    url = FileField(
        label='电影文件',
        validators=[
            DataRequired('请选择要上传的电影文件！')
        ],
        description='电影文件',
    )
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired('请输入简介！')
        ],
        description='简介',
        render_kw={
            'class': 'form-control',
            'rows': 10
        }
    )
    logo = FileField(
        label='封面',
        validators=[
            DataRequired('请选择要上传的封面图！')
        ],
        description='封面',
    )
    star = SelectField(
        label='星级',
        validators=[
            DataRequired('请选择星级！')
        ],
        coerce=int,
        choices=[(1, '1星'),(2, '2星'),(3, '3星'),(4, '4星'),(5, '5星')],
        description='星级',
        render_kw={
            'class': 'form-control',
        }
    )
    tag_id = SelectField(
        label='标签',
        validators=[
            DataRequired('请选择标签！')
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description='标签',
        render_kw={
            'class': 'form-control',
        }
    )
    area = StringField(
        label='地区',
        validators=[
            DataRequired('请输入地区！')
        ],
        description='地区',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入地区！'
        }
    )
    length = StringField(
        label='片长',
        validators=[
            DataRequired('请输入片长！')
        ],
        description='片长',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入片长！'
        }
    )
    release_time = StringField(
        label='上映时间',
        validators=[
            DataRequired('请选择上映时间！')
        ],
        description='上映时间',
        render_kw={
            'class': 'form-control',
            'id': 'input_release_time',
            'placeholder': '请选择上映时间！'
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            'class': 'btn btn-primary',
        }
    )


# 预告逻辑相关表单
class PreviewForm(FlaskForm):
    title = StringField(
        label= '预告标题',
        validators= [
            DataRequired('请输入预告标题!')
        ],
        description='预告标题',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入预告标题!'
        }
    )
    logo = FileField(
        label= '预告封面',
        validators=[
            DataRequired('请上传预告封面!')
        ],
        description='预告封面',
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            'class': 'btn btn-prmary',
        }
    )