 
import time,os
from traceback import print_exc 
from myutils.config import globalconfig,_TR
import importlib  
from difflib import SequenceMatcher 
from myutils.exceptions import ArgsEmptyExc

import time  ,gobject
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtGui import QImage
from textsource.textsourcebase import basetext  
def qimge2np(img:QImage):
    #img=img.convertToFormat(QImage.Format_Grayscale8)
    shape=img.height(),img.width(),1
    img=img.scaled(128,8*3) 
    img.shape=shape
    return img
def compareImage(img1:QImage,img2):
    cnt=0
    for i in range(128):
        for j in range(24):
            cnt+=(img1.pixel(i,j)==img2.pixel(i,j)) 
    return cnt/(128*24)
     
def getEqualRate(  str1, str2):
    
        score = SequenceMatcher(None, str1, str2).quick_ratio()
        score = score 

        return score
import math,win32utils
class ocrtext(basetext):
    
    def imageCut(self,x1,y1,x2,y2):
     
        if self.hwnd:
            try:  
                hwnduse=self.hwnd
                rect=win32utils.GetWindowRect(hwnduse)  
                if rect==(0,0,0,0):
                    raise Exception
                rect2=win32utils.GetClientRect(hwnduse)
                windowOffset = math.floor(((rect[2]-rect[0])-rect2[2])/2)
                h= ((rect[3]-rect[1])-rect2[3]) - windowOffset
                 
                pix = self.screen.grabWindow(hwnduse, x1-rect[0], y1-rect[1]-h, x2-x1, y2-y1) 
                if pix.toImage().allGray():
                    raise Exception()
            except:
                pix = self.screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1) 
        else:
            pix = self.screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2-x1, y2-y1) 
        return pix.toImage()
    def __init__(self,textgetmethod)  :
        self.screen = QApplication.primaryScreen() 
        self.savelastimg=None
        self.savelastrecimg=None
        self.savelasttext=None 
        self.lastocrtime=0
        self.nowuseocr=None
        self.timestamp=time.time() 
        super(ocrtext,self ).__init__(textgetmethod,'0','0_ocr') 
    def gettextthread(self ):
                 
            if gobject.baseobject.rect is None:
                time.sleep(1)
                return None
            
            time.sleep(0.1)
            #img=ImageGrab.grab((gobject.baseobject.rect[0][0],gobject.baseobject.rect[0][1],gobject.baseobject.rect[1][0],gobject.baseobject.rect[1][1]))
            #imgr = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            if gobject.baseobject.rect is None:
                return None
            imgr=self.imageCut(gobject.baseobject.rect[0][0],gobject.baseobject.rect[0][1],gobject.baseobject.rect[1][0],gobject.baseobject.rect[1][1])
            
            ok=True
            
            if globalconfig['ocr_auto_method'] in [0,2]: 
                imgr1=qimge2np(imgr)
                h,w,c=imgr1.shape 
                if self.savelastimg is not None and  (imgr1.shape==self.savelastimg.shape) : 
                    
                    image_score=compareImage(imgr1 ,self.savelastimg )
                    
                else:
                    image_score=0 
                self.savelastimg=imgr1
                
                if image_score>globalconfig['ocr_stable_sim'] : 
                    if self.savelastrecimg is not None and  (imgr1.shape==self.savelastrecimg.shape   ) :
                        image_score2=compareImage(imgr1 ,self.savelastrecimg ) 
                    else:
                        image_score2=0 
                    if image_score2>globalconfig['ocr_diff_sim']:
                        ok=False
                    else: 
                        self.savelastrecimg=imgr1
                else:
                    ok=False
            if globalconfig['ocr_auto_method'] in [1,2]:
                if time.time()-self.lastocrtime>globalconfig['ocr_interval']:
                    ok=True
                else:
                    ok=False
            if ok==False:
                return None
            text=self.ocrtest(imgr)  
            self.lastocrtime=time.time()
            
            if self.savelasttext is not None:
                sim=getEqualRate(self.savelasttext,text)
                #print('text',sim)
                if sim>0.9: 
                    return  None
            self.savelasttext=text
            
            return (text)
            
    def runonce(self): 
        
        if gobject.baseobject.rect is None:
            return
        if gobject.baseobject.rect[0][0]>gobject.baseobject.rect[1][0] or gobject.baseobject.rect[0][1]>gobject.baseobject.rect[1][1]:
            return  
        img=self.imageCut(gobject.baseobject.rect[0][0],gobject.baseobject.rect[0][1],gobject.baseobject.rect[1][0],gobject.baseobject.rect[1][1])
        
        

        text=self.ocrtest(img)
        imgr1=qimge2np(img)
        self.savelastimg=imgr1
        self.savelastrecimg=imgr1
        self.lastocrtime=time.time()
        self.savelasttext=text
        self.textgetmethod(text,False)
    def ocrtest(self,img):
        use=None
        for k in globalconfig['ocr']:
            if globalconfig['ocr'][k]['use']==True and os.path.exists(('./LunaTranslator/ocrengines/'+k+'.py')):
                use=k
                break
        if use is None:
            return ''
        fname='./cache/ocr/{}.png'.format(self.timestamp)
        img.save(fname)
        
        try:
            if self.nowuseocr!=use:
                try: self.ocrengine.end()
                except:pass
                aclass=importlib.import_module('ocrengines.'+use).OCR 
                self.ocrengine=aclass(use)   
                self.nowuseocr=use
            return self.ocrengine.ocr(fname)
        except Exception as e:
            if isinstance(e,ArgsEmptyExc):
                msg=str(e)
            else:
                print_exc()
                msg=str(type(e))[8:-2]+' '+str(e).replace('\n','').replace('\r','')
            msg='<msg>'+_TR(globalconfig['ocr'][use]['name'])+' '+msg
            return msg

    def end(self):
        super().end()
        try: self.ocrengine.end()
        except:pass