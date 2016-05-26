"""
Quick pictoral walk through an FT of a 1D sine wave

This has been modified from: https://plot.ly/matplotlib/fft/

@author Chris
@date 25/05/16
"""

import matplotlib.pyplot as plt
import numpy as np

# create a sine wave (combination of 2)
Fs = 150.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = np.arange(0,1,Ts) # time vector
ff = 5;   # frequency of the signal
y = np.sin(2*np.pi*ff*t)      # more frequent
#y2 = np.sin(0.9*np.pi*ff/2*t) # same magnitude but less frequent
y2 = 0.5*np.sin(0.9*(np.pi)*(ff*7)*t) # smaller and more frequent
y3=y+y2

# plot your [cumulative] sine wave
fig=plt.figure()
ax1=fig.add_subplot(311)
ax2=fig.add_subplot(312)
ax3=fig.add_subplot(313)
ax1.plot(t,y)
ax1.set_ylim(-1.5, 1.5)
#ax1.set_title("sine #1")
ax2.plot(t,y2)
ax2.set_ylim(-1.5, 1.5)
#ax2.set_title("sine #2")
ax2.set_ylabel('Amplitude')
ax3.plot(t,y3)
ax3.set_ylim(-1.5, 1.5)
#ax3.set_title("sine #1 + sine #2")
ax3.set_xlabel('Time')
plt.show(block=False)
ofile="./combined_sine_wave.png"
plt.tight_layout()
plt.savefig(ofile, dpi=300, transparent=True)#, figsize= )

# calculate your frequencies
n = len(y3) # length of the signal
k = np.arange(n)
T = n/Fs
frq = k/T # two sides frequency range
frq = frq[range(n/2)] # one side frequency range

Y = np.fft.fft(y3)/n # fft computing and normalization
Y = Y[range(n/2)]

# plot the real wave and its representation in (one way) frequency space 
fig, ax = plt.subplots(2, 1)
ax[0].plot(t,y3)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
#ax[0].set_title("sine #1 + sine #2")
ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
#ax[1].set_ylabel('|Y(freq)|')
ax[1].set_ylabel('Magnitude')
#ax[1].set_title("Magnitude/Frequency")
plt.tight_layout()
plt.show(block=False)
ofile="./combined_sine_wave_and_frqmag.png"
plt.savefig(ofile, dpi=300, transparent=True)#, figsize= )
