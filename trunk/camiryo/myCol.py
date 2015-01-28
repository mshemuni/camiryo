# -*- coding: utf-8 -*-
"""
myCol Module.
For further information:

        From camiryo import myCol
        help(myCol)
"""

import h5py
import numpy
import os
import Image

__all__ = ["coloring", "env", "h5", "stat"]
class env():
	"""
	Environment class of myCol.
	This class contains Environmental functions.
	"""
	__all__ = ["getCh", "isFile", "printIf"]
	def __init__(self, verb=False):
		"""
		__init__(self, verb=False) -> None
		Initial class. Welcome the user.

		@param verb: Get information while operation (Optional, False by default).
		@type verb: boolean
		@return: None
		"""
		if verb:
			print "env.__init__: Environment Class imported..."
		self.verb = verb
		
	def printIf(self, text):
		"""
		printIf(self, text) -> None
		Prints if verbose is True.

		@param text: Text to print.
		@type text: String
		@return: None
		"""
		if self.verb:
			print text
		
	def isFile(self, fileName):
		"""
		isFile(self, fileName) -> Boolean
		Returns True if file exist or False if file doesn't exist.

		@param fileName: File to check.
		@type fileName: String
		@return: Boolean
		"""
		self.printIf("env.isFile: isFile started...")
		try:
			if os.path.isfile(fileName):
				self.printIf("env.isFile: File does exist...")
			else:
				self.printIf("env.isFile: File Does not exist...")
			
			self.printIf("env.isFile: isFile successfully done...")
			return os.path.isfile(fileName)
		except:
			self.printIf("env.isFile: Something bad happened...")
		
	def getCH(self, number):
		"""
		getCH(self, number) -> String
		Returns channel name of given order.

		@param number: Order of wanted channel.
		@type number: String
		@return: String
		"""
		self.printIf("env.getCH: getCH started")
		try:
			chList = {"1": "Ch1(VIS06)","2": "Ch2(VIS08)","3": "Ch3(VIS16)","4r": "Ch4(IR39)","4": "Ch4(VIS39)","5": "Ch5(WV62)","6": "Ch6(WV73)","7": "Ch7(IR87)","8": "Ch8(IR97)","9": "Ch9(IR108)","10": "Ch10(IR120)","11": "Ch11(IR134)","12": "Ch12(VISHRV)","Sinfo": "Slot_Info","Tinfo": "TMet_Info"}

			self.printIf("env.getCH: getCH successfully done...")
			return chList[number]
		except:
			self.printIf("env.getCH: Something bad happened...")
			return False

class h5():
	"""
	h5 class of myCol.
	This class contains HDF5 operation functions.
	"""
	__all__ = ["getData", "openHDF5", "printIf", "printIf"]
	def __init__(self, verb=False):
		"""
		__init__(self, verb=False) -> None
		Initial class. Welcome the user.

		@param verb: Get information while operation (Optional, False by default).
		@type verb: boolean
		@return: None
		"""
		if verb:
			print "h5.__init__: HDF5 Class imported..."
		self.verb = verb
		self.env = env()
		
	def printIf(self, text):
		"""
		printIf(self, text) -> None
		Prints if verbose is True.

		@param text: Text to print.
		@type text: String
		@return: None
		"""
		if self.verb:
			print text
	
	def openHDF5(self, fileName, mode):
		"""
		openHDF5(self, fileName) -> h5py._hl.files.File
		Returns HDF5 file.

		@param fileName: File to open.
		@type fileName: String
		@param mode: Open mode. (r)ead, (w)rite, etc
		@type mode: String
		@return: h5py._hl.files.File
		"""
		self.printIf("h5.openHDF5: openHDF5 started...")
		try:
			if self.env.isFile(fileName):
				f = h5py.File(str(fileName), mode)
				self.printIf("h5.openHDF5: openHDF5 successfully done...")
				return f
			else:
				return False
		except:
			self.printIf("h5.openHDF5: openHDF5 Can not open the file %s ..." %(fileName))
			return False

	def getData(self, inFile, ch):
		"""
		getData(self, inFile, ch) -> ndarray
		Returns HDF5 file.

		@param inFile: File to open.
		@type inFile: String
		@param ch: Channel to optain data from.
		@type ch: String
		@return: ndarray
		"""
		self.printIf("h5.getData: getData started...")
		try:
			fl = self.openHDF5(inFile, "r")
			if not fl == False:
				c = self.env.getCH(ch)
				self.printIf("h5.getData: getData successfully done...")
				return fl[c][...]
			else:
				return False
				
		except:
			self.printIf("h5.getData: Something bad happened...")
			return False

class coloring():
	"""
	Coloring class of myCol.
	This Class Contains functions for obtaining and creating colored images.
	"""
	__all__ = ["ccsfD", "cfcN", "dtccDN", "printIf", "scD", "scjPVaDN", "sfD", "vssdfD"]
	def __init__(self, verb=False):
		"""
		__init__(self, verb=False) -> None
		Coloring class. Welcome the user.

		@param verb: Get information while operation (Optional, False by default).
		@type verb: boolean
		@return: None
		"""
		if verb:
			print "coloring.__init__: Coloring Class imported..."
		self.verb = verb
		self.env = env()
		self.h5 = h5()
		self.stat = stat()
		
	def printIf(self, text):
		"""
		printIf(self, text) -> None
		Prints if verbose is True.

		@param text: Text to print.
		@type text: String
		@return: None
		"""
		if self.verb:
			print text

	def vssdfD(self, inFile):
		"""
		vssdfD(self, inFile) -> numpy.ndarray
		Returns a (3, [image size]) shaped array for Vegetation, Snow, Smoke, Dust and Fog (Day)

		@param inFile: File to open.
		@type inFile: String
		@return: numpy.ndarray
		"""
		self.printIf("coloring.vssdfD: vssdfD started...")
		try:
			R = self.h5.getData(inFile, "3")
			RR = self.stat.normalizeArray(R)
			G = self.h5.getData(inFile, "2")
			GG = self.stat.normalizeArray(G)
			B = self.h5.getData(inFile, "1")
			BB = self.stat.normalizeArray(B)
			if type(R) == numpy.ndarray and type(G) == numpy.ndarray and type(B) == numpy.ndarray:
				img = numpy.asarray([RR, GG, BB])
				self.printIf("coloring.vssdfD: vssdfD successfully done...")
				return img
			else:
				return False
		except:
			self.printIf("coloring.vssdfD: Something bad happened...")
			return False
		
	def ccsfD(self, inFile):
		"""
		ccsfD(self, inFile) -> numpy.ndarray
		Returns a (3, [image size]) shaped array for Clouds, Convection, Snow, Fog and Fires (Day)

		@param inFile: File to open.
		@type inFile: String
		@return: numpy.ndarray
		"""
		self.printIf("coloring.ccsfD: ccsfD started...")
		try:
			R = self.h5.getData(inFile, "2")
			RR = self.stat.normalizeArray(R)
			G = self.h5.getData(inFile, "4r")
			GG = self.stat.normalizeArray(G)
			B = self.h5.getData(inFile, "9")
			BB = self.stat.normalizeArray(B)
			if type(R) == numpy.ndarray and type(G) == numpy.ndarray and type(B) == numpy.ndarray:
				img = numpy.asarray([RR, GG, BB])
				self.printIf("coloring.ccsfD: ccsfD successfully done...")
				return img
			else:
				return False
		except:
			self.printIf("coloring.ccsfD: Something bad happened...")
			return False

	def sfD(self, inFile):
		"""
		sfD(self, inFile) -> numpy.ndarray
		Returns a (3, [image size]) shaped array for Snow and Fog (Day)

		@param inFile: File to open.
		@type inFile: String
		@return: numpy.ndarray
		"""
		self.printIf("coloring.sfD: sfD started...")
		try:
			R = self.h5.getData(inFile, "2")
			RR = self.stat.normalizeArray(R)
			G = self.h5.getData(inFile, "3")
			GG = self.stat.normalizeArray(G)
			B = self.h5.getData(inFile, "4r")
			BB = self.stat.normalizeArray(B)
			if type(R) == numpy.ndarray and type(G) == numpy.ndarray and type(B) == numpy.ndarray:
				img = numpy.asarray([RR, GG, BB])
				self.printIf("coloring.sfD: sfD successfully done...")
				return img
			else:
				return False
		except:
			self.printIf("coloring.sfD: Something bad happened...")
			return False

	def scD(self, inFile):
		"""
		scD(self, inFile) -> numpy.ndarray
		Returns a (3, [image size]) shaped array for Severe Convection (Day)

		@param inFile: File to open.
		@type inFile: String
		@return: numpy.ndarray
		"""
		self.printIf("coloring.scD: scD started...")
		try:
			R1 = self.h5.getData(inFile, "5")
			R2 = self.h5.getData(inFile, "6")
			R = self.stat.subs(R1, R2)
			RR = self.stat.normalizeArray(R)
			G1 = self.h5.getData(inFile, "4")
			G2 = self.h5.getData(inFile, "9")
			G = self.stat.subs(G1, G2)
			GG = self.stat.normalizeArray(G)
			B1 = self.h5.getData(inFile, "3")
			B2 = self.h5.getData(inFile, "1")
			B = self.stat.subs(B1, B2)
			BB = self.stat.normalizeArray(B)
			if type(R) == numpy.ndarray and type(G) == numpy.ndarray and type(B) == numpy.ndarray:
				img = numpy.asarray([RR, GG, BB])
				self.printIf("coloring.scD: scD successfully done...")
				return img
			else:
				return False
		except:
			self.printIf("coloring.scD: Something bad happened...")
			return False

	def cfcN(self, inFile):
		"""
		cfcN(self, inFile) -> numpy.ndarray
		Returns a (3, [image size]) shaped array for Clouds, Fog and Contrails (Night)

		@param inFile: File to open.
		@type inFile: String
		@return: numpy.ndarray
		"""
		self.printIf("coloring.cfcN: cfcN started...")
		try:
			R1 = self.h5.getData(inFile, "10")
			R2 = self.h5.getData(inFile, "9")
			R = self.stat.subs(R1, R2)
			RR = self.stat.normalizeArray(R)
			G1 = self.h5.getData(inFile, "9")
			G2 = self.h5.getData(inFile, "4")
			G = self.stat.subs(G1, G2)
			GG = self.stat.normalizeArray(G)
			B = self.h5.getData(inFile, "9")
			BB = self.stat.normalizeArray(B)
			if type(R) == numpy.ndarray and type(G) == numpy.ndarray and type(B) == numpy.ndarray:
				img = numpy.asarray([RR, GG, BB])
				self.printIf("coloring.cfcN: cfcN successfully done...")
				return img
			else:
				return False
		except:
			self.printIf("coloring.cfcN: Something bad happened...")
			return False

	def dtccDN(self, inFile):
		"""
		dtccDN(self, inFile) -> numpy.ndarray
		Returns a (3, [image size]) shaped array for Dust, Thin Clouds and Contrails (Day and Night)

		@param inFile: File to open.
		@type inFile: String
		@return: numpy.ndarray
		"""
		self.printIf("coloring.dtccDN: dtccDN started...")
		try:
			R1 = self.h5.getData(inFile, "10")
			R2 = self.h5.getData(inFile, "9")
			R = self.stat.subs(R1, R2)
			RR = self.stat.normalizeArray(R)
			G1 = self.h5.getData(inFile, "9")
			G2 = self.h5.getData(inFile, "7")
			G = self.stat.subs(G1, G2)
			GG = self.stat.normalizeArray(G)
			B = self.h5.getData(inFile, "9")
			BB = self.stat.normalizeArray(B)
			if type(R) == numpy.ndarray and type(G) == numpy.ndarray and type(B) == numpy.ndarray:
				img = numpy.asarray([RR, GG, BB])
				self.printIf("coloring.dtccDN: dtccDN successfully done...")
				return img
			else:
				return False
		except:
			self.printIf("coloring.dtccDN: Something bad happened...")
			return False

	def scjPVaDN(self, inFile):
		"""
		scjPVaDN(self, inFile) -> numpy.ndarray
		Returns a (3, [image size]) shaped array for Severe Cyclones, Jets and PV Analysis, (Day and Night)

		@param inFile: File to open.
		@type inFile: String
		@return: numpy.ndarray
		"""
		self.printIf("coloring.scjPVaDN: scjPVaDN started...")
		try:
			R1 = self.h5.getData(inFile, "5")
			R2 = self.h5.getData(inFile, "6")
			R = self.stat.subs(R1, R2)
			RR = self.stat.normalizeArray(R)
			G1 = self.h5.getData(inFile, "8")
			G2 = self.h5.getData(inFile, "9")
			G = self.stat.subs(G1, G2)
			GG = self.stat.normalizeArray(G)
			B = self.h5.getData(inFile, "5")
			BB = self.stat.normalizeArray(B)
			if type(R) == numpy.ndarray and type(G) == numpy.ndarray and type(B) == numpy.ndarray:
				img = numpy.asarray([RR, GG, BB])
				self.printIf("coloring.scjPVaDN: scjPVaDN successfully done...")
				return img
			else:
				return False
		except:
			self.printIf("coloring.scjPVaDN: Something bad happened...")
			return False

	def imgCreate(self, inArray, oFile):
		"""
		imgCreate(self, inArray, oFile) -> None
		Creates an image for given matrix

		@param inArray: Input array to use for creating Image.
		@type inArray: ndarray
		@param oFile: Output file path to save Image.
		@type oFile: string
		@return: None
		"""
		self.printIf("coloring.imgCreate: imgCreate started...")
		try:
			if len(numpy.shape(inArray)) == 3:
				imRGB = Image.fromarray(numpy.dstack((inArray[0], inArray[1], inArray[2])))
				imRGB.save(oFile)
				self.printIf("coloring.imgCreate: imgCreate successfully done...")
			elif len(numpy.shape(inArray)) == 2:
				imRGB = Image.fromarray(inArray)
				imRGB.save(oFile)
				self.printIf("coloring.imgCreate: imgCreate successfully done...")
			else:
				self.printIf("coloring.imgCreate: Something bad happened...")
				return False
		except:
			self.printIf("coloring.imgCreate: Something bad happened...")
			return False

			

class stat():
	"""
	stat class of myCol.
	This class contains Statistical functions.
	"""
	__all__ = ["normalizeArray", "printIf", "subs"]
	def __init__(self, verb=False):
		"""
		__init__(self, verb=False) -> None
		Initial class. Welcome the user.

		@param verb: Get information while operation (Optional, False by default).
		@type verb: boolean
		@return: None
		"""
		if verb:
			print "stat.__init__: Statistical Class imported..."
		self.verb = verb
		self.env = env()
		
	def printIf(self, text):
		"""
		printIf(self, text) -> None
		Prints if verbose is True.

		@param text: Text to print.
		@type text: String
		@return: None
		"""
		if self.verb:
			print text

	def subs(self, arr1, arr2):
		self.printIf("stat.subs: subs started...")
		try:
			sub = numpy.subtract(arr1, arr2)
			self.printIf("stat.subs: subs successfully done...")
			return sub
		except:
			self.printIf("stat.subs: Something bad happened...")
			return False

	def normalizeArray(self, inArray):
		"""
		normalizeArray(self, inArray) -> numpy.ndarray
		Returns HDF5 file.

		@param inArray: Array to normalize.
		@type inArray: numpy.ndarray
		@return: numpy.ndarray
		"""
		self.printIf("stat.normalizeArray: normalizeArray started...")
		try:
			if type(inArray) == numpy.ndarray:
				arrMin = numpy.amin(inArray)
				arrMax = numpy.amax(inArray)
				c = float(255) / float(arrMax - arrMin)
				s = (float(c)*inArray-arrMin).astype(numpy.uint8)
				self.printIf("stat.normalizeArray: normalizeArray successfully done...")
				return s
			else:
				self.printIf("stat.normalizeArray: Wrong array type...\n\tExpected numpy.ndarray, give %s" %(type(inArray)))
		except:
			self.printIf("stat.normalizeArray: Something bad happened...")
			return False
