from flask import Flask, render_template, url_for, request, redirect
import json
import requests
import smtplib, ssl
import pymongo
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pyfiscal.generate import GenerateRFC, GenerateCURP, GenerateNSS, GenericGeneration




class GenerateDataFiscal(GenericGeneration):
	generadores = (GenerateCURP, GenerateRFC)

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

@app.route('/confirm/<string:curp>', methods=['GET', 'POST'])
def confirm(curp):
	request_method = request.method
	if request.method == 'POST':
		print('------------------------------------------')
		print(request.form)
		nombre =	request.form['nombre']
		apellido = request.form['apellido']
		mail = request.form['mail']
		zipc  = request.form['zip']
		#check if curp is registered again
		match2 = users.find_one({"id":curp});
		if(match2):
			return "CURP registrado"
		else:
			match = users.find_one({}, sort=[("folio", pymongo.DESCENDING)])

			f = int(match['folio'])
			f +=1
			doc = {'id':curp,'nombre':nombre, 'apellido':apellido, 
			'mail':mail,'zip_code':zipc, 'folio':f}

			users.insert_one(doc)
            sendMail(nombre, f)
			return render_template('confirm.html',fol=f)

	else:
		return 'error'
	
	return 'cock'

@app.route('/registrar/<string:curp>', methods=['GET', 'POST'])
def registrar(curp):

	request_method = request.method

	match2 = users.find_one({"id":curp});

	#no es un curp
	if(len(curp)!=18):
		return 'CURP invalido';

	print(match2)


	#el curp ya esta
	if(match2):
		return "CURP registrado"

	#cargar pagina para rellenar el resto de los datos
	#if request.method == 'POST':
		#render_template('register.html', request_method=request_method)

	
	return render_template('register.html',clav=curp, request_method=request_method)



@app.route('/datos')
def datos():
	return 'datos'

@app.route('/varios')
def varios():
	return 'varios'


if __name__ == '__main__':
	app.run(debug=True)

def sendMail(nombre,folio):
    port = 465  # For SSL
    mail = 'aadsi6449@gmail.com'
    password = 'Adsi123Adsi'
    receiver = 'josepe430@gmail.com'

    message =  MIMEMultipart("alternative")
    message["Subject"] = "Confirmación registro MiVacuna"
    message["From"] = mail
    message["To"] = receiver

    text = """\
    X
    Estimado o estimada,
    Le agradecemos haberse registrado para el plan de vacunación contra el COVID-19
    Su cita a quedado guardada para el día 30 de septiembre de 2021
    En el centro de vacunación de ITAM campus Santa Teresa
    """
    rawhtml = ""
    with open(os.path.join('templates','mail.txt'), 'r', encoding='utf8') as file:
        rawhtml = file.read().replace('\n', '')
    html = rawhtml.replace("NOMBRE",nombre)
    html = html.replace("NFOLIO",folio)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mail, password)
        server.sendmail(mail, receiver, message.as_string())
