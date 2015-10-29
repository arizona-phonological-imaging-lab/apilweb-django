from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from UATracker.models import Image
from UATracker.forms import SearchForm

def imageListView(request, page):
    form = SearchForm()
    readyMadeTableCode = searchHandlerView(request, page).getvalue()
    return render_to_response('uatracker/imageList.html', {"tableCode": readyMadeTableCode, 'form': form})


def searchHandlerView(request, page):
#     import pdb;
#     pdb.set_trace()
    result = Image.objects.all()
    if len(request.GET)>0:
        if len(request.GET['theTitle'])>0:
            result = Image.objects.filter(title__contains=request.GET['theTitle'])
        if len(request.GET['project'])>0:    
            result = Image.objects.filter(video__project__title=request.GET['project'])
        if len(request.GET['experiment'])>0:    
            result = Image.objects.filter(experiment__content=request.GET['experiment'])
        if len(request.GET['tag'])>0:    
            result = Image.objects.filter(tag__content=request.GET['tag'])
        if len(request.GET['language'])>0:    
            result = Image.objects.filter(video__project__language=request.GET['language'])
        if len(request.GET['tracers'])>0 and request.GET['tracers']=='3':    
            result = Image.objects.exclude(trace_count='0')
            result = Image.objects.exclude(trace_count='1')
            result = Image.objects.exclude(trace_count='2')
            result = Image.objects.exclude(trace_count='')
        elif len(request.GET['tracers'])>0:
            result = Image.objects.filter(trace_count=request.GET['tracers'])
        if len(request.GET['traced_by'])>0:    
            result = Image.objects.filter(trace__tracer__first_name=request.GET['traced_by'])
        if len(request.GET['autotraced'])>0 and request.GET['autotraced']=='Yes':    
            result = Image.objects.filter(autotraced="1")
        elif len(request.GET['autotraced'])>0 and request.GET['autotraced']=='No':    
            result = Image.objects.filter(autotraced="0")
        if len(request.GET['project'])>0:    
            result = Image.objects.filter(video__project__title=request.GET['project'])
        if len(request.GET['project'])>0:    
            result = Image.objects.filter(video__project__title=request.GET['project'])
        if len(request.GET['project'])>0:    
            result = Image.objects.filter(video__project__title=request.GET['project'])
        if len(request.GET['project'])>0:    
            result = Image.objects.filter(video__project__title=request.GET['project'])
        if len(request.GET['project'])>0:    
            result = Image.objects.filter(video__project__title=request.GET['project'])
        
        
    result = result.order_by('sorting_code')
    paginator = Paginator(result, 20)
    visibleItems = paginator.page(page)
    return render_to_response('uatracker/searchHandler.html', {"visibleItems": visibleItems})




