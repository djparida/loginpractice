from flask import Flask, render_template, redirect, request, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from pymsgbox import *

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format((os.path.join(project_dir, "foraiesh.db")))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SECRET_KEY"] = 'my secret'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard', methods=['post'])
def dashboard():
    name = request.form.get('name')
    password = request.form.get('password')
    print(name)
    print(password)
    try:
        if name == 'kanha':
            data = User.query.filter_by(name=name, password=password).first()
            session['usersession'] = data.id
            #usersession = session['usersession']
            print(True)
            alldata = User.query.all()
            print(session['usersession'])
            if 'usersession' in session:
                usersession = session['usersession']
            #return "Yaa it will be done"
                return render_template("dashboard.html", alldata=alldata, usersession=usersession)
            else:
                return "something wrong"
    except Exception as e:
        return e
    finally:
        data = User.query.filter_by(name=name, password=password).first()
        print(data)
        if data == None:
            return redirect('/')
        else:
            alldata = User.query.all()
            #confirm(text='', title='', buttons=['OK', 'Cancel'])
            return render_template("dashboard.html", alldata=alldata)
        #return "something went wrong"



@app.route('/adduser')
def adduser():
    return render_template('add.html')



@app.route('/add', methods=['post'])
def add():
    name = request.form.get('name')
    password = request.form.get('password')
    Add = User(name=name, password=password)
    db.session.add(Add)
    db.session.commit()
    alldata = User.query.all()
    flash('Successfully Added')
    return render_template("dashboard.html", alldata = alldata )


@app.route('/logout')
def logout():
    if 'usersession' in session:
        session.pop('usersession', None)
        flash("Logout Successfully!!!")
        return redirect('/')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)