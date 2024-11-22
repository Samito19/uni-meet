from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html", person=name)
