from flask import Flask

app = Flask(__name__)
#Dashboard
@app.route('/')
def home():
    return "Flask Coba Anjing"

if __name__ == '__main__':
    app.run()