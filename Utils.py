import numpy as np
import cv2

global Xcm
global Ycm
    
import threading, queue

q = queue.Queue()


def testVideo():
    
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Display the resulting frame
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
def takeFoto():
    
    cap = cv2.VideoCapture(0)
    salir = False
    foto = False
    
    while (not salir):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('Presione f para tomar foto',frame)
        key = cv2.waitKey(1)
        if not key == -1 :
            if key == ord('q'):
                salir = True
            if key == ord('f'):
                salir = True
                foto = True
    cap.release()
    cv2.destroyAllWindows()
    
    if foto:
        return frame
    
def binarizar(binario):
    binario = np.int16(binario)
    binario = binario[:,:,0] + binario[:,:,1] + binario[:,:,2]
    binario = binario/3
    binario = np.uint8(binario)
    return binario

def centrodemasa(binario):
    binario = binario > 200
    x = np.arange(binario.shape[1])
    y = np.arange(binario.shape[0])
    xcm = np.dot(x,np.sum(binario,0))/np.sum(binario)
    ycm = np.dot(y,np.sum(binario,1))/np.sum(binario)
    global Ycm
    Ycm= ycm
    global Xcm
    Xcm = xcm
    return [xcm,ycm]
        
def showresta(imagen,color,gris=False,tolerancia=20,destroy=False, binaria = False):
    imagen = np.int16(imagen)
    color = np.int16(color)
    mostrar = np.zeros(imagen.shape,np.int16)
    mostrar[:,:,0] = imagen[:,:,0] - color[0]
    mostrar[:,:,1] = imagen[:,:,1] - color[1]
    mostrar[:,:,2] = imagen[:,:,2] - color[2]
    mostrar = np.abs(mostrar)
    mostrar = np.uint8(mostrar)
    if gris:
        tituloVentana = 'Imagen al restar color'
        cv2.destroyWindow(tituloVentana)
        cv2.namedWindow(tituloVentana)
        cv2.imshow(tituloVentana, mostrar)
    mostrar[:,:,0] = (mostrar[:,:,0] < tolerancia) * 255 
    mostrar[:,:,1] = (mostrar[:,:,1] < tolerancia) * 255 
    mostrar[:,:,2] = (mostrar[:,:,2] < tolerancia) * 255 
    xcm, ycm = centrodemasa(binarizar(mostrar))
    mostrar = cv2.circle(mostrar,(int(xcm),int(ycm)),20,(0, 255, 0),3)
    tituloVentana = 'Imagen binarizada'
    if destroy:
        cv2.destroyWindow(tituloVentana)
        cv2.namedWindow(tituloVentana)
    if binaria:
        cv2.imshow(tituloVentana, binarizar(mostrar))
    else:
        cv2.imshow(tituloVentana, mostrar)
    
def mainrutine(umbral=20):
    # Definimos parametros y cosas para el recorte
    refPt = []
    cropping = False
    lastPosition = None
    ventanaRecorte = 'Recorte'
    title = 'Seleccione la zona con el color a reconocer'
    ventanaColor = 'Color promedio seleccionado'
    sizeColor = (100,100,3)
    color = None
    colorchange = False
    
    def windowsEvents(event, x, y, flags, param):
        nonlocal refPt
        nonlocal cropping
        nonlocal lastPosition
        nonlocal image
        nonlocal bkp
        nonlocal color
        nonlocal colorchange
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDBLCLK:
            # Hacemos el color y lo mostramos
            colorshow = np.zeros(sizeColor,np.uint8)
            color = image[y,x]
            colorchange = True
            colorshow[:,:,:] = image[y,x]
            cv2.destroyWindow(ventanaColor)
            cv2.namedWindow(ventanaColor)
            cv2.imshow(ventanaColor, colorshow)
        
        elif event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True
 
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            refPt.append((x, y))
            cropping = False
            image = bkp.copy()
            cv2.imshow(title, image)
            
            
            # Calculamos la zona a recortar
            xstart = min(refPt[0][0],refPt[1][0])
            xend = max(refPt[0][0],refPt[1][0])
            ystart = min(refPt[0][1],refPt[1][1])
            yend = max(refPt[0][1],refPt[1][1])
            
            # Hacemos el recorte y lo mostramos
            recorte = image[ystart:yend,xstart:xend]
            if len(recorte):
                cv2.destroyWindow(ventanaRecorte)
                cv2.namedWindow(ventanaRecorte)
                cv2.imshow(ventanaRecorte, recorte)

                # Hacemos el color medio y lo mostramos
                colorshow = np.zeros(sizeColor,np.uint8)
                colorshow[:,:,0] = np.average(recorte[:,:,0])
                colorshow[:,:,1] = np.average(recorte[:,:,1])
                colorshow[:,:,2] = np.average(recorte[:,:,2])
                color = colorshow[0,0]
                colorchange = True
                cv2.destroyWindow(ventanaColor)
                cv2.namedWindow(ventanaColor)
                cv2.imshow(ventanaColor, colorshow)

        elif event == cv2.EVENT_MOUSEMOVE:
            lastPosition = (x,y)
            
    # tomamos una foto
    image = takeFoto()
    if image is None:
        return
    bkp=image.copy()
    
    # La mostramos
    cv2.namedWindow(title)
    cv2.setMouseCallback(title, windowsEvents)
    cv2.imshow(title, image)
    
    # Iniciamos el loop de seleccion de color
    salir = False
    video = False
    while (not salir):
        key = cv2.waitKey(1)
        if key == ord('q'):
            salir = True
        if cropping:
            image = cv2.rectangle(bkp.copy(), refPt[0], lastPosition, (0, 255, 0), 2)
            cv2.imshow(title, image)
        if colorchange:
            showresta(image.copy(),color.copy(),tolerancia=umbral,gris=True)
            colorchange=False
        if key == ord('s'):
            salir = True
            video = True
    cv2.destroyAllWindows()
    
    if video:
        # inicializamos el modo video
        cap = cv2.VideoCapture(0)
        salir = False
        while (not salir):
            key = cv2.waitKey(1)
            if key == ord('q'):
                salir = True
            # Capture frame-by-frame
            ret, frame = cap.read()
            showresta(frame.copy(),color.copy(),tolerancia=umbral,gris=False, binaria = False)
            q.put((xcm, ycm))
            
        cap.release()
        cv2.destroyAllWindows()

def getCM ():
    return Xcm,Ycm

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()

t = threading.Thread(target=worker)
t.start()
