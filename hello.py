from flask import Flask, render_template, url_for
import csv, random

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<username>')
def hello_name(username=None):
    return render_template('hello.html', name=username)

@app.route('/blog/')
def blog():
    return render_template('blog.html')

@app.route('/projects/roulette/')
def chart():

	#popular vote
    party_names = ["Conservatives", "Labour", "UKIP", "Liberal Democrats", "SNP", "Green", "DUP", "Plaid Cymru", "Sinn Fein", "UUP", "SDLP", "Other"]
    party_results = [36.8, 30.5, 12.7, 7.9, 4.7, 3.8, 0.6, 0.6, 0.6, 0.4, 0.3, 1.1]
    party_colours = ["#0087DC", "#DC241F", "#70147A", "#FDBB30", "#FFFF00", "#6AB023", "#D46A4C", "#008142", "#008800", "#9999FF", "#99FF66", "#FFFFFF"]
	
	#simulation
    names, mps, colours = runSimulation()
    print(names)

	#actual results
    real_party_names = ["Conservatives", "Labour", "UKIP", "Liberal Democrats", "SNP", "Green", "DUP", "Plaid Cymru", "Sinn Fein", "UUP", "SDLP", "Independent", "Speaker"]
    real_results = [330, 232, 1, 8, 56, 1, 8, 3, 4, 2, 3, 1, 1]
    real_party_colours = ["#0087DC", "#DC241F", "#70147A", "#FDBB30", "#FFFF00", "#6AB023", "#D46A4C", "#008142", "#008800", "#9999FF", "#99FF66","#DDDDDD", "#FFFFFF"]

    #make all the same length
    while len(party_names) < len(names):
    	party_names.append("")
    	party_results.append(0)
    	party_colours.append("#FFFFFF")
    
    while len(real_party_names) < len(names):
    	real_party_names.append("")
    	real_results.append(0)
    	real_party_colours.append("#FFFFFF")

    return render_template('chart.html', set=zip(mps, names, colours, party_results, party_names, party_colours, real_results, real_party_names, real_party_colours))

def runSimulation():
    data_file = open('RESULTS.csv', encoding = "ISO-8859-2")
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
            print("") 

    names = []
    mps = []
    colours = []
    r = lambda: random.randint(0,255)

    for x in parties:
        if x[1] > 0:  
            if x[0] == 'Con':
        	    names.append("Conservatives")
        	    mps.append(x[1])
        	    colours.append("#0087DC")
            elif x[0] == 'Lab':
                names.append("Labour")
                mps.append(x[1])
                colours.append("#DC241F")
            elif x[0] == 'UKIP':
                names.append(x[0])
                mps.append(x[1])
                colours.append('#70147A')
            elif x[0] == 'LD':
                names.append("Liberal Democrats")
                mps.append(x[1])
                colours.append("#FDBB30")
            elif x[0] == "SNP":
                names.append(x[0])
                mps.append(x[1])
                colours.append("#FFFF00")
            elif x[0] == "Green":
                names.append(x[0])
                mps.append(x[1])
                colours.append("#6AB023")
            elif x[0] == "DUP":
                names.append(x[0])
                mps.append(x[1])
                colours.append("#D46A4C")
            elif x[0] == "UUP":
                names.append(x[0])
                mps.append(x[1])
                colours.append("#9999FF")  
            elif x[0] == "SDLP":
                names.append(x[0])
                mps.append(x[1])
       	        colours.append("#99FF66")       
            elif x[0] == 'SF':
                names.append("Sinn Fein")
                mps.append(x[1])
                colours.append("#008800")
            elif x[0] == 'PC':
                names.append("Plaid Cymru")
                mps.append(x[1])
                colours.append("#008142")
            else:
                #Give other parties random colours
                names.append(x[0])
                mps.append(x[1])
                colours.append('#%02X%02X%02X' % (r(),r(),r())) 

               
    return names, mps, colours

if __name__ == '__main__':
    app.run(debug=True)

