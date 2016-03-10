from django import forms
from UATracker.models import Project, Tag, Experiment, Tracer

class SearchForm(forms.Form):
    theTitle = forms.CharField(label='Image Title', max_length=80)
    theTitle.widget.attrs['style'] = "width:115px"
    project = forms.ChoiceField(label='Project', choices= [["",""]]+[[proj.title,proj.title] for proj in Project.objects.all()])
    project.widget.attrs['style'] = "width:115px"
    experiment = forms.ChoiceField(label='Experiment', choices= [["",""]]+[[exp[0],exp[0]] for exp in Experiment.objects.values_list('content').distinct()])
    experiment.widget.attrs['style'] = "width:115px"
    traced_by = forms.ChoiceField(label='Traced by', choices= [["",""]]+[[tracer.first_name,tracer.first_name] for tracer in Tracer.objects.all()])
    traced_by.widget.attrs['style'] = "width:115px"
    tracers = forms.ChoiceField(label='Tracers', choices= [["",""]]+[["0","0"], ["1","1"], ["2","2"], ["m","More than 2"], ])
    tracers.widget.attrs['style'] = "width:115px"
    tag = forms.ChoiceField(label='Tag', choices= [["",""]]+[[tag[0],tag[0]] for tag in Tag.objects.values_list('content').distinct()])
    tag.widget.attrs['style'] = "width:115px"
    word = forms.CharField(label='Word', max_length=80)
    word.widget.attrs['style'] = "width:115px"
    segment = forms.CharField(label='Segment', max_length=80)
    segment.widget.attrs['style'] = "width:115px"
    segcontext = forms.CharField(label='Context', max_length=60)
    segcontext.widget.attrs['style'] = "width:115px"
    show_only = forms.ChoiceField(label='Show only', choices= [["",""]]+[["Middle","Middle"], ["Second","Second"], ["Second to last","Second to last"], ["Initial","Initial"], ["Final","Final"]])
    show_only.widget.attrs['style'] = "width:115px"
    language = forms.ChoiceField(label='Language', choices= [["",""]]+[[lang[0],lang[0]] for lang in Project.objects.values_list('language').distinct()])
    language.widget.attrs['style'] = "width:115px"
    autotraced = forms.ChoiceField(label='Autotraced', choices= [["",""]]+[["Yes","Yes"], ["No","No"]])
    autotraced.widget.attrs['style'] = "width:115px"
