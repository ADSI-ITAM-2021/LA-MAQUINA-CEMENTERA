from flask import Flask, render_template, url_for, request, redirect
import pymongo
import json

with open('tokens.json') as json_file:
    data = json.load(json_file)

client = pymongo.MongoClient(data['mongo'])
users = client['lamaquina'].usuarios

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

	match2 = users.find_one({"id":curp});
	
	#no es un curp
	if(len(curp)!=18):
		return 'cringe';
	
	print(match2)

	#el curp ya esta
	if(match2):
		return "CURP registrado"

	#cargar pagina para rellenar el resto de los datos
	return curp

@app.route('/datos')
def datos():
	return 'datos'

@app.route('/varios')
def varios():
	return 'varios'


if __name__ == '__main__':

	app.run(debug=True)
