from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("r.html")

@app.route("/a1/s1/")
def a1s1():
    return render_template("a1s1.html")

@app.route("/a1/s2/")
def a1s2():
    return render_template("a1s2.html")

app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)