from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def main():
  return render_template('main.html')

@app.route('/submitted/', methods=['POST'])
def handle_multiple():
  return render_template('submitted.html', form=request.form)


app.debug = True
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)