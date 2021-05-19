from sqlalchemy import event
import requests
from main import db
import datetime

api = 'https://cdn-api.co-vin.in/api'

class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    districts = db.relationship('District', backref='state', cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"State('{self.id}', '{self.name}', '{self.districts}')"

class District(db.Model):
    __tablename__ = 'district'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    centers = db.relationship('Center', backref='district', cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"State('{self.id}', '{self.name}', '{self.state_id}')"

class Center(db.Model):
    __tablename__ = 'center'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)
    block_name = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    lat = db.Column(db.Text, nullable=False)
    long = db.Column(db.Text, nullable=False)
    frm = db.Column(db.Time, nullable=False)
    to = db.Column(db.Time, nullable=False)
    fee_type = db.Column(db.Text, nullable=False)
    sessions = db.relationship('Session', backref='center', cascade="all, delete", lazy=True)

class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Text, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    available_capacity =  db.Column(db.Integer, nullable=False, default=0)
    available_capacity_dose1 =  db.Column(db.Integer, nullable=False, default=0)
    available_capacity_dose2 =  db.Column(db.Integer, nullable=False, default=0)
    min_age_limit = db.Column(db.Integer, nullable=False, default=0)
    vaccine = db.Column(db.Text, nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'), nullable=False)
    slots = db.relationship('Slot', backref='session', cascade="all, delete", lazy=True)

class Slot(db.Model):
    __tablename__ = 'slot'
    id = db.Column(db.Integer, primary_key=True)
    slot_starts = db.Column(db.Time, nullable=False)
    slot_ends = db.Column(db.Time, nullable=False)
    session_id = db.Column(db.Text, db.ForeignKey('session.id'), nullable=False)

@event.listens_for(State.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    res = requests.get(api + '/v2/admin/location/states', headers={'content-type': 'application/json', 'User-Agent': ''})
    if res.status_code == 200:
        states = list([tuple(d.values()) for d in res.json()['states']])
        for i in states:
            db.session.add(State(id=i[0], name=i[1]))
        db.session.commit()
    else:
        print('states fetch result :', res.status_code)

@event.listens_for(District.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    res = requests.get(api + '/v2/admin/location/states', headers={'content-type': 'application/json', 'User-Agent': ''})
    if res.status_code == 200:
        states = list([tuple(d.values()) for d in res.json()['states']])
        for s in states:
            res = requests.get(api + '/v2/admin/location/districts/' + str(s[0]), headers={'content-type': 'application/json', 'User-Agent': ''})
            if res.status_code == 200:
                districts = list([tuple(d.values())for d in res.json()['districts']])
                for i in districts:
                    db.session.add(District(id=i[0], name=i[1], state_id=s[0]))
                db.session.commit()
            else:
                print('district fetch result :', res.status_code)
    else:
        print('states fetch result :', res.status_code)
