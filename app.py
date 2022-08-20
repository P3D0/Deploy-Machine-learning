from flask import Flask, render_template, request
import pandas as pd

#buat model
import tensorflow as tf
import numpy as np
import pickle

def loadCSV():
    df = pd.read_csv('Preprocessing.csv')
    df1 = df.head(1000)
    return df1

def loadHasilLabel():
    df = pd.read_csv('Labeling.csv')
    df1 = df.head(1000)
    return df1

app = Flask(__name__)
#import model
# model = tf.keras.models.load_model('ModelP3D02.h5')
#load tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

#Dashboard
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/preprocessing', methods=['GET', 'POST'])
def preprocessing():
    df1 = loadCSV()
    print(request.form.get)
    #Case Folding
    if request.form.get('Data') == 'Case Folding':
        judul = 'Case Folding'
        heading = ('Ulasan','Case Folding')
        df1 = df1[['content', 'cleaned_content']]
    #Text Cleaning
    elif  request.form.get('Data') == 'Text Cleaning':
        judul = 'Text Cleaning'
        heading = ('Case Folding','Text Cleaning')
        df1 = df1[['cleaned_content', 'cleaning_data']]
    #Normalisasi
    elif  request.form.get('Data') == 'Normalisasi':
        judul = 'Normalisasi'
        heading = ('Text Cleaning', 'Normalisasi')
        df1 = df1[['cleaning_data','Remove_noise']]
    #Crawling Data
    else:
        judul = 'Crawling Data'
        heading = ('Username','Ulasan')
        df1 = df1[['userName','content']]
    results = [tuple(x) for x in df1.values]
    return render_template('preprocessing.html', header = heading, results = results, judul = judul)

@app.route('/labeling', methods=['GET', 'POST'])
def labeling():
    df1 = loadHasilLabel()
    heading = ('Review', 'Skor Polaritas', 'Sentimen')
    df1 = df1[['Remove_noise','nilai','sentimen']]
    results = [tuple(x) for x in df1.values]
    return render_template('labeling.html', header = heading, results = results)

@app.route('/visualisasi')
def visualisasi():
    return render_template('visualisasi.html')

@app.route('/sentimen', methods=['GET', 'POST'])
def sentimen():
    if request.method == 'GET':
        return render_template('sentimen.html')
    elif request.method == 'POST':
        terxt = request.form.get('textnya')

        #prediksii
        # max_length = 200
        data = [terxt] #ngubah jadi dictionary
        enc = tokenizer.texts_to_sequences(data)
        # enc = tf.keras.preprocessing.sequence.pad_sequences(enc, maxlen=max_length, dtype='int32', value=0)
        # sentiment = model.predict(enc)[0]
        # if (np.argmax(sentiment) == 0):
        #     sentimennya = 0
        # elif (np.argmax(sentiment) == 1):
        #     sentimennya = 1
        # else:
        #     sentimennya = 2


        return render_template('sentimen.html',sentiimen = enc, kata = terxt)
        # return render_template('sentimen.html', sentiimen = data)



if __name__ == '__main__':
    app.run()