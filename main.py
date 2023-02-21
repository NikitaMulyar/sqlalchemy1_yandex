from datetime import datetime
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class RegisterForm(FlaskForm):
    email = StringField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age')
    pos = StringField('Position')
    spec = StringField('Speciality')
    adrs = StringField("Address")
    submit = SubmitField('Register')


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    user = User()
    user.name = "Ridley"
    user.surname = "Scott"
    user.age = 21
    user.position = 'captain'
    user.speciality = 'research engineer'
    user.address = 'module_1'
    user.email = 'scott_chief@mars.org'
    if db_sess.query(User).filter_by(email=user.email).count() < 1:
        db_sess.add(user)
        db_sess.commit()
    data = {1: {'name': 'River', 'surname': 'Song', 'age': 30, 'position': 'бортмеханик',
                'speciality': 'управляет ТАРДИС', 'address': 'module_0', 'email': 'river_song@tardis.gallifrey'},
            2: {'name': 'Dalek', 'surname': '1', 'age': 999999, 'position': 'enemy',
                'speciality': 'engineer', 'address': 'Scaro', 'email': 'dalek1@scaro.universe'},
            3: {'name': 'Master', 'surname': '-', 'age': 2000, 'position': 'clown',
                'speciality': 'изобретатель', 'address': 'TARDIS', 'email': 'master@gallifrey.universe'}}
    for i in data:
        user = User()
        user.name = data[i]['name']
        user.surname = data[i]['surname']
        user.age = data[i]['age']
        user.position = data[i]['position']
        user.speciality = data[i]['speciality']
        user.address = data[i]['address']
        user.email = data[i]['email']
        if db_sess.query(User).filter_by(email=user.email).count() < 1:
            db_sess.add(user)
            db_sess.commit()

    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.start_date = datetime.now()
    job.is_finished = False
    if db_sess.query(Jobs).filter_by(job=job.job).count() < 1:
        db_sess.add(job)
        db_sess.commit()


"""
@app.route('/<title>')
@app.route('/index/<title>')
def base(title):
    return render_template('base.html', title=title)
"""


@app.route('/')
@app.route('/index/')
def table():
    db_sess = db_session.create_session()
    res = db_sess.query(Jobs).all()
    data = []
    for job in res:
        title = job.job
        time = f'{round((job.end_date - job.start_date).total_seconds() / 3600)} hours'
        team_leader = job.user.name + ' ' + job.user.surname
        collab = job.collaborators
        f = job.is_finished
        data.append([title, team_leader, time, collab, f])
    return render_template('log.html', jobs=data)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register form',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.pos.data,
            address=form.adrs.data,
            speciality=form.spec.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/success')
    return render_template('register.html', title='Register form', form=form)


@app.route('/success')
def ok_page():
    return render_template('success.html')


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
