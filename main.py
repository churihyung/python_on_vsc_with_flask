from flask import Flask, render_template, request, redirect
from scrapper import get_indeed_job

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    fromDb = db.get(word)
    if fromDb:
      jobs = fromDb
    else:
      jobs = get_indeed_job(word)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html", SearchBy=word,resultsNumber=len(jobs))



app.run(host="0.0.0.0")