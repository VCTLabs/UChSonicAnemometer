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
# Authors: Karel Mundnich <kmundnic@ing.uchile.cl>
#          Luis Alberto Herrera <herrera.luis.alberto@gmail.com>

import numpy as np
from scipy import signal as scipysignal
from scipy import optimize

class ToFEstimator:
  def estimate_tof(self, signals):
    """ Estimator interface. Takes a list of signals and returns a single
        number. """
    pass

class EnvelopeThresholdEstimator(ToFEstimator):
  def estimate_tof(self, signals):
    signal = signals[0]
    for i in range(signal.values.size):
      if signal.values[i] > 0.1:
        return signal.get_timestamp(i)
    return 0

def peak_detection(signal, window_length):
  return scipysignal.find_peaks_cwt(signal, np.arange(1,window_length))

def envelope_analytical_function(x, x0, V0, m, h):
  """ Parameters of the envelope as seen on the paper M. Parrilla et al.,
     "Digital Signal Processing Techniques for High Accuracy Ultrasonic Range
     Measurements"."""

  xdata = np.maximum(0, x - x0)

  return V0*np.power(xdata, m) * np.exp(-xdata / h)

def estimate_envelope(func, x, y, p0 = np.array((1100,10e-2,2,1e2))):

  return optimize.curve_fit(func, x, y, p0)
