# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 18:42:31 2018

@author: Agus
"""

import serial
import camara
import control
import numpy as np

color = camara.seleccionarColor(idn=1)




x, y = camara.get_CM(color,show = True,idn = 1)


