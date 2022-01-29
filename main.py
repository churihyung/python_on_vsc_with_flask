from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_indeed_job
from export import export_to_csv

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
  return render_template("report.html", SearchBy=word,resultsNumber=len(jobs)
  ,jobs=jobs)


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()

    export_to_csv(jobs)

    return send_file("./jobs/jobs.csv")
    

  except:
    return redirect("/")
  



app.run(host="0.0.0.0")