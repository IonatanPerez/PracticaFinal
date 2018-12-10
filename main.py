# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 18:42:31 2018

@author: Agus
"""
import camara
import control
import numpy as np
import serial 

# abro arduino
motor = serial.Serial('COM5',9600)

## ACÁ HAY QUE SETEAR LA ALTURA EN PIXELES, EN PPIO A MANO
setpoint = 





