from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import ContactForm, Upload
from werkzeug.utils import secure_filename
from core import convert, resumen_extracto
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Faça. Ou não faça. Não existe a tentativa.'
WTF_CSRF_SECRET_KEY = 'a random string'
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class PI(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), unique=True, nullable=False)
    course = db.Column(db.String(120), nullable=False)
    pole = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    resumen = db.Column(db.String(1200), nullable=True)
    filename = db.Column(db.String(120), nullable=False)
    filename_page1 = db.Column(db.String(120), nullable=False)
    filename_page2 = db.Column(db.String(120), nullable=False)
    filename_page3 = db.Column(db.String(120), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return self.title


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if request.method == 'POST':
        list(form)
        courses = [form.check_computacao, form.check_producao,
                   form.check_fisica, form.check_matematica, form.check_pedagogia]
        form_list_courses = [course.id for course in courses if course.data]
        year_list = [form.check_2017, form.check_2018, form.check_2019, form.check_2020]
        form_list_year = [year.id for year in year_list if year.data]
        poles = [form.check_itanhaem, form.check_mongagua, form.check_peruibe]
        form_poles_list = [pole.id for pole in poles if pole.data]
        if form_list_courses or form_list_year or form_poles_list:
            pi = PI.query.filter(
                PI.course.in_(form_list_courses) | PI.pole. in_(form_poles_list) | PI.year.in_(form_list_year)).all()
            return render_template("catalog-page.html", pi=pi, form=form)
        else:
            pi = PI.query.all()
            return render_template("catalog-page.html", pi=pi, form=form)

    pi = PI.query.all()
    return render_template("catalog-page.html", pi=pi, form=form)


@app.route("/<page>")
def detail(page):
    pi = PI.query.filter_by(title=str(page)).first()
    all_pi = PI.query.all()
    return render_template("product-page.html", pi=pi, all_pi=all_pi)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/registration")
def registration():
    return render_template("registration.html")


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    form = Upload()
    path = str(app.instance_path[:-8] + "static/assets")
    if form.validate_on_submit():
        pdf = form.pdf.data
        filename = secure_filename(f"{form.title.data}.pdf")
        pdf.save(os.path.join(path, 'library', filename))
        pi = PI(
            title=str(form.title.data).capitalize(),
            course=str(form.course.data).capitalize(),
            pole=str(form.pole.data).capitalize(),
            year=form.year.data,
            filename=filename,
            resumen=str(resumen_extracto(filename))[6:],
            filename_page1=f"{filename[:-4]}_page1_small.jpg",
            filename_page2=f"{filename[:-4]}_page2_small.jpg",
            filename_page3=f"{filename[:-4]}_page3_small.jpg"
        )
        db.session.add(pi)
        db.session.commit()
        convert(F"{path}/library/{str(filename)}")
        flash('Projeto salvo com sucesso!')
        return redirect(url_for('home'))
    return render_template("upload.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
