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

def pll(signal, angular_frecuency, sample_rate):
  """ Detects the phase of the signal using minimum square error."""
  best_phase = 0
  best_mse = float('inf')
  x = np.arange(0, signal.size)/(1.0*sample_rate)
  for phase in np.arange(0, 2*np.pi, 0.01):
    difference = signal - np.sin(angular_frecuency*x+phase)
    mse = np.sum(np.power(difference, 2))
    if mse < best_mse:
      best_mse = mse
      best_phase = phase
  return best_phase
