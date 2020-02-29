from flask import Flask, render_template, redirect, request, make_response, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, \
    IntegerField
from wtforms.validators import DataRequired
from data import db_session, users
import datetime as dt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum'


class LoginForm(FlaskForm):
    email = StringField('Login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        sessions = db_session.create_session()
        if sessions.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.speciality.data
        )
        user.set_password(form.password.data)
        sessions.add(user)
        sessions.commit()
        return 'Вы успешно зарегестрированны'
    return render_template('register.html', form=form)


def main():
    db_session.global_init('db/blogs.sqlite')
    app.run()


if __name__ == '__main__':
    main()
