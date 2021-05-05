from flask import Flask, render_template, url_for, request, redirect
import json
import requests
import smtplib, ssl
import pymongo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
		return 'CURP invalido';

	print(match2)

	#el curp ya esta
	if(match2):
		return "CURP registrado"

	#cargar pagina para rellenar el resto de los datos
	#render_template('index.html', request_method=request_method)
	return curp

@app.route('/datos')
def datos():
	return 'datos'

@app.route('/varios')
def varios():
	return 'varios'


if __name__ == '__main__':
	app.run(debug=True)

def sendMail(centroV,diaV,urlMap):
	port = 465  # For SSL
mail = 'aadsi6449@gmail.com'
password = 'Adsi123Adsi'
receiver = 'josepe430@gmail.com'

print('datos ingresados')

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
html = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title></title>
    <!--[if (mso 16)]>
    <style type="text/css">
    a {text-decoration: none;}
    </style>
    <![endif]-->
    <!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]-->
    <!--[if gte mso 9]>
<xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG></o:AllowPNG>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
</xml>
<![endif]-->
</head>

<body>
    <div class="es-wrapper-color">
        <!--[if gte mso 9]>
			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
				<v:fill type="tile" color="#2980d9"></v:fill>
			</v:background>
		<![endif]-->
        <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0">
            <tbody>
                <tr>
                    <td class="esd-email-paddings" valign="top">
                        <table cellpadding="0" cellspacing="0" class="es-content esd-header-popover" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" align="center">
                                        <table bgcolor="transparent" class="es-content-body" align="center" cellpadding="0" cellspacing="0" width="600" style="background-color: transparent;">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure es-p10t es-p10b es-p20r es-p20l" align="left">
                                                        <table cellpadding="0" cellspacing="0" width="100%">
                                                            <tbody>
                                                                <tr>
                                                                    <td width="560" class="esd-container-frame" align="center" valign="top">
                                                                        <table cellpadding="0" cellspacing="0" width="100%">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-image" style="font-size: 0px;"><a target="_blank" href="https://www.gob.mx"><img class="adapt-img" src="https://demo.stripocdn.email/content/guids/21403aec-f80d-41a8-a23c-f9487ea4208b/images/12701620172029019.png" alt style="display: block;" width="560"></a></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-image" style="font-size: 0px;"><a target="_blank"><img class="adapt-img" src="https://demo.stripocdn.email/content/guids/21403aec-f80d-41a8-a23c-f9487ea4208b/images/99261620173259461.png" alt style="display: block;" width="100"></a></td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-image" style="font-size: 0px;"><a target="_blank" href="https://www.cementocruzazul.com.mx"><img class="adapt-img" src="https://demo.stripocdn.email/content/guids/21403aec-f80d-41a8-a23c-f9487ea4208b/images/16991620172780041.png" alt style="display: block;" width="560"></a></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="es-content" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" align="center" esd-custom-block-id="61183">
                                        <table class="es-content-body" style="background-color: transparent;" width="600" cellspacing="0" cellpadding="0" bgcolor="transparent" align="center">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure" style="background-position: center bottom;" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="600" valign="top" align="center">
                                                                        <table style="background-position: center bottom; background-color: #ffffff;" width="100%" cellspacing="0" cellpadding="0" bgcolor="#ffffff">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-p10t es-p5b es-p20r es-p20l es-m-txt-l" bgcolor="transparent" align="left">
                                                                                        <h3 style="color: #2980d9;">Estimado o estimada,</h3>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-p10t es-p20r es-p20l" bgcolor="transparent" align="left">
                                                                                        <p>Le agradecemos haberse registrado para el plan de vacunación contra el COVID-19</p>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-p5t es-p20r es-p20l" bgcolor="transparent" align="left">
                                                                                        <p>Su cita a quedado guardada para el día {diaV}</p>
                                                                                    </td>
                                                                                </tr>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-p5t es-p5b es-p20r es-p20l" bgcolor="transparent" align="left">
                                                                                        <p>En el centro de vacunación de {centroV}</p>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="esd-structure" style="background-position: center bottom;" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="600" valign="top" align="center">
                                                                        <table style="background-position: center bottom; background-color: #ffffff; border-radius: 0px 0px 5px 5px; border-collapse: separate;" width="100%" cellspacing="0" cellpadding="0" bgcolor="#ffffff">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="esd-block-spacer" height="0" align="center"></td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="es-content" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" align="center" esd-custom-block-id="61184">
                                        <table class="es-content-body" style="background-color: transparent;" width="600" cellspacing="0" cellpadding="0" bgcolor="transparent" align="center">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure es-p20t es-p20b" style="background-position: center bottom;" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" esd-custom-block-id="14364" width="600" align="left">
                                                                        <table style="background-color: #ffffff; border-radius: 5px; border-collapse: separate;" width="100%" cellspacing="0" cellpadding="0" bgcolor="#ffffff">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td>
                                                                                        <table class="es-table-not-adapt" cellspacing="0" cellpadding="0">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td class="esd-block-image es-p10t es-p5b es-p10r es-p20l" valign="top" align="left" style="font-size:0"><a href="{urlMap}" target="_blank"><img src="https://uxyja.stripocdn.email/content/guids/CABINET_b748f68723c08ea6110c059c05f4df42/images/48681566985721743.png" alt style="display: block;" width="18"></a></td>
                                                                                                    <td align="left">
                                                                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                                                                            <tbody>
                                                                                                                <tr>
                                                                                                                    <td class="esd-block-text es-p5t es-p5b" align="left">
                                                                                                                        <p style="color: #333333; line-height: 120%; font-size: 15px;">{centroV}</p>
                                                                                                                    </td>
                                                                                                                </tr>
                                                                                                            </tbody>
                                                                                                        </table>
                                                                                                    </td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="es-footer esd-footer-popover" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" align="center" esd-custom-block-id="61185">
                                        <table class="es-footer-body" style="background-color: transparent;" width="600" cellspacing="0" cellpadding="0" bgcolor="rgba(0, 0, 0, 0)" align="center">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure es-p5t es-p20b es-p20r es-p20l" style="background-position: center bottom; background-color: transparent;" bgcolor="transparent" align="left">
                                                        <!--[if mso]><table width="560" cellpadding="0" cellspacing="0"><tr><td width="270" valign="top"><![endif]-->
                                                        <table class="es-left" cellspacing="0" cellpadding="0" align="left">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="270" valign="top" align="center">
                                                                        <table style="background-position: center top;" width="100%" cellspacing="0" cellpadding="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="esd-block-text es-m-txt-c es-p5t es-p15b" align="left">
                                                                                        <p>Redes sociales oficiales&nbsp;</p>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <!--[if mso]></td><td width="20"></td><td width="270" valign="top"><![endif]-->
                                                        <table class="es-right" cellspacing="0" cellpadding="0" align="right">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="270" align="left">
                                                                        <table style="background-position: center top;" width="100%" cellspacing="0" cellpadding="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td class="esd-block-social es-p5t es-p5b es-m-txt-c" align="right" style="font-size:0">
                                                                                        <table class="es-table-not-adapt es-social" cellspacing="0" cellpadding="0">
                                                                                            <tbody>
                                                                                                <tr>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href="https://www.facebook.com/gobmexico"><img title="Facebook" src="https://stripo.email/static/assets/img/social-icons/rounded-colored-bordered/facebook-rounded-colored-bordered.png" alt="Fb" width="32"></a></td>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href="https://twitter.com/GobiernoMX"><img title="Twitter" src="https://stripo.email/static/assets/img/social-icons/rounded-colored-bordered/twitter-rounded-colored-bordered.png" alt="Tw" width="32"></a></td>
                                                                                                    <td class="es-p10r" valign="top" align="center"><a target="_blank" href="https://www.instagram.com/gobmexico/"><img title="Instagram" src="https://stripo.email/static/assets/img/social-icons/rounded-colored-bordered/instagram-rounded-colored-bordered.png" alt="Inst" width="32"></a></td>
                                                                                                    <td valign="top" align="center"><a target="_blank" href="https://www.youtube.com/channel/UCvzHrtf9by1-UY67SfZse8w"><img title="Youtube" src="https://stripo.email/static/assets/img/social-icons/rounded-colored-bordered/youtube-rounded-colored-bordered.png" alt="Yt" width="32"></a></td>
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <!--[if mso]></td></tr></table><![endif]-->
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</body>

</html>
"""
print('mensaje escrito')

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

print('mensaje listo')

# Create a secure SSL context
context = ssl.create_default_context()

print('enviando...')

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(mail, password)
    server.sendmail(mail, receiver, message.as_string())
