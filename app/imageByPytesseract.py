import numpy as np
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew
from matplotlib import pyplot as plt
import pytesseract
import cv2
from PIL import Image
import re
import time 
import os,sys
import getpass
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from app.utils.timer import LoopStopper


prefix = r"C:\Users"
localuser = getpass.getuser()
spfolderpath= r"Southeastern Computer Associates, LLC\GCA Deployment - Documents\Database\GCA Report Requests\ASAP Pickup Data"
folderdate = r"2022-02-21"
familyid = r"174682"
filesingle = "FID 174682 1378302_962_20220221_100224 - Copy.png"
filefolder = prefix+'\\'+localuser+'\\'+spfolderpath+'\\'+folderdate+'\\'+familyid
file =prefix+'\\'+localuser+'\\'+spfolderpath+'\\'+folderdate+'\\'+familyid+'\\'+filesingle


startTime = time.time()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def deskew(_img):
    image = io.imread(_img)
    grayscale = rgb2gray(image)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, resize=True) * 255
    return rotated.astype(np.uint8)


def display_avant_apres(_original):
    plt.subplot(1, 2, 1)
    plt.imshow(io.imread(_original))
    plt.subplot(1, 2, 2)
    plt.imshow(deskew(_original))


def imagesearch(file,retry=''):
    
    img = cv2.imread(file)
    img = cv2.resize(img, None, fx=3, fy=3,interpolation=cv2.INTER_LINEAR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1,1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.imwrite(filefolder+'\\afterimage\\'+'-thresh-'+filename, img)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    gcakeyword = 0
    buffer = 0
    for psm in range(11,13+1):
        config = '--oem 3 --psm  %d' % psm 
        txt = pytesseract.image_to_string(img, config= config, lang='eng')
        # print('psm ', psm, ':',txt.split("GCA-",1)[1])
        keyword = 'GCA-' #Uses GCA- as the keyword to discover the keyword after GCA- which should be the AssetID
        before_keyword, keyword, after_keyword = txt.partition(keyword) #Partitions the lines in the returned txt to make it easier to parse
        keyword = after_keyword #Makes everything After GCA- the keyword
        try:
            keyword = keyword.splitlines()[0] #Uses index to only keep the first Keyword line which has The AssetID in it. 
        except IndexError:
            buffer+=1
            print(psm,'Buffer Count: ',buffer)
            continue
        keyword = keyword.replace(':','') #Replaces any : with blank space
        keyword = keyword.replace(' ','')#Replaces any space with a blank space
        print(keyword)
        if keyword == '':
            print('No keyword found in ',psm,'Buffer Count: ',buffer)
        else:
            print('psm ', psm,': ','GCA-',keyword)
            print('Buffer Count: ',buffer)
            gcakeyword = 'GCA-'+keyword
            completeTime = (time.time() - startTime)
            print(completeTime)
    return buffer,gcakeyword
    
        
def retry(retryfile):
    display_avant_apres(retryfile)
    io.imsave(filefolder+'\\afterimage\\'+'-thresh-'+filename, deskew(retryfile))
    # image1 = Image.open("C:\Users\Mbrown\Desktop\GCA-Coding\Projects\Python\asapShip\output.png")
    reImage = filefolder+'\\afterimage\\'+'-thresh-'+filename
    buffer,gcakeyword = imagesearch(reImage)
    if buffer <2:
        print(gcakeyword)
    else:
        print('No AssetID found in image')


for filename in os.listdir(filefolder):
    f = os.path.join(filefolder, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)
        buffer,gcakeyword = imagesearch(f)
        if buffer > 2:
            retry(f)
    # else:
    #     os.rename(file,filefolder+'\\'+gcakeyword+'.png') 

completeTime = (time.time() - startTime)
print(completeTime)


