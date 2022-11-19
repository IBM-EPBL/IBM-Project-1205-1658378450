# importing required libraries

from feature import FeatureExtraction
from flask import Flask, request, render_template, redirect, session, url_for
import numpy as np
import pandas as pd
from sklearn import metrics
import warnings
import pickle
import time
import requests
from flask_mail import Mail, Message
import smtplib

warnings.filterwarnings('ignore')

# for security reasons haven't displayed API key
API_KEY = ""
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer' + mltoken}


app = Flask(__name__)
app.secret_key = 'key'
mail = Mail(app)


#file = open("phishingmodel.pkl", "rb")
#gbc = pickle.load(file)
#file.close()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'webphishingdetection@gmail.com'
app.config['MAIL_PASSWORD'] = ''  #password has not been displayes
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# Step – 4 (creating route for login)


@app.route('/', methods=['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        email = request.form.get('email')
        session['email'] = email
        return redirect('/login')

    return render_template("login.html")

# Step -5(creating route for dashboard and logout)


@app.route('/dashboard')
def dashboard():

    time.sleep(5)
    return '<h1>Welcome to the dashboard</h1>'


# Step -6(creating route for logging out)


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        email = session['email']
        url = request.form.get("url")
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList())
        x = np.insert(x,0,0,axis=0)
        print(x)
        x=x.reshape(1,-1)
        t=x.tolist()
        print("len: ",len(t))
        print("t is",t)
        payload_scoring = {"input_data": [{"fields": [['index','having_IPhaving_IP_Address', 'URLURL_Length', 'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix,having_Sub_Domain', 'SSLfinal_State', 'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token',
                                                       'Request_URL,URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL', 'Redirect	on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report']], "values": t}]}

        print(len(payload_scoring['input_data']))
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/948ea9c4-816c-4e28-92c1-1ebd3f4c9b27/predictions?version=2022-11-18',
                                         json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        predic = response_scoring.json()
        y_pred = predic['predictions'][0]['values'][0][0]
        print(y_pred)

        if(y_pred == 1):

            return render_template('index.html', xx=1, url=url, email=email)
        else:
            msg = Message(
                'Web Phishing Detection - Identified Malicious URL',
                sender='webphishingdetection@gmail.com',
                recipients=[email]
            )
            msg.body = 'This url: '+url + \
                ' is malicious as per our predictions, please be careful and not open the website'
            mail.send(msg)
            return render_template('index.html', xx=-1, url=url, email=email)
    return render_template("index.html", xx=0)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
