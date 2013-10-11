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
from scipy import optimize
import math

def sin_w(w):
  def f(x, phi):
    return -np.cos(x*w+phi)
  return f

#return optimize.curve_fit(func, x, y, p0)

def pll(signal, angular_frecuency):
  """ Detects the phase of the signal using minimum square error."""
  popt, pcov = optimize.curve_fit(sin_w(angular_frecuency), signal.get_timestamp_array(), signal.values, 0)
  return math.fmod(popt[0], np.pi)
