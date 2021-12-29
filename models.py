from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vlad@localhost/platform_interview_admin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a really really really really long secret key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Platform for interview', template_mode='bootstrap2')


class Role(db.Model):
    __tablename__ = 'Role'

    role_id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    # users = db.relationship('User', backref='Role')
    role_ids = db.relationship('User', backref='Role')  # done

    def __repr__(self):
        return self.name
        # return '<Role id={} name={}>'.format(self.role_id, self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    user_login = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(100), index=True, unique=True)
    surname = db.Column(db.String(100))
    password = db.Column(db.String(255))  # passwodr_hash?
    role_id = db.Column(db.Integer, db.ForeignKey('Role.role_id'), unique=True, primary_key=True)  # primary_key
    # role = db.relationship('Role', backref='User')  # ??
    user_logins = db.relationship('UserInterview')  # done

    def __repr__(self):
        return '<User {}:{}>'.format(self.name, self.surname)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # return self.password_hash
        return check_password_hash(self.password_hash, password)

    # @staticmethod
    # def get_selection_list():
    #     result = []
    #     try:
    #         for i in User.query.all():
    #             result.append((f"{i.user_login}", f"{i.name} {i.surname}"))
    #         return result
    #     except AttributeError:
    #         return []


class Interview(db.Model):
    __tablename__ = 'Interview'

    interview_id = db.Column(db.Integer(), primary_key=True)
    candidate_name = db.Column(db.String(100), nullable=False)
    candidate_surname = db.Column(db.String(100))
    course = db.Column(db.String(50))
    date_time = db.Column(db.DateTime())
    link_zoom = db.Column(db.String())
    total_mark = db.Column(db.Float(precision=2), default=0)
    interview_ids = db.relationship('UserInterview', backref='Interview')  # done
    interview_ids_1 = db.relationship('InterviewQuestions', backref='Interview')  # done

    def __repr__(self):
        return f'{self.candidate_name}, {self.candidate_surname}'


class UserInterview(db.Model):
    __tablename__ = 'User_interview'

    user_interview_id = db.Column(db.Integer(), primary_key=True)
    user_login = db.Column(db.String(), db.ForeignKey('User.user_login'), unique=True)
    interview_id = db.Column(db.Integer(), db.ForeignKey('Interview.interview_id'), unique=True, nullable=False)
    user_comments = db.Column(db.String(255))

    # user = db.relationship('User', backref=db.backref('user_interview.id', cascade='all,delete'))

    def __repr__(self):
        return '<UserInterview %r>' % self.id


class InterviewQuestions(db.Model):
    __tablename__ = 'Interview_questions'

    interview_question_id = db.Column(db.Integer(), primary_key=True)
    interview_id = db.Column(db.Integer(), db.ForeignKey('Interview.interview_id'), unique=True, nullable=False)
    question_id = db.Column(db.Integer(), db.ForeignKey('Questions.question_id'), unique=True, nullable=False)
    answer = db.Column(db.String(255))
    user_mark = db.Column(db.Float(), nullable=False, default=0)

    # interviewer = db.relationship('User',
    #                                backref=db.backref('interviewQuestions.interview_question_id', cascade='all,delete'))

    def __repr__(self):
        return f'{self.interview_id}, {self.intrerviewer}'


class Questions(db.Model):
    __tablename__ = 'Questions'

    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255))
    course = db.Column(db.String(255))
    kind_of_question = db.Column(db.String(255), nullable=False)
    question_ids = db.relationship('InterviewQuestions', backref='Questions')  # done

    def __repr__(self):
        return 'Question %r' % self.id

    # @staticmethod
    # def get_selection_list():
    #     result = []
    #     for i in Questions.query.all():
    #         result.append((f"{i.id}", f"{i.kind_of_question}"))
    #     return result


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(InterviewQuestions, db.session))
admin.add_view(ModelView(Interview, db.session))
admin.add_view(ModelView(Questions, db.session))
admin.add_view(ModelView(UserInterview, db.session))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
