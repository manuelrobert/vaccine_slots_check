from flask import render_template, request, Blueprint, jsonify
import requests
from datetime import date, time, datetime
from main.home.forms import SlotCheckForm
from main.models import State, District, Center, Session, Slot


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

@home.route('/test')
def test():
    districts = District.query.all()
    for d in districts:
        if d.state_id == 17:
            print(d)
            res = requests.get(api + '/v2/appointment/sessions/public/calendarByDistrict?district_id='+str(d.id)+'&date='+date.today().strftime("%d-%m-%Y"), headers = {'content-type': 'application/json', 'User-Agent':''})
            if res.status_code == 200:
                for c in res.json()['centers']:
                    f = c['from'].split(':')
                    frm = [int(i) for i in f]
                    t = c['to'].split(':')
                    to = [int(i) for i in t]
                    # print(time(frm[0], frm[1], frm[2]), time(to[0], to[1], to[2]))
                    # print(c['center_id'], c['name'], c['address'], d.id, c['block_name'], c['pincode'], c['lat'], c['long'], time(frm[0], frm[1], frm[2]), time(to[0], to[1], to[2]), c['fee_type'])
                    center = Center(
                        id = c['center_id'], 
                        name = c['name'], 
                        address = c['address'], 
                        district_id = d.id, 
                        block_name = c['block_name'], 
                        pincode = c['pincode'], 
                        lat = c['lat'], 
                        long = c['long'], 
                        frm = time(frm[0], frm[1], frm[2]), 
                        to = time(to[0], to[1], to[2]), 
                        fee_type = c['fee_type']
                        )
                    print(center)
            else:
                print('result :', res.status_code)
    return 'ok'
