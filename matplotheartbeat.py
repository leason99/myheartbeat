import sys
import numpy as np
import matplotlib.pyplot as plt
import threading
import copy
import sys, serial
from time import sleep
from collections import deque
import time 
import random

class AnalogData:
    # constr
    def __init__(self, maxLen):
        self.ax = deque([0.0]*maxLen)
        self.ay = deque([0.0]*maxLen)
        self.maxLen = maxLen

    # ring buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)
    # add data
    def add(self, data):
        #assert(len(data) == 1)
        self.addToBuf(self.ax, data)
    
class AnalogPlot:
    def __init__(self, analogData):
        
        self.fs = 2301.0  #sampleRate

        plt.ion()
        plt.subplot(211)
        self.axline, = plt.plot(range(len(analogData.ax)),analogData.ax)
        plt.title('Input Signal')
        plt.draw()
        
        plt.subplot(212)
        plt.title('FFT')
        fftdata=np.abs(np.fft.rfft(analogData.ax))[10:1000]                 #remove dc value  and high frequency value
        fftfreq=np.fft.rfftfreq(len(analogData.ax),d=1./self.fs)[10:1000] #remove dc value  and high frequency value
        self.axline2,= plt.plot(fftfreq,fftdata)
        
        plt.draw()
    
    def update(self, analogData):

        data=copy.deepcopy(np.array(analogData.ax))
        self.axline.set_ydata(data)
        self.axline.set_xdata(range(len(data)))

        fftdata=np.abs(np.fft.rfft(data))[10:1000]               #remove dc value  and high frequency value
        fftfreq=np.fft.rfftfreq(len(data),d=1./self.fs)[10:1000] #remove dc value  and high frequency value

        plt.subplot(2,1,1)
        plt.ylim([np.min(list(data))-10, np.max(list(data))+10])
        plt.subplot(2,1,2)
        self.axline2.set_ydata(fftdata)
        self.axline2.set_xdata(fftfreq)
        plt.ylim([np.min(list(fftdata))-10, np.max(list(fftdata))+10])
        
        plt.draw()
        plt.pause(0.000001)
        return fftfreq[np.argmax(fftdata[:60])]*60

def recvieData(analogData):
    strPort='/dev/cu.usbmodem1421'   ###### Change to your port   ######
    ser = serial.Serial(strPort, 115200)
    while True:
        line = ser.readline()
        try:
            for val in line.split():
                
                data = float(val)
                analogData.add(data)
    
        except:
            pass


analogData = AnalogData(40000)
analogPlot = AnalogPlot(analogData)

t1 = threading.Thread(target=recvieData, args=(analogData,) )
t1.start()


if __name__ == '__main__':  
    while True:
        print(str(analogPlot.update(analogData)))
        sleep(0.1)
        
    
    