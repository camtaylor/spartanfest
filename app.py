from flask import Flask, request, render_template
import sendgrid
from sendgrid.helpers.mail import *
import os
from flask_sslify import SSLify

app = Flask(__name__, static_url_path='/static')
# sslify = SSLify(app)

@app.route("/", methods=["GET"])
def home():
  return render_template("index.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
  if request.method == "POST":
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(request.form['email'])
    to_email = Email("camerontaylor00@gmail.com")
    subject = "Contact Form From Website"
    if request.form['phone']:
      phone = request.form['phone']
    else:
      phone = ""
    if request.form['name'] and request.form['message']:
      content = Content("text/plain", "Name: {} Phone:{} Body: {}".format(
        request.form['name'],phone,request.form['message']
      ))
    else:
      return render_template("index.html")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

  return render_template("index.html")
if __name__ == "__main__":
  app.run(host='0.0.0.0')