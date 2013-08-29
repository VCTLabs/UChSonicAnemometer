import numpy as np
import scipy.signal as scipysignal
import pylab
import pll

def envelope_detector(signal, frecuency, sampling_rate):
  """ Returns the envelope of the signal received in the transducer.
  
  The signal is multiplied by the carrier signal (in phase), and then low pass
  filtered."""
  angular_frecuency = 2*np.pi*frecuency
  nyquist_frequency = sampling_rate/2
  frecuency_width = 100
  filter_size = 11
  
  phase = pll.pll(signal, angular_frecuency, sampling_rate)
  time = np.arange(0, signal.size)/(1.0*sampling_rate)
  demodulated_signal = np.multiply(signal,
                                   np.sin(angular_frecuency*time+phase))
  
  lowpass = scipysignal.firwin(filter_size, cutoff = frecuency_width,
                               nyq = nyquist_frequency)
  demodulated_signal = scipysignal.lfilter(lowpass, 1, demodulated_signal)
  # The energy of the signal splits into a DC and twice the frecuency
  # components, so it must be multiplied by two.
  return 2*np.abs(demodulated_signal)