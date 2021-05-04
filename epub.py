import globalVar
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
import os
import shutil
from bs4 import BeautifulSoup
import requests
import urllib.request

class Book:

    def __init__(self,directory): 

        """
        Here we are making the current working directory
        here we assume that this is an entirely new project
        thus we will create all the require files.   

        """

        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        os.chdir(path)
        self.mimetype()
         
         
        #Traverse into META-INF folder 
        directory = "META-INF"
        path1 = os.path.join(path, directory)
        os.mkdir(path1)
        os.chdir(path1) 
        self.container()
        
        #Return back into the Home directory
        os.chdir(path) 
        
        directory = "OEBPS"
        path1 = os.path.join(path,directory)
        os.mkdir(path1)
        
        #initialize the subfolders
        self.oebps(path1) 
        
        return
 
 
    def container(self):

        container2 = open("container.xml", "w+")
        container2.write(globalVar.container)
        container2.close()
        
        return 


    def mimetype(self):

        mime = open("mimetype", "w+")
        mime.write("application/epub+zip")
        mime.close()
        
        return

        
    def sgctoc(self):

        sgc = open("sgc-toc.css", "w+")
        sgc.write(globalVar.sgcToc)
        sgc.close()
        
        return


    def oebps(self, path):

        directory = ["Images", "Styles" , "Text"]
        
        for name in directory:
            path1 = os.path.join(path, name)
            os.mkdir(path1)
        
            if name == "Styles":
                os.chdir(path1)
                self.sgctoc()
                
        return 
   

def writer(fileLocation , path, chapterNum):

    """ 
        function to write the html file.
        this function specifically take a filelocation, the homedirectory and chapternumber
    
    """
    #given a file path we get the file name 
    baseFileName = os.path.basename(fileLocation) 
    
    # get name of file
    fileLocationName = os.path.splitext(baseFileName)[0] 
    
    os.chdir(path)
    
    newFileName  = str(chapterNum)+"."+fileLocationName +".html" 
    chapter = open(newFileName, "w+", encoding="utf-8")
    title = "Chapter" + " " + str(chapterNum)+": "+fileLocationName 
    
    startOfHtml = globalVar.htmlStart + title + globalVar.htmlEnd
        
    chapter.write(globalVar.htmlHeader)
    chapter.write(startOfHtml)
    
    #begin writing the html file
    with open(fileLocation, "r", encoding="utf-8") as file: 
    
        file = file.read()
        file = file.replace("\n", """</p> \n\n <p>""")
        chapter.write(file)
   
    chapter.write("""</p>""")
    chapter.write(globalVar.htmlEndHeader)
    chapter.close()
   
    return 


def opfManifest(path,title, listOfRef = []):

    """
        for this function we will iterate through the  exising folder, Text and Images.
        We will store them into a list then after that iterate through the list and starts
        writing the Manifest itself. 
        
        For convience, we will name the html file base on numbers. ie 1 correspond to chapter 1 , so on so forth
        
        we will use os.walk() to traverse through the subdirectories.
        
        Furthermore this function will also create the table of content 
    """
    
    id_entry = []
    href = []
    os.chdir(os.path.join(path,"OEBPS"))
    
    for root, dirs, files in os.walk(path):
       
       
        for filename in files:
            
            filepath = os.path.join(root, filename)
            
            if filepath.endswith(".html"):
                id_entry.append(filename)
                href.append("Text/"+filename)
                
            if filepath.endswith(".css"):
                id_entry.append(filename)
                href.append("Styles/"+filename)
            
            if filepath.endswith(".jpg"):
                id_entry.append(filename)
                href.append("Images/"+filename)
                
    
    #we begin writing the manifest here   
    content = open("content.opf" , "w+")
    content.write(globalVar.opfManifestStart)
    
    for hreff,idx in zip(href , id_entry):
    
        manifestEntry = "\t<item href="+"\""+hreff+"\""+" "+"id="+"\""+idx+"\""+" "+"""media-type="application/xhtml+xml" />\n"""
        content.write(manifestEntry)
        
    content.write("  </manifest>\n")
     
    #here we will write the spine  
    content.write("""  <spine toc="ncx">\n""")
    
    for i in id_entry:
    
        #we do not want to write the .css file into the spine
        if i.endswith(".css") or i.endswith(".jpg"):  
            pass
            
        else:
            idref = "\t<itemref idref="+"\""+i+"\""+" />\n"
            content.write(idref)
    
    content.write("""  </spine> \n </package>""")
    
    #we write the table of content here 
    tableOfContent = open("toc.ncx", "w+", encoding="utf-8")
    
    tableOfContent.write(globalVar.tocStart)
    tableOfContent.write("\t<text>"+ title + "</text>\n  </docTitle> \n  <navMap>\n")
    
    orderNum = 1
    
    if not listOfRef:
        for hreff,idx in zip(href, id_entry):
            
            if idx.endswith(".css") or idx.endswith(".jpg"):
                pass
                
            else:
                
                filenameSplit = idx.split(".")
                
                tableOfContent.write("""\t<navPoint id="navPoint-"""+str(orderNum)+"\""+ """ playOrder=\""""+str(orderNum)+"\""
                +""">\n  \t<navLabel>\n""")
              
                tableOfContent.write("\t\t<text>"+ "Chapter " + filenameSplit[0]+ ": " + filenameSplit[1] + "</text>\n")
                
                tableOfContent.write("\t  </navLabel>\n")
                
                tableOfContent.write("""  \t<content src=\""""+hreff +"\""+ """ />\n\t</navPoint>\n""")
                    
               
                orderNum +=1
    else:
        
        hreff = [html for html in href if html.endswith(".html")][0]
        
        for entry in listOfRef:
        
            tableOfContent.write("""\t<navPoint href="navPoint-"""+str(orderNum)+"\""+ """ playOrder=\""""+str(orderNum)+"\""
                +""">\n  \t<navLabel>\n""")
              
            tableOfContent.write("\t\t<text>"+ entry + "</text>\n")
            
            tableOfContent.write("\t  </navLabel>\n")
            
            tableOfContent.write("""  \t<content src=\""""+hreff+"#"+entry.replace(" ","_") +"\""+ """ />\n\t</navPoint>\n""")
            
            orderNum +=1
            
    tableOfContent.write("""  </navMap>\n</ncx>""")
    tableOfContent.close()
    
    return 



def folderOrFile():
    """ 
        Returns a List of file location
    
    """
    
    listOfFiles = []
    response=""
    
    while True:
        
        print("Would you like to manually insert files or just select a folder? ")
        response = input("Respond with \"File\" or \"Folder\": " )
        
        if response.casefold()=="file" or response.casefold()=="folder":
            break
        
    if response.casefold() == "file":
        numOfChapter = input("How many files to add?: " )
        
        for i in range(int(numOfChapter)):
    
    
            #suppress the tk gui from appearing
            tk.Tk().withdraw()
            
            #opens the box for us to find the files
            filename = askopenfilename()  
            
            if not filename:
                pass 
                
            else: 
                listOfFiles.append(filename)
        
    
    else: 
        tk.Tk().withdraw()
        filenam = askdirectory()
        
        if filenam:
            for root, dirs, filename in os.walk(filenam):        
                for name in filename:
                
                    if name.endswith(".txt"):
                        listOfFiles.append(os.path.join(root,name))
        else:
            print("No Folder Selected")
          
    return listOfFiles



def webScraper(path):


    os.chdir(path)
    #So far works with wikipedia
    url = input("Enter a webpage: " )
    page = requests.get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content , "html.parser")
    else:
        raise ValueError("Page not available")
   
    
    soup = BeautifulSoup(open(filename,"r+",encoding="utf-8"), "html.parser")
    """
    So the next bit will parse the headers the text and the images
    """

    links = soup.find_all(lambda tag: tag.get('class')==["mw-headline"] or tag.name in ["p", "img"])


    """
    for image support we would need to download the images and set the pathway in the file
    so this would mean that we need to manually write in the image location in the epub into the output file

    """
    imgNum = 1
    chapNum = 1
    chaptArr = [] # this will contain the name of our chapters

    """
    The directory name will be the title of the article
    """
    title = (soup.find_all("title")[0].get_text().split(" - "))[0] 
    
    chapter = open("1.html", "w+", encoding="utf-8")
    chapter.write(globalVar.htmlHeader)
    
    for link in links:
        
        if link.get('class') == ["mw-headline"]:
            headline = link.get_text()
            chaptArr.append(headline)
            header = """<h2><strong>""" + "<span id="+str(headline).replace(" ","_")+">" + str(headline)+ """</span></strong></h2> \n\n"""
            chapter.write(header)

        elif link.name == "img":
            img_link = link["src"].split("src=")[-1]
            print(img_link)
            if img_link.endswith("svg.png") or "static/images/footer" in img_link or "CentralAutoLogin" in img_link or "Wooden_hourglass_3" in img_link or "mediawiki" in img_link or not img_link:
                pass
            
            else:
                #image downloading not working atm
                #imgToJpeg = open(str(imgNum)+".jpg", "wb")

                #download_img= urllib.request.urlopen(img_link)
                #imgToJpeg.write(download_img.read())
                #imgToJpeg.close()
                imgNum+=1
                fileLoc = """<p style="text-align: center;">""" +"<img alt="+ "\""+str(imgNum)+"\""+" " +"src=\"../Images/"+str(imgNum)+""".jpg\" /><br /></p>\n\n<p style="text-align: left;"><!--StartFragment--></p>\n"""
                chapter.write(fileLoc)
        else:
            
            chapter.write("<p>"+str(link)+"</p>\n\n")
            
    chapter.write(globalVar.htmlEndHeader)
    chapter.close()
    
    #Now we need to write the manifest and the toc
    # We still neeed to move the images into the image folder
    return chaptArr



def main():

    
    directory = input("Project Name: " )
    path = os.getcwd()
    
    
    while True:
        if os.path.isdir(directory):
            print("Folder Exist! Please input another name.")
            directory = input("Project Name: ")
        else:
            break
    #Webscraping still experimental
    onlineOrOffline = 2 
    #input("1.Online or 2.Offline? (Reply with 1 or 2) : ")
    if int(onlineOrOffline) == 2:
        
        listOfText = folderOrFile()
        
        while not listOfText:
        
            answer = input("No files selected. Try Again? Respond with Y or N: " )
            
            if answer == "Y" or answer == "y":
                listOfText = folderOrFile()
            else:
                print("GoodBye!")
                
                return 
        
    Book(directory)
    
    """
    The next 3 line is here is to prevent hardcoding the path with forward slashes or backwarded
    slashes ie \OEBPS\Text and /OEBPS/Text which could cause problem on unix 
    """
    
    path1 = os.path.join(path, directory)
    path1Copy = path1
    path1 = os.path.join(path1, "OEBPS")
    path1 = os.path.join(path1, "Text")
    
    os.chdir(path1)
    chaptArr = [] 
    
    if int(onlineOrOffline) ==2:
        chaptNum = 1               
    
        #we proceed to convert the text files into html files 
        for i in listOfText:
            writer(i,path1, chaptNum)
            chaptNum+=1
    else:
        chaptArr = webScraper(path1)
    
    #Write the opfManifest
    opfManifest(os.path.join(path,directory), directory, chaptArr)
      
    #return back to home directory
    os.chdir(path) 
    
    """
        Here we will zip the file and change the .zip extension to a .epub 
        and thus the epub has been created

    """

    shutil.make_archive(directory, 'zip', directory)
    book = directory + ".zip"
    base = os.path.splitext(book)[0]
    os.rename(book, base + ".epub")
    #remove our folder
    shutil.rmtree(path1Copy)
    print("Success!")
    
    return 


if __name__ == "__main__":

    main()
    
    