from textgrid import TextGrid
from UATracker.models import Image,Word,Segment
import re,time
dbTimeInTG = 0
import pdb

def readTextGrid(tgAddress, images):
    global dbTimeInTG
    phonePattern = re.compile('(^[Pp]hone(s{0,1})$)|(^[Ss]egment(s{0,1})$)')
    wordPattern = re.compile('^[Ww]ord(s{0,1})$')
    start = time.time()
    tg = TextGrid()
    tg.read(tgAddress)
    duration = tg.maxTime - tg.minTime
    imageLength = duration/len(images)
    words = []
    tiers = tg.tiers
    if not wordPattern.match(tg.getNames()[0]):
        tiers = reversed(tg.tiers)
    #This loop handles words and segments at once, because many of the operations are shared    
    for tier in tiers:
        imageCounter = -1
        wordCounter = 0
        if not wordPattern.match(tier.name) and not phonePattern.match(tier.name):
            print ("Unexpected tier name: "+tier.name)
        else:
            if wordPattern.match(tier.name):
                tierType = 'Words'
            else:
                tierType = 'Segments'
        for interval in tier.intervals:
            mark = interval.mark
            simpleSpelling = getSimpleSpelling(mark)
            if len(mark)<1 and tierType=='Words':
                continue
            #Add the new segment/word to the DB
            if len(mark)>0:
                wordOrSeg = addIntervalToDB(mark,simpleSpelling,tierType)    #the third arg tells whether it is a word or a segment
            else:
                continue
            #assign the segment/word to all of the images it covers:
            if imageCounter>0:
                imageCounter -= 1   #So in the beginning of each interval we first check the last image we saw. It may need more than one seg.
            while True:
#                 if imageCounter%100==0:
#                     print("annotating image: "+str(imageCounter))
                imageCounter += 1
                if imageCounter>=len(images):
                    break
                image = images[imageCounter]
                imageMin = imageCounter*imageLength
                imageMax = (imageCounter+1)*imageLength
                imageCenter = (imageMin+imageMax)/2
                #image center inside interval:
                if imageMax<interval.minTime:
                    continue
                if imageCenter>interval.minTime and imageCenter<interval.maxTime:
                    assignMainObject(image,wordOrSeg,tierType)
                #image has startSegment:
                elif imageCenter>interval.maxTime and imageMin<interval.maxTime:
                    assignStartObject(image,wordOrSeg,tierType)
                #image has endSegment:
                elif imageCenter<interval.minTime and imageMax>interval.minTime:
                    assignEndObject(image,wordOrSeg,tierType)
                #image occurs after the interval
                else:
                    imageCounter -= 1
                    break
            #Save it somewhere if it is a word:
            if tierType=='Words':
                word = WordEntry("","",interval.maxTime,wordOrSeg.id)
                words.append(word)
            #Now assign the segment to the word if it is a segment
            if tierType=='Segments':
                #Increment the words until you reach a word that covers the current segment:
                while words[wordCounter].maxTime<=interval.minTime:
                    wordCounter += 1
                word = words[wordCounter]
                id = wordOrSeg.id
                if len(mark.strip())<1:
                    simpleSpelling = "0"
                    id = "0"
                word.addSegment(str(id),simpleSpelling)
                
    #Now that we're done reading the TextGrid file, it's time to add the segment sequence for each word to the DB
    for word in words:
        word.updateSegmentsInDB()
    end = time.time()
    file = open('log.txt', 'a')
    elapsed = str(end-start)
    file.write("textgrid: \t"+elapsed+'\n')
    file.write("dbInTG: \t"+str(dbTimeInTG)+'\n')
    file.close()
 
def assignMainObject(image,object,type): #e.g. (<image234>,[the id of the segment],"Segments")
     if type=="Words":
         word = object
         image.word = word
     elif type=="Segments":
         segment = object
         image.segment = segment
 
def assignStartObject(image,object,type): 
     if type=="Words":
         word = object
         image.start_word = word
     elif type=="Segments":
         segment = object
         image.start_segment = segment
         
def assignEndObject(image,object,type): 
     if type=="Words":
         word = object
         image.end_word = word
     elif type=="Segments":
         segment = object
         image.end_segment = segment
         
         
def addIntervalToDB(detailedSpelling, simpleSpelling,type):
    start = time.time()
    global dbTimeInTG
    if type=="Segments":
        seg = Segment(spelling=simpleSpelling, detailed_spelling=detailedSpelling)
        seg.save()
        end = time.time()
        dbTimeInTG += (end-start)
        return seg
    if type=="Words":
        word = Word(spelling=detailedSpelling)
        word.save()
        end = time.time()
        dbTimeInTG += (end-start)    
        return word
    
    
def getSimpleSpelling(detailedSpelling):
    detailedSpelling = detailedSpelling.replace("neutral", "0")
    detailedSpelling = detailedSpelling.strip()
    if " " in detailedSpelling:
        result = re.compile("\s+").split(detailedSpelling)[1]
        if re.search(r"^.*[ifpncv]$",result) or result.endswith("f") or re.search(r"^.*[0-9]$",result):
            if len(result)>1:
                result = result[0:-1]                
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
        start = time.time()
        global dbTimeInTG
        word = Word.objects.get(pk=self.id)
        word.segment_sequence = self.segmentSequence
        word.segment_id_sequence = self.segmentIDSequence
        word.save()
        end = time.time()
        dbTimeInTG += (end-start)
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
    
    