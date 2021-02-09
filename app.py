from flask import Flask , render_template , redirect , url_for ,request , flash 
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from db import db_init, db
from models import  UserModel ,Img
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config.from_pyfile('config.py')

db_init(app)

# adding flower method
def addFlower():
    flowername = request.form["flowername"]
    flowerdescription = request.form["flowerdescription"]
    pic = request.files['flowerimage']

    if not flowername and not flowerdescription and not pic:
        flash("You did not add anything in blog")
        return redirect(url_for("admin"))

    if not flowername:
        flash("kindly Add flower name")
        return redirect(url_for("admin"))

    if not flowerdescription:
        flash("kindly Add flower description")
        return redirect(url_for("admin"))

    if not pic:
        flash("kindly select a picture of flower")
        return redirect(url_for("admin"))

    picture = Img.query.filter_by(name=pic.filename).first()

    if picture:
        flash("This picture already exits, kindly select another picture")
        return redirect(url_for("admin"))

    filename = secure_filename(pic.filename)

    img = Img( name=filename , writtenflowername = flowername , flowerdescription = flowerdescription)

    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    try:
        db.session.add(img)
        db.session.commit()
        flash("You flower added successfully !")
        return redirect("admin")
    except Exception as e:
        print(e)
        return "Error occur during Adding flower"


    return redirect(url_for("admin"))


# default route when app starts
@app.route('/')
def index():
    return render_template("index.html" , active='index')


# home route
@app.route("/home")
def home():
    return render_template("index.html" , active='index')

# about us route
@app.route("/about")
def about():
    return render_template("about.html" , active='about')

# blog route
@app.route("/blog")
def blog():
    AllImages = Img.query.order_by(Img.id).all()
    return render_template("blog.html" , active='blog' , images = AllImages  )

# contact us route
@app.route("/contact")
def contact():
    return render_template("contact.html" , active='contact')

# sign in route
@app.route("/signin")
def signin():
    return render_template("signin.html" , active='signin')

# sign up route
@app.route("/signup")
def signup():
    return render_template("signup.html" , active='signup')

# admin route
@app.route("/admin")
def admin():
    AllImages = Img.query.order_by(Img.id).all()
    return render_template("admin.html" , active='admin' , images = AllImages)

# showing all users
@app.route('/allusers')
def allusers():
    AllUsers = UserModel.query.order_by(UserModel.date_created).all()
    return render_template("allUsers.html" ,  allusers = AllUsers , active='allusers')

# sign up user
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

# sign in user
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


# route for adding flower to database
@app.route('/addflower', methods=['POST'])
def upload():
    if request.method == "POST":
        return addFlower()
    else:
        return redirect("/blog")


@app.route("/delete/<int:id>")
def delete(id):

    Image = Img.query.filter_by(id = id).first()
    
    try:
        db.session.delete(Image)
        db.session.commit()
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], Image.name))
        flash("You have deleted image successfully !")
        return redirect("/admin")
    except Exception as e:
            print(e)
            return "Error occur during deleting image"
        


@app.route("/updateFlower" , methods=['POST'])
def update():
    if request.method == 'POST':

        dataFromId = Img.query.get(request.form.get('id'))

        dataFromId.writtenflowername = request.form['flowername']
        dataFromId.flowerdescription = request.form['flowerdescription']
        flowerImg = request.files['flowerimage']
        imagefromid = dataFromId.name

        if flowerImg:
            filename = secure_filename(flowerImg.filename)
            dataFromId.name = filename
            flowerImg.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], imagefromid))
        try:
            db.session.commit()
            flash("You have updated successfully !")
            return redirect("/admin")
        except Exception as e:
            print(e)
            return "Error occur during updating post"
    else :
        return redirect("/blog")


if __name__ == '__main__':
    app.run()