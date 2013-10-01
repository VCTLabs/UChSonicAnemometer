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


import adc_reader

import matplotlib.pyplot as plt
import unittest

class ADCReadTest(unittest.TestCase):
  def test_actual_read(self):
    reader = adc_reader.ADCReader()
    x = reader.get_frame()
    plt.plot(x, '.')
    plt.show()
    
  def test_file_read(self):
    reader = adc_reader.MockADCReader("test_adc.bin")
    x = reader.get_frame()
    plt.plot(x, '.')
    plt.show()


if __name__ == '__main__':
  unittest.main()
