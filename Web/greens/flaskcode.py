from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/t1')
def t1():
    return render_template("template1.html")

@app.route('/t2')
def t2():
    return render_template("template2.html")

@app.route('/t3')
def t3():
    return render_template("template3.html")

@app.route('/level2/')
def l2():
    return render_template("l2.html")

@app.route('/level2/level3/')
def l3():
    return render_template("l3.html")

@app.route('/user/<name>')
def render_name(name=None):
    return render_template("name_template.html", name=name)

app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)