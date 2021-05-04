from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
	print("in")
	request_method = request.method

	if request.method == 'POST':
		c = request.form['clave']
		print('----------')
		print(request.form)
		print('----------')
		return redirect(url_for('registrar',curp=c))

	return render_template('index.html', request_method=request_method)



@app.route('/registrar/<string:curp>')
def registrar(curp):
	return curp

@app.route('/datos')
def datos():
	return 'datos'

@app.route('/varios')
def varios():
	return 'varios'


if __name__ == '__main__':
	app.run(debug=True)
