from flask import render_template, request, Blueprint
import requests

home = Blueprint('home', __name__)

@home.route('/')
def home_view():
    api = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
    res = requests.get(api).json()
    print(res)
    return render_template('home.html')