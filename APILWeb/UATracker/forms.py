from django import forms
from UATracker.models import Project, Tag, Experiment, Tracer

class SearchForm(forms.Form):
    theTitle = forms.CharField(label='Image Title', max_length=80)
    theTitle.widget.attrs['style'] = "width:115px"
    project = forms.ChoiceField(label='Project', choices= [["",""]]+[[proj.title,proj.title] for proj in Project.objects.all()])
    project.widget.attrs['style'] = "width:115px"
    experiment = forms.ChoiceField(label='Experiment', choices= [["",""]]+[[exp.content,exp.content] for exp in Experiment.objects.all()])
    experiment.widget.attrs['style'] = "width:115px"
    traced_by = forms.ChoiceField(label='Traced by', choices= [["",""]]+[[tracer.first_name,tracer.first_name] for tracer in Tracer.objects.all()])
    traced_by.widget.attrs['style'] = "width:115px"
    tracers = forms.ChoiceField(label='Tracers', choices= [["",""]]+[["0","0"], ["1","1"], ["2","2"], ["m","More than 2"], ])
    tracers.widget.attrs['style'] = "width:115px"
    tag = forms.ChoiceField(label='Tag', choices= [["",""]]+[[tg.content,tg.content] for tg in Tag.objects.all()])
    tag.widget.attrs['style'] = "width:115px"
    word = forms.CharField(label='Word', max_length=80)
    word.widget.attrs['style'] = "width:115px"
    segment = forms.CharField(label='Segment', max_length=80)
    segment.widget.attrs['style'] = "width:115px"
    peripherals = forms.CharField(label='Peripherals', max_length=60)
    peripherals.widget.attrs['style'] = "width:115px"
    show_only = forms.ChoiceField(label='Show only', choices= [["",""]]+[["Middle","Middle"], ["Second","Second"], ["Second to last","Second to last"], ["Initial","Initial"], ["Final","Final"]])
    show_only.widget.attrs['style'] = "width:115px"
    language = forms.ChoiceField(label='Language', choices= [["",""]]+[[lang,lang] for lang in Project.objects.order_by().values('language').distinct()[0]])
    language.widget.attrs['style'] = "width:115px"
    autotraced = forms.ChoiceField(label='Autotraced', choices= [["",""]]+[["Yes","Yes"], ["No","No"]])
    autotraced.widget.attrs['style'] = "width:115px"