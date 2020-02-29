from flask import Flask, render_template
from data import db_session
from data import users
from data import jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum'


@app.route('/')
def index():
    session = db_session.create_session()
    job = session.query(jobs.Jobs).all()
    workers = []
    for item in job:
        user = session.query(users.User).filter(users.User.id == item.team_leader).all()
        print(user)
        workers.append([user[0].name, user[0].surname])
    return render_template('index.html', job=job, workers=workers)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.run()


if __name__ == '__main__':
    main()
