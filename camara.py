# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 19:10:12 2018

@author: Agus
"""

import numpy as np
import cv2

global Xcm
global Ycm



def takeFoto(interactivo = False, idn=0):
    """
    Esta funcion sirve para sacara fotos con la opcion de hacerlo interactivo (que muestre video hasta que uno aprieta f)
    Y la opcion de pasar un id de la camara para que no sea la default 0
    devuelve una imagen en BGR
    
    Parameters
    ----------
    interactive: boolean
        Define si pone video y saca foto al apretar f o saca la primer foto que ve
    idn: int
        Id del device que va a buscar para tomar la foto, sirve por si hay mas deuna webcam conectada.
        
    Returns
    -------
    Devuelve un array de tres capas en formato BGR con los pixeles de la foto. Los ejes son y,x.
    
    """
    cap = cv2.VideoCapture(idn)
    salir = False
    foto = False
    
    if interactivo:
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
        cv2.destroyAllWindows()
    else:
        ret, frame = cap.read()
        foto = ret
        
    cap.release()
    
    if foto:
        return frame
    else:
        print("No se pudo sacar la foto")
        return None

def seleccionarColor(tolerancia=20,idn=0):
    """
        Rutina que sirve para seleccionar un color a partir del cual se va a reconocer la imagen.
        
        Parameters
        ----------
        tolerancia: Nivel de diferencia que acepta en cada capa del BGR al decidir su el color coincide o no para binarizar la imagen. Este parametro se inicializa aca porque se hereda a lo largo de las funciones. 
        idn: Identificacion del device a usar que se hereda a la funcion que toma la foto, pro default es el primero.
    """
    
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
    image = takeFoto(interactivo = True, idn=idn)
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
            #showresta(image.copy(),color.copy(),tolerancia=tolerancia,gris=True)
            binarizar(hacerResta(image.copy(),color.copy()),tolerancia = tolerancia)
            colorchange=False
        if key == ord('s'):
            salir = True
            video = True
    cv2.destroyAllWindows()
    
    if video:
        # inicializamos el modo video
        salir = False
        cap = cv2.VideoCapture(idn)
        while (not salir):
            key = cv2.waitKey(1)
            if key == ord('q'):
                salir = True
            # Capture frame-by-frame
            ret, frame = cap.read()
            xcm, ycm = get_CM(color, tolerancia = tolerancia, idn = idn,show = True, imagen = frame)
        cap.release()
        cv2.destroyAllWindows()
        
    return color

def hacerResta (imagen,color):
    
    # Calculamos la resta entre la imagen y el color seleccionado
    imagen = np.int16(imagen)
    color = np.int16(color)
    resta = np.zeros(imagen.shape,np.int16)
    resta[:,:,0] = imagen[:,:,0] - color[0]
    resta[:,:,1] = imagen[:,:,1] - color[1]
    resta[:,:,2] = imagen[:,:,2] - color[2]
    resta = np.abs(resta)
    resta = np.uint8(resta)
    
    return resta

def binarizar (imagen, tolerancia = 20):
    
    restaSaturada = np.zeros(imagen.shape,np.int16)
    restaSaturada[:,:,0] = (imagen[:,:,0] < tolerancia) * 255 
    restaSaturada[:,:,1] = (imagen[:,:,1] < tolerancia) * 255 
    restaSaturada[:,:,2] = (imagen[:,:,2] < tolerancia) * 255 
    restaSaturada = restaSaturada[:,:,0] + restaSaturada[:,:,1] + restaSaturada[:,:,2]
    restaSaturada = restaSaturada/3
    restaSaturada = np.uint8(restaSaturada)
    return restaSaturada
   
def centrodemasa(binario):
    """
    Esta funcion calcula el centro de masa a partir de una matriz donde considera los puntos con intensidad mayor a 200
    """
    binario = binario > 200
    x = np.arange(binario.shape[1])
    y = np.arange(binario.shape[0])
    xcm = np.dot(x,np.sum(binario,0))/np.sum(binario)
    ycm = np.dot(y,np.sum(binario,1))/np.sum(binario)
    return [xcm,ycm]

def get_CM(color, tolerancia = 20, idn=0, show=False, imagen = None):
    """
    Funcion que sirve para calcular el centro de masa conociendo el color a buscar.
    """
    if imagen is None:
        imagen = takeFoto(idn = idn)
    imagen = binarizar(hacerResta(imagen,color),tolerancia=tolerancia)
    xcm, ycm = centrodemasa(imagen)
    if show:
        showimage(imagen,CM=True,Xcm=xcm,Ycm=ycm)
    return xcm, ycm

    
def showimage(imagen, CM=False, Xcm=None, Ycm=None):
    tituloVentana = 'Visualizacion'
    cv2.namedWindow(tituloVentana)
    if CM:
        if not np.isnan(Xcm):
            if not np.isnan(Ycm):
                imagen = cv2.circle(imagen,(int(Xcm),int(Ycm)),20,(200, 200, 200),3)
    cv2.imshow(tituloVentana, imagen)
   