# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 16:19:28 2018

@author: Agus
"""

import numpy as np
import matplotlib.pyplot as plt
import time

class PIDController:

    def __init__(self, setpoint, kp=1.0, ki=0.0, kd=0.0,tau_i=10000,clamp=True,s_min=0,s_max=5):

        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.time_init = time.time()
        self.tau_i = tau_i #iteraciones que entran en la integral
        self.clamp = clamp
        self.s_min = s_min
        self.s_max = s_max
        
        self.current_time = 0
        self.last_time = self.time_init
        self.medicion = 0
        self.error = 0
        self.last_error = 0
        self.p_term = 0
        self.i_term = 0
        self.d_term = 0
        self.dt = 0 
        
        ### Listas vacías para guardar data que puedo querer plotear. 
        self.medicion_t = []
        self.out_t = []
        self.error_t = []
        self.p_term_t = [] 
        self.i_term_t = []
        self.d_term_t = []
        self.tiempos = []
        

    def calculate(self, medicion, dt = None):
        
        self.current_time = time.time()
        self.dt = self.current_time - self.last_time
        self.medicion = medicion
        self.error = self.setpoint - self.medicion

        delta_error = self.error - self.last_error
        
        self.p_term = self.kp * self.error
        self.i_term += self.error * self.ki
        self.d_term = delta_error * self.kd

        self.last_error = self.error
        
        self.senal = self.p_term + self.i_term + self.d_term
        
        if self.clamp:
            self.senal = np.clip(self.senal,self.s_min,self.s_max)
            
        ## guardo
        self.medicion_t.append(medicion)
        self.out_t.append(self.senal)
        self.error_t.append(self.error)
        self.p_term_t.append(self.p_term)
        self.i_term_t.append(self.i_term)
        self.d_term_t.append(self.d_term)
        self.tiempos.append(self.current_time-self.time_init)
        self.last_time=self.current_time

        return self.senal
    
    def plots(self, medicion = True, senal = True, error = True, p_term = True, i_term = True, d_term = True):
        nrows = medicion + senal + error + p_term + i_term + d_term
        f,ax = plt.subplots(nrows = nrows,sharex = True)        
        f.text(0.5,0.04,"Tiempo (s)",ha='center')
        n_grafico = -1
        if medicion: 
            n_grafico+= 1 
            ax[n_grafico].plot(self.tiempos,self.medicion_t,'.-',markersize = 10)
            ax[n_grafico].plot(self.tiempos, [self.setpoint]*len(self.tiempos),'r-',linewidth = 4)
            ax[n_grafico].set_ylabel("Mediciones")
            ax[n_grafico].grid(True)
        if senal:
            n_grafico+= 1 
            ax[n_grafico].plot(self.tiempos,self.out_t,'.-',markersize = 10)
            ax[n_grafico].set_ylabel("Senal enviada")
            ax[n_grafico].grid(True)
        if error:
            n_grafico+= 1 
            ax[n_grafico].plot(self.tiempos,self.error_t,'.-',markersize = 10)
            ax[n_grafico].set_ylabel("Error")
            ax[n_grafico].grid(True)
        if p_term:
            n_grafico+= 1 
            ax[n_grafico].plot(self.tiempos,self.p_term_t,'.-',markersize = 10)
            ax[n_grafico].set_ylabel("Término proporcional")
            ax[n_grafico].grid(True)
        if i_term:
            n_grafico+= 1 
            ax[n_grafico].plot(self.tiempos,self.i_term_t,'.-',markersize = 10)
            ax[n_grafico].set_ylabel("Término integral")
            ax[n_grafico].grid(True)
        if d_term:
            n_grafico+= 1 
            ax[n_grafico].plot(self.tiempos,self.d_term_t,'.-',markersize = 10)
            ax[n_grafico].set_ylabel("Término derivada")
            ax[n_grafico].grid(True)
            
        return
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        