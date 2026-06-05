from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("a.html")

@app.route("/giraffe")
def giraffe():
    return render_template("g.html")

app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)