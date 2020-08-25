from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# login code
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login'


# Creating model table for our CRUD database
class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    id = Login.query.get(int(user_id))
    return id


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))
    comments = db.Column(db.String(100))

    def __init__(self, title, description, comments):
        self.title = title
        self.description = description
        self.comments = comments


@app.route('/')
def Index():
    """if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello"""
    # name = current_user.username
    return render_template("index.html")


@app.route('/admin')
def AdminIndex():
    all = Login.query.all()
    return render_template("admin_index.html", member=all)


@app.route('/UserHome')
def UserHome():
    # return redirect(url_for('Check_Login'))
    return render_template("login.html")


@app.route('/Check_Login', methods=['GET', 'POST'])
def Check_Login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        if username == '' and password == '':
            flash('Please enter username and password')
            return render_template("login.html")
        else:
            if username == "admin" and password == "admin":
                return redirect(url_for("AdminIndex"))
            else:
                all_user = List.query.all()
                return render_template("list.html", get=all_user)
        return "Its not Working.!"
    return render_template("index.html")


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        my_data = Login(username, email, password)
        db.session.add(my_data)
        db.session.commit()

        flash("User Inserted Successfully")
        return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Login.query.get(request.form.get('id'))
        my_data.username = request.form['username']
        my_data.email = request.form['email']
        my_data.password = request.form['password']
        db.session.commit()
        flash("Member Updated Successfully")
        return redirect(url_for('Index'))


# This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Login.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Member Deleted Successfully")
    return redirect(url_for('Index'))


# this route is for inserting data to mysql database via html forms
@app.route('/insertList', methods=['POST'])
def insertList():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        comments = request.form['comments']

        list_data = List(title, description, comments)
        db.session.add(list_data)
        db.session.commit()

        flash("User Inserted Successfully")
        all_user = List.query.all()
        return render_template("list.html", user=all_user)


@app.route('/updateList', methods=['GET', 'POST'])
def updateList():
    if request.method == 'POST':
        my_data = List.query.get(request.form.get('id'))

        my_data.title = request.form['title']
        my_data.description = request.form['description']
        my_data.comments = request.form['comments']

        db.session.commit()
        flash("Member Updated Successfully")
        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
