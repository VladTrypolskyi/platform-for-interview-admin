# from flask import render_template, request, redirect, flash
from flask_login import login_required, login_user, logout_user
# from models import User, Role, Questions, UserInterview, Interview, InterviewQuestions
# from forms import UserForm, QuestionsForm, UserInterviewForm, InterviewForm, InterviewQuestionsForm, LoginForm
from models import app, db


# @app.route('/')
# def root():
#     return redirect('/login')
#
#
# @app.route('/home')
# # @login_required
# def home():
#     role = 'user'
#     if role == 'admin':  # это хардкод
#         return "hello admin"
#     elif role == 'user':
#         return "hello user"
#     else:
#         return redirect('/login')

@app.route('/')
@app.route('/users')
@login_required
def all_user():
    query = User.query.all()
    return render_template('index.html', query=query)


@app.route('/add-user', methods=["GET", "POST"])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    surname=form.surname.data,
                    is_admin=form.is_admin.data
                    )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("user added")
        return redirect('/add-user')
    return render_template('form.html', form=form)


@app.route('/questions')
@login_required
def questions():
    query = Questions.query.all()
    return render_template('index.html', query=query)


@app.route('/add-question', methods=["GET", "POST"])
@login_required
def add_question():
    form = QuestionsForm()
    if form.validate_on_submit():
        question = Questions(question=form.question.data, course=form.corse.data,
                             kind_of_question=form.kind_of_question.data)
        db.session.add(question)
        db.session.commit()
        return redirect('/add-question')
    return render_template('form.html', form=form)


@app.route('/interviews')
@login_required
def interviews():
    query = Interview.query.all()
    return render_template('index.html', query=query)


@app.route('/add-interview', methods=["GET", "POST"])
@login_required
def add_interview():
    form = InterviewForm().new()
    if form.validate_on_submit():
        question_list = []
        interviewers = []
        for question_id in form.question_list.data:
            question = Questions.query.filter_by(id=question_id).first()
            question_list.append(question)
        for interviewer_id in form.interviewers.data:
            user = User.query.filter_by(id=interviewer_id).first()
            interviewers.append(user)
        interview = Interview(candidate_name=form.candidate_name.data,
                              question_list=question_list,
                              interviewers=interviewers,
                              )
        all = [interview]
        for user in interviewers:
            for question in question_list:
                grade = total_mark(
                    question=question,
                    interviewer=user,
                    interview=interview
                )
                all.append(grade)
        db.session.add_all(all)
        db.session.commit()
        return redirect('/add-interview')
    return render_template('form.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user:
            if user.get_password(form.password.data):
                login_user(user)
                flash("Login successful")
                return redirect("/")
            flash("Invalid password")
            return render_template("form.html", form=form)
        flash("Invalid username")
    return render_template("form.html", form=form)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user = User.query.filter_by(username=request.form['username']).first()
#         return redirect('/home')
#         if not user or not check_password_hash(user.password, password):
#             flash('Please check your login details and try again.')
#             return redirect(url_for('login'))
#         # print(request.form['psw'])
#         # user = User.query.filter_by(username=request.form['username']).first()
#         # проверяем аутентификацию
#         # if user.password_hash == request.form['psw']:
#         #     return redirect('/home')
#         # else:
#         #     return redirect('/login')
#     return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
# @login_required
def registration():
    if request.method == 'POST':
        if request.form['psw'] != request.form['psw-repeat']:
            render_template("registration.html")
        user_role = Role.query.filter_by(name='user').first()
        user = User(name=request.form['name'], surname=request.form['surname'],
                    password=request.form['psw'])
        # role=user_role)
        # if User.password_hash==False:

        # hash = generate_password_hash(request.form['psw'])
        # else:
        #     render_template("registration.html")
        db.session.add(user)
        db.session.commit()
        return redirect('/home')

    return render_template("registration.html")


@app.route('/')
@app.route('/users')
# @login_required
def alluser():
    query = User.query.all()
    return render_template('index.html', query=query)




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
