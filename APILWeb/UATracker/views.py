from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect
from UATracker.models import Image, Tag, Experiment
from UATracker.forms import SearchForm
import re
from django.http import HttpResponse
from math import floor
from django.views.decorators.csrf import ensure_csrf_cookie
import pdb
import json
import zipfile
from django.template import RequestContext

#needed for importing files
import os

@ensure_csrf_cookie
def imageListView(request, page):
    form = SearchForm()
    readyMadeTableCode = searchHandlerView(request, page).getvalue()
    return render_to_response('uatracker/imageList.html', {"tableCode": readyMadeTableCode, 'form': form},context_instance=RequestContext(request))

@ensure_csrf_cookie
def downloadView(request):
    imageList = request.POST.get('ids')
    isWithTrace = request.POST.get('withTrace')
    zf = zipfile.ZipFile("myzipfile.zip", "w")
    pdb.set_trace()
    for id in imageList:
        theImage = Image.objects.get(pk=id)
        theAddress = theImage.address
        print(theAddress)
        zf.write(theAddress)
    zf.close()
    response = HttpResponse(zf, content_type='application/zip', )
    response['Content-Disposition'] = 'attachment; filename=images.zip'
    response['context_instance'] = RequestContext(request)
    return response
    
def getAllIDsView(request):
    result = getResults(request)
    result = result[0]
#     pdb.set_trace()
    ids = []
    for image in result:
        ids.append(image.id)
    print("length: "+str(len(ids)))
    dumped = json.dumps(ids) 
    return HttpResponse(dumped)

def tagView(request):
    imageList = request.POST.getlist('imgs[]')
    newTag = request.POST.get('tagContent')
    if(len(imageList)>0):
        for i in imageList:
            try:
#                 pdb.set_trace()
                t = Tag(image_id=int(i), content=newTag)
                t.save()
            except:
                return HttpResponse("failure:"+sys.exc_info()[0])
        return HttpResponse("success")
    else:
        return HttpResponse("failure")

def untagView(request):
    imageList = request.POST.getlist('imgs[]')
    unwantedTag = request.POST.get('tagContent')
    deletionCounter = 0;
#     pdb.set_trace()
    if(len(imageList)>0):
        for i in imageList:
            try:
                ts = Tag.objects.filter(image_id=int(i), content=unwantedTag)
                for t in ts: 
                    t.delete()
                    deletionCounter += 1
            except:
                pass
        return HttpResponse(str(deletionCounter))
    else:
        return HttpResponse("failure")

def addexpView(request):
    imageList = request.POST.getlist('imgs[]')
    newTag = request.POST.get('expContent')
    if(len(imageList)>0):
        for i in imageList:
            try:
#                 pdb.set_trace()
                t = Experiment(image_id=int(i), content=newTag)
                t.save()
            except:
                return HttpResponse("failure:"+sys.exc_info()[0])
        return HttpResponse("success")
    else:
        return HttpResponse("failure")

def removeexpView(request):
    imageList = request.POST.getlist('imgs[]')
    unwantedTag = request.POST.get('expContent')
    deletionCounter = 0;
    if(len(imageList)>0):
        for i in imageList:
            try:
                ts = Experiment.objects.filter(image_id=int(i), content=unwantedTag)
                for t in ts: 
                    t.delete()
                    deletionCounter += 1
            except:
                pass
        return HttpResponse(str(deletionCounter))
    else:
        return HttpResponse("failure")

def searchHandlerView(request, page):
    result, thickBorders, shaded = getResults(request)
    paginator = Paginator(result, 20)
    visibleItems = paginator.page(page)
    #Recalculate thickBorders and shaded based on page number
    pageThickBorders = {}
    pageShaded = {}
    for i in range(1,21):
        overallIndex = (int(page)-1)*20 + (i-1)
        if overallIndex in thickBorders:
            pageThickBorders[i] = 1
        if overallIndex in shaded:
            pageShaded[i] = 1
    return render_to_response('uatracker/searchHandler.html', {"visibleItems": visibleItems, "urlrequest":request.GET.copy(), "pageThickBorders": pageThickBorders, "pageShaded": pageShaded})

def getResults(request):
    result = Image.objects.all()
    if len(request.GET)>0:
        if len(request.GET['theTitle'])>0:
            result = result.filter(title__contains=request.GET['theTitle'])
        if len(request.GET['project'])>0:    
            result = result.filter(video__project__title=request.GET['project'])
        if len(request.GET['experiment'])>0:
            result = result.filter(experiment__content=request.GET['experiment'])
        if len(request.GET['tag'])>0:  
            result = result.filter(tag__content=request.GET['tag'])
        if len(request.GET['language'])>0:    
            result = result.filter(video__project__language=request.GET['language'])
        if len(request.GET['tracers'])>0 and request.GET['tracers']=='3':    
            result = result.exclude(trace_count='0')
            result = result.exclude(trace_count='1')
            result = result.exclude(trace_count='2')
            result = result.exclude(trace_count='')
        elif len(request.GET['tracers'])>0:
            result = result.filter(trace_count=request.GET['tracers'])
        if len(request.GET['traced_by'])>0:    
            result = result.filter(trace__tracer__first_name=request.GET['traced_by'])
        if len(request.GET['autotraced'])>0 and request.GET['autotraced']=='Yes':    
            result = result.filter(autotraced="1")
        elif len(request.GET['autotraced'])>0 and request.GET['autotraced']=='No':    
            result = result.filter(autotraced="0")
        if len(request.GET['word'])>0:
            result = result.filter(word__spelling=request.GET['word'])
        if len(request.GET['segment'])>0:
            result = result.filter(segment__spelling=getTargetSegment(request.GET['segment']))
        
        
    result = result.order_by('sorting_code')
    if len(request.GET)>0 and len(request.GET['segment'])>0:
            result = advancedSegmentSearch(result,request.GET['segment'])
            
    thickBorders = {}
    shaded = {}
    if (len(request.GET)>0 and len(request.GET['segcontext'])>0) or (len(request.GET)>0 and len(request.GET['show_only'])>0):
        conSize = request.GET['segcontext']
        if len(conSize)>0:
            conSize = int(conSize)
        else:
            conSize = 0
        result, thickBorders, shaded = calculateContext(result,conSize,request.GET['show_only'])
    return result, thickBorders, shaded

def getTargetSegment(inputt):
    inputt = inputt.strip()
    target = re.sub(".*\\[(\\w+)\\].*","\\1", inputt)
    if len(target)>0:
        return target
    else:
        return inputt


def advancedSegmentSearch(imageList, inputt):
    #This is how it works:
    #inputt: c [ch] ea            image.getSegmentSequence: c [ch] (ea) r 0 V
    #NoParan gets rid of the () around ea. Then it's simple substring matching. WITHOUT using regex.
    output = [image for image in imageList if image.segment.spelling==getTargetSegment(inputt) and inputt in noParan(image.getSegmentSequence())]
    return output
        
def noParan(str):
    return re.sub("[\\(\\)]","",str)


def getContextImage(image, offset):
    correctLength = len(image.title)
    titleNumber = re.sub("\\D","",image.title)  # img000045.png --> 000045
    titleNumber = re.sub("^0+","",titleNumber)  # 000045 --> 45
    titleNumber = int(titleNumber)
    newNumber = str(titleNumber+offset)
    lastPart = newNumber+".png"
    prefix = re.sub("^(\\D*).*","\\1",image.title)
    zeros = ""
    for i in range(correctLength-(len(prefix)+len(lastPart))):
        zeros += "0"
    newTitle = prefix+zeros+lastPart
    output = Image.objects.filter(title=newTitle).filter(video=image.video)
#     import pdb
#     pdb.set_trace()
    if len(output)>0:
        return output[0]
    else:
        return None


def calculateContext(result, conSize, showOnly):
    newResult = []
    thickBorders = {}       #It's a Dictionary (HashMap) but in fact I'm using it as a HashList. The values are always 1.
    shaded = {}             #The same idea
    lastImage = None
    counter = 0
    currentSet = []
    result = [r for r in result]
    if len(result)>0:
        result.append(result[0])        #A dummy image added to the end so that we can do things when we get to the end of the list
    for image in result:
        if counter!=len(result)-1 and lastImage and image.segment==lastImage.segment:
            #We are in the middle of a continuous sequence
            currentSet.append(image)
        else:
            #This is the beginning of a new sequence. So let's handle the previous sequence (which is called currentSet!)
            #Update currentSet to only include the required representative frames
            if showOnly=="Middle":
                if len(currentSet)<1:
                    currentSet = []
                else:
                    currentSet = [currentSet[floor(len(currentSet)/2)]]
            elif showOnly=="Second":
                if len(currentSet)<2:
                    currentSet = []
                else:
                    currentSet = [currentSet[1]]
            elif showOnly=="Second to last":
                if len(currentSet)<2:
                    currentSet = []
                else:
                    currentSet = [currentSet[-2]]
            elif showOnly=="Initial":
                if len(currentSet)<1:
                    currentSet = []
                else:
                    currentSet = [currentSet[0]]
            elif showOnly=="Final":
                if len(currentSet)<1:
                    currentSet = []
                else:
                    currentSet = [currentSet[-1]]
            #Add head and tail to currentSet based on the context number chosen
            if len(currentSet)>0:
                for i in range(conSize,0,-1):
                    contextImage = getContextImage(currentSet[0],-i)
                    if contextImage:
                        newResult.append(contextImage)
                        shaded[len(newResult)-1] = 1
                for im in currentSet:
                    newResult.append(im)
                for i in range(1,conSize+1):
                    contextImage = getContextImage(currentSet[-1],i)
                    if contextImage:
                        newResult.append(contextImage)
                        shaded[len(newResult)-1] = 1
                thickBorders[len(newResult)-1] = 1
            #Start a new currentSet
            currentSet = []
            if counter!=len(result)-1:
                currentSet.append(image)
        lastImage = image
        counter += 1
    return newResult, thickBorders, shaded



#Trevor's stuff

def addFilesView(request):

    import re

    print(request);
    if len(request.GET)>0:
        if len(request.GET['projectTitle'])>0:
            title = request.GET['projectTitle']
            print("Project Title:", title)
        if len(request.GET['projectLang'])>0:
            lang = request.GET['projectLang']
            print("Project Language:", lang)
        if len(request.GET['filepath'])>0:
            path = request.GET['filepath']
            print("Image Directory:", path)


    # add stuff to go to filepath and get the files there and add them to the database
    filesindir = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]

    bigdirpattern = re.compile("(\d*)\w_(\d*-\d*-\d*)")
    pngpattern = re.compile("frame-(\d*.png)$")

    for x in os.listdir(path):
        if os.path.isdir(os.path.join(path,x)):
            if bigdirpattern.match(x):
                subject = re.search(bigdirpattern,x).group(1)
                date = re.search(bigdirpattern,x).group(2)
                for f in os.listdir(os.path.join(path,x,"frames")): 
                    if pngpattern.match(f):
                        filename = re.search(pngpattern,f).group(1)
                        tracedpattern = re.compile("frame-"+filename+".(\w).traced.txt")
                        for r in os.listdir(os.path.join(path,x,"frames")): 
                            if pngpattern.match(r):
                                tracer = re.search(tracedpattern,r).group(1)





    print(filesindir)
    
    return redirect('/uat/successfullyadded/')

def addsuccess(request):
    return redirect('/uat/1')