import camiryo

col = camiryo.myCol

color = col.coloring(verb=True)
im = color.scD("20140103/MSG_Turkiye_201401031345.h5")
color.imgCreate(im, "my.png")

