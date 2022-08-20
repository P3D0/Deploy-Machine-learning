from flask import Flask, render_template, request
import pandas as pd

def loadCSV():
    df = pd.read_csv('Preprocessing.csv')
    df1 = df.head(1000)
    return df1

def loadHasilLabel():
    df = pd.read_csv('Labeling.csv')
    df1 = df.head(1000)
    return df1

app = Flask(__name__)
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


if __name__ == '__main__':
    app.run()