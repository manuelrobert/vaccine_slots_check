from sqlalchemy import event
import requests
from main import db

api = 'https://cdn-api.co-vin.in/api'


class State(db.Model):
    __tablename__ = "state"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    districts = db.relationship('District', backref='state', lazy=True)

    def __repr__(self):
        return f"State('{self.id}', '{self.name}',  '{self.districts}')"


class District(db.Model):
    __tablename__ = "district"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    def __repr__(self):
        return f"State('{self.id}', '{self.name}',  '{self.state_id}')"


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
