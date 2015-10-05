from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from UATracker.models import Image

def imageListView(request, page):
    fullList = Image.objects.all()
    paginator = Paginator(fullList, 25) # Show 25 images per page

    try:
        visibleItems = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        visibleItems = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        visibleItems = paginator.page(paginator.num_pages)

    return render_to_response('uatracker/imageList.html', {"visibleItems": visibleItems})