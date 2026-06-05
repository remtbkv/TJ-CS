from flask import Flask, render_template, jsonify
app = Flask(__name__)

kitchen = {
    "eggs": 1,
    "onions": 3,
    "garlic": 4
}

@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route("/kitchen")
def kitchen_ops():
    return jsonify(kitchen)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
