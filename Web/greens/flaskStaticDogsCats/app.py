from flask import Flask, render_template
app = Flask(__name__)

@app.route('/dogs')
def hello_world():
    return render_template('a.html')

@app.route('/cats')
def yoCallback():
    return render_template('b.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)