from flask_wtf import FlaskForm
from wtforms import SelectField
import requests

api = 'https://cdn-api.co-vin.in/api'
states = [(None, 'Select State'), (17, 'Kerala')]
res = requests.get(api + '/v2/admin/location/states', headers = {'content-type': 'application/json', 'User-Agent':''})
if res.status_code == 200:
    states = [tuple(d.values()) for d in res.json()['states']]

class SlotCheckForm(FlaskForm):
    state = SelectField('Select State', choices = states)
    district = SelectField('Select District', choices=[(None, 'Select District')])

    