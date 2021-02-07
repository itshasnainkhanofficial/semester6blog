from flask import Flask , render_template , redirect , url_for ,request , flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


# class for register model

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    useremail = db.Column(db.String(200), nullable=False)
    userpassword = db.Column(db.String(900), nullable=False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):
        return  "<Task %r>" % self.id



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


if __name__ == '__main__':
    app.run()