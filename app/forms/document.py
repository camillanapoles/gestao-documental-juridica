from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, Optional

class CaseForm(FlaskForm):
    title = StringField('Título do Caso', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Descrição', validators=[Optional()])
    client_email = StringField('E-mail do Cliente', validators=[DataRequired()])
    client_name = StringField('Nome do Cliente (se novo)', validators=[Optional()])

class DocumentForm(FlaskForm):
    name = StringField('Nome do Documento', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Descrição/Instruções', validators=[Optional()])
    file = FileField('Arquivo')
    notes = TextAreaField('Observações', validators=[Optional()])

class DocumentStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('PENDING', 'Pendente'),
        ('SUBMITTED', 'Enviado'),
        ('REVIEWING', 'Em Análise'),
        ('APPROVED', 'Aprovado'),
        ('REJECTED', 'Rejeitado'),
        ('CORRECTION_REQUESTED', 'Correção Solicitada')
    ], validators=[DataRequired()])
    comment = TextAreaField('Comentário', validators=[Optional()])
    include_in_process = BooleanField('Incluir no Processo', default=False)
