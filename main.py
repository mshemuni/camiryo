import sys, os, glob
from ftplib import FTP
import camiryo

import tempfile

try:
	import camiryo as cm
except:
	print "Something went wrong while importing Camiryo Library"

try:
	from PyQt4 import QtCore, QtGui
except:
	print "Something went wrong while importing PyQt4"

try:
	from camiryoGUI import Ui_Form
	import GUI
except:
	print "Something went wrong while importing Camiryo GUI"

class MyForm(QtGui.QWidget, Ui_Form):
	def __init__(self, verb=False):
		super(MyForm, self).__init__()
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.verb = verb
		
		self.ui.pushButton.clicked.connect(self.addLocalPath)
		self.ui.pushButton_2.clicked.connect(lambda: self.remFromList(self.ui.listWidget))
		self.ui.pushButton_3.clicked.connect(lambda: self.remFromList(self.ui.listWidget_2))
		self.ui.pushButton_5.clicked.connect(self.testConnection)
		self.ui.pushButton_4.clicked.connect(self.addRemotePath)
		self.ui.pushButton_7.clicked.connect(self.updateSetting)
		self.ui.pushButton_6.clicked.connect(self.animate)
		self.ui.graphicsView.wheelEvent = self.ZoomAMS
		
		self.timer = QtCore.QBasicTimer()
		self.step = 0
		
		self.loadSetting()
		self.getLists()
		self.it = 0
		self.count = 1
	def timerEvent(self, e):
		self.it = (self.it + 1)%int(self.count)
		self.showmeani(self.it+1)


	def animate(self):
		if not self.timer.isActive():
			
			self.ui.pushButton_6.setText("Stop")
			self.ui.comboBox.setEnabled(False)
			
			listWidget = self.lst[self.ui.tabWidget_2.currentIndex()]
			it = 0
			dispType = self.ui.comboBox.currentText()
			for i in listWidget.selectedItems():
				ln = i.text()
				it = it + 1
				if ln.contains("@"):
					u, pa = ln.split("@")
					usr, passwd = u.split("|")
					ip, path = pa.split("|")
					print str(tempfile.gettempdir())
					tmpFile = self.pathName(str(path))[1]
					self.getDataOverFTP(ip, usr, passwd, path, str(tempfile.gettempdir()))

					eFile = "%s/%s" %(str(tempfile.gettempdir()), tmpFile)
					mc = camiryo.myCol
					col = mc.coloring(verb=self.verb)
					if dispType == "Vegetation, Snow, Smoke, Dust and Fog (Day)":
						data = col.vssdfD(eFile)
					elif dispType == "Clouds, Convection, Snow, Fog and Fires (Day)":
						data =  col.ccsfD(eFile)
					elif dispType == "Snow and Fog (Day)":
						data =  col.sfD(eFile)
					elif dispType == "Severe Convection (Day)":
						data =  col.scD(eFile)
					elif dispType == "Clouds, Fog and Contrails (Night)":
						data =  col.cfcN(eFile)
					elif dispType == "Dust, Thin Clouds and Contrails (Day & Night)":
						data =  col.dtccDN(eFile)
					elif dispType == "Severe Cyclones, Jets and PV Analysis (Day & Night)":
						data =  col.scjPVaDN(fle)
					col.imgCreate(data, "%s/cam%s.png" %(tempfile.gettempdir(), it))
					
					if os.path.isfile(eFile):
						os.remove(eFile)
						
				else:
					eFile = str(ln)
					mc = camiryo.myCol
					col = mc.coloring(verb=self.verb)
					if dispType == "Vegetation, Snow, Smoke, Dust and Fog (Day)":
						data = col.vssdfD(eFile)
					elif dispType == "Clouds, Convection, Snow, Fog and Fires (Day)":
						data =  col.ccsfD(eFile)
					elif dispType == "Snow and Fog (Day)":
						data =  col.sfD(eFile)
					elif dispType == "Severe Convection (Day)":
						data =  col.scD(eFile)
					elif dispType == "Clouds, Fog and Contrails (Night)":
						data =  col.cfcN(eFile)
					elif dispType == "Dust, Thin Clouds and Contrails (Day & Night)":
						data =  col.dtccDN(eFile)
					elif dispType == "Severe Cyclones, Jets and PV Analysis (Day & Night)":
						data =  col.scjPVaDN(fle)
					col.imgCreate(data, "%s/cam%s.png" %(tempfile.gettempdir(), it))
					
			self.count = it
			self.timer.start(300, self)
		else:
			self.timer.stop()
			self.ui.pushButton_6.setText("Animate")
			self.it = 0
			self.count = 1
			self.ui.comboBox.setEnabled(True)


	def testConnection(self):
		ip = str(self.ui.lineEdit.text())
		user = str(self.ui.lineEdit_2.text())
		passwd = str(self.ui.lineEdit_3.text())
		remPath = str(self.ui.lineEdit_4.text())
		
		if self.ftp(ip, user, passwd, remPath) == True:
			GUI.inf(self, "ftp: Connection confirmed.")
		elif self.ftp(ip, user, passwd, remPath) == False:
			GUI.err(self, "Connection Failed.\nCheck the server, user name and password or your connection")
		elif self.ftp(ip, user, passwd, remPath) == None:
			GUI.err(self, "Check remote directory")
	
	def remFromList(self, listDev):
		GUI.takeFromList(self, listDev)

	def printIf(self, text):
		if self.verb:
			print text
	
	def pathName(self, path):
		fileName = os.path.basename(path)
		pathName = path.replace(fileName, "")
		return pathName, fileName

	def isH5(self, inFile):
		mc = camiryo.myCol
		h = mc.h5(verb=self.verb)
		if not h.openHDF5(inFile, "r") == False:
			return True
		else:
			return False

	def listFiles(self, path):
		fl = []
		for path, subdirs, files in os.walk(path):
			for name in files:
				fl.append(os.path.join(path, name))
				
		return fl

	def loadSetting(self):
		self.printIf("loadSetting: loadSetting started...")
		try:
			if os.path.isfile(".set"):
				GUI.takeAllFromList(self, self.ui.listWidget)
				GUI.takeAllFromList(self, self.ui.listWidget_2)
				f = open(".set", "r")
				for i in f:
					ln = i.replace("\n","")
					if ln.startswith("aa"):
						aa = ln.split("=")[1]
						isaa, inaa = aa.split("|")
						self.ui.spinBox.setValue(int(inaa))
						if isaa == "True":
							self.ui.groupBox_3.setChecked(True)
						else:
							self.ui.groupBox_3.setChecked(False)
					elif ln.startswith("lp"):
						self.printIf("loadSetting: Local Path detected...")
						lp = ln.split("=")[1]
						GUI.add2List(self, lp, self.ui.listWidget)
					elif ln.startswith("rp"):
						self.printIf("loadSetting: Remote Path detected...")
						rp = ln.split("=")[1]
						GUI.add2List(self, rp, self.ui.listWidget_2)	
					else:
						self.printIf("loadSetting: Unknown line in setting file. Skipping...")
		except:
			self.printIf("loadSetting: Something went wrong...")		
			
	def updateSetting(self):
		self.printIf("updateSetting: updateSetting started...")
		try:
			f = open("./.set", "w")
			if self.ui.groupBox_3.isChecked():
				aa = True
			else:
				aa = False
			
			interv = self.ui.spinBox.value()
			
			f.write("aa=%s|%s\n" %(aa, interv))
				
			for i in GUI.returnAllList(self, self.ui.listWidget_2):
				f.write("rp=%s\n" %(i))
			
			for i in GUI.returnAllList(self, self.ui.listWidget):
				f.write("lp=%s\n" %(i))
			
			self.printIf("updateSetting: updateSetting successfully done...")
			f.close()
		except:
			self.printIf("updateSetting: someting went wrong...")

	def addRemotePath(self):
		self.printIf("addRemotePath: addRemotePath started...")
		
		ip = str(self.ui.lineEdit.text())
		user = str(self.ui.lineEdit_2.text())
		passwd = str(self.ui.lineEdit_3.text())
		remPath = str(self.ui.lineEdit_4.text())		


		if self.ftp(ip, user, passwd, remPath) == True:
			server = str(self.ui.lineEdit.text())
			user = str(self.ui.lineEdit_2.text())
			passwd = str(self.ui.lineEdit_3.text())
			remPath = str(self.ui.lineEdit_4.text())
			if self.ui.checkBox_2.checkState() == QtCore.Qt.Checked:
				res = True
			else:
				res = False
			
			remotePath = "%s|%s@%s|%s|%s" %(user, passwd, server, remPath, res)
			GUI.add2List(self, remotePath, self.ui.listWidget_2)
			self.printIf("ftp: Connection confirmed.")
			self.printIf("addRemotePath: addRemotePath successfully done...")
		elif self.ftp(ip, user, passwd, remPath) == False:
			GUI.err(self, "Connection Failed.\nCheck the server, user name and password or your connection")
			self.printIf("addRemotePath: someting went wrong...")
		elif self.ftp(ip, user, passwd, remPath) == None:
			GUI.err(self, "Check remote directory")
		
	def getDataOverFTP(self, ip, usr, passwd, rFile, lPath):
		server = str(ip)
		user = str(usr)
		passwd = str(passwd)
		remPath = str(rFile)
		ftp = FTP(server)
		ftp.login(user, passwd)
		filePath, fileName  = self.pathName(remPath)
		ftp.cwd(filePath)
		print "get data"
		ftp.retrbinary("RETR " + fileName ,open("%s/%s" %(lPath, fileName), 'wb').write)
		
		
		
	def ftp(self, ip, usr, passwd, rDir):
		self.printIf("ftp: Check remote connection started...")
		server = str(ip)
		user = str(usr)
		passwd = str(passwd)
		remPath = str(rDir)
		
		try:
			ftp = FTP(server)
			ftp.login(user, passwd)
			con = True
		except:
			con = False
		if con:
			try:
				ftp.cwd(remPath)
				remp = True
			except:
				remp = False
				return None
				ftp.quit()
		
		if con and remp:
			ftp.quit()
			return True
		else:
			return False
			
	def addLocalPath(self):
		self.printIf("Add local path started...")
		try:
			odir = GUI.dirSelect(self)
			if not odir == "":
				if self.ui.checkBox.checkState() == QtCore.Qt.Checked:
					res = True
				else:
					res = False
					
				localPath = "%s|%s" %(odir, res)
				GUI.add2List(self, localPath, self.ui.listWidget)
				self.printIf("addLocalPath: addLocalPath successfully done...")
			else:
				self.printIf("addLocalPath: path selection canceled...")
		except:
			self.printIf("addLocalPath: someting went wrong...")

	def getLists(self):
		it = -1
		self.lst = []
		for i in GUI.returnAllList(self, self.ui.listWidget):
			it = it + 1
			self.tab = QtGui.QWidget()
			self.tab.setObjectName(("tab%s") %(it))
			lDirPath, isRes = i.split("|")
			lPath, lDir = self.pathName(lDirPath)
			self.ui.tabWidget_2.addTab(self.tab, ("%s" %(lDir)))
			self.gridLayout = QtGui.QGridLayout(self.tab)
			self.lst.append(QtGui.QListWidget(self.tab))
			self.lst[it].setObjectName(("listWidget%s" %(it)))
			self.gridLayout.setObjectName("gridLayout")
			self.gridLayout.addWidget(self.lst[it], 0, 0, 1, 1)
			if isRes == "False":
				lFiles = glob.glob("%s/*.h5" %(lDirPath))
				for u in lFiles:
					if self.isH5(u):
						GUI.add2List(self, u, self.lst[it])
			elif isRes == "True":
				for u in self.listFiles(lDirPath):
					if self.isH5(u):
						GUI.add2List(self, u, self.lst[it])
			self.lst[it].sortItems(1)
		
		for k in GUI.returnAllList(self, self.ui.listWidget_2):
			user, passwd = k.split("@")[0].split("|")
			ip, rDirPath, isRes = k.split("@")[1].split("|")
			if self.ftp(ip, user, passwd, rDirPath) == True:
				it = it + 1
				self.tab = QtGui.QWidget()
				self.tab.setObjectName(("tab%s") %(it))
				rPath, rDir = self.pathName(rDirPath)
				self.ui.tabWidget_2.addTab(self.tab, ("FTP(%s)" %(rDir)))
				self.gridLayout = QtGui.QGridLayout(self.tab)
				self.lst.append(QtGui.QListWidget(self.tab))
				self.lst[it].setObjectName(("listWidget%s" %(it)))
				self.gridLayout.setObjectName("gridLayout")
				self.gridLayout.addWidget(self.lst[it], 0, 0, 1, 1)
				ftp = FTP(ip)
				ftp.login(user, passwd)
				self.lst[it].sortItems(1)
				
				ftp.cwd(rDirPath)
				data = []
				dire = []
				files = []
				ftp.dir(data.append)
				
				for i in data:
					if i.startswith("-"):
						files.append(i.split()[len(i.split())-1])
					if i.startswith("d"):
						dire.append(i.split()[len(i.split())-1])
				
				if isRes == "False":
					for u in files:
						if u.endswith("h5"):
							ln = "%s|%s@%s|%s/%s" %(user, passwd, ip, rDirPath, u)
							GUI.add2List(self, ln, self.lst[it])
				elif isRes == "True":
					for u in files:
						if u.endswith("h5"):
							ln = "%s|%s@%s|%s/%s" %(user, passwd, ip, rDirPath, u)
							GUI.add2List(self, ln, self.lst[it])
					
					for u in dire:
						subData = []
						ftp.cwd("%s/%s" %(rDirPath, u))
						ftp.dir(subData.append)
						for l in subData:
							if l.endswith("h5"):
								ll = l.split()[len(l.split())-1]
								ln = "%s|%s@%s|%s/%s/%s" %(user, passwd, ip, rDirPath, u, ll)
								GUI.add2List(self, ln, self.lst[it])
							
			
			
			elif self.ftp(ip, user, passwd, remPath) == False:
				self.printIf("Connection Failed.\nCheck the server, user name and password or your connection")
			elif self.ftp(ip, user, passwd, remPath) == None:
				self.printIf("Check remote directory")
		
		for i in self.lst:
			self.addDisplay(i)
			i.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		if self.ui.tabWidget_2.count() > 0:
			self.ui.pushButton_6.setEnabled(True)
		else:
			self.ui.pushButton_6.setEnabled(False)

	def addDisplay(self, listDev):
		listDev.clicked.connect(lambda: self.display(listDev))
		
	def display(self, listDev):
		dispType = self.ui.comboBox.currentText()
		fle = listDev.currentItem()
		fle = fle.text()
		
		if fle.contains("@"):
			user, passwd = str(fle).split("@")[0].split("|")
			server, rFile = str(fle).split("@")[1].split("|")
			print rFile
			tmpFile = self.pathName(rFile)[1]
			
			self.getDataOverFTP(server, user, passwd, rFile, str(tempfile.gettempdir()))
			
			eFile = "%s/%s" %(str(tempfile.gettempdir()), tmpFile)
			
			mc = camiryo.myCol
			col = mc.coloring(verb=self.verb)
			if dispType == "Vegetation, Snow, Smoke, Dust and Fog (Day)":
				data = col.vssdfD(eFile)
			elif dispType == "Clouds, Convection, Snow, Fog and Fires (Day)":
				data =  col.ccsfD(eFile)
			elif dispType == "Snow and Fog (Day)":
				data =  col.sfD(eFile)
			elif dispType == "Severe Convection (Day)":
				data =  col.scD(eFile)
			elif dispType == "Clouds, Fog and Contrails (Night)":
				data =  col.cfcN(eFile)
			elif dispType == "Dust, Thin Clouds and Contrails (Day & Night)":
				data =  col.dtccDN(eFile)
			elif dispType == "Severe Cyclones, Jets and PV Analysis (Day & Night)":
				data =  col.scjPVaDN(fle)
			col.imgCreate(data, "%s/cam.png" %(tempfile.gettempdir()))
			self.showme()
			
			if os.path.isfile(eFile):
				os.remove(eFile)
			if os.path.isfile("%s/cam.png" %(tempfile.gettempdir())):
				os.remove("%s/cam.png" %(tempfile.gettempdir()))

			
		else:
			eFile = fle
			
			mc = camiryo.myCol
			col = mc.coloring(verb=self.verb)
			if dispType == "Vegetation, Snow, Smoke, Dust and Fog (Day)":
				data = col.vssdfD(eFile)
			elif dispType == "Clouds, Convection, Snow, Fog and Fires (Day)":
				data =  col.ccsfD(eFile)
			elif dispType == "Snow and Fog (Day)":
				data =  col.sfD(eFile)
			elif dispType == "Severe Convection (Day)":
				data =  col.scD(eFile)
			elif dispType == "Clouds, Fog and Contrails (Night)":
				data =  col.cfcN(eFile)
			elif dispType == "Dust, Thin Clouds and Contrails (Day & Night)":
				data =  col.dtccDN(eFile)
			elif dispType == "Severe Cyclones, Jets and PV Analysis (Day & Night)":
				data =  col.scjPVaDN(fle)
			col.imgCreate(data, "%s/cam.png" %(tempfile.gettempdir()))
			self.showme()
			os.remove("%s/cam.png" %(tempfile.gettempdir()))
				
	def showme(self):
		diss = "%s/cam.png" %(tempfile.gettempdir())
		if os.path.isfile(str(diss)):
			scene = QtGui.QGraphicsScene()
			scene.addPixmap(QtGui.QPixmap(diss))
			self.ui.graphicsView.setScene(scene)
			
	def showmeani(self, i):
		diss = "%s/cam%s.png" %(tempfile.gettempdir(), i)
		if os.path.isfile(str(diss)):
			scene = QtGui.QGraphicsScene()
			scene.addPixmap(QtGui.QPixmap(diss))
			self.ui.graphicsView.setScene(scene)

	def ZoomAMS(self, ev):
		if ev.delta() < 0:
			  self.ui.graphicsView.scale(0.9, 0.9)
		else:
			  self.ui.graphicsView.scale(1.1, 1.1)

app = QtGui.QApplication(sys.argv)
if len(sys.argv) >= 2:
	if "True".startswith(sys.argv[1].upper()):
		print "Verbose mode activated"
		ver = True
	else:
		print "Verbose mode deactivated"
		ver = False
else:
	print "Verbose mode deactivated"
	ver = False
f = MyForm(verb=ver)
f.show()

app.exec_()
