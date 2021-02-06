from flask import Flask , render_template , redirect , url_for

app = Flask(__name__)


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



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)