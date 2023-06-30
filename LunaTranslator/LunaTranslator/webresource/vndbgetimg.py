
from urllib.parse import quote
import base64
import queue,time,requests,re,os
from traceback import print_exc
import hashlib
from myutils.utils import getproxy
from myutils.config import globalconfig
def b64string(a): 
    return hashlib.md5(a.encode('utf8')).hexdigest()


def vndbdownloadimg(url):
    if url is None:
         return None
    savepath='./cache/vndb/'+b64string(url)+'.jpg'
    if os.path.exists(savepath):
         return savepath
    headers= {
        'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'Referer': 'https://vndb.org/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
        'sec-ch-ua-platform': '"Windows"',
    }  
    try:
        time.sleep(1)
        _content=requests.get(url,headers=headers,proxies=getproxy()).content
        with open(savepath,'wb') as ff:
            ff.write(_content)
        return savepath
    except:
         return None
def vndbsearch(title):#301直接跳转到目标
    cookies = {
        'vndb_samesite': '1',
    }
            
    headers = {
        'authority': 'vndb.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 
        'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
    }     
    url='https://vndb.org/v?sq='+quote(title)
    savepath='./cache/vndb/'+b64string(url)+'.html'
    #print(url,savepath)
    #print(getproxy())
    if not os.path.exists(savepath): 
        try: 
            time.sleep(1)
            response = requests.get(url, cookies=cookies, headers=headers,proxies=getproxy())
            with open(savepath,'w',encoding='utf8') as ff:
                 ff.write(response.text)
            text=response.text
        except:
            print_exc()
            return None
    else:
         with open(savepath,'r',encoding='utf8') as ff:
            text=ff.read()
    try:
        #301
        imgurl=(re.search('<div class="imghover--visible"><img src="(.*?)"',text).groups()[0])
        return imgurl
    except:
        pass
    
    try:
        found=re.findall('<td class="tc_title"><a href="(.*?)"',text)
    except:
        return None 
     
    if len(found)==0:
         return None
     
    url='https://vndb.org'+found[0]
    savepath='./cache/vndb/'+b64string(url)+'.html'
    #print(url,savepath)
    if not os.path.exists(savepath): 
        try: 
            time.sleep(1)
            response = requests.get(url, cookies=cookies, headers=headers,proxies=getproxy())
            with open(savepath,'w',encoding='utf8') as ff:
                 ff.write(response.text)
            text=response.text
        except:
            return None
    else:
         with open(savepath,'r',encoding='utf8') as ff:
            text=ff.read()
    try: 
        imgurl=(re.search('<div class="imghover--visible"><img src="(.*?)"',text).groups()[0])
        return imgurl
    except:
        pass
def vndbsearchinfo(title):#301直接跳转到目标
    cookies = {
        'vndb_samesite': '1',
    }
            
    headers = {
        'authority': 'vndb.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 
        'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
    }     
    url='https://vndb.org/v?sq='+quote(title)
    savepath='./cache/vndb/'+b64string(url)+'.html'
    #print(url,savepath)
    #print(getproxy())
    if not os.path.exists(savepath): 
        try: 
            time.sleep(1)
            response = requests.get(url, cookies=cookies, headers=headers,proxies=getproxy())
            with open(savepath,'w',encoding='utf8') as ff:
                 ff.write(response.text)
            text=response.text
        except:
            print_exc()
            return None
    else:
         with open(savepath,'r',encoding='utf8') as ff:
            text=ff.read()
    try:
        #301
        imgurl=(re.search('<div class="imghover--visible"><img src="(.*?)"',text).groups()[0])
        return savepath
    except:
        pass
    
    try:
        found=re.findall('<td class="tc_title"><a href="(.*?)"',text)
    except:
        return None 
     
    if len(found)==0:
         return None
     
    url='https://vndb.org'+found[0]
    savepath='./cache/vndb/'+b64string(url)+'.html'
    #print(url,savepath)
    if not os.path.exists(savepath): 
        try: 
            time.sleep(1)
            response = requests.get(url, cookies=cookies, headers=headers,proxies=getproxy())
            with open(savepath,'w',encoding='utf8') as ff:
                 ff.write(response.text)
            text=response.text
        except:
            return None
    else:
         with open(savepath,'r',encoding='utf8') as ff:
            text=ff.read()
    try: 
        imgurl=(re.search('<div class="imghover--visible"><img src="(.*?)"',text).groups()[0])
        return savepath
    except:
        pass

def searchdatamethod(title):

    if os.path.exists('./cache/vndb')==False:
        os.mkdir('./cache/vndb')
    imgurl=vndbsearch(title) 
    #print(imgurl)
    savepath= vndbdownloadimg(imgurl)
    infosavepath=vndbsearchinfo(title)   
    return {'imagepath':savepath,'infopath':infosavepath}

import re
def parsehtmlmethod(infopath):
    with open(infopath,'r',encoding='utf8') as ff:
        text=ff.read()
    ##隐藏横向滚动
    text=text.replace('<body>','<body style="overflow-x: hidden;">')
    ##删除header
    text=re.sub('<header>([\\s\\S]*?)</header>','',text)
    text=re.sub('<footer>([\\s\\S]*?)</footer>','',text)
    text=re.sub('<article class="vnreleases"([\\s\\S]*?)</article>','',text)
    text=re.sub('<article class="vnstaff"([\\s\\S]*?)</article>','',text)
    text=re.sub('<article id="stats"([\\s\\S]*?)</article>','',text)
 
    text=re.sub('<nav>([\\s\\S]*?)</nav>','',text)
    text=re.sub('<p class="itemmsg">([\\s\\S]*?)</p>','',text) 
    text=re.sub('<div id="vntags">([\\s\\S]*?)</div>','',text) 
    text=re.sub('<div id="tagops">([\\s\\S]*?)</div>','',text) 
    resavepath=infopath+'parsed.html'

    if globalconfig['languageuse']==0:
        text=re.sub('<a href="(.*?)" lang="ja-Latn" title="(.*?)">(.*?)</a>','<a href="\\1" lang="ja-Latn" title="\\3">\\2</a>',text)

    try: 
        imgurl=(re.search('<div class="imghover--visible"><img src="(.*?)"',text).groups()[0])
        savepath='./cache/vndb/'+b64string(imgurl)+'.jpg'
        if os.path.exists(savepath):
            text=re.sub('<div class="imghover--visible"><img src="(.*?)"','<div class="imghover--visible"><img src="file://'+os.path.abspath(savepath).replace('\\','/')+'"',text)
    except:
        print_exc()
    
    with open(resavepath,'w',encoding='utf8') as ff:
        ff.write(text)

     
    return resavepath