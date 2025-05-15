from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')

class RegisterForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('password', message='As senhas devem ser iguais')
    ])
    role = SelectField('Tipo de Usuário', choices=[
        ('client', 'Cliente'),
        ('lawyer', 'Advogado')
    ], validators=[DataRequired()])
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este e-mail já está registrado. Por favor, use outro.')
