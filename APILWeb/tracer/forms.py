from django.forms import *
from django.core import validators

# TODO: figure out what to do about submit button
class TraceForm(forms.Form):
    name = CharField(label='tracer', required=True)
    subject = CharField(label='subject')
    project_id = CharField(label='project', required=True)
    #trim_points = SelectField(u'Remove points outside RoI?', choices=[(False, 'No'), (True, 'Yes')], validators=[Required()])
    data = CharField(widget=HiddenInput(), label='trace-data')
    roi = CharField(widget=HiddenInput(), label='roi-data')
    #submit = SubmitField(label='dump-traces')
