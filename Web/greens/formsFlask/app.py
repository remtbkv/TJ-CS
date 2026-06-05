from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/hello_form')
def hello_form():
  return render_template('f.html')

@app.route('/thank_you')
def handle_form():
  return render_template('s.html', answer=request.args.get('ans'))

@app.route('/formed/')
def handle_select():
  return render_template('s.html', answer=request.args.get('choice'))

@app.route('/checkboxed/')
def handle_check():
  return render_template('s.html', answer=request.args.getlist('match'))

@app.route('/multipled/', methods=['POST'])
def handle_multiple():  
  return render_template('s.html', answer=request.form.get('multiple'))


app.debug = True
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)