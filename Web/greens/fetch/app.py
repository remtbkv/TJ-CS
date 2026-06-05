from flask import Flask, render_template, jsonify
app = Flask(__name__)
app.debug = True

kitchen = {
    "eggs": 1,
    "onions": 3,
    "garlic": 4
}

@app.route('/')
def hello_world():
    return render_template('template.html')

@app.route("/kitchen")
def kitchen_ops():
    return jsonify(kitchen)


# @app.route("/set/<name>/<val>")
# def incEgg(name=None, val=None):
#     global kitchen
#     print('hi')
#     kitchen[name] = int(val)
#     return redirect('/')
#     # return render_template('template.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)