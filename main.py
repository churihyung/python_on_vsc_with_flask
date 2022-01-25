from flask import Flask

app = Flask("SuperScrapper")

@app.route("/")
def home():
    return ""

app.run(host="127.0.0.1")