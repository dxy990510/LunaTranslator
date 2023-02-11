 
from traceback import print_exc

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QLabel ,QProgressBar,QLineEdit,QPushButton 
import os 
from utils.config import globalconfig  ,_TR 
from utils.wrapper import threader
from version import version
def resourcegrid( ) :  
        grid=[
            [_TR('项目网站'),'<a href="https://github.com/HIllya51/LunaTranslator">https://github.com/HIllya51/LunaTranslator</a>',''],
            [_TR('使用说明'),'<a href="https://hillya51.github.io/">https://hillya51.github.io/</a>'],
            [_TR('OCR-简体中文'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.34.5/zh.zip">zh.zip</a>'],
            [_TR('OCR-繁体中文'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.34.5/cht.zip">cht.zip</a>'],
            [_TR('OCR-韩语'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.34.5/ko.zip">ko.zip</a>'],
            [_TR('辞书-MeCab'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/Mecab.zip">Mecab.zip</a>'],
            [_TR('辞书-小学馆'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/xiaoxueguan.db">xiaoxueguan.db</a>'],
            [_TR('辞书-EDICT'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/edict.db">edict.db</a>'],
            [_TR('辞书-EDICT2'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.1.2/edict2">edict2</a>'],
           # [_TR('辞书-JMdict'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.1.2/JMdict.xml">JMdict.xml</a>'],
            [_TR('辞书-灵格斯词典'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/Lingoes.zip">Lingoes.zip</a>'],
            [_TR('翻译-J北京7'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/JBeijing7.zip">JBeijing7.zip</a>'],
            [_TR('翻译-J北京7-用户词典'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v2.2.0/JBeijing7UserDict.zip">JBeijing7UserDict.zip</a>'],
            [_TR('翻译-金山快译'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/FastAIT09_Setup.25269.4101.zip">FastAIT09_Setup.25269.4101.zip</a>'],
            [_TR('翻译-快译通'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/DR.eye.zip">DR.eye.zip</a>'],
            [_TR('转区-Locale-Emulator'),'<a href="https://github.com/xupefei/Locale-Emulator/releases/download/v2.5.0.1/Locale.Emulator.2.5.0.1.zip">Locale.Emulator.2.5.0.1.zip</a>'],
            [_TR('转区-Locale_Remulator'),'<a href="https://github.com/InWILL/Locale_Remulator/releases/download/v1.5.0/Locale_Remulator.1.5.0.zip">Locale_Remulator.1.5.0.zip</a>'],
            [_TR('语音-VoiceRoid2'),'<a href="https://github.com/HIllya51/LunaTranslator/releases/download/v1.0/Yukari2.zip">Yukari2.zip</a>'],
            [_TR('语音-VOICEVOX'),'<a href="https://github.com/VOICEVOX/voicevox/releases/download/0.13.3/voicevox-windows-cpu-0.13.3.zip">voicevox-windows-cpu-0.13.3.zip</a>'],
        ]
        return grid
@threader
def getversion(self):
    import requests 
    import shutil
    import zipfile
    from utils.downloader import mutithreaddownload
    # with open('files/about.txt','r',encoding='utf8') as ff:
    #     about=ff.read()
    # with open('files/version.txt','r',encoding='utf8') as ff:
    #     version=ff.read()  
    url='https://github.com/HIllya51/LunaTranslator/releases/'
    self.versiontextsignal.emit(_TR('当前版本')+':'+  version+'  '+_TR("最新版本")+':'+ _TR('获取中'))#,'',url,url)) 
    try:
        requests.packages.urllib3.disable_warnings()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
             'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        res= requests.get('https://api.github.com/repos/HIllya51/LunaTranslator/releases/latest', headers=headers,proxies={'http': None,'https': None} ,verify = False).json() 
        #print(res)
        _version=res['tag_name']
       # print(version)
        url=res['assets'][0]['browser_download_url'] 
    except:
        print_exc()
        _version=_TR("获取失败") 
    self.versiontextsignal.emit((_TR('当前版本')+':'+  version+'  '+_TR("最新版本")+':'+ _version) ) #,'' if version== _version else  newcontent,url,'LunaTranslator.zip'))
    if _version!=_TR("获取失败") and version!=_version:
        if globalconfig['autoupdate']:
            self.downloadprogress.show()
            self.progresssignal.emit('……',0)
        
            savep=f'./cache/update/LunaTranslator.zip' 
            def endcallback():
                if os.path.exists('./cache/update/LunaTranslator'):
                    shutil.rmtree('./cache/update/LunaTranslator')
                zipf=(zipfile.ZipFile('./cache/update/LunaTranslator.zip'))
                zipf.extractall('./cache/update')
                self.needupdate=True
                self.updatefile=savep
            mutithreaddownload(savep,url,self.progresssignal.emit,lambda: globalconfig.__getitem__('autoupdate'),endcallback) 
 
def updateprogress(self,text,val):
    self.downloadprogress.setValue(val)
    self.downloadprogress.setFormat(text)
    

def setTab_about_dicrect(self) : 
    
    self.versionlabel = QLabel()
    self.versionlabel.setOpenExternalLinks(True)
    self.versionlabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse) 
    self.versiontextsignal.connect(lambda x:self.versionlabel.setText(x) )
    self.downloadprogress=QProgressBar()
        
    self.downloadprogress.hide()
    self.downloadprogress.setRange(0,10000)

    self.downloadprogress.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    self.progresssignal.connect(lambda text,val:updateprogress(self,text,val))
    getversion(self)
def setTab_about(self) : 
    self.tabadd_lazy(self.tab_widget, ('其他设置'), lambda :setTab_aboutlazy(self)) 
def setTab_aboutlazy(self) : 
        
 

        def _setproxy(x): 
            if x:
                os.environ['https_proxy']=globalconfig['proxy'] 
                os.environ['http_proxy']=globalconfig['proxy'] 
            else:
                os.environ['https_proxy']='' 
                os.environ['http_proxy']=''
        #_setproxy(globalconfig['useproxy'])
        if globalconfig['useproxy']:
                os.environ['https_proxy']=globalconfig['proxy'] 
                os.environ['http_proxy']=globalconfig['proxy'] 
        proxy=QLineEdit(globalconfig['proxy'])
        btn=QPushButton(_TR('确定' ))
        def __resetproxy(x):
            globalconfig.__setitem__('proxy',proxy.text())
            if globalconfig['useproxy']:
                os.environ['https_proxy']=globalconfig['proxy'] 
                os.environ['http_proxy']=globalconfig['proxy'] 
        btn.clicked.connect(lambda x: __resetproxy(x))

        
        
        grid1=[ 
            [
                ("使用代理",5),(self.getsimpleswitch(globalconfig  ,'useproxy',callback=lambda x: _setproxy(x)),1),''],
            [        ("代理设置(ip:port)",5),        (proxy,5),(btn,2),  
            ], 
        ]
        grid2=[                
                [('自动下载更新(需要连接github)',5),(self.getsimpleswitch(globalconfig ,'autoupdate',callback= lambda x:getversion(self)),1) ],
                [(self.versionlabel,10)], 
                [(self.downloadprogress,10)],
                #[(self.versionlabel4,10)] 
        ]  
         
         
        tab=self.makesubtab_lazy(['自动更新','代理设置','资源下载' ],[
                lambda: self.makescroll(self.makegrid(grid2 )   ) ,
                lambda: self.makescroll(self.makegrid(grid1 )   ),
                lambda:self.makescroll( self.makegrid(resourcegrid(),link=True ) )
                ]) 

        wh=self.rate*360
         
        shuoming = (QLabel('如果你感觉该软件对你有帮助，欢迎微信扫码或者前往<a href="https://afdian.net/a/HIllya51">爱发电</a>赞助，谢谢，么么哒~<br>'+f'<img src="./files/zan.jpg" heigth={wh} width={wh}>') )
        shuoming.setOpenExternalLinks(True)
        
        return self.makevbox([tab,shuoming ])