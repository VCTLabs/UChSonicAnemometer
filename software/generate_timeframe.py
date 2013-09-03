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
import scipy
import scipy.optimize
import pll


def generate_timeframe(signal, angular_frecuency, sampling_rate):
  """ Generate a vector with the times of the samples in signal.
  
  Signal must be composed of a number of pulses and noise.
  
  The estimatiom of the starting point is done by detecting the phase of the
  signal, and then finding the root using newton's method using the first
  sample over a threshold as a starting guess."""
  
  threshold = 5000
  start = 0
  for i in range(signal.size):
    if abs(signal[i]) > threshold:
      start = i*1.0/sampling_rate
      break
  phase = pll.pll(signal, angular_frecuency, sampling_rate)
  
  def f(x):
    return scipy.sin(angular_frecuency*x+phase)
  def fprime(x):
    return angular_frecuency*scipy.cos(angular_frecuency*x+phase)
    
  start = scipy.optimize.newton(f, start, fprime=fprime)
  
  return np.arange(-start, -start+1.0*signal.size/sampling_rate, 1.0/sampling_rate)[0:signal.size]
