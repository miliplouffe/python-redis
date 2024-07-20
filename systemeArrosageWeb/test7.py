from flask import Flask, render_template

directory="C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\Systemes\\systemeArrosageWeb\\templates"
app = Flask(__name__, template_folder=directory)
@app.route('/')
def index():
    return render_template('index.html')


app.run(host='0.0.0.0', port=8100)