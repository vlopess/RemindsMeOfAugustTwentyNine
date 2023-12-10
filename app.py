import os
import sys
from flask import Flask, redirect, render_template, request, make_response
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
from os.path import join, dirname, realpath

from EmailRepository import emailRepository
from EmailException import EmailException

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/images/')
scheduler = APScheduler()

app = Flask(__name__,template_folder='templates',   static_folder='static')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
bootstrap = Bootstrap(app)
scheduler.init_app(app)
scheduler.start()

db = emailRepository()

tz = timezone('America/Sao_Paulo')

def connect():
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('remindmeofthisdate@gmail.com','stxdwardlseyadsz')
    return smtpObj

def send_email(email, content):
    smtpObj = connect()
    smtpObj.sendmail('remindmeofthisdate@gmail.com', email, content.as_string())
    smtpObj.quit()

def confirm_email(nome, email):
  try:
    email_msg = MIMEMultipart('related')
    email_msg['Subject'] = " Lembrete - 29 de agosto: O Fabuloso Destino de Amélie Poulain"
    msg = MIMEMultipart('alternative')
    email_msg.attach(msg)
    msgText = MIMEText(f"""<h1>Confirmação de Recebimento - Lembrete Especial</h1><br><p>Olá {nome}, este email é de verificação !</p>
                      <p>Se você não se inscreveu para receber esses lembretes ou mudou de ideia, simplesmente ignore este e-mail.</p>
                      <img src="cid:image1"><br>
                      Atenciosamente,<br>
                      Developer <a href='github.com/vlopess'>Victor L.</a>""", 'html')
    msg.attach(msgText)
    file = open(UPLOADS_PATH + 'amelie-1.jpg', 'rb')    
    msgImage = MIMEImage(file.read())
    file.close()
    msgImage.add_header('Content-ID', '<image1>')
    email_msg.attach(msgImage)  
    send_email(email, email_msg)
    print(f'Enviado para {email}')
  except Exception as e:
    print(e)

def Week_before_email(nome, email):
  try:
    email_msg = MIMEMultipart('related')
    email_msg['Subject'] = " Lembrete - 29 de agosto: O Fabuloso Destino de Amélie Poulain"
    msg = MIMEMultipart('alternative')
    email_msg.attach(msg)
    msgText = MIMEText(
      f"""<h1>Assunto: Lembrança Especial em Breve!</h1><br><p>Olá  {nome},</p><p>Espero que esta mensagem o encontre bem. 
      Estou escrevendo para lembrá-lo que 28 de agosto é em breve. Se você ainda não viu o filme ou se deseja reviver esse momento encantador, 
      reserve um tempo para assisti-lo ou apenas reflita sobre o mesmo.</p>
      <p>Que essa data sirva como inspiração para pequenos gestos de bondade e mudanças positivas em nossas próprias vidas.</p>      
      <br><img src="cid:image1"><br>
      Atenciosamente,<br>
      Developer <a href='github.com/vlopess'>Victor L.</a>"""
      , 'html')
    msg.attach(msgText)
    file = open(UPLOADS_PATH + 'amelie-2.jpg', 'rb')
    msgImage = MIMEImage(file.read())
    file.close()
    msgImage.add_header('Content-ID', '<image1>')
    email_msg.attach(msgImage)  
    send_email(email, email_msg)
    print(f'Enviado para {email}')    
  except Exception as e:
    print(e)

def in_day_email(nome, email):
  try:
    email_msg = MIMEMultipart('related')
    email_msg['Subject'] = " Lembrete - 29 de agosto: O Fabuloso Destino de Amélie Poulain"
    msg = MIMEMultipart('alternative')
    email_msg.attach(msg)
    msgText = MIMEText(
      f"""<h1>Assunto: O Dia que a Vida de Amélie Mudou!</h1><br><p>Olá  {nome}, <br>Hoje é um dia especial! 
        No filme "O Fabuloso Destino de Amélie Poulain", Amélie experimentou uma mudança significativa em sua vida no dia 28 de agosto. 
        Seja assistindo ao filme novamente ou simplesmente lembrando da importância dessa data, convido você a aproveitar o dia para refletir 
        sobre as pequenas alegrias da vida e considerar como podemos fazer a diferença na vida das pessoas ao nosso redor.</p><br>
        <p>Que este lembrete traga inspiração e reflexão para o seu dia!</p>
      <br><img src="cid:image1"><br>
      Atenciosamente,<br>
      Developer <a href='github.com/vlopess'>Victor L.</a>"""
      , 'html')
    msg.attach(msgText)
    file = open(UPLOADS_PATH + 'phase.png', 'rb')
    msgImage = MIMEImage(file.read())
    file.close()
    msgImage.add_header('Content-ID', '<image1>')
    email_msg.attach(msgImage)  
    send_email(email, email_msg)
    print(f'Enviado para {email}')    
  except Exception as e:
    print(e)

@app.route("/")
def index():
  return render_template('index.html')
  
@app.route('/enviar', methods=['POST'])
def receber_dados():
  try:
      nome = request.form['nome']
      email = request.form['email']
      db.selectwhere(email)
      db.insert(email)
      # Primeiro email: confirmação
      job = scheduler.add_job(
            func=confirm_email,
            trigger="date", 
            run_date=tz.localize(datetime.now()),                 args=[nome, email],
            id=f'{email}_1',
            replace_existing=True,
            misfire_grace_time=None
      )
      print(job)
      #Segundo email: Uma semana antes
      job = scheduler.add_job(
            func=Week_before_email,
            trigger="date", 
            run_date=tz.localize(datetime(2023, 12, 11, 10, 3)),                 args=[nome, email],
            id=f'{email}_2',
            replace_existing=True,
            misfire_grace_time=None
      )
      print(job)
      #Terceiro email: No dia
      job = scheduler.add_job(
            func=in_day_email,
            trigger="date", 
            run_date=tz.localize(datetime(2023, 12, 10, 10, 5)),                 args=[nome, email],
            id=f'{email}_3',
            replace_existing=True,
            misfire_grace_time=None
      )
      print(job)
      return render_template('result.html', title = 'Seu e-mail será enviado!', subtitle='Aguarde, pois você será lembrado.')  
  except EmailException as e:
    return render_template('registered.html')

  
@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(e):
 return render_template('405.html'), 405

@app.route("/500")
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden_zone(e):
 return render_template('500.html'), 500

  
if __name__ == '__main__':
  app.run("0.0.0.0",8080, True)
  
