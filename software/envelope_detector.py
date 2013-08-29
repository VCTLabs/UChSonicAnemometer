#
# Copyright (C) 2013  UNIVERSIDAD DE CHILE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luis Alberto Herrera <herrera.luis.alberto@gmail.com>


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