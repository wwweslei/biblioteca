
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, BooleanField, SelectField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileRequired


class ContactForm(FlaskForm):
    computacao = TextField('ENG Computação')
    producao = TextField('ENG Produção')
    fisica = TextField('Física')
    matematica = TextField('Matemática')
    pedagogia = TextField('Pedagogia')
    check_computacao = BooleanField("ok", id="Eng computação")
    check_producao = BooleanField("ok", id='ENG Produção')
    check_fisica = BooleanField("ok", id='Física')
    check_matematica = BooleanField("ok", id='Matemática')
    check_pedagogia = BooleanField("ok", id='Pedagogia')
    ano2017 = TextField('2017')
    ano2018 = TextField('2018')
    ano2019 = TextField('2019')
    ano2020 = TextField('2020')
    check_2017 = BooleanField("ok", id=2017)
    check_2018 = BooleanField("ok", id=2018)
    check_2019 = BooleanField("ok", id=2019)
    check_2020 = BooleanField("ok", id=2020)
    mongagua = TextField('Mongaguá')
    itanhaem = TextField('Itanhaém')
    peruibe = TextField('Peruíbe')
    check_itanhaem = BooleanField("ok", id='Itanhaém')
    check_mongagua = BooleanField("ok", id='Mongaguá')
    check_peruibe = BooleanField("ok", id='Peruíbe')

    submit = SubmitField("Filtrar")


class Upload(FlaskForm):
    title = TextField("Título", validators=[Required()])
    year = SelectField("Ano", choices=[
                       ('2017', 2017), ('2018', 2018), ('2019', 2019), ('2020', 2020)])
    pole = TextField("Polo", validators=[Required()])
    pdf = FileField("pdf", validators=[FileRequired()])
    course = SelectField("Curso", choices=[("ENG Computação", "ENG Computação"),
                                           ("ENG Produção", "ENG Produção"),
                                           ("Física", "Física"),
                                           ("Matemática", "Matemática"),
                                           ("Pedagogia", "Pedagogia")])
    submit = SubmitField('Submit')
