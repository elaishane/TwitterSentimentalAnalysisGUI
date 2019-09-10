from tkinter import Tk
from tkinter import *
import requests
import datetime
import bs4
from PIL import Image, ImageTk
import socket
import bs4


import numpy as np
import pandas as pd
import re
import tweepy

from tkinter import scrolledtext

#Splash Screen
splash = Tk()
splash.title("Twitter Sentimental Analysis")

splash.geometry("1000x500+100+100")
splash.resizable(False,False)
	
lbl = Button(splash,text = "Welcome!",font = ("Helvetica",20,'bold'),command=splash.destroy)
lbl.pack(pady = 10)
res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
soup=bs4.BeautifulSoup(res.text,'lxml')
quote = soup.find('img',{"class":"p-qotd"})

img_url="https://www.brainyquote.com"+quote['data-img-url']

img_name = datetime.datetime.now().date()

r=requests.get(img_url)
with open(str(img_name) + ".gif","wb") as f:
	f.write(r.content)
s = datetime.datetime.now().date()
image_file = str(s)+".gif"
image = Image.open(image_file)
photo = ImageTk.PhotoImage(image)
label = Label(image=photo,width=1000,height = 400)
label.image = photo # keep a reference!
label.pack()

splash.mainloop()


root = Tk()
root.title("Twitter Sentimental Analysis")
root.geometry("700x530+100+100")
root.resizable(True,True)
HSG = Label(root,text='Enter your Hashtag/Twitter Account Name:',font=(5))
HSG.grid(column=0,row=0)
name=Entry(root,bd=10)
name.grid(row=0,column=1)
n1 = Label(root,text = 'Enter the number of tweets to consider',font = (5))
n1.grid(row = 1,column = 0)
number = Entry(root,bd = 5)
number.grid(row = 1,column = 1) 

reason = IntVar()
reason.set(2)
reason1 = Radiobutton(root,text = 'Graph',variable = reason , value = 1,font = ('ariel',14)) 
reason2 = Radiobutton(root,text = 'Non-Graph',variable = reason , value = 2,font = ('ariel',14))
reason1.grid(row = 2,column=0)
reason2.grid(row=2,column=1)
scrollbar = Scrollbar(root)
scrollbar.grid(row = 4 ,column = 1)
st=scrolledtext.ScrolledText(root,width=80,height=50,yscrollcommand=scrollbar.set)
scrollbar.config(command=st.yview)
st.grid(row=4,column=0,columnspan = 19,rowspan = 30,sticky = E+S+W)

def f1():
	from tkinter import messagebox
	try:
		hashtag1 =name.get()
		if len(hashtag1) == 0:
			messagebox.showerror("Incomplete","Please Enter Hashtag/Twitter Account Name")
			name.focus()
			number.delete(0,END)
			return
		num = number.get()
		if len(num)==0:
			messagebox.showerror("Incomplete","Please Enter the number of tweets to consider")
			number.delete(0,END)
			number.focus()
			return
		if not num.isdigit() or int(num)<1:
			messagebox.showerror("Error","Number should be Positive,Greater than 0 \nIt should be and Integer")
			number.delete(0,END)
			number.focus()
			return
		r = reason.get()
		num = int(num)
		if r == 1:
			messagebox.showinfo("Result","You have selected Graph")
			st.delete(1.0,END)
			from tweepy_streamer import TwitterClient
			from tweepy_streamer import TweetAnalyzer
			import numpy as np
			twitter_client = TwitterClient()
			tweet_analyzer = TweetAnalyzer()
			api = twitter_client.get_twitter_client_api()
			tweets = api.user_timeline(screen_name=hashtag1, count=num)
			df = tweet_analyzer.tweets_to_data_frame(tweets)
			df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
			df.head(250)
			st.insert(INSERT,df,df['sentiment'])
			pos,neg,neu = 0,0,0
			from textblob import TextBlob
			import matplotlib.pyplot as plt
			for tweet in tweets:
				analysis1 = TextBlob(tweet_analyzer.clean_tweet(tweet.text))
				if analysis1.sentiment.polarity > 0:
					pos = pos + 1
				if analysis1.sentiment.polarity  == 0:
					neu = neu + 1
				if analysis1.sentiment.polarity < 0:
					neg = neg + 1
			positive = (pos/num)*100
			negative = (neg / num)*100
			neutral = (neu / num)*100
			if(positive>negative & postive>neutral){result = "Postive"}
			elif(negative>positive & negative>neutral){result = "Negative"}
			else{result = "Neutral"}
			labels = [str(positive)+'% '+'Positive',str(negative)+'% '+'Negative',str(neutral)+'% '+'Neutral',"Result: "+Result]
			sizes = [positive,negative,neutral]
			colors = ['yellowgreen', 'red', 'gold']
			patches, texts = plt.pie(sizes, colors=colors, startangle=90)
			plt.legend(patches, labels, loc="best")
			plt.title("People's Reaction")
			plt.axis('equal')
			plt.tight_layout()
			plt.show()
		if r == 2:
			messagebox.showinfo("Result","You have selected Non-Graph")
			st.delete(1.0,END)
			from tweepy_streamer import TwitterClient
			from tweepy_streamer import TweetAnalyzer
			import numpy as np
			twitter_client = TwitterClient()
			tweet_analyzer = TweetAnalyzer()
			api = twitter_client.get_twitter_client_api()
			tweets = api.user_timeline(screen_name=hashtag1, count=num)
			df = tweet_analyzer.tweets_to_data_frame(tweets)
			df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
			st.insert(INSERT,df,df['sentiment'])
			df.head(250)
	#except socket.gaierror as e:
	#	messagebox.showerror("Error","Check your Internet Connection")
	except tweepy.error.TweepError as e:
		messagebox.showerror("Result","Check your Internet Connection")
	except ConnectionError as e:
		messagebox.showerror("Result","Check your Internet Connection")

submit = Button(root,text = 'Submit',font =('ariel',18,'bold'),command = f1)
submit.grid(row=0,column=3)
root.mainloop()
