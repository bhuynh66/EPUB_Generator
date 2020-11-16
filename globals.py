
""" 
    This file just contains global variables to make the main file a little 
    cleaner.
    
"""


container = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>""" 


sgcToc = """div.sgc-toc-title {
    font-size: 2em;
    font-weight: bold;
    margin-bottom: 1em;
    text-align: center;
}

div.sgc-toc-level-1 {
    margin-left: 0em;
}

div.sgc-toc-level-2 {
    margin-left: 2em;
}

div.sgc-toc-level-3 {
    margin-left: 2em;
}

div.sgc-toc-level-4 {
    margin-left: 2em;
}

div.sgc-toc-level-5 {
    margin-left: 2em;
}

div.sgc-toc-level-6 {
    margin-left: 2em;
}"""


htmlHeader = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title></title>
</head>"""

htmlEndHeader = """<!--EndFragment-->
</body>
</html>"""


htmlStart = """<body>
  <h2><strong>"""

htmlEnd = """</strong></h2>
  <div>
    <strong><br /></strong>
  </div><!--StartFragment--><p>"""

opfManifestStart = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:8e5377c9-0095-4442-9a99-d6e4ade7e988</dc:identifier>
    <dc:language>en</dc:language>
    <dc:date opf:event="modification">0000-00-00</dc:date>
    <meta content="0.7.4" name="Sigil version" />
  </metadata>
  <manifest>
    <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml" />\n"""


tocStart = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta content="urn:uuid:8e5377c9-0095-4442-9a99-d6e4ade7e988" name="dtb:uid"/>
    <meta content="3" name="dtb:depth"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>\n"""
