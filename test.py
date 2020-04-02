import cv2
import numpy
import math
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt

def surfApplication(surf,img1,Origintrasnform): 
    matches = []
    bestMatch = []
    con=0
    noc=0

    keypoints_surf1, descriptors1 = surf.detectAndCompute(img1, None)

    for j,k in zip(Origintrasnform,range(len(keypoints_surf1[:100]))):
        x1 = j[0]
        y1 = j[1]
        x2 = keypoints_surf1[k].pt[0]
        y2 = keypoints_surf1[k].pt[1]
        # resultx = x1-x2
        # resulty = y1-y2
        result = math.pow(math.pow(x1-x2,2)+math.pow(y1-y2,2),1/2)
        # print(f'result X,Y {resultx,resulty}')
        # if (resultx<=3 and resultx>=-3 and resulty<=3 and resulty>=-3):
        if(result<=20 and result>=-20):
            con = con+1
        else:
            noc = noc+1 
    print(f'con {con}')
    print(f'noc {noc}')
    generatePercent(con)

# def matches(trasnform,keypoints_surf1):
#     # bf = cv2.BFMatcher(cv2.NORM_L2,crossCheck=True)
#     # matches = bf.match(descriptors0,descriptors1)
#     # matches = sorted(matches, key = lambda x:x.distance)
#     # match = len(matches)
# for i in originalesAmanita:
#             for j in keypointsT:
#                 result=pow(pow(j[0]-i[0],2)+pow(j[1]-i[1],2),1/2)
#                 if(result<=3 and result>=-3):
#                     acertado.append(result)
#                     coincidenciasO.append(keypointsO[contador])
#                     coincidenciasT.append(j)
                    
#                 else:
#                     fallidos.append(result)
#             contador=contador+1
#     # generatePercent(match)

def generatePercent(match):
    z = (match*100)/oneHundred
    percent.append(z)

def setImgRotation():
    global img0
    global oneHundred

    xs = []
    transform = []
    grade = int(ValueG.get()) 
    count= grade
    finalGrade=grades-grade

    img0 = datoImage() 
    (h,w) = img0.shape[:2]
    center = (w/2,h/2)
    surf = cv2.xfeatures2d.SURF_create(500)
    
    keypoints_surf0, descriptors0 = surf.detectAndCompute(img0, None)
    # oneHundred = len(keypoints_surf0)
    # generatePercent(oneHundred)
    while(count<=finalGrade):
        transform = transformOriginal(keypoints_surf0,center,(0,count))
        xs.append(str(count))
        m = cv2.getRotationMatrix2D(center,count,1.0)
        img1 = cv2.warpAffine(img0, m, (h, w))
        print(f'GRADOS {count}')
        surfApplication(surf,img1,transform[:100])
        transform.clear()
        count = count +grade
 
    graph(xs)

def setImgScale():
    global img0
    global oneHundred
    sizes = [0.25,0.5,1,2,4]
    transform = []

    img0 = datoImage()
   
    surf = cv2.xfeatures2d.SURF_create(300)
    
    keypoints_surf0, descriptors0 = surf.detectAndCompute(img0, None)
    # oneHundred = len(keypoints_surf0)
    # generatePercent(oneHundred)

    for i in sizes:
        width = int(img0.shape[1] * i )
        height = int(img0.shape[0] * i)
        dim = (width, height)
        img1 = cv2.resize(img0,dim,interpolation=cv2.INTER_AREA)
        transform = transformOriginal(keypoints_surf0,i,(2,0))
        surfApplication(surf,img1,transform[:100])
        transform.clear()
    graph(X)

def setImgDisplacement():
    global img0
    global oneHundred
    transform = []
    cardinal_points = []
    count = 0
    posX=0
    posY=0
    posXi = int(ValueX.get())
    posYi = int(ValueY.get())

    img0 = datoImage()

    surf = cv2.xfeatures2d.SURF_create(300)
   
    keypoints_surf0, descriptors0 = surf.detectAndCompute(img0, None)
    # oneHundred = len(keypoints_surf0)
    # generatePercent(oneHundred)

    while(count<=7):
        if count == 0:
            posX = 0
            posY = posYi
            transform = transformOriginal(keypoints_surf0,(posX,posY),(1,0))
            north = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(north)
            transform.clear()

            count= count+1
        if count == 1:
            posX = -posXi
            posY = posYi
            transform = transformOriginal(keypoints_surf0,(posX,posY),(1,0))
            northWest = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(northWest)
            transform.clear()
            
            count= count+1
        if count == 2:
            posX = -posXi
            posY = 0
            transform = transformOriginal(keypoints_surf0,(posX,posY),(1,0))
            west = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(west)
            transform.clear()
            
            count= count+1
        if count == 3:
            posX = -posXi
            posY = -posYi
            transform = transformOriginal(keypoints_surf0,(posX,posY),(1,0))
            southWest = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(southWest)
            transform.clear()

            count= count+1
        if count == 4:
            posX = 0
            posY = -posYi
            transform = transformOriginal(keypoints_surf0,(posX,posY),(1,0))
            south = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(south)
            transform.clear()

            count= count+1
        if count == 5:
            posX = posXi
            posY = -posYi
            transform = transformOriginal(keypoints_surf0,(posX,posY),(1,0))
            southEast = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(southEast)
            transform.clear()
            
            count= count+1
        if count == 6:
            posX = posXi
            posY = 0
            transform = transformOriginal(keypoints_surf0,(posX,posY),(1,0))
            east = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(east)
            transform.clear()

            count= count+1 
        if count == 7:
            posX = posXi
            posY = posYi
            transform = transformOriginal(keypoints_surf0,(posX,posY),(1,0))
            northEast = displacement(surf,img0,transform[:100],posX,posY)
            cardinal_points.append(northEast)
            transform.clear()

            count= count+1 
    print("ACABO")
    
    graph(cardinal_points)

def displacement(surf,img0,transform,posX,posY):
    (h,w) = img0.shape[:2]

    m = numpy.float32([[1,0,posX],[0,1,posY]])
    img1 = cv2.warpAffine(img0, m,(h + posX, w + posY))
    surfApplication(surf,img1,transform)

    return str(posX)+","+str(posY)

def transformOriginal(keypoints_surf0,param,val):
    transform=[]
    if val[0] == 0:
        for i in range(len(keypoints_surf0)):
            x = keypoints_surf0[i].pt[0]
            y = keypoints_surf0[i].pt[1]

            rotatedX = math.cos(val[1]) * (x - param[0]) - math.sin(val[1]) * (y - param[1]) + param[0]
            rotatedY = math.sin(val[1]) * (x - param[0]) + math.cos(val[1]) * (y - param[1]) + param[1]
            
            rotated = rotatedX,rotatedY
            transform.append(rotated)
    if val[0] == 1:
        xi=param[0]
        yi=param[1]
        for i in range(len(keypoints_surf0)):
           x = keypoints_surf0[i].pt[0]
           y = keypoints_surf0[i].pt[1]

        #    print(f'valor original x,y {x,y}')
           displacementX = x + xi
           displacementY = y + yi

           displacement = displacementX,displacementY
        #    print(f"TRANSFORMADOS {displacement}")
           transform.append(displacement)
    if val[0] == 2:
        for i in range(len(keypoints_surf0)):
            x = keypoints_surf0[i].pt[0]
            y = keypoints_surf0[i].pt[1]

            newX = x * param
            newY = y * param
            
            new = newX,newY
            transform.append(new)
    return transform

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