from flask import render_template, request, Blueprint, jsonify, json
from home.forms import SlotCheckForm
import requests
from datetime import date


api = 'https://cdn-api.co-vin.in/api'

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def home_view():
    form = SlotCheckForm()
    if request.method == 'POST':
        print(form.district.data, date.today().strftime("%d-%m-%Y"))
        res = requests.get(api + '/v2/appointment/sessions/public/findByDistrict?district_id=' + form.district.data + '&date=' + '11-05-2021', headers={'content-type': 'application/json', 'User-Agent': ''})
        if res.status_code == 200:
            print('result', res.json())
        return 'ok'
    return render_template('home.html', form=form)


@home.route('/district/<state>')
def get_district(state):
    res = requests.get(api + '/v2/admin/location/districts/' + state, headers={'content-type': 'application/json', 'User-Agent': ''})
    if res.status_code == 200:
        districts = [{'id': d['district_id'], 'name':d['district_name']} for d in res.json()['districts']]
        return jsonify({'districts': districts})
    return res.status_code
