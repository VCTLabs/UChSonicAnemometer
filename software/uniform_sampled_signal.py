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

class UniformSampledSignal:
  def __init__(self, values, sampling_rate):
    self.values = values
    self.sampling_rate = sampling_rate
    self.start_timestamp = 0

  def get_timestamp(self, index):
    return 1.0*index/self.sampling_rate + self.start_timestamp

  def get_timestamp_array(self):
    return np.array(range(self.values.size))/self.sampling_rate + self.start_timestamp


def average(signals):
  assert len(signals) > 0
  result = UniformSampledSignal(None, signals[0].sampling_rate)
  result.start_timestamp = signals[0].start_timestamp
  values = list()
  for signal in signals:
    assert signal.start_timestamp == result.start_timestamp
    assert signal.sampling_rate == result.sampling_rate
    values.append(signal.values)
  result.values = np.average(values, 0)
  return result
