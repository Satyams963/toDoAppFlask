from flask import render_template, request, redirect, flash, url_for
from todo.forms import AdminLoginForm, AdminRegistrationForm
from todo.models import Todo, User
from todo import app, bcrypt, db



@app.route("/register", methods=["GET", "POST"])
def register():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        _email = form.data['email']
        _password = form.data['password']
        _password = bcrypt.generate_password_hash(_password).decode("utf-8")
        user = User(email = _email, password = _password)
        try:
            db.session.add(user)
            db.session.commit()
            flash("Account successfully created, you may now login", "success")
            return redirect(url_for("login"))
        except:
            flash("Something went wrong with database", "warning")
    return render_template("register.html", form = form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        _email = form.data['email']
        _password = form.data['password']
        user = User.query.filter_by(email = _email).first()
        if not user:
            flash(f"No user with email {_email} found! Register today.", "danger")
            return redirect(url_for("register"))
        else:
            if bcrypt.check_password_hash(user.password, _password):
                flash("Successfully log in!", "success")
                return redirect(url_for("home"))
            else:
                flash("You've entered wrong password, please try again")
    return render_template("login.html", form = form)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()    
    return render_template("home.html", allTodo = allTodo)

@app.route('/update/<int:sno>',methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
