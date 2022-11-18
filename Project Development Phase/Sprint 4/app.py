# importing required libraries

from feature import FeatureExtraction
from flask import Flask, request, render_template, redirect, session
import numpy as np
import pandas as pd
from sklearn import metrics
import warnings
import pickle
import time
import requests
warnings.filterwarnings('ignore')

API_KEY = "" #for security reasons haven't displayed API key
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer' + mltoken}

file = open("phishingmodel.pkl", "rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)
app.secret_key = 'key'

user = {"username": "admin", "password": "au_dist_123@"}

# Step – 4 (creating route for login)


@app.route('/', methods=['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:

            session['user'] = username
            return redirect('/login')

        return "<h1>Wrong username or password</h1>"

    return render_template("login.html")

# Step -5(creating route for dashboard and logout)


@app.route('/dashboard')
def dashboard():
    if('user' in session and session['user'] == user['username']):
        time.sleep(5)
        return '<h1>Welcome to the dashboard</h1>'

    return '<h1>You are not logged in.</h1>'

# Step -6(creating route for logging out)


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def hello():
    if request.method == "POST":

        url = request.form.get("url")
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, -1)
        print(x)
        t=[obj.getFeaturesList()]
        payload_scoring = {"input_data": [{"fields": [['having_IPhaving_IP_Address','URLURL_Length','Shortining_Service','having_At_Symbol','double_slash_redirecting','Prefix_Suffix,having_Sub_Domain','SSLfinal_State','Domain_registeration_length','Favicon','port','HTTPS_token','Request_URL,URL_of_Anchor','Links_in_tags','SFH','Submitting_to_email','Abnormal_URL','Redirect	on_mouseover','RightClick','popUpWidnow','Iframe','age_of_domain','DNSRecord','web_traffic','Page_Rank','Google_Index','Links_pointing_to_page','Statistical_report']], "values": t}]}
        

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/859ae568-d692-4958-9dbe-60431a8a0918/predictions?version=2022-11-11', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        y_pred = gbc.predict(x)[0]
        print(y_pred)

        if(y_pred == 1):
            return render_template('index.html', xx=1, url=url)
        else:
            return render_template('index.html', xx=-1, url=url)
    return render_template("index.html", xx=0)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
