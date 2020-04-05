import cv2
import numpy as np
import imutils
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

def surfApplication(surf,img1,Origintrasnform): 
    global KPorigin
    KPmatches = []
    KPoriginOK = []
    con=0
    noc=0
    count = 0
    kp2 = surf.detect(img1,None)

    for j,k in zip(Origintrasnform,kp2[:100]):
        x1 = j.pt[0]
        y1 = j.pt[1]
        x2 = k.pt[0]
        y2 = k.pt[1]
        resultx = x1-x2
        resulty = y1-y2

        if (resultx<=5 and resultx>=-5 and resulty<=5 and resulty>=-5):
            con = con+1
            KPoriginOK.append(KPorigin[count])
            KPmatches.append(k)
        else:
            noc = noc+1
        count = count+1

    drawMatches(KPoriginOK,KPmatches,img1) 
    print(f'con {con}')
    print(f'noc {noc}')
    KPoriginOK.clear()
    KPmatches.clear()

    generatePercent(con)

def drawMatches(KPmatchO,KPmatchT,img1):
    global img0
    
    img = cv2.drawKeypoints(img0, KPmatchO,None, color=(0,255,0))
    img2 = cv2.drawKeypoints(img1, KPmatchT,None, color=(0,255,0))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.imshow(img)
    ax2.imshow(img2)
    ax1.title.set_text("Imagen original")
    ax2.title.set_text("Resultado")
    coordsA = "data"
    coordsB = "data"

    for k,l in zip(range(len(KPmatchO)),range(len(KPmatchT))):
        xyA =  (KPmatchO[k].pt[0],KPmatchO[k].pt[1])
        xyB =  (KPmatchT[l].pt[0],KPmatchT[l].pt[1])
        
        print(f'X {KPmatchO[k].pt[0]} , Y {KPmatchO[k].pt[1]}')
        print(f'X2 {KPmatchT[l].pt[0]} , Y2 {KPmatchT[l].pt[1]}')

        con = ConnectionPatch(xyA=xyA, xyB=xyB, coordsA=coordsA, coordsB=coordsB,
            axesA=ax1, axesB=ax2,
            arrowstyle="-",color="red", shrinkB=5)
        ax2.add_artist(con)

def generatePercent(match):
    z = (match*100)/oneHundred
    percent.append(z)

def setImgRotation():
    global img0
    global KPorigin

    xs = []
    transform = []
    
    grade = int(ValueG.get())
    count = grade

    img0 = datoImage()
    (row,col) = img0.shape[:2]

    if (row!=col):
        imgNew = cv2.resize(img0,(row,col),1)
        img0=imgNew
        pass



    surf = cv2.xfeatures2d.SURF_create(500)
    KPorigin = surf.detect(img0,None)
    
    while(count < 360):
        xs.append(str(count))

        img1 = imutils.rotate_bound(img0, count)
        
        kp1 = surf.detect(img0,None)

        (heigt,width) = img0.shape[:2]
        (heigt1,width1)= img1.shape[:2]

        transform = transformOriginal(kp1,(heigt,width,heigt1,width1),(0,count))
        surfApplication(surf,img1,transform[:100])
        transform.clear()

        count = count + grade
    graph(xs)

def setImgScale():
    global img0
    global KPorigin

    sizes = [0.25,0.5,1,2,4]
    transform = []

    img0 = datoImage()
   
    surf = cv2.xfeatures2d.SURF_create(300)
    
    KPorigin = surf.detect(img0, None)
   
    for i in sizes:
        width = int(img0.shape[1] * i )
        height = int(img0.shape[0] * i)
        dim = (width, height)
        img1 = cv2.resize(img0,dim,interpolation=cv2.INTER_AREA)
        transform = transformOriginal(KPorigin,i,(2,0))
        surfApplication(surf,img1,transform[:100])
        transform.clear()
    graph(X)

def setImgDisplacement():
    global img0
    global KPorigin

    transform = []
    cardinal_points = []
    count = 0
    posX=0
    posY=0
    posXi = int(ValueX.get())
    posYi = int(ValueY.get())

    img = datoImage()

    img0 = cv2.copyMakeBorder(img,posYi,posYi,posXi,posXi,cv2.BORDER_CONSTANT)

    surf = cv2.xfeatures2d.SURF_create(300)
   
    KPorigin = surf.detect(img0, None)

    while(count<=7):
        if count == 0:
            posX = 0
            posY = posYi
            transform = transformOriginal(KPorigin,(posX,posY),(1,0))
            north = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(north)
            transform.clear()

            count= count+1
        if count == 1:
            posX = -posXi
            posY = posYi
            transform = transformOriginal(KPorigin,(posX,posY),(1,0))
            northWest = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(northWest)
            transform.clear()
            
            count= count+1
        if count == 2:
            posX = -posXi
            posY = 0
            transform = transformOriginal(KPorigin,(posX,posY),(1,0))
            west = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(west)
            transform.clear()
            
            count= count+1
        if count == 3:
            posX = -posXi
            posY = -posYi
            transform = transformOriginal(KPorigin,(posX,posY),(1,0))
            southWest = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(southWest)
            transform.clear()

            count= count+1
        if count == 4:
            posX = 0
            posY = -posYi
            transform = transformOriginal(KPorigin,(posX,posY),(1,0))
            south = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(south)
            transform.clear()

            count= count+1
        if count == 5:
            posX = posXi
            posY = -posYi
            transform = transformOriginal(KPorigin,(posX,posY),(1,0))
            southEast = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(southEast)
            transform.clear()
            
            count= count+1
        if count == 6:
            posX = posXi
            posY = 0
            transform = transformOriginal(KPorigin,(posX,posY),(1,0))
            east = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(east)
            transform.clear()

            count= count+1 
        if count == 7:
            posX = posXi
            posY = posYi
            transform = transformOriginal(KPorigin,(posX,posY),(1,0))
            northEast = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(northEast)
            transform.clear()

            count= count+1 
    print("ACABO")
    
    graph(cardinal_points)

def displacement(surf,img,transform,posX,posY):
    (h,w) = img.shape[:2]
    m = np.float32([[1,0,posX],[0,1,posY]])
    img1 = cv2.warpAffine(img, m,(h,w))
    surfApplication(surf,img1,transform)

    return str(posX)+","+str(posY)

def transformOriginal(keypoints_surf0,param,val):
    transform=[]
    if val[0] == 0:
        center = (param[3]/2,param[2]/2) 
        dify = (param[2]-param[0])/2  
        difx = (param[3]-param[1])/2  
        grade = np.radians(val[1])
        
        for i in keypoints_surf0:
            x = round(i.pt[0]+difx,4)
            y = round(i.pt[1]+dify,4)

            rotatedX = np.cos(grade) * (x - center[0]) - np.sin(grade) * (y - center[1]) + center[0]
            rotatedY = np.sin(grade) * (x - center[0]) + np.cos(grade) * (y - center[1]) + center[1]
            
            rotated = rotatedX,rotatedY
            i.pt = rotated
    if val[0] == 1:
        xi=param[0]
        yi=param[1]
        for i in keypoints_surf0:
           x = i.pt[0]
           y = i.pt[1]

           displacementX = x + xi
           displacementY = y + yi

           displacement = displacementX,displacementY
           i.pt = displacement
    if val[0] == 2:
        for i in keypoints_surf0:
            x = i.pt[0]
            y = i.pt[1]

            newX = x * param
            newY = y * param
            
            new = newX,newY
            i.pt = new
    return keypoints_surf0

def graph(x):
    fig, (ax1) = plt.subplots(nrows=1, ncols=1)

    ax1.bar(O,original,label = "Original", color="red")
    ax1.bar(x,percent,label = "Results", color="green")
    ax1.set_xlabel('Results')
    ax1.set_ylabel('Percent')
    ax1.set_title('Comparative graph of the original with results')
    ax1.legend()
    plt.ylim(0, 100)
    percent.clear()
    KPorigin.clear()
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
    oneHundred = 100
    img0 = None
    arrayImg = []
    original = []
    original.append(oneHundred)
    percent = []
    KPorigin = []
    X = ['1/16','1/4','1','2X','4X']
    O = ['Original']

    path = Tk()
    path.configure(bg = 'azure')
    path.title('SURF')
    ValueX = StringVar()
    ValueY = StringVar()
    ValueG = StringVar()
    datoI = StringVar()
    menuOptions()