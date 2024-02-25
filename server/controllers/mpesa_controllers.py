from flask import Flask, request, Blueprint
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64


mpesa_bp=Blueprint("mpesa_bp", __name__)

base_url = 'http://172.21.0.106:5555'
consumer_key_det = 'EGbS4odEnAjVL276tW3juXG7iGSVj9wzeBckxHsSjWi1Mpik'
consumer_secret_det = 'Ioo6MNTifVWP6sMoTmjpeyN3tdkdFvyAm26yxM5ZxSPJjuKqR50jxp02OwJbTwA2'


@mpesa_bp.route('/')
def home():
    return 'Hello World!'

@mpesa_bp.route('/access_token')
def get_access_token():
    consumer_key = consumer_key_det
    consumer_secret = consumer_secret_det
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data['access_token']

@mpesa_bp.route('/register')
def register_urls():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    access_token = _access_token()
    my_endpoint = base_url + "c2b/"
    headers = { "Authorization": "Bearer %s" % access_token }
    r_data = {
        "ShortCode": "600383",
        "ResponseType": "Completed",
        "ConfirmationURL": my_endpoint + '/con',
        "ValidationURL": my_endpoint + '/val'
    }

    response = requests.post(endpoint, json = r_data, headers = headers)
    return response.json()


@mpesa_bp.route('/simulate')
def test_payment():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    access_token = _access_token()
    headers = { "Authorization": "Bearer %s" % access_token }

    data_s = {
        "Amount": 100,
        "ShortCode": "600383",
        "BillRefNumber": "test",
        "CommandID": "CustomerPayBillOnline",
        "Msisdn": "254708374149"
    }

    res = requests.post(endpoint, json= data_s, headers = headers)
    return res.json()

@mpesa_bp.route('/b2c')
def make_payment():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
    access_token = _access_token()
    headers = { "Authorization": "Bearer %s" % access_token }
    my_endpoint = base_url + "/b2c/"

    data = {
        "InitiatorName": "apitest342",
        "SecurityCredential": "SQFrXJpsdlADCsa986yt5KIVhkskagK+1UGBnfSu4Gp26eFRLM2eyNZeNvsqQhY9yHfNECES3xyxOWK/mG57Xsiw9skCI9egn5RvrzHOaijfe3VxVjA7S0+YYluzFpF6OO7Cw9qxiIlynYS0zI3NWv2F8HxJHj81y2Ix9WodKmCw68BT8KDge4OUMVo3BDN2XVv794T6J82t3/hPwkIRyJ1o5wC2teSQTgob1lDBXI5AwgbifDKe/7Y3p2nn7KCebNmRVwnsVwtcjgFs78+2wDtHF2HVwZBedmbnm7j09JO9cK8glTikiz6H7v0vcQO19HcyDw62psJcV2c4HDncWw==",
        "CommandID": "BusinessPayment",
        "Amount": "200",
        "PartyA": "601342",
        "PartyB": "254708374149",
        "Remarks": "Pay Salary",
        "QueueTimeOutURL": my_endpoint + "timeout",
        "ResultURL": my_endpoint + "result",
        "Occasion": "Salary"
    }

    res = requests.post(endpoint, json = data, headers = headers)
    return res.json()

@mpesa_bp.route('/lnmo')
def init_stk():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    access_token = _access_token()
    headers = { "Authorization": "Bearer %s" % access_token }
    my_endpoint = base_url + "/lnmo"
    Timestamp = datetime.now()
    times = Timestamp.strftime("%Y%m%d%H%M%S")
    password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + times
    datapass = base64.b64encode(password.encode('utf-8'))

    data = {
        "BusinessShortCode": "174379",
        "Password": datapass.decode(),
        "Timestamp": times,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": "254741762502", # fill with your phone number
        "PartyB": "174379",
        "PhoneNumber": "254741762502", # fill with your phone number
        "CallBackURL": my_endpoint,
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": 2
    }

    res = requests.post(endpoint, json = data, headers = headers)
    return res.json()

@mpesa_bp.route('/lnmo', methods=['POST'])
def lnmo_result():
    data = request.get_data()
    f = open('lnmo.json', 'a')
    f.write(data)
    f.close()

@mpesa_bp.route('/b2c/result', methods=['POST'])
def result_b2c():
    data = request.get_data()
    f = open('b2c.json', 'a')
    f.write(data)
    f.close()

@mpesa_bp.route('/b2c/timeout', methods=['POST'])
def b2c_timeout():
    data = request.get_json()
    f = open('b2ctimeout.json', 'a')
    f.write(data)
    f.close()

@mpesa_bp.route('/c2b/val', methods=['POST'])
def validate():
    data = request.get_data()
    f = open('data_v.json', 'a')
    f.write(data)
    f.close()

@mpesa_bp.route('/c2b/con', methods=['POST'])
def confirm():
    data = request.get_json()
    f = open('data_c.json', 'a')
    f.write(data)
    f.close()


def _access_token():
    consumer_key = consumer_key_det
    consumer_secret = consumer_secret_det
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data['access_token']


