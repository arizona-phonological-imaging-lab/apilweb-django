from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from UATracker.models import Image
from UATracker.forms import SearchForm
import re
from math import floor

def imageListView(request, page):
    form = SearchForm()
    readyMadeTableCode = searchHandlerView(request, page).getvalue()
    return render_to_response('uatracker/imageList.html', {"tableCode": readyMadeTableCode, 'form': form})

def searchHandlerView(request, page):
#     import pdb
#     pdb.set_trace()
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
    if len(request.GET['context'])>0 or len(request.GET['show_only'])>0:
        conSize = request.GET['context']
        if len(conSize)>0:
            conSize = int(conSize)
        else:
            conSize = 0
        result, thickBorders = calculateContext(result,conSize,request.GET['show_only'])
        
    paginator = Paginator(result, 20)
    visibleItems = paginator.page(page)
    return render_to_response('uatracker/searchHandler.html', {"visibleItems": visibleItems, "urlrequest":request.GET.copy(), "thickBorders": thickBorders})

def getTargetSegment(input):
    input = input.strip()
    target = re.sub(".*\\[(\\w+)\\].*","\\1", input)
    if len(target)>0:
        return target
    else:
        return input


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
#     import pdb
#     pdb.set_trace()
    output = Image.objects.filter(video=image.video).filter(title=newTitle)
    if len(output)>0:
        return output[0]
    else:
        return None


def calculateContext(result, conSize, showOnly):
    newResult = []
    thickBorders = {}       #It's a Dictionary (HashMap) but in fact I'm using it as a HashList. The values are always 1.
    lastImage = None
    counter = 0
    currentSet = []
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
                for im in currentSet:
                    newResult.append(im)
                for i in range(1,conSize+1):
                    contextImage = getContextImage(currentSet[-1],i)
                    if contextImage:
                        newResult.append(contextImage)
                thickBorders[len(newResult)-1] = 1
            #Start a new currentSet
            currentSet = []
            if counter!=len(result)-1:
                currentSet.append(image)
        lastImage = image
        counter += 1
    return newResult, thickBorders
