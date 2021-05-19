from flask import render_template, request, Blueprint, jsonify
import requests
from datetime import date, time, datetime
from main.home.forms import SlotCheckForm
from main import db
from main.models import State, District, Center, Session, Slot

api = 'https://cdn-api.co-vin.in/api'

def convt_time(ts):
    h = int(ts[0:2])
    m = int(ts[3:5])
    s = 0
    ap = ts[5:7]

    if ap == 'AM':
        if h == 12:
            h = 0
    elif ap == 'PM':
        if h != 12:
            h = h + 12
    return [h, m, s]

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

@home.route('/save')
def save_data():
    districts = District.query.all()
    for d in districts:
        if d.state_id == 17:
            res = requests.get(api + '/v2/appointment/sessions/public/calendarByDistrict?district_id='+str(d.id)+'&date='+date.today().strftime("%d-%m-%Y"), headers = {'content-type': 'application/json', 'User-Agent':''})
            if res.status_code == 200:
                for c in res.json()['centers']:
                    f = c['from'].split(':')
                    frm = [int(i) for i in f]
                    t = c['to'].split(':')
                    to = [int(i) for i in t]
                    db.session.add(Center(
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
                        ))
                    for s in c['sessions']:
                        dt = s['date'].split('-')
                        dat = [int(i) for i in dt]
                        db.session.add(Session(
                            id = s['session_id'],
                            date = date(dat[2], dat[1], dat[0]),
                            available_capacity = s['available_capacity'],
                            available_capacity_dose1 = s['available_capacity_dose1'],
                            available_capacity_dose2 = s['available_capacity_dose2'],
                            min_age_limit = s['min_age_limit'],
                            vaccine = s['vaccine'],
                            center_id = c['center_id']
                            ))
                        for slt in s['slots']:
                            ts = slt.split('-')
                            start = convt_time(ts[0])
                            end = convt_time(ts[1])
                            print(time(start[0], start[1], start[2]), time(end[0], end[1], end[2]), s['session_id'])
                            db.session.add(Slot(slot_starts = time(start[0], start[1], start[2]), slot_ends = time(end[0], end[1], end[2]), session_id = s['session_id']))
                db.session.commit()
            else:
                print('result :', res.status_code)
    return 'ok'

@home.route('/update')
def update_data():
    pass

# @home.route('/update')
# def update_data():
#     districts = District.query.all()
#     for d in districts:
#         if d.state_id == 17:
#             print(d)
#             res = requests.get(api + '/v2/appointment/sessions/public/calendarByDistrict?district_id='+str(d.id)+'&date='+date.today().strftime("%d-%m-%Y"), headers = {'content-type': 'application/json', 'User-Agent':''})
#             if res.status_code == 200:

#                 print('dealing with Centers')
#                 centers_db = Center.query.filter_by(district_id=d.id).all()
#                 centers_api = res.json()['centers']
#                 if len(centers_db) > 0:
#                     for c_db in centers_db:
#                         if any(x['center_id']==c_db.id for x in centers_api):
#                             print()
#                             print()
#                             print()
#                             print('checking for updates in center', c_db.id)
#                             c_api = next(c for c in centers_api if c['center_id'] == c_db.id)
#                             f = c_api['from'].split(':')
#                             frm = [int(i) for i in f]
#                             t = c_api['to'].split(':')
#                             to = [int(i) for i in t]
#                             print()
#                             print('from api :from', time(frm[0], frm[1], frm[2]))
#                             print('before in local db :from', c_db.frm)
#                             if time(frm[0], frm[1], frm[2]) != c_db.frm:
#                                 print('change in from')
#                                 c_db.frm = time(frm[0], frm[1], frm[2])
#                                 db.session.commit()
#                             print('after in local db :from', c_db.frm)
#                             print()
#                             print('from api :to', time(to[0], to[1], to[2]))
#                             print('before in local db :to', c_db.to)
#                             if time(to[0], to[1], to[2]) != c_db.to:
#                                 print('change in to')
#                                 c_db.to = time(to[0], to[1], to[2])
#                                 db.session.commit()
#                             print('after in local db :to', c_db.to)
#                             print()
#                             print('from api :fee_type', c_api['fee_type'])
#                             print('before in local db :fee_type', c_db.fee_type)
#                             if c_api['fee_type'] == c_db.fee_type:
#                                 print('change in fee_type')
#                                 c_db.fee_type = c_api['fee_type']
#                                 db.session.commit()
#                             print('after in local db :fee_type', c_db.fee_type)

#                             print()
#                             print()
#                             print()
#                             print('dealing with Sessions')
#                             sessions_db = c_db.sessions
#                             sessions_api = c_api['sessions']
#                             if len(sessions_db) > 0:
#                                 for s_db in sessions_db:
#                                     if any(x['session_id']==s_db.id for x in sessions_api):
#                                         print()
#                                         print('checking for updates in session', s_db.id)
#                                         s_api = next(s for s in sessions_api if s['session_id'] == s_db.id)
#                                         print(s_api)
#                                     else:
#                                         # since the latest data from api do not has such sessions,
#                                         # so we have to delete it from local database
#                                         print()
#                                         print('deleting', s_db.id)
#                                         db.session.delete(s_db)
#                                         db.session.commit()
#                             else:
#                                 # since we found data from api for the sessions for a center and it is not present
#                                 # in local database, so we have to save it
#                                 print('Query result is empty for sessions so saving the api result')
#                                 for s in sessions_api:
#                                     dt = s['date'].split('-')
#                                     dat = [int(i) for i in dt]
#                                     db.session.add(Session(
#                                         id = s['session_id'],
#                                         date = date(dat[2], dat[1], dat[0]),
#                                         available_capacity = s['available_capacity'],
#                                         min_age_limit = s['min_age_limit'],
#                                         vaccine = s['vaccine'],
#                                         center_id = c_db.id
#                                         ))
#                                     for slt in s['slots']:
#                                         ts = slt.split('-')
#                                         start = convt_time(ts[0])
#                                         end = convt_time(ts[1])
#                                         db.session.add(Slot(slot_starts = time(start[0], start[1], start[2]), slot_ends = time(end[0], end[1], end[2]), session_id = s['session_id']))
#                                 db.session.commit()

#                         else:
#                             # since the latest data from api do not has such centers,
#                             # so we have to delete it from local database
#                             print('deleting', c_db.id)
#                             db.session.delete(c_db)
#                             db.session.commit()
#                 else:
#                     # since we found data from api for the district and it is not present
#                     # in local database, so we have to save it
#                     print('Query result is empty for centers so saving the api result')
#                     for c in centers_api:
#                         f = c['from'].split(':')
#                         frm = [int(i) for i in f]
#                         t = c['to'].split(':')
#                         to = [int(i) for i in t]
#                         db.session.add(Center(
#                             id = c['center_id'], 
#                             name = c['name'], 
#                             address = c['address'], 
#                             district_id = d.id, 
#                             block_name = c['block_name'], 
#                             pincode = c['pincode'], 
#                             lat = c['lat'], 
#                             long = c['long'], 
#                             frm = time(frm[0], frm[1], frm[2]), 
#                             to = time(to[0], to[1], to[2]), 
#                             fee_type = c['fee_type']
#                             ))
#                         for s in c['sessions']:
#                             dt = s['date'].split('-')
#                             dat = [int(i) for i in dt]
#                             db.session.add(Session(
#                                 id = s['session_id'],
#                                 date = date(dat[2], dat[1], dat[0]),
#                                 available_capacity = s['available_capacity'],
#                                 min_age_limit = s['min_age_limit'],
#                                 vaccine = s['vaccine'],
#                                 center_id = c['center_id']
#                                 ))
#                             for slt in s['slots']:
#                                 ts = slt.split('-')
#                                 start = convt_time(ts[0])
#                                 end = convt_time(ts[1])
#                                 db.session.add(Slot(slot_starts = time(start[0], start[1], start[2]), slot_ends = time(end[0], end[1], end[2]), session_id = s['session_id']))
#                     db.session.commit()
#             else:
#                 print('result :', res.status_code)

#             # res = requests.get(api + '/v2/appointment/sessions/public/calendarByDistrict?district_id='+str(d.id)+'&date='+date.today().strftime("%d-%m-%Y"), headers = {'content-type': 'application/json', 'User-Agent':''})
#             # if res.status_code == 200:
#             #     for c in res.json()['centers']:
#             #         print(c['center_id'])
#             #         # ctr = Center.query.filter_by(id=c['center_id']).first()
#             #         # if ctr == None:
#             #         #     print(c['center_id'])
#             #         #     s+=1
#             #         # else:
#             #         #     print(ctr)
#             # else:
#             #     print('result :', res.status_code)
#   return 'ok'