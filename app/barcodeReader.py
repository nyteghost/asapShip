# Importing library
import cv2
from pyzbar.pyzbar import decode
import os
import getpass
import time 
from multiprocessing import Pool 
import multiprocessing

prefix = r"C:\Users"
localuser = getpass.getuser()
spfolderpath= r"Southeastern Computer Associates, LLC\GCA Deployment - Documents\Database\GCA Report Requests\ASAP Pickup Data"
folderdate = r"2022-03-08"
familyid = r"1546921 - Copy"
filefolder = prefix+'\\'+localuser+'\\'+spfolderpath+'\\'+folderdate+'\\'+familyid
dirName = r'C:\Users\Mbrown\Southeastern Computer Associates, LLC\GCA Deployment - Documents\Database\GCA Report Requests\ASAP Pickup Data' #here your dir path


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)          
    return allFiles 

# Make one method to decode the barcode


def BarcodeReader(image):
  # read the image in numpy array using cv2
  img = cv2.imread(image)
  img = cv2.resize(img, None, fx=2, fy=2,interpolation=cv2.INTER_LINEAR)
  
  # Decode the barcode image
  detectedBarcodes = decode(img)
    
  # If not detected then print the message
  if not detectedBarcodes:
    
    # print("Barcode Not Detected or your barcode is blank/corrupted!")
    return 'BarcodeNotDetected'
  else:
        # Traverse through all the detected barcodes in image
      for barcode in detectedBarcodes: 
          
          # Locate the barcode position in image
          (x, y, w, h) = barcode.rect
            
          # Put the rectangle in image using
          # cv2 to heighlight the barcode
          cv2.rectangle(img, (x-10, y-10),
                        (x + w+10, y + h+10),
                        (255, 0, 0), 2)
          
          # Print the barcode data 
          if barcode.data!="":           
              # print(barcode.data)
              # print(barcode.type)
              return barcode.data          
  #Display the image
  # cv2.imshow("Image", img)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()

def getFileNames():
    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)
    listOfFiles = [ x for x in listOfFiles if "Old Process" not in x ] 
    # Print the files
    for elem in listOfFiles:
        if "Old Process" in elem:
          input()
        else:
          print(elem)
    print ("****************")
    
    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    return listOfFiles     
    # Print the files 

def main(fileList):
    x=0
    # listOfFiles = fileList
    # for f in fileList:
    print(fileList)
    if fileList.endswith(".png"):
      newName = BarcodeReader(fileList)
      if newName == 'BarcodeNotDetected':
        x+=1
        newName = newName+str(x)
        newName = str(newName)
      else:
        newName = str(newName)
        newName = newName.replace('b','GCA-')
        newName = newName.replace("'",'')
      print(os.path.dirname(fileList)+'\\'+newName+'.png')
      # os.rename(f,os.path.dirname(f)+'\\'+newName+'.png')
    else:
      # print('Skipped ',f,' because the file is not a png.')
      pass


if __name__ == "__main__":
  startTime = time.time()
  
  fileList = getFileNames()
  
  pool = multiprocessing.Pool(4)
  y = pool.map(main, fileList)
  
  completeTime = (time.time() - startTime)
  print(completeTime)


# if __name__ == "__main__":
#   for filename in os.listdir(filefolder):
#       f = os.path.join(filefolder, filename)
#       # checking if it is a file
#       if os.path.isfile(f):
#         newName = BarcodeReader(f)
#         newName = str(newName)
#         print(newName)
#         newName = newName.replace('b','GCA-')
#         newName = newName.replace("'",'')
#         print(newName)
#         os.rename(f,filefolder+'\\'+newName+'.png')
# folder = r'C:\Users\Mbrown\Southeastern Computer Associates, LLC\GCA Deployment - Documents\Database\GCA Report Requests\ASAP Pickup Data\2022-03-08' #here your dir path

# if __name__ == "__main__":
#   for (paths, dirs, files) in os.walk(folder):
#       for f in files:
#           if f.endswith(".png"):
#             print(f)
#               # newName = BarcodeReader(f)
#               # newName = str(newName)
#               # print(newName)
#               # newName = newName.replace('b','GCA-')
#               # newName = newName.replace("'",'')
#               # print(newName)

