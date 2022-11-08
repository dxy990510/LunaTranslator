import threading  
import time,sqlite3,json,os
from traceback import print_exc
from utils.config import globalconfig
class basetext:
    def __init__(self,textgetmethod)  : 
        self.suspending=False
        self.textgetmethod=textgetmethod 
        self.lock=threading.Lock()
        self.t=threading.Thread(target=self.gettextthread_)
        self.t.setDaemon(True)
        self.t.start()
        try:
            def loadjson(self):
                if os.path.exists(self.jsonfname):
                    with open(self.jsonfname,'r',encoding='utf8') as ff:
                        self.json=json.load(ff)
                else:
                    self.json={}
            threading.Thread(target=loadjson,args=(self,)).start()
            
            self.sqlwrite=sqlite3.connect(self.sqlfname,check_same_thread = False)
            self.sqlwrite2=sqlite3.connect(self.sqlfname_all,check_same_thread = False)
            try:
                self.sqlwrite.execute('CREATE TABLE artificialtrans(id INTEGER PRIMARY KEY AUTOINCREMENT,source TEXT,machineTrans TEXT,userTrans TEXT);')
            except:
                pass
            try:
                self.sqlwrite2.execute('CREATE TABLE artificialtrans(id INTEGER PRIMARY KEY AUTOINCREMENT,source TEXT,machineTrans TEXT);')
            except:
                pass
        except:
            print_exc
    def gettextthread_(self):
        while True:
            if self.ending:
                
                break
            if globalconfig['sourcestatus'][self.typename]==False:
                break
            if globalconfig['autorun']==False  :
                time.sleep(1)
                continue
            #print(globalconfig['autorun'])
            t=self.gettextthread()
            if t and globalconfig['autorun']:
                self.textgetmethod(t)
                if self.typename=='ocr':
                    time.sleep(globalconfig['ocrmininterval'])
    def gettextthread(self):
        pass
    def runonce(self):
        pass
    def end(self):
        self.ending=True
 