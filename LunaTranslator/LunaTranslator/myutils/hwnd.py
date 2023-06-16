
import win32con ,win32utils,threading
from traceback import print_exc
from PyQt5.QtWinExtras  import QtWin
from PyQt5.QtGui import   QPixmap,QColor ,QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout,QApplication
import gobject
import os
import time,winrtutils
from myutils.wrapper import threader
from myutils.utils import argsort
def pid_running(pid): 
    try:
        process =win32utils.OpenProcess(win32con.SYNCHRONIZE, False, pid);
        if(process==0):return False
        ret =win32utils.WaitForSingleObject(process, 0);
        win32utils.CloseHandle(process);
        return (ret == win32con.WAIT_TIMEOUT);

    except:
        return False
@threader
def grabwindow(): 

        
        tm=time.localtime()
        
        fnamebase='./cache/screenshot/{}'.format(0)
        try:
                if gobject.baseobject.textsource.md5!='0':
                        fnamebase='./cache/screenshot/{}'.format(gobject.baseobject.textsource.prefix)
        except:
                pass
        if os.path.exists(fnamebase)==False:
                os.mkdir(fnamebase)
        fname='{}/{}-{}-{}-{}-{}-{}'.format(fnamebase,tm.tm_year,tm.tm_mon,tm.tm_mday,tm.tm_hour,tm.tm_min,tm.tm_sec)
        
        hwnd=win32utils.FindWindow('Window_Magpie_967EB565-6F73-4E94-AE53-00CC42592A22',None) 
        if hwnd: 
                try:
                        winrtutils._winrt_capture_window(fname+'_winrt_magpie.png',hwnd)
                except:
                        pass
                
        hwnd= win32utils.GetForegroundWindow()  
        try:
                if hwnd==int(gobject.baseobject.translation_ui.winId()):
                        hwnd=gobject.baseobject.textsource.hwnd
        except:
                print_exc()
                pass

        try:
                winrtutils._winrt_capture_window(fname+'_winrt.png',hwnd)
        except: 
                pass
        p=QApplication.primaryScreen().grabWindow(hwnd)
        
        if(not p.toImage().allGray()):
                p.save(fname+'_gdi.png')
                 
        gobject.baseobject.translation_ui.displaystatus.emit("saved to "+fname,'red',True)
def getpidhwndfirst(pid):
        try:
                hwnds=list()
                def get_all_hwnd(hwnd,_): 
                        if win32utils.IsWindow(hwnd) and win32utils.IsWindowEnabled(hwnd) and win32utils.IsWindowVisible(hwnd): 
                                if  win32utils.GetWindowThreadProcessId(hwnd)==pid:
                                        hwnds.append( (hwnd) )
                win32utils.EnumWindows(get_all_hwnd, 0)  
                return hwnds[0]
        except:
                return 0
def getwindowlist():
        windows_list=[]
        pidlist=[]
        win32utils.EnumWindows(lambda hWnd, param: windows_list.append(hWnd), 0) 
        for hwnd in windows_list:
                try:
                        pid=win32utils.GetWindowThreadProcessId(hwnd) 
                        pidlist.append(pid)
                except:
                        pass
        return list(set(pidlist))
def getprocesslist():
        
        pids= win32utils.EnumProcesses()
        return pids
 

def is64bit(pid):
        hprocess=win32utils.OpenProcess(win32con.PROCESS_QUERY_INFORMATION,False,pid)
        if hprocess==0:return False
        res=win32utils.Is64bit(hprocess)
        win32utils.CloseHandle(hprocess)
        return res

def getpidexe(pid):
        hwnd1=win32utils.OpenProcess(win32con.PROCESS_ALL_ACCESS,False, (pid))
        if(hwnd1==0):
                
                hwnd1=win32utils.OpenProcess(win32con.PROCESS_QUERY_LIMITED_INFORMATION,False, (pid))
        if(hwnd1==0):
                name_=None
        else:
                name_ = win32utils.GetProcessFileName( hwnd1)
        win32utils.CloseHandle(hwnd1)
        return name_
def testprivilege(pid):
       hwnd1=win32utils.OpenProcess(win32con.PROCESS_INJECT_ACCESS,False, (pid))
       win32utils.CloseHandle(hwnd1)
       return hwnd1!=0


def ListProcess(filt=True):  
        ret=[]
        pids=getprocesslist()
        for pid in pids: 
                    if os.getpid()==pid:
                           continue
                    try: 
                        name_=getpidexe(pid)
                        if name_ is None:continue
                        name=name_.lower()
                        if filt:
                                if name[-4:]!='.exe' or ':\\windows\\'  in name   or '\\microsoft\\'  in name or '\\windowsapps\\'  in name:
                                        continue 
                        ret.append([pid,name_ ])
                    except:
                        pass 
        kv={}
        for pid,exe in ret:
                if exe in kv:
                        kv[exe]['pid'].append(pid)
                else:
                        kv[exe]={'pid':[pid]}
        # for exe in kv:
        #         if len(kv[exe]['pid'])>1:
        #                 mems=[getprocessmem(_) for _ in kv[exe]['pid']]
        #                 _i=argsort(mems)
        #                 kv[exe]['pid']=[kv[exe]['pid'][_i[-1]]]
        xxx=[]
        for exe in kv:
                xxx.append([kv[exe]['pid'],exe])
        return xxx

def getExeIcon( name,icon=True ): 
            large = win32utils.ExtractIconEx(name)
            if large:
                    pixmap =QtWin.fromHICON(large)
            else:
                   pixmap=QPixmap(100,100)
                   pixmap.fill(QColor.fromRgba(0))
            if icon:
                    return QIcon(pixmap)
            else:
                    return pixmap
__rate=0
def getScreenRate() :
    global __rate
    if __rate==0:
        hDC = win32utils.GetDC(0) 
        dpiX = win32utils.GetDeviceCaps(hDC, win32con.LOGPIXELSX) /96.0;
        win32utils._ReleaseDC(None, hDC); 
        __rate = round(dpiX, 2)  
    return __rate


def mouseselectwindow(callback): 
        
        def _loop():
                while True:
                        keystate=win32utils.GetKeyState(win32con.VK_LBUTTON ) #必须使用GetKeyState, GetAsyncKeyState或SetWindowHookEx都无法检测到高权限应用上的点击事件。
                        if(keystate<0):
                                break
                        time.sleep(0.01)
                try:
                        pos=win32utils.GetCursorPos()
                        hwnd=win32utils.GetAncestor(win32utils.WindowFromPoint(pos))
                        pid=win32utils.GetWindowThreadProcessId(hwnd)
                        callback(pid,hwnd)
                except:
                        pass
        threading.Thread(target=_loop).start()
        

def letfullscreen(hwnd):
        wpc=win32utils. GetWindowPlacement( hwnd,False )
        HWNDStyle = win32utils.GetWindowLong( hwnd, win32con.GWL_STYLE )
        HWNDStyleEx = win32utils.GetWindowLong( hwnd, win32con.GWL_EXSTYLE  )
        NewHWNDStyle=HWNDStyle
        NewHWNDStyle &= ~win32con.WS_BORDER;
        NewHWNDStyle &= ~win32con.WS_DLGFRAME;
        NewHWNDStyle &= ~win32con.WS_THICKFRAME;
        NewHWNDStyleEx=HWNDStyleEx
        NewHWNDStyleEx &= ~win32con.WS_EX_WINDOWEDGE;
        win32utils.SetWindowLong( hwnd, win32con.GWL_STYLE, NewHWNDStyle | win32con.WS_POPUP );
        win32utils.SetWindowLong( hwnd, win32con.GWL_EXSTYLE, NewHWNDStyleEx | win32con.WS_EX_TOPMOST )
        win32utils.ShowWindow(hwnd,win32con.SW_SHOWMAXIMIZED )
        return (wpc,HWNDStyle,HWNDStyleEx)

def recoverwindow(hwnd,status):
        wpc,HWNDStyle,HWNDStyleEx=status
        win32utils.SetWindowLong( hwnd, win32con.GWL_STYLE,  HWNDStyle );
        win32utils.SetWindowLong( hwnd, win32con.GWL_EXSTYLE,  HWNDStyleEx );
        win32utils.ShowWindow( hwnd, win32con.SW_SHOWNORMAL );
        win32utils.SetWindowPlacement( hwnd, wpc );
def showintab(hwnd,show):
        style_ex=win32utils.GetWindowLong( hwnd, win32con.GWL_EXSTYLE )
        if(show):
                style_ex|=win32con.WS_EX_APPWINDOW
                style_ex &= ~win32con.WS_EX_TOOLWINDOW
        else: 
                style_ex &=~win32con.WS_EX_APPWINDOW
                style_ex |= win32con.WS_EX_TOOLWINDOW
        win32utils.SetWindowLong(hwnd,win32con.GWL_EXSTYLE,style_ex)