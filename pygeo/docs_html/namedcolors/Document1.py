"""
 This is a simple command-line based, lightweight Python script to
 create an image album.

 Copyright 2004 Premshree Pillai. All rights reserved.
 <http://www.qiksearch.com/>

 The script takes the following five inputs:
 	1. Directory name: This is the directory from where the
 	   images are read from
  	2. Album title <optional>: This title will appear on
 	   each of the HTML files created
 	3. Thumbnail scaling factor: This is a value less than
 	   1.0 (e.g., 0.2., 0.3, etc). The size of the thumbnail
 	   images created will be the scaling factor times the
 	   original image size
 	4. Image scaling factor: This is again a value less than
 	   or equal to 1.0. Images created using this factor appear
 	   on the HTMLs of individual images
 	5. Option to Add EXIF information
 
 The script creates the following three directories within the
 image directory:
 	1. thumbnails
 	2. images
 	3. htmls
 
 The album can be viewed by running the index.htm file

 27-FEB-04 pyAlbum.py released.
 06-APR-04 Added thumbnail support.
 	   Added scaling for individual image pages.
 	   Now requires PIL (http://www.pythonware.com/products/pil)
 11-APR-04 Implemented pyAlbum as a class.
 	   Added optional EXIF support.
 	   Requires EXIF.py
	   (http://home.cfl.rr.com/genecash/digital_camera/EXIF.py)
"""

class pyAlbum:

	def __init__(self):
		self.count = 0
		self.dirName = "\\python24\\lib\site-packages\\pygeo\\docs_html\\namedcolors\\"
		
		self.title = "Named Colors"
		self.slideName = "htmls"
	
	
	def doFiles(self):
		self.files = []
		for x in os.listdir(self.dirName):
			os.chdir(self.dirName)
			try:
			   if x.split(".")[1] == "jpg": 
			      if(os.path.isfile(x)):
                	        	self.files.append(x)
			except IndexError: 
			    pass
	
	
	def createIndex(self):
		# Create the index file
		from pygeo.utils.colordict import colors_dict_lower
		self.indexFile = "index.html"
		
		os.chdir(self.dirName)
		fp = open(self.indexFile,"w")
		temp = """<html>
			<head>
				<title>%s</title>
				 <link rel="stylesheet" href="../stylesheets/pygeodoc.css" type="text/css" />

			</head>
			<body>
			<center><h2>%s</h2></center>
			<table id="colors" align="center"><tr>
			""" % (self.title, self.title)
		self.count = 0
		for x in self.files:
		#	image_size = Image.open(x).size
			
			print colors_dict_lower[x.split(".")[0].lower()]
			file_size = int(os.stat(x)[6]/1024)
			width = 60
			height = 60
			if self.count == 0 :
				temp = temp + "</tr><tr>"
			temp = temp + "<td valign=\"bottom\" align=\"center\" style=\"text-align:center\"><img src=\"" +  x + "\"><br>" + x.split(".")[0].upper() + "<br>" + colors_dict_lower[x.split(".")[0].lower()] + "<span style=\"color:gray\"></span> </td>" +"\n"
			self.count = self.count + 1
			if self.count == 6:
				self.count = 0
        	fp.write(temp)
		fp.close()

	
	def exit(self):
		# Done!
		print "\n", "Album created!"
		print "Press <enter> to exit..."
		if(raw_input()):
			exit

if __name__ == '__main__':

	import os
	album = pyAlbum()
	album.doFiles()
	album.createIndex()
	album.exit()