# Core Packages
import sys,re
import tkinter as tk
import tweepy

#for graphing the data and display in Tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#gui libraries
from tkinter import *
from tkinter import ttk

# NLP Packages
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import spacy
nlp = spacy.load('en_core_web_sm')
 
 # Structure and Layout
window = Tk()
window.title("Sentiment Analyser")
window.geometry("700x600")
window.config(background='black')

# TAB LAYOUT
tab_control = ttk.Notebook(window)
 
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

# ADD TABS TO NOTEBOOK
tab_control.add(tab1, text='Analyser')
tab_control.add(tab2, text='About')


label1 = Label(tab1, text= 'Using NLP',padx=5, pady=5)
label1.grid(column=0, row=0)

label2 = Label(tab2, text= 'About',padx=5, pady=5)
label2.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')

about_label = Label(tab2,text="Sentiment Analysis GUI V.0.0.1 \n Akshit Desai\n@codestromer",pady=5,padx=5)
about_label.grid(column=0,row=1)


#My Twitter API Authentication Variables
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Clear display widget
def clear_display_result():
	tab1_display.delete('1.0',END)

# Functions FOR NLP  FOR TAB ONE
def get_sentiment():
	raw_text = str(raw_entry.get())

	tweets = tweepy.Cursor(api.search, q=raw_text, lang = "en").items(100)

	polarity = 0
	positive = 0
	wpositive = 0
	spositive = 0
	negative = 0
	wnegative = 0
	snegative = 0
	neutral = 0
	
	NoOfTerms = 100
	tweetTexts = []

	# iterating through tweets fetched
	for tweet in tweets:
		#Append to temp so that we can store in csv later. I use encode UTF-8
		tweetTexts.append(cleanTweet(tweet.text).encode('utf-8'))
		analysis = TextBlob(tweet.text)
		
		polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

		if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
			neutral += 1
		elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
			wpositive += 1
		elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
			positive += 1
		elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
			spositive += 1
		elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
			wnegative += 1
		elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
			negative += 1
		elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
			snegative += 1

	# finding average of how people are reacting
	positive = percentage(positive, NoOfTerms)
	wpositive = percentage(wpositive, NoOfTerms)
	spositive = percentage(spositive, NoOfTerms)
	negative = percentage(negative, NoOfTerms)
	wnegative = percentage(wnegative, NoOfTerms)
	snegative = percentage(snegative, NoOfTerms)
	neutral = percentage(neutral, NoOfTerms)


	# = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
	for tweetText in tweetTexts:
		tab1_display.insert(tk.END,str(tweetText)+'\n')
	plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, raw_text, NoOfTerms)

def cleanTweet(tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

#for finding percentage
def percentage(part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

#plotting a graph on entered data
def plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
	labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
				'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
	sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
	colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']

	f=Figure(figsize=(5,5),dpi=100)
	f.suptitle('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.', fontsize=10)
	plt=f.add_subplot(111)
	patches, texts = plt.pie(sizes, colors=colors, startangle=90)
	plt.legend(patches, labels, loc="best")
	plt.axis('equal')
	canvas = FigureCanvasTkAgg(f)
	canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=FALSE)


# MAIN NLP TAB
l1=Label(tab1,text="Enter Text for Analysis")
l1.grid(row=1,column=0)

#input widget
raw_entry=StringVar()
entry1=Entry(tab1,textvariable=raw_entry,width=50)
entry1.grid(row=1,column=1)

# bUTTONS
button1=Button(tab1,text="Start", width=12,command=get_sentiment,bg='#03A9F4',fg='#fff')
button1.grid(row=4,column=1,padx=0,pady=10)
button1=Button(tab1,text="Clear", width=12,command=clear_display_result,bg='#03A9F4',fg='#fff')
button1.grid(row=5,column=1,padx=0,pady=10)

# Display Screen For Result
tab1_display = Text(tab1,height=8)
tab1_display.grid(row=8,column=0, columnspan=3,padx=5,pady=5)

# Allows you to edit
tab1_display.config(state=NORMAL)

window.mainloop()

# Akshit Desai @codestromer
