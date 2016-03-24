#!/home/izhleba/anaconda2/bin/python
# -*- coding:utf-8 -*-

import cgi
import os
import uuid
from datetime import datetime
from recognize_img import recognize
import shutil

UPLOAD_DIR = "/srv/image_analize/html/img"
UPLOAD_DIR_ORIG = "/srv/image_analize/html/img/orig"

HTML_TEMPLATE = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head><title>File Upload</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head><body><h1>File Upload</h1>
<form  method="POST" enctype="multipart/form-data">
File name: <input name="img_file" type="file"><br>
<input name="submit" type="submit">
</form>
</body>
</html>"""

print "Content-Type: text/html; charset=utf-8"
print ""


form = cgi.FieldStorage()
if 'img_file' in form:
    fileitem = form['img_file']
    if not fileitem.file: 
      print "Bad file!"
    else:
      fname = str(uuid.uuid4()) + fileitem.filename + ".png"
      fpath = os.path.join(UPLOAD_DIR, fname)
      fout = file (fpath, 'wb')
      while 1:
	chunk = fileitem.file.read(100000)
        if not chunk: break
        fout.write (chunk)
      fout.close()
      shutil.copy(fpath, UPLOAD_DIR_ORIG)
      recognize(str(fpath))
      print "/img/"+fname    
else:
    print HTML_TEMPLATE 

