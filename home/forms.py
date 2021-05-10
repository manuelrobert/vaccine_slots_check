from flask_wtf import FlaskForm
from wtforms import SelectField

# class SlotCheckForm(FlaskForm):
#     district = SelectField(u'SelectDistrict', choices=[
#         ('Alappuzha', 'Alappuzha'),
#         ('Ernakulam', 'Ernakulam'),
#         ('Idukki', 'Idukki'),
#         ('Kannur', 'Kannur')
#         ('Kasargod', 'Kasargod'),
#         ('Kollam', 'Kollam'),
#         ('Kottayam', 'Kottayam'),
#         ('Kozhikode', 'Kozhikode'),
#         ('Malapuram', 'Malapuram'),
#         ('Palakkad', 'Palakkad'),
#         ('Pathanamthitta', 'Pathanamthitta'),
#         ('Thiruvananthapuram', 'Thiruvananthapuram'),
#         ('Thrissur', 'Thrissur'),
#         ('Wayanad', 'Wayanad')
#         ])

class SlotCheckForm(FlaskForm):
    state = SelectField(u'Select State')
    district = SelectField(u'Select District')

    