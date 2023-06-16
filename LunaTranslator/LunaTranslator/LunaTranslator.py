
import time
import re
import os,threading ,ctypes
from traceback import  print_exc   
import win32utils,socket
from myutils.config import globalconfig ,savehook_new_list,savehook_new_data,noundictconfig,transerrorfixdictconfig,setlanguage ,_TR,static_data
import threading 
from myutils.utils import minmaxmoveobservefunc ,kanjitrans,checkifnewgame
from myutils.wrapper import threader 
from gui.showword import searchwordW
from gui.rangeselect    import rangeadjust
from myutils.hwnd import pid_running,getpidexe ,testprivilege,ListProcess
from textsource.copyboard import copyboard   
from textsource.texthook import texthook   
from textsource.embedded import embedded
from textsource.ocrtext import ocrtext
import  gui.selecthook     
import gui.translatorUI
from gui.languageset import languageset
import zhconv,functools
import gui.transhist 
import gui.edittext
import importlib
from functools import partial  
from gui.settin import Settin 
from gui.attachprocessdialog import AttachProcessDialog
import win32con 
import re 
import winsharedutils
from myutils.post import POSTSOLVE
from myutils.vnrshareddict import vnrshareddict 

from textsource.hook.host import RPC
 
class MAINUI() : 
    def __init__(self,app) -> None:
        super().__init__()
        self.lasttranslatorindex=0
        self.app=app   
        self.translators={}
        self.cishus={}
        self.reader=None
        self.textsource_p=None 
        self.rect=None 
        self.currentmd5='0'
        self.currenttext=''
        self.currentread=''
        self.refresh_on_get_trans_signature=0
        self.currentsignature=None
        self.isrunning=True
        self.RPC=RPC() 
    @property
    def textsource(self):return self.textsource_p
    @textsource.setter
    def textsource(self,_):
        if _ is None and self.textsource_p:
            try:
                self.textsource_p.end()  
            except:
                print_exc()
        self.textsource_p=_
        
        self.currentmd5='0' if _ is None else _.md5

    @threader  
    def loadvnrshareddict(self,_=None):
        vnrshareddict(self)  
    def solvebeforetrans(self,content):
    
        zhanweifu=0
        mp1={} 
        mp2={}
        mp3={}
        if noundictconfig['use'] :
            for key in noundictconfig['dict']: 
                usedict=False
                if type(noundictconfig['dict'][key])==str:
                    usedict=True
                else:

                    if noundictconfig['dict'][key][0]=='0' :
                        usedict=True
                
                    if noundictconfig['dict'][key][0]==self.currentmd5:  #self.textsource.md5:
                        usedict=True
                     
                if usedict and  key in content:
                    xx='ZX{}Z'.format(chr(ord("B")+zhanweifu))
                    content=content.replace(key,xx)
                    mp1[xx]=key
                    zhanweifu+=1
        if globalconfig['gongxiangcishu']['use']:
            for key,value in self.sorted_vnrshareddict_pre:
                
                if key in content:
                    content=content.replace(key,value['text']) 
            for key,value in self.sorted_vnrshareddict:
                
                if key in content:
                    # print(key)
                    # if self.vnrshareddict[key]['src']==self.vnrshareddict[key]['tgt']:
                    #     content=content.replace(key,self.vnrshareddict[key]['text'])
                    # else:
                    xx='ZX{}Z'.format(chr(ord("B")+zhanweifu))
                    content=content.replace(key,xx)
                    mp2[xx]=key
                    zhanweifu+=1
        
        return content,(mp1,mp2,mp3)
     
        
    def solveaftertrans(self,res,mp): 
        mp1,mp2,mp3=mp
        #print(res,mp)#hello
        if noundictconfig['use'] :
            for key in mp1: 
                reg=re.compile(re.escape(key), re.IGNORECASE)
                if type(noundictconfig['dict'][mp1[key]])==str:
                    v=noundictconfig['dict'][mp1[key]]
                elif type(noundictconfig['dict'][mp1[key]])==list:
                    v=noundictconfig['dict'][mp1[key]][1]
                res=reg.sub(v,res)
        if globalconfig['gongxiangcishu']['use']:
            for key in mp2: 
                reg=re.compile(re.escape(key), re.IGNORECASE)
                res=reg.sub(self.vnrshareddict[mp2[key]]['text'],res)
            for key,value in self.sorted_vnrshareddict_post: 
                if key in res:
                    res=res.replace(key,value['text']) 
        if transerrorfixdictconfig['use']:
            for key in transerrorfixdictconfig['dict']:
                res=res.replace(key,transerrorfixdictconfig['dict'][key])
        return res

    def _POSTSOLVE(self,s):
        ss=POSTSOLVE(s)
        self.settin_ui.showandsolvesig.emit(s)
        return ss
    def textgetmethod(self,_paste_str,shortlongskip=True,embedcallback=None):
        self.currentsignature=time.time()
        if type(_paste_str)==str:
            if _paste_str[:len('<notrans>')]=='<notrans>':
                self.translation_ui.displayraw1.emit([],_paste_str[len('<notrans>'):],globalconfig['rawtextcolor'])
                self.currenttext=_paste_str
                self.currentread=_paste_str
                return   
            elif _paste_str[:len('<msg>')]=='<msg>':
                self.translation_ui.displaystatus.emit(_paste_str[len('<msg>'):],'red',False)
                return   
            elif _paste_str[:len('<msg_1>')]=='<msg_1>':
                self.translation_ui.displaystatus.emit(_paste_str[len('<msg_1>'):],'red',True)
                return 
        if _paste_str=='' or len(_paste_str)>100000:
            if embedcallback:
                embedcallback('zhs', _paste_str) 
            return 
 
        try:
            _paste_str=self._POSTSOLVE(_paste_str) 
        except Exception as e:
            msg=str(type(e))[8:-2]+' '+str(e).replace('\n','').replace('\r','')
            self.translation_ui.displaystatus.emit(msg,'red',False)
            return

        
        
        while len(_paste_str) and _paste_str[-1] in '\r\n \t':  #在后处理之后在去除换行，这样换行符可以当作行结束符给后处理用
            _paste_str=_paste_str[:-1]  
            
        if _paste_str=='' or (shortlongskip and (_paste_str==self.currenttext or len(_paste_str)>1000)):
            if embedcallback:
                embedcallback('zhs', _paste_str) 
            return 
        
        self.currenttext=_paste_str
        self.textsource.sqlqueueput((_paste_str,)) 
        
        if globalconfig['outputtopasteboard'] and globalconfig['sourcestatus']['copy']['use']==False:  
            winsharedutils.clipboard_set(_paste_str)
        

        try:
            hira=self.hira_.fy(_paste_str)
        except:
            hira=[]
            
        if globalconfig['refresh_on_get_trans']==False:
            self.translation_ui.displayraw1.emit(hira,_paste_str,globalconfig['rawtextcolor'] )
            _showrawfunction=None
            _showrawfunction_sig=0
        else:
            _showrawfunction=functools.partial(self.translation_ui.displayraw1.emit,hira,_paste_str,globalconfig['rawtextcolor'] )
            _showrawfunction_sig=time.time()

        if globalconfig['read_raw']:
            self.currentread=_paste_str
            self.readcurrent()
            
        paste_str_solved,optimization_params= self.solvebeforetrans(_paste_str) 
        
        skip=shortlongskip and  (len(paste_str_solved)<globalconfig['minlength'] or len(paste_str_solved)>globalconfig['maxlength'] )

        self.premtalready=['premt']
        if 'premt' in self.translators:
            try:
                ret=self.translators['premt'].translate(paste_str_solved)
                self.GetTranslationCallback('premt',self.currentsignature,optimization_params,_showrawfunction,_showrawfunction_sig,_paste_str,ret,embedcallback)
            except:
                pass
        if globalconfig['loadbalance']:
            usenum=min(globalconfig['loadbalance_oncenum'],len(self.translators))
        else:
            usenum= len(self.translators)
        thistimeusednum=0
        self.lasttranslatorindex=self.lasttranslatorindex %len(self.translators)
        _len=len(self.translators)
        keys=list(self.translators.keys())+list(self.translators.keys())
        keys=keys[self.lasttranslatorindex:self.lasttranslatorindex+_len]
        #print(keys,usenum,self.lasttranslatorindex)
        for engine in keys:  
            if engine not in self.premtalready:
                self.translators[engine].gettask((partial(self.GetTranslationCallback,engine,self.currentsignature, optimization_params,_showrawfunction,_showrawfunction_sig,_paste_str),_paste_str,paste_str_solved,skip,embedcallback,shortlongskip)) 
            thistimeusednum+=1
            self.lasttranslatorindex+=1
            if(thistimeusednum>=usenum):
                break
                
    
        
    def GetTranslationCallback(self,classname,currentsignature,optimization_params,_showrawfunction,_showrawfunction_sig,contentraw,res,embedcallback):
        if currentsignature!=self.currentsignature:
            return 
        
        
        if type(res)==str:
            if res[:len('<msg>')]=='<msg>':
                self.translation_ui.displayres.emit(globalconfig['fanyi'][classname]['name'],'red',res[len('<msg>'):])
                return   
        if classname not in static_data["fanyi_pre"]: 
            res=self.solveaftertrans(res,optimization_params)
        
        if globalconfig['read_trans']  and (list(globalconfig['fanyi'].keys())[globalconfig['read_translator']]==classname):
            self.currentread=res
            self.readcurrent()

        needshowraw=_showrawfunction and self.refresh_on_get_trans_signature!=_showrawfunction_sig
        if needshowraw:
            self.refresh_on_get_trans_signature=_showrawfunction_sig
            _showrawfunction()
        if classname=='premt':
            for k in res:
                if k in globalconfig['fanyi']:
                    _colork=k
                else:
                    _colork='premt'
                self.translation_ui.displayres.emit(globalconfig['fanyi'][_colork]['name'],globalconfig['fanyi'][_colork]['color'],res[k])
                self.premtalready.append(k)
        else:
            self.translation_ui.displayres.emit(globalconfig['fanyi'][classname]['name'],globalconfig['fanyi'][classname]['color'],res)
            
            if embedcallback: 

                if globalconfig['embedded']['as_fast_as_posible'] or classname==list(globalconfig['fanyi'])[globalconfig['embedded']['translator']]:    
                    
                    embedcallback('zhs', kanjitrans(zhconv.convert(res,'zh-tw')) if globalconfig['embedded']['trans_kanji'] else res) 
        
        
        if classname not in static_data["fanyi_pre"]:
              
            self.textsource.sqlqueueput((contentraw,classname,res))

    def readcurrent(self,force=False):
        try: 
            if force or globalconfig['autoread']:
                self.reader.read(self.currentread) 
        except:
            print_exc()
    @threader
    def startreader(self,use=None,checked=True):
        try:
            self.reader.end()
        except:
            pass
        self.reader=None
        self.settin_ui.voicelistsignal.emit([],-1)
        if checked:  
            if use is None:
                
                for key in globalconfig['reader']:
                    if globalconfig['reader'][key]['use'] and os.path.exists(('./LunaTranslator/tts/'+key+'.py')):
                        use=key  
                        break
            if use:
                aclass=importlib.import_module('tts.'+use).TTS  
                
                
                self.reader_usevoice=use
                self.reader=aclass( use,self.settin_ui.voicelistsignal,self.settin_ui.mp3playsignal) 
            
            
    def selectprocess(self,selectedp): 
        self.textsource=None
        pids,pexe,hwnd=(  selectedp)   
        checkifnewgame(pexe) 
        if globalconfig['sourcestatus']['texthook']['use']:
            self.textsource=texthook(self.RPC,self.textgetmethod,self.hookselectdialog,pids,hwnd,pexe)  
        elif globalconfig['sourcestatus']['embedded']['use']:
            self.textsource=embedded(self.textgetmethod,self.hookselectdialog,pids,hwnd,pexe, self)  
         
    #@threader
    def starttextsource(self,use=None,checked=True):   
        self.rect=None 
        self.translation_ui.showhidestate=False 
        self.translation_ui.refreshtooliconsignal.emit()
        self.range_ui.hide() 
        self.settin_ui.selectbutton.setEnabled(globalconfig['sourcestatus']['texthook']['use']) 
        self.settin_ui.selecthookbutton.setEnabled(globalconfig['sourcestatus']['texthook']['use'] )
        self.settin_ui.selectbuttonembed.setEnabled(globalconfig['sourcestatus']['embedded']['use']) 
        self.textsource=None
        if checked: 
            classes={'ocr':ocrtext,'copy':copyboard,'texthook':None,'embedded':None} 
            if use is None:
                use=list(filter(lambda _ :globalconfig['sourcestatus'][_]['use'],classes.keys()) )
                use=None if len(use)==0 else use[0]
            if use is None:
                return
            elif use=='texthook' or use=='embedded':
                pass
            else:
                self.textsource=classes[use](self.textgetmethod)
        
    @threader
    def starthira(self,use=None,checked=True): 
        if checked:
            hirasettingbase=globalconfig['hirasetting']
            _hira=None
            for name in hirasettingbase:
                if hirasettingbase[name]['use']:
                    if os.path.exists('./LunaTranslator/hiraparse/'+name+'.py')==False:
                        continue
                    _hira=importlib.import_module('hiraparse.'+name).hira
                    break
             
            try:
                if _hira:
                    self.hira_=_hira()  
                else:
                    self.hira_=None
            except:
                print_exc()
                self.hira_=None
        else:
            self.hira_=None
    def fanyiinitmethod(self,classname):
        if classname=='selfbuild':
            if os.path.exists('./userconfig/selfbuild.py')==False:
                return None
            aclass=importlib.import_module('selfbuild').TS  
        else:
            if os.path.exists('./LunaTranslator/translator/'+classname+'.py')==False:
                return None
            aclass=importlib.import_module('translator.'+classname).TS  
        return aclass(classname)   
     
    def prepare(self,now=None,_=None):    
        self.commonloader('fanyi',self.translators,self.fanyiinitmethod,now)
         
    def commonloader(self,fanyiorcishu,dictobject,initmethod,_type=None):
        if _type:
            self.commonloader_warp(fanyiorcishu,dictobject,initmethod,_type)
        else:
            for key in globalconfig[fanyiorcishu]: 
                self.commonloader_warp(fanyiorcishu,dictobject,initmethod,key)
    @threader
    def commonloader_warp(self,fanyiorcishu,dictobject,initmethod,_type):
        try:
            if _type in dictobject: 
                try: dictobject[_type].end() 
                except:print_exc()
                try:  del dictobject[_type]
                except:print_exc()
            if globalconfig[fanyiorcishu][_type]['use']==False:
                return
            item=initmethod(_type)
            if item:
                dictobject[_type]=item
        except:
            print_exc()
 
    def startxiaoxueguan(self,type_=None,_=None):  
        self.commonloader('cishu',self.cishus,self.cishuinitmethod,type_) 
    def cishuinitmethod(self,type_):
                try:
                    aclass=importlib.import_module('cishu.'+type_)
                    aclass=getattr(aclass,type_)
                except:
                    return 
                class cishuwrapper:
                    def __init__(self,_type) -> None:
                        self._=_type() 
                    @threader
                    def search(self,sentence):
                        try:
                            res=self._.search(sentence) 
                            if res is None or res=='':  
                                return 
                            self.callback(res)
                        except:
                            pass 
                _=cishuwrapper(aclass)
                return _
    
      

    def onwindowloadautohook(self): 
        if not(globalconfig['autostarthook'] and (globalconfig['sourcestatus']['texthook']['use'] or globalconfig['sourcestatus']['embedded']['use'])):
            return 
            
        elif self.AttachProcessDialog.isVisible():
                return 
        else:
            try:
                
                
                if   self.textsource is None:   
                        hwnd=win32utils.GetForegroundWindow()
                        pid=win32utils.GetWindowThreadProcessId(hwnd)
                        name_=getpidexe(pid)
                          
                
                        if name_  and name_ in savehook_new_list:   
                            lps=ListProcess(False)
                            for pids,_exe  in lps:
                                if _exe==name_: 
                                    
                                    if any(map(testprivilege,pids)):
                                        self.textsource=None
                                        if globalconfig['sourcestatus']['texthook']['use']:
                                            needinserthookcode=savehook_new_data[name_]['needinserthookcode']
                                            self.textsource=texthook(self.RPC,self.textgetmethod,self.hookselectdialog,pids,hwnd,name_ ,autostarthookcode=savehook_new_data[name_]['hook'],needinserthookcode=needinserthookcode)
                                        elif globalconfig['sourcestatus']['embedded']['use']:
                                            self.textsource=embedded(self.textgetmethod,self.hookselectdialog,pids,hwnd,name_  ,self)
                                        break
                
                else: 
                    pids=self.textsource.pids
                    if sum([int(pid_running(pid)) for pid in pids])==0:
                        self.textsource=None  
            except:
                       
                       print_exc()
    
    def autohookmonitorthread(self):
        for game in savehook_new_data:
            checkifnewgame(game)
        while self.isrunning:
            self.onwindowloadautohook()
            time.sleep(0.5)#太短了的话，中间存在一瞬间，后台进程比前台窗口内存占用要大。。。
    def autocheckhwndexists(self):
        def setandrefresh(bool):
            if self.translation_ui.isbindedwindow!=bool:
                self.translation_ui.isbindedwindow=bool
                self.translation_ui.refreshtooliconsignal.emit()
        while self.isrunning:
            if self.textsource:
                
                hwnd=self.textsource.hwnd
                
                if hwnd==0:
                    if globalconfig['sourcestatus']['texthook']['use'] or globalconfig['sourcestatus']['embedded']['use']:
                        fhwnd=win32utils.GetForegroundWindow() 
                        pids=self.textsource.pids
                        if hwnd==0 and win32utils.GetWindowThreadProcessId( fhwnd ) in pids:
                            if 'once' not in dir(self.textsource):
                                self.textsource.once=True
                                self.textsource.hwnd=fhwnd 
                                setandrefresh(True)
                    else:
                        setandrefresh(False)
                else:
                    if win32utils.GetWindowThreadProcessId( hwnd )==0:
                        self.textsource.hwnd=0
                        setandrefresh(False)
                    elif 'once' not in dir(self.textsource):
                        self.textsource.once=True
                        setandrefresh(True)
                if len(self.textsource.pids):
                    _mute=winsharedutils.GetProcessMute(self.textsource.pids[0])  
                    if self.translation_ui.processismuteed!=_mute:
                        self.translation_ui.processismuteed=_mute
                        self.translation_ui.refreshtooliconsignal.emit()
            else: 
                setandrefresh(False)
            
            time.sleep(0.5) 
    def aa(self):   
        self.translation_ui =gui.translatorUI.QUnFrameWindow(self)   
        
        self.translation_ui.show()
        self.mainuiloadafter()
    def checkgameplayingthread(self):
        while True:
            statistictime=time.time()
            time.sleep(1)
            
            try:
                _hwnd=win32utils.GetForegroundWindow()
                _pid=win32utils.GetWindowThreadProcessId(_hwnd)
                if self.textsource and 'pids' in dir(self.textsource) and len(self.textsource.pids):

                    if _pid in self.textsource.pids:
                        savehook_new_data[self.textsource.pname]['statistic_playtime']+=(time.time()-statistictime)
                else:
                    name_=getpidexe(_pid)
                    if name_  and name_ in savehook_new_list: 
                        savehook_new_data[name_]['statistic_playtime']+=(time.time()-statistictime)
            except:
                print_exc()
    def mainuiloadafter(self):    
        self.localocrstarted=False 
        self.loadvnrshareddict()
        self.prepare()  
        self.startxiaoxueguan()
        self.starthira()      
        
        self.settin_ui = Settin(self.translation_ui)  
        
        self.startreader()  
        self.transhis=gui.transhist.transhist(self.translation_ui)  
        self.edittextui=gui.edittext.edittext(self.translation_ui)  
        self.searchwordW=searchwordW(self.translation_ui)
        self.range_ui = rangeadjust(self.translation_ui)   
        self.hookselectdialog=gui.selecthook.hookselect(self.settin_ui) 
        self.AttachProcessDialog=AttachProcessDialog(self.settin_ui,self.selectprocess,self.hookselectdialog)
        self.starttextsource()  
        threading.Thread(target=self.autocheckhwndexists).start()   
        threading.Thread(target=self.autohookmonitorthread).start()    
        threading.Thread(target=minmaxmoveobservefunc,args=(self.translation_ui,)).start()
        threading.Thread(target=self.checkgameplayingthread ).start()
    def checklang(self):
        if  globalconfig['language_setted_2.4.5']==False:
            
            x=languageset(static_data['language_list_show'])
            x.exec()
            globalconfig['language_setted_2.4.5']=True
            globalconfig['languageuse']=x.current
            globalconfig['tgtlang3']=x.current
            setlanguage()
      