from PyQt4 import QtGui, QtCore

def printIf(self, text):
	if self.verb:
		print text

def add2List(self, inLine, listDev):
	try:
		it = listDev.count()
		item = QtGui.QListWidgetItem()
		listDev.addItem(item)
		item = listDev.item(it)
		self.printIf("add2List: add2List successfully done...")
		item.setText(QtGui.QApplication.translate("Form", inLine, None, QtGui.QApplication.UnicodeUTF8))
	except:
		self.printIf("add2List: add2List went wrong...")
		return False

def dirSelect(self):
	try:
		fileName = QtGui.QFileDialog.getExistingDirectory( self, 'Select Local Data Path...')
		self.printIf("dirSelect: dirSelect successfully done...")
		return fileName
	except:
		self.printIf("dirSelect: takeFromList went wrong...")
		return False

def takeFromList(self, listDev):
	try:
		for x in listDev.selectedItems():
			listDev.takeItem(listDev.row(x))
		self.printIf("takeFromList: takeFromList successfully done...")
	except:
		self.printIf("takeFromList: takeFromList went wrong...")
		return False

def takeAllFromList(self, listDev):
	try:
		for x in xrange(listDev.count()):
			listDev.takeItem(listDev.row(0))
		self.printIf("takeFromList: takeFromList successfully done...")
	except:
		self.printIf("takeFromList: takeFromList went wrong...")
		return False

def err(self, text):
	QtGui.QMessageBox.critical( self,  ("Camiryo Error"), (text))

def inf(self, text):
	QtGui.QMessageBox.information( self,  ("Camiryo Error"), (text))

def returnAllList(self, listDev):
	items = []
	for x in xrange(listDev.count()):
		line = listDev.item(x)
		ln = line.text()
		items.append(ln)
	return map(str, items)
