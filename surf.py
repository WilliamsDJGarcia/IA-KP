import cv2
import numpy
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt

def surfApplication(surf,img1,descriptors0): 
    global img0

    keypoints_surf1, descriptors1 = surf.detectAndCompute(img1, None)
    print(f'x% {len(keypoints_surf1)}')

    matches(img0,img1,descriptors0,descriptors1) 

def matches(img0,img1,descriptors0,descriptors1):
    bf = cv2.BFMatcher(cv2.NORM_L2,crossCheck=True)
    matches = bf.match(descriptors0,descriptors1)
    matches = sorted(matches, key = lambda x:x.distance)
    match = len(matches)
    print(f'coindidencia% {match}')

    generatePercent(match)

def generatePercent(match):
    z = (match*100)/oneHundred
    if z == 100.0:
        original.append(z)
    else:
        percent.append(z)

def setImgRotation():
    global img0
    global oneHundred

    xs = []
    grade = int(ValueG.get()) 
    count= grade
    finalGrade=grades-grade

    img0 = datoImage() 
    (h,w) = img0.shape[:2]
    center = (w/2,h/2)
    surf = cv2.xfeatures2d.SURF_create(300)
    
    keypoints_surf0, descriptors0 = surf.detectAndCompute(img0, None)
    oneHundred = len(keypoints_surf0)
    print(f'100% {oneHundred}')
    generatePercent(oneHundred)
    while(count<=finalGrade):
        xs.append(str(count))
        m = cv2.getRotationMatrix2D(center,count,1.0)
        img1 = cv2.warpAffine(img0, m, (h, w))
       
        surfApplication(surf,img1,descriptors0)
        count = count +grade
 
    graph(xs)

def setImgScale():
    global img0
    global oneHundred
    sizes = []

    img0 = datoImage()
    img1 = cv2.resize(img0, (int(img0.shape[1]/2), int(img0.shape[0]/2)))
    img2 = cv2.resize(img1, (int(img1.shape[1]/2), int(img1.shape[0]/2)))
    img3 = cv2.resize(img0, (int(img0.shape[1]*1.5), int(img0.shape[0]*1.5)))
    img4 = cv2.resize(img0, (int(img0.shape[1]*2), int(img0.shape[0]*2)))

    sizes.append(img1)
    sizes.append(img2)
    sizes.append(img3)
    sizes.append(img4)
   
    surf = cv2.xfeatures2d.SURF_create(300)
    
    keypoints_surf0, descriptors0 = surf.detectAndCompute(img0, None)
    oneHundred = len(keypoints_surf0)
    generatePercent(oneHundred)
    for i in sizes:
        surfApplication(surf,i,descriptors0)

    graph(X)

def setImgDisplacement():
    global img0
    global oneHundred
    cardinal_points = []
    count = 0
    posX=0
    posY=0
    posXi = int(ValueX.get())
    posYi = int(ValueY.get())

    img0 = datoImage()

    surf = cv2.xfeatures2d.SURF_create(300)
   
    keypoints_surf0, descriptors0 = surf.detectAndCompute(img0, None)
    oneHundred = len(keypoints_surf0)
    generatePercent(oneHundred)

    while(count<=7):
        if count == 0:
            posX = 0
            posY = posYi

            north = displacement(surf,img0,descriptors0,posX,posY)
            cardinal_points.append(north)

            count= count+1
        if count == 1:
            posX = -posXi
            posY = posYi

            northWest = displacement(surf,img0,descriptors0,posX,posY)
            cardinal_points.append(northWest)

            count= count+1
        if count == 2:
            posX = -posXi
            posY = 0

            west = displacement(surf,img0,descriptors0,posX,posY)
            cardinal_points.append(west)
            
            count= count+1
        if count == 3:
            posX = -posXi
            posY = -posYi

            southWest = displacement(surf,img0,descriptors0,posX,posY)
            cardinal_points.append(southWest)

            count= count+1
        if count == 4:
            posX = 0
            posY = -posYi

            south = displacement(surf,img0,descriptors0,posX,posY)
            cardinal_points.append(south)

            count= count+1
        if count == 5:
            posX = posXi
            posY = -posYi
            
            southEast = displacement(surf,img0,descriptors0,posX,posY)
            cardinal_points.append(southEast)
            
            count= count+1
        if count == 6:
            posX = posXi
            posY = 0

            east = displacement(surf,img0,descriptors0,posX,posY)
            cardinal_points.append(east)

            count= count+1 
        if count == 7:
            posX = posXi
            posY = posYi

            northEast = displacement(surf,img0,descriptors0,posX,posY)
            cardinal_points.append(northEast)
    
            count= count+1 
    print("ACABO")
    
    graph(cardinal_points)

def displacement(surf,img0,descriptors0,posX,posY):
    (h,w) = img0.shape[:2]

    m = numpy.float32([[1,0,posX],[0,1,posY]])
    img1 = cv2.warpAffine(img0, m,(h + posX, w + posY))
    surfApplication(surf,img1,descriptors0)
    print(f'Cardinal {posX} {posY}')
    return str(posX)+","+str(posY)

def graph(x):
    fig, (ax1) = plt.subplots(nrows=1, ncols=1)

    ax1.bar(O,original,label = "Original", color="red")
    ax1.bar(x,percent,label = "Results", color="green")
    ax1.set_xlabel('Results')
    ax1.set_ylabel('Percent')
    ax1.set_title('Comparative graph of the original with results')
    ax1.legend()
    plt.ylim(0, 100)
    original.clear()
    percent.clear()
    plt.show()

def datoImage():
    global img0

    img0 = cv2.imread(datoI.get(), cv2.IMREAD_GRAYSCALE)
    return img0

def select():
    path.filename = filedialog.askopenfilename(initialdir="C:/Users/WSGO/Desktop/UPchiapas/8vo/IA/codes/ImgProcess", title="Select file", filetypes=(("jpg files",".jpg"), ("all files", ".*")))
    print(path.filename)
    ls = path.filename
    datoI.set(ls)

def menuOptions():
    Button(path,text='Seleccionar Archivo',font='Helvetica 8 bold', bg="#E1EAF3",command=select, fg="blue").pack()
    Label(path, text="X para desplazamiento", font='Helvetica 14 bold').pack()
    Entry(path, textvariable=ValueX, width=10 ,bd=3).pack()        
    Label(path, text="Y para desplazamiento", font='Helvetica 14 bold').pack()
    Entry(path, justify="center", textvariable=ValueY, width=10 ,bd=3).pack()        
    Button(path, text="Desplazamiento",font='Helvetica 8 bold', bg="#2471A3",command=setImgDisplacement).pack()
    
    Label(path, text="Grados a rotar: ", font='Helvetica 14 bold').pack()
    Entry(path, justify="center", textvariable=ValueG, width=10 ,bd=3).pack()    
    Button(path, text="Rotación",font='Helvetica 8 bold',bg="#566573", command=setImgRotation).pack()
    Button(path, text="Escala",font='Helvetica 8 bold', bg="#117A65",command=setImgScale).pack()
    path.mainloop()

if __name__ == '__main__':
    grades = 360
    scale = 1.0
    oneHundred = 0
    img0 = None
    original = []
    percent = []
    X = ['1/4','1/16','2X','4X']
    O = ['Original']

    path = Tk()
    path.configure(bg = 'azure')
    path.title('SURF')
    ValueX = StringVar()
    ValueY = StringVar()
    ValueG = StringVar()
    datoI = StringVar()
    menuOptions()