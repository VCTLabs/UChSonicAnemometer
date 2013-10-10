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
from scipy import optimize
import utilities
import uniform_sampled_signal

class ToFEstimator:
  def estimate_tof(self, signals):
    """ Estimator interface. Takes a list of signals and returns a single
        number. """
    pass

class EnvelopeThresholdEstimator(ToFEstimator):
  thresholds_levels = [0.75, 0.8, 0.85]
  def get_intersection(self, signal, level):
    for i in range(1, signal.values.size):
      if signal.values[i] > level:
        return signal.get_timestamp(i)
    return -1

  def estimate_tof(self, signals):
    average = uniform_sampled_signal.average(signals)
    envelope = utilities.get_signal_envelope(average)
    thresholds = []
    for thresholds_level in self.thresholds_levels:
      thresholds.append(self.get_intersection(envelope, thresholds_level))
    return (thresholds[0]+thresholds[1]+thresholds[2])/3


def envelope_analytical_function(x, x0, V0, m, h):
  """ Parameters of the envelope as seen on the paper M. Parrilla et al.,
     "Digital Signal Processing Techniques for High Accuracy Ultrasonic Range
     Measurements"."""

  xdata = np.maximum(0, x - x0)

  return V0*np.power(xdata, m) * np.exp(-xdata / h)

def estimate_envelope(func, x, y, p0 = np.array((1100,10e-2,2,1e2))):

  return optimize.curve_fit(func, x, y, p0)
