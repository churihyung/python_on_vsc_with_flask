import csv

def export_to_csv(jobs):
  
  file = open("./jobs/jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title","company","location","link"])
  
  for job in jobs:
    
    writer.writerow(job.values())