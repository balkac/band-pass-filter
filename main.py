from numpy import pi, tan
from scipy import signal
from scipy.io import wavfile
import numpy as np


"""
HASAN FURKAN BALKAÇ 
150150056

BAND PASS FILTER DESIGN with lowpass and highpass filter function using Butterworth.
Low Pass and High Pass parameter details and calculation are given in pdf.
Also There are pseudo codes for these in pdf.


Espacially in the low pass filter, music volume drops unbelievably. 
High Pass part of Band Pass Filter works more like the original graph characteristic of high pass part.

"""

def lowpass_filter(data, cutoff, fs):

    """
    Does a lowpass filter over the given data.
    :param data: The data (numpy array) to be filtered.
    :param cutoff: The high cutoff in Hz.
    :param fs: The sample rate in Hz of the data.
    :ORDER OF FILTER = 3
    :returns: Filtered data (numpy array).

    """
    
    angle = (2* pi * cutoff) / fs
    omega = tan (angle/2)
    
    #Array coefficents were calculated in pdf 
    #Functions only calculate the omega value for given frequency and
    #Numerator and Denumerator are calculated depends on this omega value

    num = np.array([ pow(omega,3), pow(omega,3)*3 , pow(omega,3)*3 , pow(omega,3) ])
    dem = np.array([ pow(omega,3) + 2*omega + 3 , -1*omega-1 , -1*omega+1, 3*omega-3 ])

    #print(num)
    #print(dem)

    y = signal.lfilter(num, dem, data)
    return y 
    
def highpass_filter(data, cutoff, fs):

    """
    Does a highpass filter over the given data.

    :param data: The data (numpy array) to be filtered.
    :param cutoff: The low cutoff in Hz.
    :param fs: The sample rate in Hz of the data.
    :param order: The order of the filter. The higher the order, the tighter the roll-off.
    :ORDER OF FILTER = 3
    :returns: Filtered data (numpy array).
    """
    #nyq = 0.5 * fs
    #omega = cutoff / nyq
    
    angle = (2* pi * cutoff) / fs
    omega = tan (angle/2)
    
    #Array coefficents were calculated in pdf 
    #Functions only calculate the omega value for given frequency and
    #Numerator and Denumerator are calculated depends on this omega value

    num = np.array([ 1, -3 , 3 , -1 ])
    dem = np.array([ pow(omega,3) + 4*omega + 1 , 3*pow(omega,3) -3 , 3*pow(omega,3)-4*omega+3, pow(omega,3)-1 ])

    #print(num)
    #print(dem)

    y = signal.lfilter(num, dem, data)
    return y 

def main():

    samplerate_Africa, data_Africa = wavfile.read("Africa.wav")
    
    filtered_data_Africa = highpass_filter(data_Africa,400,samplerate_Africa)
    filtered_data_Africa = lowpass_filter(filtered_data_Africa,3000,samplerate_Africa)
    #print(filtered_data)
    substract_data_Africa = data_Africa - filtered_data_Africa
    
    wavfile.write('AfricaBPF.wav',samplerate_Africa,filtered_data_Africa.astype(np.int16))
    print("------------------------------------------")
    print("AfricaBPF.wav Saved")
    wavfile.write('AfricaBSP.wav',samplerate_Africa,substract_data_Africa.astype(np.int16))
    print("------------------------------------------")
    print("AfricaBSP.wav Saved")

    samplerate_Winner, data_Winner = wavfile.read("WinnerTakesAll.wav")

    filtered_data_Winner = highpass_filter(data_Winner,400,samplerate_Winner)
    filtered_data_Winner = lowpass_filter(filtered_data_Winner,3000,samplerate_Winner)
    #print(filtered_data)
    substract_data_Winner = data_Winner - filtered_data_Winner
    
    wavfile.write('WinnerTakesAllBPF.wav',samplerate_Winner,filtered_data_Winner.astype(np.int16))
    print("------------------------------------------")
    print("WinnerTakesAllBPF.wav Saved")
    wavfile.write('WinnerTakesAllBSP.wav',samplerate_Winner,substract_data_Winner.astype(np.int16))
    print("------------------------------------------")
    print("WinnerTakesAllBSP.wav Saved")

if __name__ == "__main__":
    main()
