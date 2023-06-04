from cmath import sin
import threading
from traceback import print_exc
import requests
from utils.config import globalconfig    
from utils.utils import getproxy

import websockets
import asyncio
from datetime import datetime
import time
import re
import uuid 
import os
import time
import threading
from traceback import print_exc
import requests
from utils.config import globalconfig    
import base64
import os
import time
from tts.basettsclass import TTSbase 
class TTS(TTSbase): 
    
    def getvoicelist(self):
        self.alllist=requests.get('https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4',proxies=getproxy()).json()
        return [_['ShortName'] for _ in self.alllist]
         
    def speak(self,content,rate,voice,voiceidx):
        return asyncio.run(transferMsTTSData( rate,content, voice))
         

# Fix the time to match Americanisms
def hr_cr(hr):
    corrected = (hr - 1) % 24
    return str(corrected)

# Add zeros in the right places i.e 22:1:5 -> 22:01:05
def fr(input_string):
    corr = ''
    i = 2 - len(input_string)
    while (i > 0):
        corr += '0'
        i -= 1
    return corr + input_string

# Generate X-Timestamp all correctly formatted
def getXTime():
    now = datetime.now()
    return fr(str(now.year)) + '-' + fr(str(now.month)) + '-' + fr(str(now.day)) + 'T' + fr(hr_cr(int(now.hour))) + ':' + fr(str(now.minute)) + ':' + fr(str(now.second)) + '.' + str(now.microsecond)[:3] + 'Z'

def date_to_string() -> str:
    """
    Return Javascript-style date string.

    Returns:
        str: Javascript-style date string.
    """
    # %Z is not what we want, but it's the only way to get the timezone
    # without having to use a library. We'll just use UTC and hope for the best.
    # For example, right now %Z would return EEST when we need it to return
    # Eastern European Summer Time.
    return time.strftime(
        "%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)", time.gmtime()
    )

def ssml_headers_plus_data(request_id: str, timestamp: str, ssml: str) -> str:
    """
    Returns the headers and data to be used in the request.

    Returns:
        str: The headers and data to be used in the request.
    """

    return (
        f"X-RequestId:{request_id}\r\n"
        "Content-Type:application/ssml+xml\r\n"
        f"X-Timestamp:{timestamp}Z\r\n"  # This is not a mistake, Microsoft Edge bug.
        "Path:ssml\r\n\r\n"
        f"{ssml}"
    )

def mkssml(text , voice: str, rate: str) -> str:
    """
    Creates a SSML string from the given parameters.

    Returns:
        str: The SSML string.
    """
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    ssml = (
        "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"
        f"<voice name='{voice}'><prosody pitch='+0Hz' rate='{rate}'>"
        f"{text}</prosody></voice></speak>"
    )
    return ssml
def connect_id() -> str:
    """
    Returns a UUID without dashes.

    Returns:
        str: A UUID without dashes.
    """
    return str(uuid.uuid4()).replace("-", "")
async def transferMsTTSData(rate,content, voice):
    
    req_id = uuid.uuid4().hex.upper()
     
    endpoint2 = f"wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1?TrustedClientToken=6A5AA1D4EAFF4E9FB37E23D68491D6F4"
    headers={
        "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "Origin": "chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    " (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41",
    }
    async with websockets.connect(endpoint2,extra_headers=headers) as websocket:
        date = date_to_string()
         
        await websocket.send( f"X-Timestamp:{date}\r\n"
                    "Content-Type:application/json; charset=utf-8\r\n"
                    "Path:speech.config\r\n\r\n"
                    '{"context":{"synthesis":{"audio":{"metadataoptions":{'
                    '"sentenceBoundaryEnabled":false,"wordBoundaryEnabled":true},'
                    '"outputFormat":"audio-24khz-48kbitrate-mono-mp3"'
                    "}}}}\r\n")
        await websocket.send(
                    ssml_headers_plus_data(
                        connect_id(),
                        date,
                        mkssml(content, voice, f'{int((rate)/20*100)}%'  ),
                    )
                )
        # payload_2 = '{"synthesis":{"audio":{"metadataOptions":{"sentenceBoundaryEnabled":false,"wordBoundaryEnabled":false},"outputFormat":"audio-16khz-32kbitrate-mono-mp3"}}}'
        # message_2 = 'Path : synthesis.context\r\nX-RequestId: ' + req_id + '\r\nX-Timestamp: ' + \
        #     getXTime() + '\r\nContent-Type: application/json\r\n\r\n' + payload_2
        # await websocket.send(message_2)
 
        # payload_3 = '<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"> <voice name="%s">   <prosody rate="%s%%" pitch="0%%">   %s  </prosody>   </voice>  </speak>'%(globalconfig['reader']['azuretts']['voice'],str(rate*10),content)
        # message_3 = 'Path: ssml\r\nX-RequestId: ' + req_id + '\r\nX-Timestamp: ' + \
        #     getXTime() + '\r\nContent-Type: application/ssml+xml\r\n\r\n' + payload_3
        # await websocket.send(message_3)
         
        end_resp_pat = re.compile('Path:turn.end')
        audio_stream = b''
        while(True):
            response = await websocket.recv() 
            # print(response)
            # print(type(response),"++++++++++++")
            # Make sure the message isn't telling us to stop
            if (re.search(end_resp_pat, str(response)) == None):
                # Check if our response is text data or the audio bytes
                if type(response) == type(bytes()):
                    # Extract binary data
                    try:
                        needle = b'Path:audio\r\n'
                        start_ind = response.find(needle) + len(needle)
                        audio_stream += response[start_ind:]
                    except:
                        pass
            else:
                break
        outputPath='./cache/tts/'+str(time.time())+'.mp3'
        with open(outputPath, 'wb') as audio_out:
            audio_out.write(audio_stream)
        return outputPath