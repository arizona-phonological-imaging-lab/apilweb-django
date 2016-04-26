from textgrid import TextGrid
from UATracker.models import Image,Word,Segment
import re

def readTextGrid(tgAddress, images):
    tg = TextGrid()
    tg.read(tgAddress)
    duration = tg.maxTime - tg.minTime
    imageLength = duration/len(images)
    words = []
        
    #This loop handles words and segments at once, because many of the operations are shared    
    for tier in tg:
        imageCounter = -1
        wordCounter = 0
        if tier.name!="Words" and tier.name!="Segments":
            print ("Unexpected tier name: "+tier.name)
        for interval in tier.intervals:
            mark = interval.mark
            simpleSpelling = getSimpleSpelling(mark)
            if len(mark)<1 and tier.name=="Words":
                continue
            #Add the new segment/word to the DB
            if len(mark)>0:
                id = addIntervalToDB(mark,simpleSpelling,tier.name)    #the second arg tells whether it is a word or a segment
            #assign the segment/word to the image:
            while(1):
                if imageCounter%100==1:
                    print(imageCounter)
                imageCounter += 1
                if imageCounter>len(images):
                    break
                image = images[imageCounter]
                imageMin = imageCounter*imageLength
                imageMax = (imageCounter+1)*imageLength
                imageCenter = (imageMin+imageMax)/2
                #image center inside interval:
                if imageCenter>interval.minTime and imageCenter<interval.maxTime:
                    assignMainObject(image,id,tier.name)
                #image has startSegment:
                elif imageCenter>interval.maxTime and imageMin<interval.maxTime:
                    assignStartObject(image,id,tier.name)
                #image has endSegment:
                elif imageCenter<interval.minTime and imageMax>interval.minTime:
                    assignEndObject(image,id,tier.name)
                #image is 
                else:
                    imageCounter -= 1
                    break
            #Save it somewhere if it is a word:
            if tier.name=='Words':
                word = WordEntry("","",interval.maxTime,id)
                words.append(word)
            #Now assign the segment to the word if it is a segment
            if tier.name=='Segments':
                #Increment the words until you reach a word that covers the current segment:
                while words[wordCounter].maxTime<interval.minTime:
                    wordCounter += 1
                word = words[wordCounter]
                if len(mark.strip())<1:
                    simpleSpelling = "0"
                    id = "0"
                word.addSegment(str(id),simpleSpelling)
                
    #Now that we're done reading the TextGrid file, it's time to add the segment sequence for each word to the DB
    for word in words:
        word.updateSegmentsInDB()
                
 
def assignMainObject(image,objectID,type): #e.g. (<image234>,[the id of the segment],"Segments")
     image = Image.objects.get(pk=image.id)
     if type=="Words":
         word = Word.objects.get(pk=objectID)
         image.word = Word
         image.save()
     elif type=="Segments":
         segment = Segment.objects.get(pk=objectID)
         image.segment = Segment
         image.save()
 
def assignStartObject(image,objectID,type): 
     image = Image.objects.get(pk=image.id)
     if type=="Words":
         word = Word.objects.get(pk=objectID)
         image.start_word = Word
         image.save()
     elif type=="Segments":
         segment = Segment.objects.get(pk=objectID)
         image.start_segment = Segment
         image.save()
         
def assignEndObject(image,objectID,type): 
     image = Image.objects.get(pk=image.id)
     if type=="Words":
         word = Word.objects.get(pk=objectID)
         image.end_word = Word
         image.save()
     elif type=="Segments":
         segment = Segment.objects.get(pk=objectID)
         image.end_segment = Segment
         image.save()
         
         
         
def addIntervalToDB(detailedSpelling, simpleSpelling,type):
    if type=="Segments":
        seg = Segment(spelling=simpleSpelling, detailed_spelling=detailedSpelling)
        seg.save()
    if type=="Words":
        word = Word(spelling=detailedSpelling)
        word.save()    
        
def getSimpleSpelling(detailedSpelling):
    detailedSpelling = detailedSpelling.replace("neutral", "neut")
    detailedSpelling = detailedSpelling.strip()
    if " " in detailedSpelling:
        result = re.compile("\s+").split(detailedSpelling)[1]
        if re.search(r"^.*[ifpncv]$",result) or result.endswith("f") or re.search(r"^.*[0-9]$",result):
            if len(result)>1:
                result = result[0:]                
        if result.startswith("V"):
            result = "V"
        return result
    else:
        return detailedSpelling
               
class WordEntry:
    def __init__(self,segs,segIDs,maxTime,id):
        self.segmentSequence = segs
        self.segmentIDSequence = segIDs
        self.maxTime = maxTime
        self.id = id
    def updateSegmentsInDB(self):
        word = Word.objects.get(pk=self.id)
        word.segment_sequence = self.segmentSequence
        word.segment_id_sequence = self.segmentIDSequence
        word.save()
    def addSegment(self,segID,segSpelling):
        if len(self.segmentSequence)==0:
            self.segmentSequence = segSpelling
            self.segmentIDSequence = segID
        else:
            self.segmentSequence += " "+segSpelling
            self.segmentIDSequence += " "+segID
    
    
# images = Image.objects.all()[:10000]
# readTextGrid('/Users/Updates/git/apilweb-django/APILWeb/UATracker/example.TextGrid',images)
# randomImages = Image.objects.filter(word__spelling='cuip')
# print(len(randomImages))
# self.assertGreater(len(randomImages), 0)
#     
    
    