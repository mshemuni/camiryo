#!/usr/bin/env python
import numpy, Image, h5py, sys, os
from PyQt4 import QtGui, QtCore

#Returns Channel's Name.
def getCH(STRnumber):
	ll=open('./chTable', 'r')
	for line in ll:
		ch,cn=line.split("	")
		cn=cn.replace("\n","")
		if cn == str(STRnumber):
			channel=ch
	return channel
	
def scale(array, lower, upper):
	low = numpy.where(array[...]>lower, array[...], lower)
	final = numpy.where(low[...]<upper, low[...], upper)	
	return final
#Returns An Array from H5 file ready for use as RGB image layer.
def getArray(FileName, Layer, isScale, lowerLimit, upperLimit, gamma):
	f = h5py.File(str(FileName), 'r')
	dset = f[str(getCH(str(Layer)))]
	if isScale:
		sArray = scale(dset[...], lowerLimit, upperLimit)
	else:
		sArray = dset[...]
		
	sArrayMin = numpy.amin(sArray[...])
	sArrayMax = numpy.amax(sArray[...])
	s = 255*(sArray[...]*1.0 - sArrayMin*1.0)/(sArrayMax*1.0 - sArrayMin*1.0)**(1/gamma)
	return s.astype( numpy.uint8)
		
#Returns Two Arrays and prepair them for use as RGB image layer.
def getArrayDiff(FileName, Layer, Layer2, isScale, lowerLimit, upperLimit, gamma):
	f = h5py.File(str(FileName), 'r')
	dset1 = f[str(getCH(str(Layer)))]
	dset2 = f[str(getCH(str(Layer2)))]
	dset = numpy.subtract(dset1, dset2)
	if isScale:
		sArray = scale(dset[...], lowerLimit, upperLimit)
	else:
		sArray = dset[...]
		
	sArrayMin = numpy.amin(sArray[...])
	sArrayMax = numpy.amax(sArray[...])
	s = 255*(sArray[...]*1.0 - sArrayMin*1.0)/(sArrayMax*1.0 - sArrayMin*1.0)**(1/gamma)
	return s.astype( numpy.uint8)
		
#Mod1: Vegetation, Snow, Smoke, Dust, Fog, Day
def vssdfD(FileName):
	R = getArray(FileName,"3", False, 20, 40, 1)
	G = getArray(FileName,"2", False, 20, 30, 1)
	B = getArray(FileName,"1", False, 10, 20, 1)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")

#Mod2S: Cloud Analysis, Convection, Fog, Snow, Fires Summer
def ccffsS(FileName):
	R = getArray(FileName,"2", False, 20, 40, 1)
	G = getArray(FileName,"4r", True, 0, 60, 2.5)
	B = getArray(FileName,"9", True, 203, 323, 1)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")
#Mod2W: Cloud Analysis, Convection, Fog, Snow, Fires Winter
def ccffsW(FileName):
	R = getArray(FileName,"2", False, 20, 40, 1)
	G = getArray(FileName,"4r", True, 0, 25, 1.5)
	B = getArray(FileName,"9", True, 203, 323, 1)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")

#Mod3: Severe Convective Storms
def scs(FileName):
	R = getArrayDiff(FileName,"5","6", True, -35, 5, 1)
	G = getArrayDiff(FileName,"4","9", True, -5, 60, 0.5)
	B = getArrayDiff(FileName,"3","1", True, -75, 25, 1)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")

#Mod4: Fog/Low Clouds, Snow
def flcs(FileName):
	R = getArray(FileName,"2", False, 20, 40, 1.7)
	G = getArray(FileName,"3", True, 0, 70, 1.7)
	B = getArray(FileName,"4r", True, 0, 30, 1.7)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")

#Mod5: Cloud Analysis, Fog, Contrails
def cafc(FileName):
	R = getArrayDiff(FileName,"10","9", True, -4, 2, 1)
	G = getArrayDiff(FileName,"9","4", True, 0, 10, 1)
	B = getArray(FileName,"9", True, 243, 293, 1)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")

#Mod6: Dust, Thin Clouds, Contrails
def dtcc(FileName):
	R = getArrayDiff(FileName,"10","9", True, -4, 2, 1)
	G = getArrayDiff(FileName,"9","7", True, 0, 15, 2.5)
	B = getArray(FileName,"9", True, 261, 289, 1)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")

#Mod7: Rapid Cyclogenesis, Jet Stream Analysis, PV Analysis
def rcjsapva(FileName):
	R = getArrayDiff(FileName,"5","6", True, -25, 0, 1)
	G = getArrayDiff(FileName,"8","9", True, -40, 5, 1)
	B = getArray(FileName,"5", True, 243, 208, 1)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")

#Mod8: 24-hour Ash Microphysics
def tham(FileName):
	R = getArrayDiff(FileName,"10","9", True, -4, 2, 1)
	G = getArrayDiff(FileName,"9","7", True, -4, 5, 1)
	B = getArray(FileName,"9", True, 243, 303, 1)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")
	
#Mod9: HRV Clouds
def hrvc(FileName):
	R = getArray(FileName,"12", False, 0, 100, 1.7)
	G = getArray(FileName,"12", False, 0, 100, 1.7)
	B = getArray(FileName,"9", True, 203, 323, 1)
	imRGB = Image.fromarray(numpy.dstack((R[:,:], G[:,:], B[:,:])))
	imRGB.save("tmp/disp.png")
	
def createImage(Name, fil):
	fil=fil.text()
	if Name == "Day Natural Colours":
	  vssdfD(str(fil))
	elif Name == "Day Microphysical (Summer)":
	  ccffsS(str(fil))
	elif Name == "Day Microphysical (Winter)":
	  ccffsW(str(fil))
	elif Name == "Convective Storms":
	  scs(str(fil))
	elif Name == "Day Solar":
	  flcs(str(fil))
	elif Name == "Night Microphysical":
	  cafc(str(fil))
	elif Name == "Dust":
	  dtcc(str(fil))
	elif Name == "Airmas	s":
	  rcjsapva(str(fil))
	elif Name == "24-hour Ash Microphysics":
	  tham(str(fil))
	elif Name == "HRV Clouds":
	  hrvc(str(fil))
	  
def createImage_ani(Name, fil):
	if Name == "Day Natural Colours":
	  vssdfD(str(fil))
	elif Name == "Day Microphysical (Summer)":
	  ccffsS(str(fil))
	elif Name == "Day Microphysical (Winter)":
	  ccffsW(str(fil))
	elif Name == "Convective Storms":
	  scs(str(fil))
	elif Name == "Day Solar":
	  flcs(str(fil))
	elif Name == "Night Microphysical":
	  cafc(str(fil))
	elif Name == "Dust":
	  dtcc(str(fil))
	elif Name == "Airmas	s":
	  rcjsapva(str(fil))
	elif Name == "24-hour Ash Microphysics":
	  tham(str(fil))
	elif Name == "HRV Clouds":
	  hrvc(str(fil))
#f = sys.argv[1]
