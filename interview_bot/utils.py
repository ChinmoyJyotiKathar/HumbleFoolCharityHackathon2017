import csv
def record_convo(Question, Reply, Answer, Score):
	row = list([Question, Reply, Answer, Score])
	with open("./records/Interview.csv","a") as wf:
		writer = csv.writer(wf)
		writer.writerow(row)