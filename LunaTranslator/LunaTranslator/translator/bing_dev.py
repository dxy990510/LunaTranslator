 
from traceback import print_exc
import requests,os
from urllib.parse import quote
import re
import winsharedutils
from urllib.parse import quote
import websockets
import asyncio,json
from utils.subproc import subproc_w
from utils.config import globalconfig
import json  
from translator.basetranslator import basetrans
import time
import time,hashlib

_id=1
async def SendRequest(websocket,method,params):
    global _id
    _id+=1
    await websocket.send(json.dumps({'id':_id,'method':method,'params':params}))
    res=await websocket.recv()
    return json.loads(res)['result']
  

async def waitload( websocket):  
        for i in range(10000):
            state =(await SendRequest(websocket,'Runtime.evaluate',{"expression":"document.readyState"})) 
            if state['result']['value']=='complete':
                break
            time.sleep(0.1)

async def waittransok( websocket):   
        for i in range(10000):
            state =(await SendRequest(websocket,'Runtime.evaluate',{"expression":"document.getElementById('tta_output_ta').value","returnByValue":True}))
            if state['result']['value']!=' ...':
                return state['result']['value']
            time.sleep(0.1)
        return ''
async def tranlate(websocketurl,content,src,tgt ): 
    async with websockets.connect(websocketurl) as websocket: 
        # 
        await SendRequest(websocket,'Runtime.evaluate',{"expression":
            f'''document.getElementById('tta_clear').click();document.getElementById('tta_input_ta').value="{content}";
            document.getElementById('tta_input_ta').click();
            '''})  
        res=await waittransok(websocket)

        #document.getElementById('tta_input_ta')
        return (res)


async def createtarget(websocketurl  ): 
    async with websockets.connect(websocketurl) as websocket: 
        a=await SendRequest(websocket,'Target.createTarget',{'url':f'https://www.bing.com/translator/'})  
        return a['targetId']
class TS(basetrans):
    # def end(self):
    #     try:
    #         self.engine.kill() 
    #     except:
    #         pass 
    def inittranslator(self ) : 
    
        self.path=None 
        self.websocketurl=None
        
        
        port =globalconfig['debugport']
        info=requests.get(f'http://127.0.0.1:{port}/json/list').json()
        print(info)
        websocketurl=info[0]['webSocketDebuggerUrl'] 
        self.websocketurl=websocketurl[:websocketurl.rfind('/')]+'/'+asyncio.run(createtarget(websocketurl ))
         
    def translate(self,content):  
        return(asyncio.run(tranlate(self.websocketurl,content,self.srclang,self.tgtlang)))
        