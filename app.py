from flask import Flask, request, render_template
import sendgrid
from sendgrid.helpers.mail import *
import os
from flask_sslify import SSLify
import json
from web3.auto.infura import w3
import web3
import contract_abi


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

@app.route("/refer", methods=["POST"])
def refer():
  w3 = web3.Web3(web3.HTTPProvider("https://ropsten.infura.io/v3/55a7676bd3db4746a9a536918d9d448e"))
  contract_address = w3.toChecksumAddress('0xd5b319cCFEF5B5D2BD1C81Fb6B46109Eef63F0eE'.lower())
  advertiser_address = w3.toChecksumAddress('0x5cBA0F3a23023B711C0d94527247a92eea9c982d'.lower())
  adtract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)
  refer_key = request.get_json()['account']
  refer_address = w3.toChecksumAddress(refer_key.lower())
  refer_txn = adtract.functions.refer(refer_address).buildTransaction()
  refer_txn['nonce'] = w3.eth.getTransactionCount(advertiser_address)
  print(refer_txn['nonce'])
  refer_txn['gas'] = 70000
  signed_txn = w3.eth.account.signTransaction(refer_txn, private_key=os.environ['ETH_PRIV'])
  w3.eth.sendRawTransaction(signed_txn.rawTransaction)
  return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
  app.run(host='0.0.0.0')