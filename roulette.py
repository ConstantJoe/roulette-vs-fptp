"""
TODO: 
Calculate % error

Begin designing web app / site - make in Flask, use Chart.js for charts
https://pythonspot.com/flask-and-great-looking-charts-using-chart-js/

Run 1,000,000 times, calculate highest, lowest, average % error
Calculate average seats per party

User reads a quick blurb on how it works

User can click to start a run
They're shown some animation

Run finishes - user is shown pie charts with their results, real results,
actual votes by general population

Map of UK coloured in by voters
"""
from pylab import *
import csv, random

data_file = open('RESULTS.csv')
reader = csv.reader(data_file)
data = list(reader)

constituencies = [[] for i in range(651)]
parties = []

#get all the parties
for row in data:
    if row[4] != 'PANO' and row[4] != '':
        constituencies[int(row[4])].append(row)
        if [row[18],0] not in parties:
            parties.append([row[18], 0])


for constituency in constituencies:
    total = 0

    for row in constituency:
        #5 is number of votes achieved
        total += int(row[5])

    prev_prob = 0.0
    probs = []

    for row in constituency:
        prob = prev_prob + (float(row[5]) / total) 
        probs.append(prob)
        prev_prob = prob

    rand = random.random() # Run the roulette

    count = 0
    choice = 0

    while count < len(probs):
        if probs[count] < rand:
            count += 1
        else:
            choice = count # This is the MP we've picked
            break

    try: 
        ind = next((i for i, sublist in enumerate(parties) if constituency[choice][18] in sublist), -1)
        parties[ind][1] += 1 #Add the MP to its parties total
    except Exception as err:
        #print "Error! - there's always one (I think the first or last) thats always empty"
        print "" 


print parties[0]


""" Something going wrong in here, I'll sort it out later
Only going to be a temp thing anyway
 """
def makeSimplePieChart(parties):
    figure(1, figsize=(6,6))
    ax = axes([0.1,0.1,0.8,0.8])


    labels  = []
    fracs   = []
    explode = []
    for party in parties:
        if party[1] > 0:
            labels.append(party[0])
            fracs.append(float(party[1])/650.0*100.0)
            explode.append(0)
    print fracs
    print labels
    print explode
    pie(fracs, explode=explode, labels=labels, autopct='%1.1%%', shadow=False, startangle=90)
    title('Roulette election results', bbox={'facecolor':'0.8','pad':5}) 
    show()  
    
print ""
print "% of MPs gained:"
print float(parties[0][1])/650.0*100.0
print ""
print "% of MPs gained in reality"
print 330.0/650.0*100.0
print "Actual popular vote: 36.9%"

#makeSimplePieChart(parties)
