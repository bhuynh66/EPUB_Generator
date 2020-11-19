import globals
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
import os
import shutil

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
        container2.write(globals.container)
        container2.close()
        
        return 


    def mimetype(self):

        mime = open("mimetype", "w+")
        mime.write("application/epub+zip")
        mime.close()
        
        return

        
    def sgctoc(self):

        sgc = open("sgc-toc.css", "w+")
        sgc.write(globals.sgcToc)
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
    
    startOfHtml = globals.htmlStart + title + globals.htmlEnd
    
    fileToConvert = open(fileLocation, "r", encoding="utf-8")
        
    chapter.write(globals.htmlHeader)
    chapter.write(startOfHtml)
    
    #parse the files for multi newlines
    for i in fileToConvert.readlines(): 
    
        with open("out.txt", "a+", encoding="utf-8") as output:
            
            if i != "\n":
                output.write(i)
    
    output.close()
    
    #begin writing the html file
    with open("out.txt", encoding="utf-8") as file: 
    
        file = file.read()
        file = file.replace("\n", """</p> \n\n <p>""")
        chapter.write(file)
    
    output.close()
    
    # we delete the dummy file 
    parent_dir = os.getcwd()  
    path  = os.path.join(parent_dir, "out.txt")
    os.remove(path)
    
    chapter.write("""</p>""")
    chapter.write(globals.htmlEndHeader)
    chapter.close()
    fileToConvert.close()
    
    return 


def opfManifest(path,title):

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
                
    
    #we begin writing the manifest here   
    content = open("content.opf" , "w+")
    content.write(globals.opfManifestStart)
    
    for hreff,idx in zip(href , id_entry):
    
        manifestEntry = "    <item href="+"\""+hreff+"\""+" "+"id="+"\""+idx+"\""+" "+"""media-type="application/xhtml+xml" />\n"""
        content.write(manifestEntry)
        
    content.write("  </manifest>\n")
     
    #here we will write the spine  
    content.write("""  <spine toc="ncx">\n""")
    
    for i in id_entry:
    
        #we do not want to write the .css file into the spine
        if i.endswith(".css"):  
            pass
            
        else:
            idref = "    <itemref idref="+"\""+i+"\""+" />\n"
            content.write(idref)
    
    content.write("""  </spine> \n </package>""")
    
    #we write the table of content here 
    tableOfContent = open("toc.ncx", "w+", encoding="utf-8")
    
    tableOfContent.write(globals.tocStart)
    tableOfContent.write("    <text>"+ title + "</text>\n  </docTitle> \n  <navMap>\n")
    
    orderNum = 1
    
    for hreff,idx in zip(href, id_entry):
        
        if idx.endswith(".css"):
            pass
            
        else:
            filenameSplit = idx.split(".")
            
            tableOfContent.write("""    <navPoint id="navPoint-"""+str(orderNum)+"\""+ """ playOrder=\""""+str(orderNum)+"\""
            +""">\n      <navLabel>\n""")
          
            tableOfContent.write("        <text>"+ "Chapter " + filenameSplit[0]+ ": " + filenameSplit[1] + "</text>\n")
            
            tableOfContent.write("      </navLabel>\n")
            
            tableOfContent.write("""      <content src=\""""+hreff +"\""+ """ />\n    </navPoint>\n""")
    
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



def main():

    
    directory = input("Project Name: " )
    path = os.getcwd()
    
    while True:
        if os.path.isdir(directory):
            print("Folder Exist! Please input another name.")
            directory = input("Project Name: ")
        else:
            break
            
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
    path1 = os.path.join(path1, "OEBPS")
    path1 = os.path.join(path1, "Text")
    
    os.chdir(path1)
    

    chaptNum = 1               
    
    #we proceed to convert the text files into html files 
    for i in listOfText:
        writer(i,path1, chaptNum)
        chaptNum+=1

    opfManifest(os.path.join(path,directory), directory)
    
    
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
    
    print("Success!")
    
    return 


if __name__ == "__main__":

    main()
    
    