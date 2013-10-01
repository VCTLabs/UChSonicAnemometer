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

import subprocess
import numpy as np
import StringIO
import tempfile


class ADCReader:
  """ Python interface to access the ADC."""
  def get_frame(self):
    """ Get a new measurement from the ADC. It will usually be a concatenation
    of measurement in every direction."""
    process = subprocess.Popen("./adc/adc_read", stdout=subprocess.PIPE)
    process_output, process_error = process.communicate()
    return np.frombuffer(process_output, np.dtype(np.int16))


class MockADCReader:
  """ Python interface to access the ADC."""
  def __init__(self, filename):
    self.data_file = filename

  def get_frame(self):
    return np.fromfile(open(self.data_file, 'rb'), np.dtype(np.int16))
    