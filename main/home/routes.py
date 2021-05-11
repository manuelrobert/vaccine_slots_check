from flask import render_template, request, Blueprint, jsonify
import requests
from datetime import date
from main.home.forms import SlotCheckForm


api = 'https://cdn-api.co-vin.in/api'

home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def home_view():
    form = SlotCheckForm()
    if request.method == 'POST':
        print(form.district.data, date.today().strftime("%d-%m-%Y"))
        res = requests.get(api + '/v2/appointment/sessions/public/calendarByDistrict?district_id=' + form.district.data + '&date=' + '11-05-2021', headers={'content-type': 'application/json', 'User-Agent': ''})
        if res.status_code == 200:
            return jsonify({'centers':res.json()['centers']})
    return render_template('home.html', form=form)


@home.route('/district/<state>')
def get_district(state):
    res = requests.get(api + '/v2/admin/location/districts/' + state, headers={'content-type': 'application/json', 'User-Agent': ''})
    if res.status_code == 200:
        districts = [{'id': d['district_id'], 'name':d['district_name']} for d in res.json()['districts']]
        return jsonify({'districts': districts})
    return res.status_code
