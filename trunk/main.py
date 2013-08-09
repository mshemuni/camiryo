# -*- coding: utf-8 -*-
"""
Created---------------------------------------------------------------------------------------------
﻿  ﻿  By:
﻿  ﻿  ﻿  Muhammed SHEMUNI﻿	Developer
﻿  ﻿  ﻿  Yücel KILIÇ﻿		Developer
﻿  ﻿  at:
﻿  ﻿  ﻿  Begin﻿				01.03.2013
﻿  ﻿  ﻿  Last update﻿		19.07.2013
"""

import sys , os, time, string, math, signal, datetime, glob

from atasamMeteosat import Ui_Form
import MSHYK_Color as myc
from PyQt4 import QtGui, QtCore

class MyForm(QtGui.QWidget):
  def __init__(self):
    super(MyForm, self).__init__()
    self.ui = Ui_Form()
    self.ui.setupUi(self)
    
    f = open('./pat', 'r')
    for line in f:
		li=line.strip()
		
    #self.ui.lineEdit.setText(QtGui.QApplication.translate("Form", str(li), None, QtGui.QApplication.UnicodeUTF8))
    self.ui.lineEdit.hide()
    self.ui.lineEdit_2.hide()
    self.ui.tabWidget_2.setTabEnabled(2,False)
    self.ui.tabWidget_3.setTabEnabled(2,False)
    self.ui.tabWidget_4.setTabEnabled(2,False)

    #self.ui.listWidget.clicked.connect(self.dispTMS)
    
    self.ui.listWidget.clicked.connect(self.dispAMS)
    self.ui.listWidget_2.clicked.connect(self.dispAMR)
    self.ui.listWidget_3.clicked.connect(self.dispAMP)
    self.ui.listWidget_4.clicked.connect(self.dispDMS)
    self.ui.listWidget_5.clicked.connect(self.dispDMR)
    self.ui.listWidget_6.clicked.connect(self.dispDMP)
    self.ui.listWidget_7.clicked.connect(self.dispTMS)
    self.ui.listWidget_8.clicked.connect(self.dispTMR)
    self.ui.listWidget_9.clicked.connect(self.dispTMP)
    
    
    self.ui.pushButton_2.clicked.connect(self.fillList)
    self.ui.pushButton_3.clicked.connect(self.fillList)
    self.ui.pushButton_5.clicked.connect(self.fillList)
    self.ui.pushButton_7.clicked.connect(self.fillList)
    self.ui.pushButton_9.clicked.connect(self.fillList)
    self.ui.pushButton_11.clicked.connect(self.fillList)
    self.ui.pushButton_13.clicked.connect(self.fillList)
    self.ui.pushButton_15.clicked.connect(self.fillList)
    self.ui.pushButton_17.clicked.connect(self.fillList)
    
    self.ui.pushButton.clicked.connect(self.animAMS)
    self.ui.pushButton_4.clicked.connect(self.animAMR)
    self.ui.pushButton_6.clicked.connect(self.animAMP)
    self.ui.pushButton_8.clicked.connect(self.animDMS)
    self.ui.pushButton_10.clicked.connect(self.animDMR)
    self.ui.pushButton_12.clicked.connect(self.animDMP)
    self.ui.pushButton_14.clicked.connect(self.animTMS)
    self.ui.pushButton_16.clicked.connect(self.animTMR)
    self.ui.pushButton_18.clicked.connect(self.animTMP)
    

    self.ui.comboBox.currentIndexChanged['QString'].connect(self.dispAMS)
    self.ui.comboBox_2.currentIndexChanged['QString'].connect(self.dispAMR)
    self.ui.comboBox_3.currentIndexChanged['QString'].connect(self.dispAMP)
    
    self.ui.comboBox_4.currentIndexChanged['QString'].connect(self.dispDMS)
    self.ui.comboBox_5.currentIndexChanged['QString'].connect(self.dispDMR)
    self.ui.comboBox_6.currentIndexChanged['QString'].connect(self.dispDMP)
    
    self.ui.comboBox_7.currentIndexChanged['QString'].connect(self.dispTMS)
    self.ui.comboBox_8.currentIndexChanged['QString'].connect(self.dispTMR)
    self.ui.comboBox_9.currentIndexChanged['QString'].connect(self.dispTMP)
    
    #self.ui.pushButton_3.clicked.connect(self.saveSettings)
    self.ui.graphicsView.wheelEvent = self.ZoomAMS
    self.ui.graphicsView_2.wheelEvent = self.ZoomAMR
    self.ui.graphicsView_3.wheelEvent = self.ZoomAMP
    
    self.ui.graphicsView_4.wheelEvent = self.ZoomDMS
    self.ui.graphicsView_5.wheelEvent = self.ZoomDMR
    self.ui.graphicsView_6.wheelEvent = self.ZoomDMP
    
    self.ui.graphicsView_7.wheelEvent = self.ZoomTMS
    self.ui.graphicsView_8.wheelEvent = self.ZoomTMR
    self.ui.graphicsView_9.wheelEvent = self.ZoomTMP
    
    self.timer = QtCore.QBasicTimer()
    self.step = 0
    self.fillList()
    
  def getListofItems(self, listDev):
	  items = listDev.selectedItems()
	  x=[]
	  for i in list(items):
		  x.append(str(i.text()))
	  return x
    
  def animStart(self, listDev, dispDev):
	  if self.timer.isActive():
		  self.timer.stop()
		  self.ui.progressBar.setProperty("value", math.ceil(0))
		  self.ui.progressBar.setFormat(QtGui.QApplication.translate("Form", "%p%", None, QtGui.QApplication.UnicodeUTF8))
	  else:
		  self.timer.start(300, self)
		  self.ui.lineEdit_2.setText("0")
		  
	  	
  def timerEvent(self, e):
	  if self.ui.lineEdit.text() == "AMS":
		  lst = self.getListofItems(self.ui.listWidget)
		  self.ui.lineEdit_2.setText(str(int(self.ui.lineEdit_2.text())+1))
		  if int(self.ui.lineEdit_2.text()) < len(lst):
			  myc.createImage_ani(self.ui.comboBox.currentText(), lst[len(lst) - int(self.ui.lineEdit_2.text())])
			  self.display(self.ui.graphicsView)
			  
			  self.ui.progressBar.setProperty("value", math.ceil((100/len(lst))*(int(self.ui.lineEdit_2.text())+1)))
			  self.ui.progressBar.setFormat(QtGui.QApplication.translate("Form", "%p%" + " | " + self.getTime(self.fileNamePath(lst[len(lst) - int(self.ui.lineEdit_2.text())])), None, QtGui.QApplication.UnicodeUTF8))
		  else:
			  self.ui.lineEdit_2.setText("0")
		  
		  
	  if self.ui.lineEdit.text() == "AMR":
		  lst = self.getListofItems(self.ui.listWidget_2)
		  self.ui.lineEdit_2.setText(str(int(self.ui.lineEdit_2.text())+1))
		  if int(self.ui.lineEdit_2.text()) < len(lst):
			  myc.createImage_ani(self.ui.comboBox_2.currentText(), lst[len(lst) - int(self.ui.lineEdit_2.text())])
			  self.display(self.ui.graphicsView_2)
			  
			  self.ui.progressBar_2.setProperty("value", math.ceil((100/len(lst))*(int(self.ui.lineEdit_2.text())+1)))
			  self.ui.progressBar_2.setFormat(QtGui.QApplication.translate("Form", "%p%" + " | " + self.getTime(self.fileNamePath(lst[len(lst) - int(self.ui.lineEdit_2.text())])), None, QtGui.QApplication.UnicodeUTF8))
		  else:
			  self.ui.lineEdit_2.setText("0")
			  

	  if self.ui.lineEdit.text() == "AMP":
		  lst = self.getListofItems(self.ui.listWidget_3)
		  self.ui.lineEdit_2.setText(str(int(self.ui.lineEdit_2.text())+1))
		  if int(self.ui.lineEdit_2.text()) < len(lst):
			  myc.createImage_ani(self.ui.comboBox_3.currentText(), lst[len(lst) - int(self.ui.lineEdit_2.text())])
			  self.display(self.ui.graphicsView_3)
			  
			  self.ui.progressBar_3.setProperty("value", math.ceil((100/len(lst))*(int(self.ui.lineEdit_2.text())+1)))
			  self.ui.progressBar_3.setFormat(QtGui.QApplication.translate("Form", "%p%" + " | " + self.getTime(self.fileNamePath(lst[len(lst) - int(self.ui.lineEdit_2.text())])), None, QtGui.QApplication.UnicodeUTF8))
		  else:
			  self.ui.lineEdit_2.setText("0")

	  if self.ui.lineEdit.text() == "DMS":
		  lst = self.getListofItems(self.ui.listWidget_4)
		  self.ui.lineEdit_2.setText(str(int(self.ui.lineEdit_2.text())+1))
		  if int(self.ui.lineEdit_2.text()) < len(lst):
			  myc.createImage_ani(self.ui.comboBox_4.currentText(), lst[len(lst) - int(self.ui.lineEdit_2.text())])
			  self.display(self.ui.graphicsView_4)
			  
			  self.ui.progressBar_4.setProperty("value", math.ceil((100/len(lst))*(int(self.ui.lineEdit_2.text())+1)))
			  self.ui.progressBar_4.setFormat(QtGui.QApplication.translate("Form", "%p%" + " | " + self.getTime(self.fileNamePath(lst[len(lst) - int(self.ui.lineEdit_2.text())])), None, QtGui.QApplication.UnicodeUTF8))
		  else:
			  self.ui.lineEdit_2.setText("0")
		  
		  
	  if self.ui.lineEdit.text() == "DMR":
		  lst = self.getListofItems(self.ui.listWidget_5)
		  self.ui.lineEdit_2.setText(str(int(self.ui.lineEdit_2.text())+1))
		  if int(self.ui.lineEdit_2.text()) < len(lst):
			  myc.createImage_ani(self.ui.comboBox_5.currentText(), lst[len(lst) - int(self.ui.lineEdit_2.text())])
			  self.display(self.ui.graphicsView_5)
			  
			  self.ui.progressBar_5.setProperty("value", math.ceil((100/len(lst))*(int(self.ui.lineEdit_2.text())+1)))
			  self.ui.progressBar_5.setFormat(QtGui.QApplication.translate("Form", "%p%" + " | " + self.getTime(self.fileNamePath(lst[len(lst) - int(self.ui.lineEdit_2.text())])), None, QtGui.QApplication.UnicodeUTF8))
		  else:
			  self.ui.lineEdit_2.setText("0")
			  
			  
	  if self.ui.lineEdit.text() == "DMP":
		  lst = self.getListofItems(self.ui.listWidget_6)
		  self.ui.lineEdit_2.setText(str(int(self.ui.lineEdit_2.text())+1))
		  if int(self.ui.lineEdit_2.text()) < len(lst):
			  myc.createImage_ani(self.ui.comboBox_6.currentText(), lst[len(lst) - int(self.ui.lineEdit_2.text())])
			  self.display(self.ui.graphicsView_6)
			  
			  self.ui.progressBar_6.setProperty("value", math.ceil((100/len(lst))*(int(self.ui.lineEdit_2.text())+1)))
			  self.ui.progressBar_6.setFormat(QtGui.QApplication.translate("Form", "%p%" + " | " + self.getTime(self.fileNamePath(lst[len(lst) - int(self.ui.lineEdit_2.text())])), None, QtGui.QApplication.UnicodeUTF8))
		  else:
			  self.ui.lineEdit_2.setText("0")
			  
	  if self.ui.lineEdit.text() == "TMS":
		  lst = self.getListofItems(self.ui.listWidget_7)
		  self.ui.lineEdit_2.setText(str(int(self.ui.lineEdit_2.text())+1))
		  if int(self.ui.lineEdit_2.text()) < len(lst):
			  myc.createImage_ani(self.ui.comboBox_7.currentText(), lst[len(lst) - int(self.ui.lineEdit_2.text())])
			  self.display(self.ui.graphicsView_7)
			  
			  self.ui.progressBar_7.setProperty("value", math.ceil((100/len(lst))*(int(self.ui.lineEdit_2.text())+1)))
			  self.ui.progressBar_7.setFormat(QtGui.QApplication.translate("Form", "%p%" + " | " + self.getTime(self.fileNamePath(lst[len(lst) - int(self.ui.lineEdit_2.text())])), None, QtGui.QApplication.UnicodeUTF8))
		  else:
			  self.ui.lineEdit_2.setText("0")

	  if self.ui.lineEdit.text() == "TMR":
		  lst = self.getListofItems(self.ui.listWidget_8)
		  self.ui.lineEdit_2.setText(str(int(self.ui.lineEdit_2.text())+1))
		  if int(self.ui.lineEdit_2.text()) < len(lst):
			  myc.createImage_ani(self.ui.comboBox_8.currentText(), lst[len(lst) - int(self.ui.lineEdit_2.text())])
			  self.display(self.ui.graphicsView_8)
			  
			  self.ui.progressBar_8.setProperty("value", math.ceil((100/len(lst))*(int(self.ui.lineEdit_2.text())+1)))
			  self.ui.progressBar_8.setFormat(QtGui.QApplication.translate("Form", "%p%" + " | " + self.getTime(self.fileNamePath(lst[len(lst) - int(self.ui.lineEdit_2.text())])), None, QtGui.QApplication.UnicodeUTF8))
		  else:
			  self.ui.lineEdit_2.setText("0")
			  
			  
	  if self.ui.lineEdit.text() == "TMP":
		  lst = self.getListofItems(self.ui.listWidget_9)
		  self.ui.lineEdit_2.setText(str(int(self.ui.lineEdit_2.text())+1))
		  if int(self.ui.lineEdit_2.text()) < len(lst):
			  myc.createImage_ani(self.ui.comboBox_9.currentText(), lst[len(lst) - int(self.ui.lineEdit_2.text())])
			  self.display(self.ui.graphicsView_9)
			  
			  self.ui.progressBar_9.setProperty("value", math.ceil((100/len(lst))*(int(self.ui.lineEdit_2.text())+1)))
			  self.ui.progressBar_9.setFormat(QtGui.QApplication.translate("Form", "%p%" + " | " + self.getTime(self.fileNamePath(lst[len(lst) - int(self.ui.lineEdit_2.text())])), None, QtGui.QApplication.UnicodeUTF8))
		  else:
			  self.ui.lineEdit_2.setText("0")
			  self.ui.lineEdit_2.setText("0")

  def fileNamePath(self, Path):
	  countOfSlashs = Path.count("/")
	  imgFileNamePath = Path.split("/")
	  Name = str(imgFileNamePath[countOfSlashs])
	  return Name

  def getTime(self, Name):
	  splitesCount = Name.count("_")
	  splites = Name.split("_")
	  DT = str(splites[splitesCount]).replace(".h5","")
	  yea=DT[0:4]
	  moun=DT[4:6]
	  day=DT[6:8]
	  hour=DT[8:10]
	  minut=DT[10:12]
	  return day + "." + moun + "." + yea + " " + hour + ":" + minut

  def animAMS(self):
	  self.anim(self.ui.comboBox, self.ui.pushButton ,self.ui.listWidget, self.ui.pushButton_2)
	  self.ui.lineEdit.setText("AMS")
	  self.animStart(self.ui.listWidget, self.ui.graphicsView )
  def animAMR(self):
	  self.ui.lineEdit.setText("AMR")
	  self.anim(self.ui.comboBox_2, self.ui.pushButton_4 ,self.ui.listWidget_2, self.ui.pushButton_3)
	  self.animStart(self.ui.listWidget_2, self.ui.graphicsView_2 )
  def animAMP(self):
	  self.ui.lineEdit.setText("AMP")
	  self.anim(self.ui.comboBox_3, self.ui.pushButton_6 ,self.ui.listWidget_3, self.ui.pushButton_5)
	  self.animStart(self.ui.listWidget_3, self.ui.graphicsView_3 )
  def animDMS(self):
	  self.ui.lineEdit.setText("DMS")
	  self.anim(self.ui.comboBox_4, self.ui.pushButton_8 ,self.ui.listWidget_4, self.ui.pushButton_7)
	  self.animStart(self.ui.listWidget_4, self.ui.graphicsView_4 )
  def animDMR(self):
	  self.ui.lineEdit.setText("DMR")
	  self.anim(self.ui.comboBox_5, self.ui.pushButton_10 ,self.ui.listWidget_5, self.ui.pushButton_9)
	  self.animStart(self.ui.listWidget_5, self.ui.graphicsView_5 )
  def animDMP(self):
	  self.ui.lineEdit.setText("DMP")
	  self.anim(self.ui.comboBox_6, self.ui.pushButton_12 ,self.ui.listWidget_6, self.ui.pushButton_10)
	  self.animStart(self.ui.listWidget_6, self.ui.graphicsView_6 )
  def animTMS(self):
	  self.ui.lineEdit.setText("TMS")
	  self.anim(self.ui.comboBox_7, self.ui.pushButton_14 ,self.ui.listWidget_7, self.ui.pushButton_13)
	  self.animStart(self.ui.listWidget_7, self.ui.graphicsView_7 )
  def animTMR(self):
	  self.ui.lineEdit.setText("TMR")
	  self.anim(self.ui.comboBox_8, self.ui.pushButton_16 ,self.ui.listWidget_8, self.ui.pushButton_15)
	  self.animStart(self.ui.listWidget_8, self.ui.graphicsView_8 )
  def animTMP(self):
	  self.ui.lineEdit.setText("TMP")
	  self.anim(self.ui.comboBox_9, self.ui.pushButton_18 ,self.ui.listWidget_9, self.ui.pushButton_17)
	  self.animStart(self.ui.listWidget_9, self.ui.graphicsView_9 )
    
  def anim(self, comb, but, listWid, butref):
	  if but.text() == "Animate":
		  listWid.setEnabled(False)
		  comb.setEnabled(False)
		  butref.setEnabled(False)
		  but.setText("Stop")
	  elif but.text() == "Stop":
		  listWid.setEnabled(True)
		  comb.setEnabled(True)
		  butref.setEnabled(True)
		  but.setText("Animate")

  def selectFolder(self):
	  file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
	  self.ui.lineEdit.setText(QtGui.QApplication.translate("Form", str(file), None, QtGui.QApplication.UnicodeUTF8))
    
  def saveSettings(self):
	  li = self.ui.lineEdit.text()
	  f = open('./pat','w')
	  f.write(li)
	  f.close
    
  def fillList(self):
	  f = open('./pat', 'r')
	  for line in f:
		  li=line.strip()
		  
	  for i in ("Avrasya","DAG","Turkiye"):
	  	for u in ("MSG","MSGRSS","MPF"):
	  		if i=="Avrasya" and u=="MSG":
	  			self.getFiles(li + "/" + i + "/" + u, self.ui.listWidget)
	  		elif i=="Avrasya" and u=="MSGRSS":
	  			self.getFiles(li + "/" + i + "/" + u, self.ui.listWidget_2)
	  		elif i=="Avrasya" and u=="MPF":
	  			self.getFiles(li + "/" + i + "/" + u, self.ui.listWidget_3)
	  		elif i=="DAG" and u=="MSG":
	  			self.getFiles(li + "/" + i + "/" + u, self.ui.listWidget_4)
	  		elif i=="DAG" and u=="MSGRSS":
	  			self.getFiles(li + "/" + i + "/" + u, self.ui.listWidget_5)
	  		elif i=="DAG" and u=="MPF":
	  			self.getFiles(li + "/" + i + "/" + u, self.ui.listWidget_6)
	  		elif i=="Turkiye" and u=="MSG":
	  			self.getFiles(li + "/" + i + "/" + u, self.ui.listWidget_7)
	  		elif i=="Turkiye" and u=="MSGRSS":
	  			self.getFiles(li + "/" + i + "/" + u, self.ui.listWidget_8)
	  		elif i=="Turkiye" and u=="MPF":
	  			self.getFiles(li + "/" + i + "/" + u, self.ui.listWidget_9)
			
  def getFiles(self, path, listDevice):
	  
	  a = listDevice.count()
	  for i in xrange(a):
		  listDevice.takeItem(0)
		  
	  files = glob.glob(path + "/*.h5")
	  a = listDevice.count()-1
	  for x in files:
		  a=a+1
		  item = QtGui.QListWidgetItem()
		  listDevice.addItem(item)
		  item = listDevice.item(a)
		  item.setText(QtGui.QApplication.translate("Form", x, None, QtGui.QApplication.UnicodeUTF8))
	  listDevice.sortItems(1)
	  
  def dispAMS(self):
	  FilePath = self.ui.listWidget.currentItem()
	  met = self.ui.comboBox.currentText()
	  myc.createImage(met, FilePath)
	  self.display(self.ui.graphicsView)

  def dispAMR(self):
	  FilePath = self.ui.listWidget_2.currentItem()
	  met = self.ui.comboBox_2.currentText()
	  myc.createImage(met, FilePath)
	  self.display(self.ui.graphicsView_2)
	  
  def dispAMP(self):
	  FilePath = self.ui.listWidget_3.currentItem()
	  met = self.ui.comboBox_3.currentText()
	  myc.createImage(met, FilePath)
	  self.display(self.ui.graphicsView_3)
	  
  def dispTMS(self):
	  FilePath = self.ui.listWidget_7.currentItem()
	  met = self.ui.comboBox_7.currentText()
	  myc.createImage(met, FilePath)
	  self.display(self.ui.graphicsView_7)

  def dispTMR(self):
	  FilePath = self.ui.listWidget_8.currentItem()
	  met = self.ui.comboBox_8.currentText()
	  myc.createImage(met, FilePath)
	  self.display(self.ui.graphicsView_8)
	  
  def dispTMP(self):
	  FilePath = self.ui.listWidget_9.currentItem()
	  met = self.ui.comboBox_9.currentText()
	  myc.createImage(met, FilePath)
	  self.display(self.ui.graphicsView_9)
		  
  def dispDMS(self):
	  FilePath = self.ui.listWidget_4.currentItem()
	  met = self.ui.comboBox_4.currentText()
	  myc.createImage(met, FilePath)
	  self.display(self.ui.graphicsView_4)

  def dispDMR(self):
	  FilePath = self.ui.listWidget_5.currentItem()
	  met = self.ui.comboBox_5.currentText()
	  myc.createImage(met, FilePath)
	  self.display(self.ui.graphicsView_5)
	  
  def dispDMP(self):
	  FilePath = self.ui.listWidget_6.currentItem()
	  met = self.ui.comboBox_6.currentText()
	  myc.createImage(met, FilePath)
	  self.display(self.ui.graphicsView_6)

  def display(self, dispp):
	  diss="tmp/disp.png"
	  if os.path.isfile(str(diss)):
		  scene = QtGui.QGraphicsScene()
		  scene.addPixmap(QtGui.QPixmap(diss))
		  dispp.setScene(scene)

  def ZoomAMS(self, ev):
	  if ev.delta() < 0:
		  self.ui.graphicsView.scale(0.9, 0.9)
	  else:
		  self.ui.graphicsView.scale(1.1, 1.1)
		  
  def ZoomAMR(self, ev):
	  if ev.delta() < 0:
		  self.ui.graphicsView_2.scale(0.9, 0.9)
	  else:
		  self.ui.graphicsView_2.scale(1.1, 1.1)
			
  def ZoomAMP(self, ev):
	  if ev.delta() < 0:
		  self.ui.graphicsView_3.scale(0.9, 0.9)
	  else:
		  self.ui.graphicsView_3.scale(1.1, 1.1)

  def ZoomDMS(self, ev):
	  if ev.delta() < 0:
		  self.ui.graphicsView_4.scale(0.9, 0.9)
	  else:
		  self.ui.graphicsView_4.scale(1.1, 1.1)
		  
  def ZoomDMR(self, ev):
	  if ev.delta() < 0:
		  self.ui.graphicsView_5.scale(0.9, 0.9)
	  else:
		  self.ui.graphicsView_5.scale(1.1, 1.1)
			
  def ZoomDMP(self, ev):
	  if ev.delta() < 0:
		  self.ui.graphicsView_6.scale(0.9, 0.9)
	  else:
		  self.ui.graphicsView_6.scale(1.1, 1.1)

  def ZoomTMS(self, ev):
	  if ev.delta() < 0:
		  self.ui.graphicsView_7.scale(0.9, 0.9)
	  else:
		  self.ui.graphicsView_7.scale(1.1, 1.1)
		  
  def ZoomTMR(self, ev):
	  if ev.delta() < 0:
		  self.ui.graphicsView_8.scale(0.9, 0.9)
	  else:
		  self.ui.graphicsView_8.scale(1.1, 1.1)
			
  def ZoomTMP(self, ev):
	  if ev.delta() < 0:
		  self.ui.graphicsView_9.scale(0.9, 0.9)
	  else:
		  self.ui.graphicsView_9.scale(1.1, 1.1)
			
app = QtGui.QApplication(sys.argv)
f = MyForm()
f.show()
app.exec_()
