from flask import Flask , render_template



app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)