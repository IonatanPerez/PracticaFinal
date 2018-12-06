import serial

class motor:
    
    pasos_acumualados = 0
        
    def __init__ (self,  COM = 'COM5'):
        self.COM = COM
        self.puertoCom = serial.Serial(self.COM,9600)
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.puertoCom.close()
    
    def mover(self,pasos):
        self.puertoCom.write(b'PASO ' + str(pasos) + '\n')
        
    def printCOM (self):
        print (self.COM)
    