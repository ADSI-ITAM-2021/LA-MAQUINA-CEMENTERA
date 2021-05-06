from flask import Flask, render_template, url_for, request, redirect, flash
import json
import requests
import smtplib, ssl
import pymongo
import os
import pgeocode
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
app.secret_key = data['mongo']

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
			sendMail(str(nombre), str(f))
			return render_template('confirm.html', postal = zipc ,fol=f)

	else:
		return 'error'
	
	return 'cock'

@app.route('/mapa/<string:zipcode>')
def mapa(zipcode):
	#try:
		postal = int(zipcode)
		llave = data["google"]
		#mandar coordinadas al mapa por aqui
		nomi = pgeocode.Nominatim('mx')
		df = nomi.query_postal_code(str(postal))
		return render_template('mapa.html',lat = df.latitude, lng=df.longitude, llave = llave)
	#except:
		return 'error'

		return zipcode

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



@app.route('/datos', methods=['GET', 'POST'])
def datos():
	request_method = request.method
	if request.method == 'POST':
		print(request.form)
		s=request.form['fecha']
		fech = s[8:]+'-'+s[5:7]+'-'+s[0:4]
		kwargs = {
		"complete_name": request.form['nombre'],
		"last_name": request.form['apellidopat'],
		"mother_last_name": request.form['apellidomat'],
		"birth_date": fech,
		"gender": request.form['gender'],
		"city": request.form['estado'],
		"state_code": "11111"
		}
		curpaprox = GenerateCURP(**kwargs)
		curpgen = curpaprox.data
		print(curpgen)
		return redirect(url_for('registrar',curp=curpgen))

	return render_template('sinCURP.html')

@app.route('/varios', methods=['GET', 'POST'])
def varios():
	request_method = request.method
	if request.method == 'POST':
		print('not cringe')
		print(request.form)
		
		curps = request.form['texts'].split(',')
		for c in curps:
			if(len(c)!=18):
				flash('Al menos un CURP es incorrecto')
				return render_template('varios.html', request_method=request_method)
		#upload to mongodb here
		#for c in curps:


	return render_template('varios.html', request_method=request_method)


if __name__ == '__main__':
    app.run(debug=True)

