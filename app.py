from flask import Flask , render_template , redirect , url_for ,request , flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from db import db_init, db
from models import flowerModel , UserModel
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

app.config.from_pyfile('config.py')

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
db_init(app)



@app.route('/')
def index():
    return render_template("index.html" , active='index')



@app.route("/home")
def home():
    return render_template("index.html" , active='index')

@app.route("/about")
def about():
    return render_template("about.html" , active='about')

@app.route("/blog")
def blog():
    return render_template("blog.html" , active='blog')

@app.route("/contact")
def contact():
    return render_template("contact.html" , active='contact')

@app.route("/signin")
def signin():
    return render_template("signin.html" , active='signin')


@app.route("/signup")
def signup():
    return render_template("signup.html" , active='signup')


@app.route("/admin")
def admin():

    return render_template("admin.html" , active='admin')


@app.route('/allusers')
def allusers():
    AllUsers = UserModel.query.order_by(UserModel.date_created).all()
    return render_template("allUsers.html" ,  allusers = AllUsers , active='allusers')


@app.route('/SignupUser' , methods=["GET", "POST"])
def SignupUser():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        cpassword = request.form['cpass']

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = UserModel.query.filter_by(useremail=email).first()

        if user:
            flash("User with this email already exists")
            return redirect(url_for("signup"))
        
        if cpassword != password:
            flash("password did not matched")
            return redirect(url_for("signup"))

        register = UserModel(username = name, useremail = email, userpassword = hashed)

        try:
            db.session.add(register)
            db.session.commit()
            flash("You have been registered")
            return redirect("admin")
        except Exception as e:
            print(e)
            return "Error occur during signup"

    else:
        return redirect("/blog")

@app.route('/SigninUser' , methods=["GET", "POST"])
def SigninUser():
    if request.method == "POST":

        email = request.form['email']
        password = request.form['pass']

        user = UserModel.query.filter_by(useremail=email).first()

        if not user :
            flash("email not exists")
            return redirect(url_for("signin"))
        
        else :
            if not bcrypt.checkpw(password.encode('utf-8'), user.userpassword):
                flash("password did not matched")
                return redirect(url_for("signin"))

            else :
                flash("Welcome")
                return redirect(url_for("admin"))

@app.route('/addflower' , methods=["GET", "POST"])
def addflower():
    print("add flower")



if __name__ == '__main__':
    app.run()