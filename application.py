from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

@app.route("/")
def home():
    return render_template("index.html", content ="Testing")

@app.route("/process", methods = ['POST'])
def process():
    title = request.form['title']
    return jsonify({'title':title})




if __name__=="__main__":
    app.run(debug = True)
    
