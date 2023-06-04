 
from traceback import print_exc
import requests,os
from urllib.parse import quote
import re
import winsharedutils
from urllib.parse import quote
import websocket as websockets2
import json
from utils.subproc import subproc_w
from utils.config import globalconfig
import json  
from translator.basetranslator import basetrans
import time
import time,hashlib

_id=1
def SendRequest(websocket,method,params):
    global _id
    _id+=1
    websocket.send(json.dumps({'id':_id,'method':method,'params':params}))
    res=websocket.recv()
    return json.loads(res)['result']
  

def waitload( websocket):  
        for i in range(10000):
            state =(SendRequest(websocket,'Runtime.evaluate',{"expression":"document.readyState"})) 
            if state['result']['value']=='complete':
                break
            time.sleep(0.1)

def waittransok( websocket):   
        for i in range(10000):
            state =(SendRequest(websocket,'Runtime.evaluate',{"expression":"document.getElementById('tta_output_ta').value","returnByValue":True}))
            if state['result']['value']!=' ...':
                return state['result']['value']
            time.sleep(0.1)
        return ''
def tranlate(websocketurl,content,src,tgt ): 
    if 1:
        websocket=websockets2.create_connection(websocketurl)   
        SendRequest(websocket,'Runtime.evaluate',{"expression":
            f'''document.getElementById('tta_clear').click();document.getElementById('tta_input_ta').value=`{content}`;
            document.getElementById('tta_input_ta').click();
            '''})  
        res=waittransok(websocket)

        #document.getElementById('tta_input_ta')
        return (res)
 
def createtarget(port  ): 
    url='https://www.bing.com/translator/'
    infos=requests.get(f'http://127.0.0.1:{port}/json/list').json() 
    use=None
    for info in infos:
         if '.bing.com/translator/' in info['url']:
              use=info['webSocketDebuggerUrl']
              break
    if use is None:
        if 1:
            websocket=websockets2.create_connection(infos[0]['webSocketDebuggerUrl'])  
            a=SendRequest(websocket,'Target.createTarget',{'url':url})  
            use= 'ws://127.0.0.1:81/devtools/page/'+a['targetId']
    return use
class TS(basetrans): 
    def inittranslator(self ) :  
            self.websocketurl=(createtarget(globalconfig['debugport'] )) 
    def translate(self,content):  
        return((tranlate(self.websocketurl,content,self.srclang,self.tgtlang)))
        