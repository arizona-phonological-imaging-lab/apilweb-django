from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from UATracker.models import *
from UATracker.forms import SearchForm
from django.http import HttpResponse
from django.template import RequestContext
from UATracker.textGridReader import readTextGrid
from math import floor
from time import gmtime, strftime
import re
import time
import pdb
import json
import zipfile
from django.core.servers.basehttp import FileWrapper
from django.db.models import Q

#needed for importing files
import os
tracersList = {}

@ensure_csrf_cookie
def imageListView(request, page):
    form = SearchForm()
    readyMadeTableCode = searchHandlerView(request, page).getvalue()
    return render_to_response('uatracker/imageList.html', {"tableCode": readyMadeTableCode, 'form': form},context_instance=RequestContext(request))

@ensure_csrf_cookie
def downloadView(request):
    imageList = request.POST.get('ids')
    isWithTrace = request.POST.get('withtraces')
    downloadStructure = request.POST.get('downloadstructure')
    zf = zipfile.ZipFile("imgs.zip", "w")
    imageList = imageList.split(',')
    print(imageList)
    for id in imageList:
        theImage = Image.objects.get(pk=id)
        theAddress = theImage.address
        if isWithTrace=='1':
            traceObjs = theImage.trace_set.all()
            for trace in traceObjs:
                abs_src = os.path.abspath(trace.address)
                if downloadStructure=='directories':
                    zf.write(abs_src, os.path.join("UATracker_download", theImage.video.project.title, theImage.video.title, theImage.title+"_"+trace.tracer.first_name+".txt"))
                else:
                    zf.write(abs_src, os.path.join("UATracker_download", theImage.video.project.title+"_"+theImage.video.title+"_"+theImage.title+"_"+trace.tracer.first_name+".txt"))
        abs_src = os.path.abspath(theAddress)
        if downloadStructure=='directories':
            zf.write(abs_src, os.path.join("UATracker_download", theImage.video.project.title, theImage.video.title, theImage.title))
        else:
            zf.write(abs_src, os.path.join("UATracker_download", theImage.video.project.title+"_"+theImage.video.title+"_"+theImage.title))
    zf.close()
    fsock = open('imgs.zip',"rb")
    response = HttpResponse(fsock, content_type='application/zip', )
    response['Content-Disposition'] = 'attachment; filename=images.zip'
    response['X-Sendfile'] = zf
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
    import logging
    logger = logging.getLogger('hoo')
    logger.error('alaki')
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
            inputSeg = re.sub('\d','',request.GET['segment'])
            targetSeg = getTargetSegment(request.GET['segment'])
            if targetSeg.endswith('*'):
                targetSeg = targetSeg[:-1]
                result = result.filter(Q(segment__spelling=targetSeg+'0') | Q(segment__spelling=targetSeg+'1') | Q(segment__spelling=targetSeg+'2') | Q(segment__spelling=targetSeg+'3'))
            else:
                result = result.filter(segment__spelling=targetSeg)
        
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
    if inputt.endswith('*'):
        output = [image for image in imageList if inputt[:-1]+'0' in noParan(image.getSegmentSequence())]
        output += [image for image in imageList if inputt[:-1]+'1' in noParan(image.getSegmentSequence())]
        output += [image for image in imageList if inputt[:-1]+'2' in noParan(image.getSegmentSequence())]
        output += [image for image in imageList if inputt[:-1]+'3' in noParan(image.getSegmentSequence())]
    else:
        output = [image for image in imageList if inputt in noParan(image.getSegmentSequence())]
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
    try:
        start = time.time()
        title = ''
        lang = ''
        path = ''
        importType = ''
        if len(request.GET)>0:
            if len(request.GET['projectTitle'])>0:
                title = request.GET['projectTitle']
                print("Project Title:", title)
            if len(request.GET['projectLang'])>0:
                lang = request.GET['projectLang']
                print("Project Language:", lang)
            if len(request.GET['filepath'])>0:
                path = request.GET['filepath']
            if len(request.GET['type'])>0:
                importType = request.GET['type']
    
        #get a list of tracers 
        listOfTracers = Tracer.objects.values('first_name').distinct()
        
        bigdirpattern = re.compile("(\d*)\w_(\d*-\d*-\d*)")
        pngpattern = re.compile("(frame-)?(\d*.(png|jpg|PNG|JPG|JPEG))$")
        projTitle = title
        newproject = Project(title=projTitle, language=lang)
        projWasSaved = False
        
        
        if importType=='1':
            for videoFolderName in os.listdir(path):
                if os.path.isdir(os.path.join(path,videoFolderName)):  
                    #Have a hashList of all of the files so that you can search for the corresponding image for each trace
                    allFilesInDir = dict()
                    for fileName in os.listdir(os.path.join(path,videoFolderName,"frames")):
                        allFilesInDir[fileName] = 1
                    subject = re.search(bigdirpattern,videoFolderName).group(1)
                    newvideo = Video(project=newproject,subject=subject,title=videoFolderName+"_"+subject)
                    sawAnyFramesInDir = 0
                    #Find the TextGrid file:
                    textGridPath = ''
                    for fileName in os.listdir(os.path.join(path,videoFolderName)):
                        if fileName.endswith('TextGrid') or fileName.endswith('Textgrid') or fileName.endswith('textgrid'):
                            textGridPath = os.path.join(path,videoFolderName,fileName)
                            break
                    #Go through all of the images and traces and save them in allFilesInDir
                    for fullFileName in os.listdir(os.path.join(path,videoFolderName,"frames")): 
                        if fullFileName.endswith('txt'):
                            correspondingImageName = re.sub('\.[^\.]+(\.traced){0,1}\.txt','',fullFileName)
                            if correspondingImageName in allFilesInDir:
                                dictValue = allFilesInDir[correspondingImageName]
                                tracer =   re.sub('^(.*\.)([^\.]+)(\.traced\.txt)','\\2',fullFileName)
                                if dictValue == 1:
                                    i = ImageRep('',fullFileName,tracer)
                                    allFilesInDir[correspondingImageName] = i
                                else:
                                    dictValue.traces.append(fullFileName)
                                    dictValue.tracers.append(tracer)
                        if pngpattern.match(fullFileName):
                            ######
                            sawAnyFramesInDir = 1
                            dictValue = allFilesInDir[fullFileName]
                            ######
                            if dictValue == 1:
                                i = ImageRep(fullFileName,[],[])
                                allFilesInDir[fullFileName] = i
                            else:
                                dictValue.name = fullFileName
                    if(sawAnyFramesInDir):
                        if not projWasSaved:
                            newproject.save()
                            projWasSaved = True
                        newvideo.project = newproject
                        newvideo.save()
                    else:
                        continue
                    #Now add all of the images and their traces to the database:
                    images = [] #A list of Image objects that will be sent to TextGridReader
                    for imageName, imageRep in allFilesInDir.items():
                        if pngpattern.match(imageName):
                            fullpath = os.path.join(path, videoFolderName, "frames", imageName)
                            cleanTitle = re.sub('.*?(\d+\..*)$','\\1',imageName)
                            newImage = Image(title=cleanTitle, video=newvideo, address=fullpath, sorting_code=projTitle+newvideo.title+cleanTitle, trace_count=len(imageRep.traces))
                            images.append(newImage)
                            imageRep.imageObj = newImage
    
                    #Get a list of the images (filter out the trace files)
                    images = sorted(images,key=lambda image:image.title)
                    
                    readTextGrid(textGridPath,images)
                    Image.objects.bulk_create(images)
                    midway = time.time()
    #                 for image in images:
    #                     image.save()
                    #Now add the traces:
                    traces = []
                    for imageName, imageRep in allFilesInDir.items():
                        if pngpattern.match(imageName):
                            theImage = Image.objects.filter(sorting_code = imageRep.imageObj.sorting_code)[0]
                            for i in range(len(imageRep.traces)):
                                traceFileName = imageRep.traces[i]
                                tracerName = imageRep.tracers[i]
                                traceFilePath = os.path.join(path, videoFolderName, "frames", traceFileName)
                                if len(tracerName)<1:
                                    tracerName = "-"
                                tracerObj = getTracerObj(tracerName)
                                newTrace = Trace(address=traceFilePath, tracer=tracerObj, image=theImage)
                                traces.append(newTrace)
                    Trace.objects.bulk_create(traces)
                    
                    
                    end = time.time()
                    file = open('log.txt', 'a')
                    full = str(end-start)
                    afterMidway = str(end-midway)
                    today = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    file.write('------------------------\n')
                    file.write(today+'\n')
                    file.write("afterMidway: \t"+afterMidway+'\n')
                    file.write("full: \t"+full+'\n')
                    file.close()
        
                        
        ####################################################################################
        else: #if importType=2
            for subjectFolderName in os.listdir(path):
                if not os.path.isdir(os.path.join(path,subjectFolderName)):
                    continue
                splitWavesDirPath = os.path.join(path,subjectFolderName,"split_wavs")
                if not os.path.isdir(splitWavesDirPath):
                    continue
                for sentenceFolderName in os.listdir(splitWavesDirPath):
                    sentencePath = os.path.join(splitWavesDirPath,sentenceFolderName)
                    if not os.path.isdir(sentencePath):
                        continue
                    for potentialTextGrid in os.listdir(sentencePath):
                        if potentialTextGrid.endswith('TextGrid') or potentialTextGrid.endswith('Textgrid') or potentialTextGrid.endswith('textgrid'):
                            textGridPath = os.path.join(sentencePath,potentialTextGrid)
                            break
                    #Found the textGrid file. Now get the images and traces
                    imageAndTraceFolderPath = os.path.join(sentencePath,'frames')
                    if not os.path.isdir(imageAndTraceFolderPath):
                        continue
                    #Have a hashList of all of the files so that you can search for the corresponding image for each trace
                    allFilesInDir = dict()
                    for fileName in os.listdir(imageAndTraceFolderPath):
                        allFilesInDir[fileName] = 1
                    newvideo = Video(subject=subjectFolderName,title=sentenceFolderName+"_"+subjectFolderName)
                    sawAnyFramesInDir = 0
                    #Go through all of the images and traces and save them in allFilesInDir
                    for fullFileName in os.listdir(imageAndTraceFolderPath): 
                        if fullFileName.endswith('txt'):
                            correspondingImageName = re.sub('\.[^\.]+(\.traced){0,1}\.txt','',fullFileName)
                            if correspondingImageName in allFilesInDir:
                                dictValue = allFilesInDir[correspondingImageName]
                                tracer = re.sub('^(.*\.)([^\.]+)(\.traced\.txt)','\\2',fullFileName)
                                if dictValue == 1:
                                    i = ImageRep('',fullFileName,tracer)
                                    allFilesInDir[correspondingImageName] = i
                                else:
                                    dictValue.traces.append(fullFileName)
                                    dictValue.tracers.append(tracer)
                        if pngpattern.match(fullFileName):
                            sawAnyFramesInDir = 1
                            dictValue = allFilesInDir[fullFileName]
                            if dictValue == 1:
                                i = ImageRep(fullFileName,[],[])
                                allFilesInDir[fullFileName] = i
                            else:
                                dictValue.name = fullFileName
                    if(sawAnyFramesInDir):
                        if not projWasSaved:
                            newproject.save()
                            projWasSaved = True
                        newvideo.project = newproject
                        newvideo.save()
                    else:
                        continue
                    #Now add all of the images and their traces to the database:
                    images = [] #A list of Image objects that will be sent to TextGridReader
                    for imageName, imageRep in allFilesInDir.items():
                        if pngpattern.match(imageName):
                            fullpath = os.path.join(imageAndTraceFolderPath, imageName)
                            cleanTitle = re.sub('.*?(\d+\..*)$','\\1',imageName)
                            newImage = Image(title=cleanTitle, video=newvideo, address=fullpath, sorting_code=projTitle+newvideo.title+cleanTitle, trace_count=len(imageRep.traces))
                            images.append(newImage)
                            imageRep.imageObj = newImage
    
                    #Get a list of the images (filter out the trace files)
                    images = sorted(images,key=lambda image:image.title)
                    readTextGrid(textGridPath,images)
                    Image.objects.bulk_create(images)
                    midway = time.time()
    #                 for image in images:
    #                     image.save()
                    #Now add the traces:
                    traces = []
                    for imageName, imageRep in allFilesInDir.items():
                        if pngpattern.match(imageName):
                            theImage = Image.objects.filter(sorting_code = imageRep.imageObj.sorting_code)[0]
                            for i in range(len(imageRep.traces)):
                                traceFileName = imageRep.traces[i]
                                tracerName = imageRep.tracers[i]
                                traceFilePath = os.path.join(imageAndTraceFolderPath, traceFileName)
                                if len(tracerName)<1:
                                    tracerName = "-"
                                tracerObj = getTracerObj(tracerName)
                                newTrace = Trace(address=traceFilePath, tracer=tracerObj, image=theImage)
                                traces.append(newTrace)
                    Trace.objects.bulk_create(traces)
                    
                    
                    end = time.time()
                    file = open('log.txt', 'a')
                    full = str(end-start)
                    afterMidway = str(end-midway)
                    file.write("afterMidway: \t"+afterMidway+'\n')
                    file.write("full: \t"+full+'\n')
                    file.close()
        if not projWasSaved:
            return HttpResponse("Failure: No frames could be found in the expected subdirectories.")
        return HttpResponse("The project was loaded successfully!")
    except Exception as e:
        return HttpResponse("Failure: "+str(e))

def addsuccess(request):
    time.sleep(1)
    return redirect('/uatracker/success.html')



def getTracerObj(tracerName):
    global tracersList
    if tracerName in tracersList:
        return tracersList[tracerName]
    else:
        if Tracer.objects.filter(first_name=tracerName).exists():
            tracer = Tracer.objects.filter(first_name=tracerName)[0]
            tracersList[tracerName] = tracer
            return tracer
        else:
            tracer = Tracer(first_name=tracerName)
            tracer.save()
            tracersList[tracerName] = tracer
            return tracer
            
def removeProjView(request):
    title = ''
    if len(request.GET)>0:
        if len(request.GET['project'])>0:
            title = request.GET['project']
    ##
    Image.objects.filter(video__project__title=title).delete()
    Video.objects.filter(project__title=title).delete()
    Project.objects.filter(title=title).delete()
    return HttpResponse("Successfully removed project.")

class ImageRep:
    def __init__(self,name,trace,tracer):
        self.name = name
        self.traces = trace
        self.tracers = tracer
        self.image = None