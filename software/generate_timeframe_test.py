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


import generate_timeframe

import adc_reader
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import unittest


class TestGenerateTimeframe(unittest.TestCase):
  def setUp(self):
    self.frecuency = 25500
    self.w = 2*np.pi*self.frecuency
    reader = adc_reader.MockADCReader("test_adc.bin")
    self.audio_data = reader.get_frame()

  def test_pll(self):
    x = generate_timeframe.generate_timeframe(self.audio_data,
                                              self.w,
                                              adc_reader.SAMPLING_RATE)
    plt.plot(x, self.audio_data, '*-')
    plt.show()


if __name__ == '__main__':
  unittest.main()
