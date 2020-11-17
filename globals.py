
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
    <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:e35708b9-d06f-4796-bf03-0690b2443825</dc:identifier>
    <dc:language>en</dc:language>
    <dc:date opf:event="modification">0000-00-00</dc:date>
    <meta content="0.7.4" name="Sigil version" />
  </metadata>
  <manifest>
    <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml" />\n"""


tocStart = """<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="eng">
  <head>
    <meta name="dtb:uid" content="e35708b9-d06f-4796-bf03-0690b2443825"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:generator" content="calibre (5.4.2)"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>\n"""
