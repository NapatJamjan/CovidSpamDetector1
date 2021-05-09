# https://jahchaisang.gitbooks.io/fra142-gui/content/chapter1-0.html tkinter
import tkinter as tk
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
data = pd.read_csv('tweet.csv')
X, y= data['Tweet'], data['class_label']
documents = []
from nltk.stem import WordNetLemmatizer
stemmer = WordNetLemmatizer()
for sen in range(0, len(X)):
    document = re.sub(r'\W', ' ', str(X[sen]))
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    document = re.sub(r'^b\s+', '', document)
    document = document.lower()
    document = document.split()
    document = [stemmer.lemmatize(word) for word in document]
    document = ' '.join(document)
    documents.append(document)

stw = stopwords.words('english')
addi = ("&amp","arc",'https','co','t','amp','s')
stw.append(addi)
vectorizer = CountVectorizer(max_features=1500, min_df=9, max_df=0.8, stop_words=stw)
X = vectorizer.fit_transform(documents).toarray()

with open("TheModel.pkl", 'rb') as file:
    model = pickle.load(file)

############################################## setup
window = tk.Tk()
window.geometry('640x480')
window.resizable(False, False)
window.title("Spam Detector")
text = tk.StringVar()
entext = tk.StringVar(value='Write here!')
text.set("")
############################################## function
def printPos():
    text.set("██████╗░░█████╗░░██████╗██╗████████╗██╗██╗░░░██╗███████╗\n"+
          "██╔══██╗██╔══██╗██╔════╝██║╚══██╔══╝██║██║░░░██║██╔════╝\n"+
          "██████╔╝██║░░██║╚█████╗░██║░░░██║░░░██║╚██╗░██╔╝█████╗░░\n"+
          "██╔═══╝░██║░░██║░╚═══██╗██║░░░██║░░░██║░╚████╔╝░██╔══╝░░\n"+
          "██║░░░░░╚█████╔╝██████╔╝██║░░░██║░░░██║░░╚██╔╝░░███████╗\n"+
          "╚═╝░░░░░░╚════╝░╚═════╝░╚═╝░░░╚═╝░░░╚═╝░░░╚═╝░░░╚══════╝\n"+
          "It is not a spam")   
def printNeg():
    text.set("███╗░░██╗███████╗░██████╗░░█████╗░████████╗██╗██╗░░░██╗███████╗\n"+
          "████╗░██║██╔════╝██╔════╝░██╔══██╗╚══██╔══╝██║██║░░░██║██╔════╝\n"+
          "██╔██╗██║█████╗░░██║░░██╗░███████║░░░██║░░░██║╚██╗░██╔╝█████╗░░\n"+
          "██║╚████║██╔══╝░░██║░░╚██╗██╔══██║░░░██║░░░██║░╚████╔╝░██╔══╝░░\n"+
          "██║░╚███║███████╗╚██████╔╝██║░░██║░░░██║░░░██║░░╚██╔╝░░███████╗\n"+
          "╚═╝░░╚══╝╚══════╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░╚═╝░░░╚══════╝\n"+
          "It is a spam")        
def predict():
    inputt = e1.get("1.0", "end-1c")
    res = model.predict(vectorizer.transform([inputt]).toarray())
    if(res[0] == 'POSITIVE'):
        printPos()
    else:
        printNeg()

########################################### UI
w = tk.Label(window, text="Welcome to Covid Spam Detector",font=("Time New Roman", 30))
w.place(x=5,y=0)
w2 = tk.Label(window, text="Please input your sentence",font=("Time New Roman", 15))
w2.place(x=180,y=50)

l1 = tk.Label(window, text=">")
l1.place(x=40,y=85)
e1 = tk.Text(height = 5, width = 65)
e1.place(x=60,y=80)

conf = tk.Button(window, text="Confirm", fg="red", command=predict)
conf.place(x=275,y=180)

res = tk.Label(window, text="result", textvariable=text,font=("Time New Roman", 10))
res.place(x=30,y=250)


window.mainloop()

