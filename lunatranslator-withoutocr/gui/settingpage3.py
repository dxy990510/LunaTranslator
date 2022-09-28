import functools
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import  QFont

from PyQt5.QtWidgets import  QWidget,QLabel,QFrame,QPushButton ,QSlider,QSpinBox,QFontComboBox 
import qtawesome 
 
from utils.config import globalconfig 
  
import gui.switchbutton
import gui.attachprocessdialog  
import gui.selecthook  
def setTabThree(self) :
     
        self.tab_3 = QWidget()
        self.tab_widget.addTab(self.tab_3, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_3), " 显示设置") 
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 20, 20, 90, 20)
        label.setText("翻译框透明度:") 
        self.horizontal_slider = QSlider(self.tab_3)
        self.customSetGeometry(self.horizontal_slider, 120, 18, 320, 25)
        self.horizontal_slider.setMaximum(100)
        self.horizontal_slider.setOrientation(Qt.Horizontal)
        self.horizontal_slider.setValue(0)
        self.horizontal_slider.setValue(globalconfig['transparent'])
        self.horizontal_slider.valueChanged.connect(functools.partial(changeHorizontal,self))  
        self.horizontal_slider_label = QLabel(self.tab_3)
        self.customSetGeometry(self.horizontal_slider_label, 450, 20, 30, 20)
        self.horizontal_slider_label.setText("{}%".format(globalconfig['transparent'])) 
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 20, 70, 145, 16)
        label.setText("字体大小:") 
        self.fontSize_spinBox = QSpinBox(self.tab_3)
        self.customSetGeometry(self.fontSize_spinBox, 95, 65, 40, 25)
        self.fontSize_spinBox.setMinimum(10)
        self.fontSize_spinBox.setMaximum(30)
        self.fontSize_spinBox.setValue(globalconfig['fontsize']) 
        self.fontSize_spinBox.valueChanged.connect(lambda x:globalconfig.__setitem__('fontsize',x))
 
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 275, 70, 145, 20)
        label.setText("字体类型:")
 
        self.font_comboBox = QFontComboBox(self.tab_3)
        self.customSetGeometry(self.font_comboBox, 350, 65, 185, 25)
        self.font_comboBox.activated[str].connect(lambda x:globalconfig.__setitem__('fonttype',x))
        self.comboBox_font = QFont(globalconfig['fonttype'])
        self.font_comboBox.setCurrentFont(self.comboBox_font)  
        
 
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 20, 170, 60, 20)
        label.setText("字体样式:")
 
        self.font_type_switch =gui.switchbutton.MySwitch(self.tab_3, sign=globalconfig['issolid'] ,textOn='实心',textOff='空心')
        self.customSetGeometry(self.font_type_switch, 95, 170,66,22)
        self.font_type_switch.clicked.connect(lambda x:globalconfig.__setitem__('issolid',x)) 
  
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 275, 120, 60, 20)
        label.setText("显示原文:")
 
        self.show_original_switch =gui.switchbutton.MySwitch(self.tab_3, sign=globalconfig['isshowrawtext'],  textOn='显示',textOff='隐藏')
        self.customSetGeometry(self.show_original_switch, 350, 120, 66,22)
        self.show_original_switch.clicked.connect(lambda x:globalconfig.__setitem__('isshowrawtext',x))  
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 20, 120, 60, 20)
        label.setText("显示假名:")
 
        self.show_hira_switch =gui.switchbutton.MySwitch(self.tab_3, sign=globalconfig['isshowhira'],  textOn='显示',textOff='隐藏')
        self.customSetGeometry(self.show_hira_switch, 95, 120,66,22)
        self.show_hira_switch.clicked.connect(lambda x:globalconfig.__setitem__('isshowhira',x)) 
        
        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 275, 170, 60, 20)
        label.setText("原文颜色:")

        
        self.original_color_button = QPushButton(qtawesome.icon("fa.paint-brush", color=globalconfig['rawtextcolor']), "", self.tab_3)
        self.customSetIconSize(self.original_color_button, 20, 20)
        self.customSetGeometry(self.original_color_button, 350, 170, 20, 20)
        self.original_color_button.setStyleSheet("background: transparent;")
        self.original_color_button.clicked.connect(lambda: self.ChangeTranslateColor("raw", self.original_color_button)) 


        label = QLabel(self.tab_3)
        self.customSetGeometry(label, 275, 220, 60, 20)
        label.setText("背景颜色:") 
        self.back_color_button = QPushButton(qtawesome.icon("fa.paint-brush", color=globalconfig['backcolor']), "", self.tab_3)
        self.customSetIconSize(self.back_color_button, 20, 20)
        self.customSetGeometry(self.back_color_button, 350, 220, 20, 20)
        self.back_color_button.setStyleSheet("background: transparent;")
        self.back_color_button.clicked.connect(lambda: self.ChangeTranslateColor("back", self.back_color_button)) 

 
def changeHorizontal(self) :

        globalconfig['transparent'] = self.horizontal_slider.value() 
        self.horizontal_slider_label.setText("{}%".format(globalconfig['transparent']))
        if globalconfig['transparent'] == 0 :
            globalconfig['transparent'] = 1 
        self.object.translation_ui.translate_text.setStyleSheet("border-width:0;\
                                                                 border-style:outset;\
                                                                 border-top:0px solid #e8f3f9;\
                                                                 color:white;\
                                                                 font-weight: bold;\
                                                                background-color: rgba(%s, %s, %s, %s)"
                                           %(int(globalconfig['backcolor'][1:3],16),int(globalconfig['backcolor'][3:5],16),int(globalconfig['backcolor'][5:7],16),globalconfig['transparent']/100))
        self.object.translation_ui._TitleLabel.setStyleSheet("border-width:0;\
                                                                 border-style:outset;\
                                                                 border-top:0px solid #e8f3f9;\
                                                                 color:white;\
                                                                 font-weight: bold;\
                                                                background-color: rgba(%s, %s, %s, %s)"
                                           %(int(globalconfig['backcolor'][1:3],16),int(globalconfig['backcolor'][3:5],16),int(globalconfig['backcolor'][5:7],16),globalconfig['transparent']/200))
    
        # # 重置状态栏界面
        # self.object.translation_ui.statusbar.setStyleSheet("font: 10pt %s;"
        #                            #  "color: %s;"
        #                               #"background-color: rgba(%s, %s, %s, 0.1)"
        #                               "background-color: rgba(62,62,62, 0.1)"
        #                            #   %(int(globalconfig['backcolor'][1:3],16),int(globalconfig['backcolor'][3:5],16),int(globalconfig['backcolor'][5:7],16),globalconfig['fonttype']))
        #                               #,self.icon_color))
        #                              % (globalconfig['fonttype'] ))
 