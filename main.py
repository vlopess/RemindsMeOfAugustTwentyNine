from flask import Flask, render_template, request, make_response
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_apscheduler import APScheduler
import time
from pytz import timezone



scheduler = APScheduler()

app = Flask(__name__,template_folder='templates',   static_folder='static')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
bootstrap = Bootstrap(app)
scheduler.init_app(app)
scheduler.start()

tz = timezone('America/Sao_Paulo')


def send_email(nome, email):
  try:
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('remindmeofthisdate@gmail.com','stxdwardlseyadsz')
    email_msg = MIMEMultipart('related')
    email_msg['Subject'] = " Lembrete - 29 de agosto: O Fabuloso Destino de Amélie Poulain"
    msg = MIMEMultipart('alternative')
    email_msg.attach(msg)
    msgText = MIMEText(f'<h1>[TESTE]!</h1><br><p>Olá {nome}, não se esqueça dessa data!</p><br><br><img src="cid:image1">', 'html')
    msg.attach(msgText)
    file = open('images/phase.png', 'rb')
    msgImage = MIMEImage(file.read())
    file.close()
    msgImage.add_header('Content-ID', '<image1>')
    email_msg.attach(msgImage)  
    smtpObj.sendmail('remindmeofthisdate@gmail.com', email, email_msg.as_string())
    smtpObj.quit()
    print(f'Enviado para {email}')
  except:
    print('Algo ocorreu')

def send_email2(nome, email):
  try:
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('remindmeofthisdate@gmail.com','stxdwardlseyadsz')
    email_msg = MIMEMultipart('related')
    email_msg['Subject'] = " Lembrete - 29 de agosto: O Fabuloso Destino de Amélie Poulain"
    msg = MIMEMultipart('alternative')
    email_msg.attach(msg)
    msgText = MIMEText(f'<h1>[TESTE2]!</h1><br><p>Olá {nome}, não se esqueça dessa data!</p><br><br><img src="cid:image1">', 'html')
    msg.attach(msgText)
    file = open('images/phase.png', 'rb')
    msgImage = MIMEImage(file.read())
    file.close()
    msgImage.add_header('Content-ID', '<image1>')
    email_msg.attach(msgImage)  
    smtpObj.sendmail('remindmeofthisdate@gmail.com', email, email_msg.as_string())
    smtpObj.quit()
    print(f'Enviado para {email}')    
  except:
    print('Algo ocorreu!')

@app.route("/")
def index():
  return render_template('index.html')
  
@app.route('/enviar', methods=['POST'])
def receber_dados():
  nome = request.form['nome']
  email = request.form['email']   
  job = scheduler.add_job(
        func=send_email,
        trigger="date", 
        run_date=tz.localize(datetime(2023, 12, 5, 6, 53)),                 args=[nome, email],
        id=f'{email}_1',
        replace_existing=True,
        misfire_grace_time=None
  )
  print(job)
  job = scheduler.add_job(
        func=send_email2,
        trigger="date", 
        run_date=tz.localize(datetime(2023, 12, 5, 6, 55)),                 args=[nome, email],
        id=f'{email}_2',
        replace_existing=True,
        misfire_grace_time=None
  )
  print(job)
  return render_template('result.html', title = 'Seu e-mail foi enviado com sucesso!', subtitle='Aguarde, pois você será lembrado.')
  
@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404
@app.errorhandler(405)
def method_not_allowed(e):
 return render_template('405.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500

  
if __name__ == '__main__':
  app.run("0.0.0.0",8080)
  